# Database setup
import sqlite3
import caribou
db_file = 'librarytest.db'
migrations_path = 'migrations'
conn = sqlite3.connect(db_file)
caribou.upgrade(db_file, migrations_path)
conn.close()

# Libraries
from datetime import date
import time
import calendar
from bottle import get, post, error, run, debug, install, request, response, redirect, template, static_file
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
from string import digits
from itertools import cycle
install(message_plugin)
install(SQLitePlugin(dbfile=db_file))
cookie_key = "1234567890987654321"

## Application specfic classes and functions
from configuration import *
from classes_and_functions import *
from loan_table import *
from access_table import *
from user_table import *


def require_auth(fn):
    def auth_wrapper(*args, **kwargs):
        signin_status = Signin_Status(cookie_key)
        if not signin_status.id:
            return redirect('/signin')
        else:
            kwargs["signin_status"] = signin_status
            return fn(*args, **kwargs)
    return auth_wrapper

class Signin_Status:
    def __init__(self, secret):
        self.secret = secret
        self.is_signed_in = True if request.get_cookie("id", secret=self.secret) else False
        self.id = request.get_cookie("id", secret=self.secret)
        self.btn_text = "My account" if self.is_signed_in else "Sign in"
    def update_secret(self, new_secret):
        self.secret = new_secret
    def get_id(self):
        return self.id
    def sign_in(self, user_id):
        response.set_cookie("id", str(user_id), self.secret)
        self.id = user_id
        self.is_signed_in = True
        self.btn_text = "My account"
    def sign_out(self):
        response.delete_cookie("id")
        self.id = None
        self.is_signed_in = False
        self.btn_text = "Sign in"


## == Routes == ##
@get('/')
def display_homepage():
    return template('index', signin_status=Signin_Status(cookie_key))


@get('/static/<file:path>')
def serve_static(file):
    return static_file(file, root='./static')

@get('/contact')
def display_contact():
    return template('contact', signin_status=Signin_Status(cookie_key))


# Sign ups and log in
@get('/signin')
def display_signin_get(db):
    signin_status = Signin_Status(cookie_key)
    if signin_status.is_signed_in:
        return redirect('/account')
    else:
        return template('signin', error=False, purpose_text=return_purpose_text(request))

@post('/signin')
def display_signin_post(db):
    signin_status = Signin_Status(cookie_key)
    if signin_status.is_signed_in:
        return redirect('/account')
    elif 'firstName' in request.forms:
        matching_id = verify_form(request.forms, db)
        if matching_id == False:
            return template('signin', error=True)
        else:
            signin_status.sign_in(matching_id)
            return redirect('/account')
    else:
        return template('signin', error=True)


@get('/signup')
def display_signup():
    this_id = Signin_Status(cookie_key).id
    if this_id:
        return redirect('/account')
    else:
        errorVal = False
        if 'error' in request.query:
            errorVal = True if str(request.query['error']) == 'True' else False
        return template('signup', error=errorVal)


@post('/confirmation')
def display_confirmation(db):
    new_user_id = verify_signup(request.forms, db)
    # verify_signup returns false if there is already an account associated with this library card number
    if new_user_id == False:
        return redirect('/signup?error=True')
    else:
        new_user = PublicUser.from_db(db, new_user_id)
        return template('confirmation', user=new_user)

@get('/confirmation')
def redirect_confirmation(db):
    # Redirect to home if anyone tries to access the confirmation page via get request
    return redirect('/')

@get('/signout')
def display_signout():
    signin_status = Signin_Status(cookie_key)
    if signin_status.is_signed_in:
        signin_status.sign_out()
        return template('signout')
    else:
        return redirect('/')


# Account management
@get('/account', apply=[require_auth])
def display_account_details(signin_status, db):
    this_id = signin_status.id
    this_user = PublicUser.from_db(db, this_id)
    # Access Log
    access_log = [{
        "bookname": book_name,
        "url": f"/resource/{resource_id}" if url else None,
        "date": time.strftime("%H:%M %d %B %Y", time.localtime(t))
        }
        for book_name, resource_id, t, url in get_user_access_log(db, this_id)]
    # Active Loan Details
    active_loans = [{
        "book_title": book_name,
        "copy_id": copy_id,
        "book_id": book_id,
        "date_borrowed": dbdate_to_date(date_borrowed),
        "date_due": dbdate_to_date(date_due),
        "max_renewal": dbdate_to_date(date_borrowed + MAX_RENEWAL),
        "renewal_length": (date.today().toordinal() + LOAN_PERIOD) - date_due
    }
    for book_name, book_id, copy_id, date_borrowed, date_due in get_user_loans(db, this_id)]

    return template('account', user=this_user, access_log=access_log, active_loans=active_loans, today=date.today(),
                    LOAN_PERIOD=LOAN_PERIOD, MAX_RENEWAL=MAX_RENEWAL)

@post('/account', apply=[require_auth]) # Accessed if user has updated their details
def update_account_details(db, signin_status):
        this_user = PublicUser.from_db(db, signin_status.id)
        try:
            this_user.update(request.forms)
            this_user.save(db)
            return redirect('/account')
        except ValidationError as e:
            return template('error', emph_details="Validation error: ", error_message=e, back_button=True, signin_status=signin_status)


# Book viewing
@get('/search')
def display_search(db):
    # If a search hasn't been carried out yet, return empty page
    if 'searchdata' not in request.params:
        return template('search', signin_status=Signin_Status(cookie_key))
    # Otherwise, deal with the form data. NOTE: need to add validation here ideally
    else:
        results = ordered_results(request, db)
        result_ids = [result["id"] for result in results]
        avail_resp = db.execute(
            f"""
            SELECT
                BookDetail.id,
                COUNT(DISTINCT HardCopy.id) as copies,
                COUNT(DISTINCT HardCopy.id) - ( COUNT(Loan.dateBorrowed)-COUNT(Loan.dateReturned) ) as available FROM BookDetail
            LEFT JOIN HardCopy on HardCopy.bookId = BookDetail.id
            LEFT JOIN Loan on Loan.hardCopyId = HardCopy.id
            WHERE BookDetail.id IN ({",".join("?" for _ in result_ids)})
            GROUP BY BookDetail.id
            """, result_ids).fetchall()
        avail_details = {int(result['id']): {'copies': result['copies'],
                                        'available': result['available']}
                            for result in avail_resp}
        return template('search', signin_status=Signin_Status(cookie_key), request=request,
                            results=[Book(row['id'], db) for row in results],
                            avail_details=avail_details)

@get('/book/<book_id:int>')
def display_book_page(db, book_id):
    this_book = Book(book_id, db)
    all_copies = db.execute("""
        SELECT HardCopy.id AS copyId, dateDue, borrowerId
        FROM HardCopy
        LEFT JOIN (SELECT * FROM LOAN WHERE dateReturned IS NULL ) -- unreturned books
            ON hardCopyId = HardCopy.id
        WHERE HardCopy.bookId = ?
        ORDER BY
            dateDue ASC,
            copyId ASC
        """, (this_book.id,)).fetchall()
    return template('book', book=this_book, all_copies=all_copies, dbdate_to_date=dbdate_to_date, signin_status=Signin_Status(cookie_key))

@get('/book/new', apply=[require_auth])
def display_add_form(db, signin_status):
    return template('add')

@post('/book/new', apply=[require_auth])
def add_book(db, signin_status):
    isbn = "".join([c for c in request.forms.get('isbn') if c in digits])
    isbn_digits = [int(c) for c in isbn]
    if len(isbn_digits) != 13:
        return  template('error', error_message="Please use the 13 digit ISBN.", back_button=True, signin_status=signin_status)

    isbn_checksum = sum(x * y for x, y in zip(isbn_digits, cycle([1,3]))) % 10

    if isbn_checksum != 0:
        return template('error', error_message="ISBN failed checksum.", back_button=True, signin_status=signin_status)

    bookdetail_id = db.execute("""
        SELECT id FROM BookDetail
        WHERE isbn = ?
        """, (isbn,)).fetchone()
    if bookdetail_id:
        bookdetail_id = bookdetail_id[0]
    else:
        if any(request.forms.get('detail') == "" for detail in ('bookName', 'yearPublished', 'author1')):
            return template('error', error_message="Not enough info.", back_button=True, signin_status=signin_status)
        # Insert book details
        bookdetail_id = db.execute(f"""
            INSERT INTO BookDetail (bookName, yearPublished, isbn)
            VALUES (?,?, ?)
            """, (request.forms.get('bookName'), request.forms.get('yearPublished'), isbn)).lastrowid

        # Link authors, creating if necessary
        for author_num in (1,2,3):
            author = request.forms.get(f"author{str(author_num)}")
            if author:
                author_id = db.execute("""
                    SELECT id from Author
                    Where name = ?
                    """, (author,)).fetchone()
                if author_id:
                    author_id = author_id[0]
                else:
                    author_id = db.execute(f"""
                        INSERT INTO Author (name)
                        VALUES (?)
                        """, (author,)).lastrowid

                db.execute("""
                    INSERT INTO BookDetailAuthor (bookId, authorId, orderPos)
                    VALUES (?,?,?)
                    """, (bookdetail_id, author_id, author_num))

    resource_type = request.forms.get('resourceType')
    if resource_type == 'hardCopy':
            # Add new copy
        db.execute("""
            INSERT INTO HardCopy (bookId)
            VALUES (?)
            """, (bookdetail_id,))
    elif resource_type == 'onlineResource':
        url = request.forms.get("url")
        if not url:
            return template('error', error_message="No url provided for online resource.", back_button=True, signin_status=signin_status)
        db.execute("""
            UPDATE BookDetail
            SET url = ?
            WHERE id = ?
            """, (url, bookdetail_id))
    else:
        return template('error', error_message="Unrecognised resource type.", back_button=True, signin_status=signin_status)

    return redirect(f"/book/{str(bookdetail_id)}")


@get('/resource/<resource_id:int>', apply=[require_auth])
def track_resource_access(db, resource_id, signin_status):
    # Redirect if no online resource available
    resource_query_response = db.execute("SELECT url, bookName FROM BookDetail WHERE id = ?", (resource_id,)).fetchone()
    if not resource_query_response:
        return template('error', error_message="Resource not found.", back_button=True, signin_status=signin_status)
    if not resource_query_response[0]:
        error_message_tail = " is not currently available online."
        return template('error', emph_details=resource_query_response[1], error_message=error_message_tail, back_button=True, signin_status=Signin_Status(cookie_key))
    # Otherwise record access and redirect to resource
    record_user_access(db, signin_status.id, resource_id)
    return redirect(resource_query_response[0])


# Loan system
@post('/renew', apply=[require_auth])
def issue_renew_book(db, signin_status):
    user_id = int(signin_status.id)
    copy_id = request.forms.get('copy_id')

    current_loan_status = get_current_loan_status(db, copy_id)
    if current_loan_status:
        # Currently on loan
        if current_loan_status["borrowerID"] != user_id:
            return template('error', error_message="Cannot renew as book on loan to another account.", back_button=True, signin_status=signin_status)

        max_renew_date = current_loan_status["dateBorrowed"] + MAX_RENEWAL
        renew_date = min(current_loan_status["dateDue"] + LOAN_PERIOD, max_renew_date, today_date()+LOAN_PERIOD)
        if current_loan_status["dateDue"] < today_date():
            return template('error', error_message="Cannot renew as already overdue.", signin_status=signin_status)
        if max_renew_date <= current_loan_status["dateDue"]:
            return template('error', error_message="Already renewed to maximum loan duration.", signin_status=signin_status)
        if renew_date <= current_loan_status["dateDue"]:
            return template('error', error_message="Already renewed as long as possible for today.", signin_status=signin_status)

        renew_copy(db, copy_id, renew_date)
        return redirect(f'/account?highlight={copy_id}')
    else:
         # Not currently on loan
        if get_user_loan_count(db, user_id) >= MAX_ON_LOAN:
            return template('error', error_message="You already have the maximum number of books on loan.", signin_status=signin_status)
        if get_user_related_copy_count(db, user_id, copy_id) >= 1:
            return template('error', error_message="You already have a copy of this book on loan.", signin_status=signin_status)
        issue_copy_to_user(db, user_id, copy_id, calculate_due_date(LOAN_PERIOD))
        return redirect(f'/account?highlight={copy_id}')


@post('/return', apply=require_auth)
def confirm_return_book(db, signin_status):
    user_id = int(signin_status.id)
    copy_id = request.forms.get('copy_id')

    current_loan_status = get_current_loan_status(db, copy_id)
    if not current_loan_status:
        return template('error', error_message="Cannot return as book not on loan.", back_button=True, signin_status=signin_status)
    if current_loan_status["borrowerID"] != user_id:
        return template('error', error_message="Cannot renew as book on loan to another account.", back_button=True, signin_status=signin_status)
    return_copy(db, copy_id)
    return redirect('/account')



@error(400)
def error400(error):
    error_text = "Something seems to have gone wrong with this page request."
    return template('error', error_message=error_text, signin_status=Signin_Status(cookie_key))
@error(401)
def error401(error):
    error_text = "You don't appear to have permission to access this page."
    return template('error', error_message=error_text, signin_status=Signin_Status(cookie_key))
@error(403)
def error403(error):
    error_text = "You don't appear to have permission to access this page."
    return template('error', error_message=error_text, signin_status=Signin_Status(cookie_key))
@error(404)
def error404(error):
    error_text = "There doesn't seem to be anything here."
    return template('error', error_message=error_text, signin_status=Signin_Status(cookie_key))

run(host='localhost', port=8080, debug=True)