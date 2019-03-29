# Configuration
LOAN_PERIOD=14 # days
MAX_RENEWAL=100 # days since issue
MAX_ON_LOAN = 4 
#####################

import caribou
db_file = 'librarytest.db'
migrations_path = 'migrations'

# Database setup
import sqlite3
conn = sqlite3.connect(db_file)
caribou.upgrade(db_file, migrations_path)
conn.close()

# Backend
## Setup
from datetime import date
import time
import calendar
from bottle import get, post, error, run, debug, install, request, response, redirect, template, static_file
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
install(message_plugin)
install(SQLitePlugin(dbfile=db_file))
cookie_key = "1234567890987654321"

## Classes and Functions
from classes_and_functions import *

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

## Routes
@get('/static/<file:path>')
def serve_static(file):
    return static_file(file, root='./static')

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

@get('/')
def display_homepage():
    return template('index', signin_status=Signin_Status(cookie_key))

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
@get('/signin')
def display_signin_get(db):
    signin_status = Signin_Status(cookie_key)
    if signin_status.is_signed_in:
        return redirect('/account')
    else:
        return template('signin', error=False, purpose_text=return_purpose_text(request))

@get('/account')
def display_account_details(db):
    this_id = Signin_Status(cookie_key).id
    if not this_id:
        return redirect('/signin?origin=account')
    else:
        this_user = User(this_id, db)
        # Access Log
        access_query_response = db.execute("""
                        SELECT BookDetail.bookName, BookDetail.id, PastAccess.dateAccessed, BookDetail.url
                        FROM PastAccess
                        INNER JOIN BookDetail
                        ON PastAccess.bookId = BookDetail.id
                        WHERE PastAccess.userId = ?
                        ORDER BY PastAccess.dateAccessed DESC
                        LIMIT 5
                        """, (this_id,)).fetchall()
        access_log = [{
            "bookname": book_name,
            "url": f"/resource/{resource_id}" if url else None,
            "date": time.strftime("%H:%M %d %B %Y", time.localtime(t))
            }
            for book_name, resource_id, t, url in access_query_response]
        # Active Loan Details
        loan_query_response = db.execute("""
                        SELECT BookDetail.bookName, BookDetail.id, Loan.hardCopyId, Loan.dateBorrowed, Loan.dateDue FROM Loan
                        INNER JOIN HardCopy ON Loan.hardCopyId = HardCopy.id
                        INNER JOIN BookDetail ON HardCopy.bookId = BookDetail.id
                        WHERE borrowerId = ? AND dateReturned IS NULL
                        ORDER BY Loan.dateDue ASC
                        """, (this_id,)).fetchall()
        active_loans = [{
            "book_title": book_name,
            "copy_id": copy_id,
            "book_id": book_id,
            "date_borrowed": dbdate_to_date(date_borrowed),
            "date_due": dbdate_to_date(date_due),
            "max_renewal": dbdate_to_date(date_borrowed + MAX_RENEWAL),
            "renewal_length": (date.today().toordinal() + LOAN_PERIOD) - date_due
        }
        for book_name, book_id, copy_id, date_borrowed, date_due in loan_query_response]

        return template('account', user=this_user, access_log=access_log, active_loans=active_loans, today=date.today(),
                        LOAN_PERIOD=LOAN_PERIOD, MAX_RENEWAL=MAX_RENEWAL)
@post('/account') # Accessed if user has updated their details
def update_account_details(db):
    this_id = Signin_Status(cookie_key).id
    if not this_id:
        return redirect('/signin?origin=account')
    else:
        this_user = User(this_id, db)
        this_user.set_GenUser_details(db, request.forms)
        # Could just use the info we already have to render the page, but redirect to GET keeps it consistent if we make changes
        return redirect('/account')

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
        new_user = User(new_user_id, db)
        return template('confirmation', user=new_user)
# Redirect to home if anyone tries to access the confirmation page via get request
@get('/confirmation')
def redirect_confirmation(db):
    return redirect('/')

@get('/signout')
def display_signout():
    signin_status = Signin_Status(cookie_key)
    if signin_status.is_signed_in:
        signin_status.sign_out()
        return template('signout')
    else:
        return redirect('/')

@get('/search')
def display_search(db):
    # If a search hasn't been carried out yet, return empty page
    if 'searchdata' not in request.params:
        return template('search', signin_status=Signin_Status(cookie_key))
    # Otherwise, deal with the form data. NOTE: need to add validation here ideally
    else:
        results = ordered_results(request, db)
        return template('search', signin_status=Signin_Status(cookie_key), request=request, results=[Book(row['id'], db) for row in results])

@get('/book/<book_id>')
def display_book_page(db, book_id):
    this_book = Book(book_id, db)
    all_copies = db.execute("SELECT HardCopy.id AS copyId, dateBorrowed, dateReturned, dateDue FROM HardCopy LEFT JOIN Loan ON HardCopy.id = hardCopyId WHERE HardCopy.bookId = ? GROUP BY HardCopy.id ORDER BY copyId ASC", (this_book.id,)).fetchall()
    return template('book', book=this_book, all_copies=all_copies, dbdate_to_date=dbdate_to_date, signin_status=Signin_Status(cookie_key))

@get('/contact')
def display_contact():
    return template('contact', signin_status=Signin_Status(cookie_key))

@get('/resource/<resource_id:int>')
def track_resource_access(db, resource_id):
    signin_status = Signin_Status(cookie_key)
    if not signin_status.is_signed_in:
        return redirect('/signin?origin=resource')
    # Redirect if no online resource available
    resource_query_response = db.execute("SELECT url, bookName FROM BookDetail WHERE id = ?", (resource_id,)).fetchone()
    if not resource_query_response:
        return template('error', error_message="Resource not found.", back_button=True, signin_status=signin_status)
    if not resource_query_response[0]:
        error_message_tail = " is not currently available online."
        return template('error', emph_details=resource_query_response[1], error_message=error_message_tail, back_button=True, signin_status=Signin_Status(cookie_key))
    # Otherwise record access and redirect to resource
    db.execute("INSERT INTO PastAccess (userID, bookID, dateAccessed) VALUES (?,?,?)", (signin_status.id, resource_id, calendar.timegm(time.localtime())))
    return redirect(resource_query_response[0])

@post('/renew')
def issue_renew_book(db):
    signin_status = Signin_Status(cookie_key)
    if not signin_status.id:
        return redirect('/signin?origin=account')

    copy_id = request.forms.get('copy_id')

    # Redirect if book taken out by someone else
    already_out = db.execute("""
        SELECT COUNT(id)
        FROM Loan
        WHERE hardCopyId = ?        -- this book
        AND   borrowerId != ?       -- borrowed by someone else 
        AND   dateReturned IS NULL  -- not returned
        """, (copy_id, signin_status.id)).fetchone()[0]
    if already_out:
        return template('error', error_message="Cannot renew as book on loan to another account.", back_button=True, signin_status=signin_status)

    current_status_query = db.execute("""
        SELECT dateDue, dateBorrowed
        FROM Loan
        WHERE hardCopyId = ?        -- this book
        AND   borrowerId = ?        -- borrowed by this user
        AND   dateReturned IS NULL  -- not returned
        """, (copy_id, signin_status.id)).fetchone()

    if current_status_query == None:
        # Book not unreturned, so issue book if don't reaach book limits and not already checked out a copy
        num_loaned_to_user = db.execute("""
            SELECT COUNT(id)
            FROM Loan
            WHERE borrowerId = ?        -- borrowed by this user 
            AND   dateReturned IS NULL  -- not returned
            """, (signin_status.id,)).fetchone()[0]
        if num_loaned_to_user == MAX_ON_LOAN:
            return template('error', error_message="You already have the maximum number of books on loan.", signin_status=signin_status)
        else:
            copies_of_book_with_user = db.execute("""
                SELECT COUNT(*) FROM Loan
                INNER JOIN HardCopy ON Loan.hardCopyId = HardCopy.id
                WHERE HardCopy.bookId = (SELECT bookId FROM HardCopy WHERE id = ?)  -- Same book (in the abstract, not hard copy)
                    AND   borrowerId  = ?                                           -- borrowed by this user
                    AND   dateReturned IS NULL                                      -- not returned
                """, (copy_id, signin_status.id)).fetchone()[0]
            if copies_of_book_with_user != 0:
                return template('error', error_message="You already a copy of this book.", signin_status=signin_status)
            else:
                db.execute(f"""
                    INSERT INTO Loan (borrowerId, hardCopyId, dateBorrowed, dateDue)
                    VALUES (?, ?, ?, ?)
                    """, (signin_status.id, copy_id, today_date(), calculate_due_date(LOAN_PERIOD)))
                return redirect('/account')
    else:
        # Book already taken out, so update due date if not already overdue.
        due_date = current_status_query[0]
        issue_date = current_status_query[1]
        max_renew_date = issue_date + MAX_RENEWAL
        if today_date() > due_date:
            return template('error', error_message="Cannot renew as already overdue.", signin_status=signin_status)
        elif calculate_due_date(LOAN_PERIOD) > max_renew_date:
            if max_renew_date == due_date:
                return template('error', error_message="Already renewed to maximum loan duration.", signin_status=signin_status)
            else:
                db.execute(f"""
                    UPDATE Loan
                    SET dateDue = ?
                    WHERE hardCopyId = ?        -- this book
                    AND   borrowerId = ?        -- borrowed by this user
                    AND   dateReturned IS NULL  -- not returned
                    """, (max_renew_date, copy_id, signin_status.id))
                return redirect('/account')

        else:
            db.execute(f"""
                UPDATE Loan
                SET dateDue = ?
                WHERE hardCopyId = ?        -- this book
                AND   borrowerId = ?        -- borrowed by this user
                AND   dateReturned IS NULL  -- not returned
                """, (calculate_due_date(LOAN_PERIOD), copy_id, signin_status.id))
            return redirect('/account')


@post('/return')
def confirm_return_book(db):
    signin_status = Signin_Status(cookie_key)
    if not signin_status.id:
        return redirect('/signin')

    copy_id = request.forms.get('copy_id')

    # Redirect if book taken out by someone else
    already_out = db.execute("""
        SELECT COUNT(id)
        FROM Loan
        WHERE hardCopyId = ?        -- this book
        AND   borrowerId != ?       -- borrowed by someone else 
        AND   dateReturned IS NULL  -- not returned
        """, (copy_id, signin_status.id)).fetchone()[0]
    if already_out:
        return template('error', error_message="Cannot return as book on loan to another account.", back_button=True, signin_status=signin_status)

    current_status_query = db.execute("""
        SELECT dateDue
        FROM Loan
        WHERE hardCopyId = ?        -- this book
        AND   borrowerId = ?        -- borrowed by this user
        AND   dateReturned IS NULL  -- not returned
        """, (copy_id, signin_status.id)).fetchone()

    if current_status_query == None:
        # Book not unreturned
        return template('error', error_message="Cannot return as book not on loan.", back_button=True, signin_status=Signin_Status(cookie_key))
    else:
        # Book taken out, so update due date if not already overdue.
            db.execute(f"""
                UPDATE Loan
                SET dateReturned = ?
                WHERE hardCopyId = ?        -- this book
                AND   borrowerId = ?        -- borrowed by this user
                AND   dateReturned IS NULL  -- not returned
                """, (today_date(), copy_id, signin_status.id))
            return redirect('/account')

run(host='localhost', port=8080, debug=True)