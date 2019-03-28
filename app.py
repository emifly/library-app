# Configuration
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
cookieKey = "1234567890987654321"

## Classes and Functions
from classes_and_functions import *
def signin_status():
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    return buttonText, signOutBtn

## Routes
### Static files - DONE
@get('/static/<file:path>')
def serve_static(file):
    return static_file(file, root='./static')

### Errors - DONE
@error(400)
def error400(error):
    buttonText, signOutBtn = signin_status()
    errorText = "Something seems to have gone wrong with this page request."
    return template('error', errormessage=errorText, buttontext=buttonText, signout=signOutBtn)
@error(401)
def error401(error):
    buttonText, signOutBtn = signin_status()
    errorText = "You don't appear to have permission to access this page."
    return template('error', errormessage=errorText, buttontext=buttonText, signout=signOutBtn)
@error(403)
def error403(error):
    buttonText, signOutBtn = signin_status()
    errorText = "You don't appear to have permission to access this page."
    return template('error', errormessage=errorText, buttontext=buttonText, signout=signOutBtn)
@error(404)
def error404(error):
    buttonText, signOutBtn = signin_status()
    errorText = "There doesn't seem to be anything here."
    return template('error', errormessage=errorText, buttontext=buttonText, signout=signOutBtn)

### Homepage - DONE
@get('/')
def display_homepage():
    buttonText, signOutBtn = signin_status()
    return template('index', buttontext=buttonText, signout=signOutBtn)

### Sign-in page - DONE. Actions:
#### - Validate user details and send them via post request to their account page
@post('/signin')
def display_signin_post(db):
    userId = request.get_cookie("id", secret=cookieKey)
    if userId:
        return redirect('/account')
    elif 'firstName' in request.forms:
        id = verify_form(request.forms, db)
        if id == False:
            return template('signin', error=True)
        else:
            response.set_cookie("id", str(id), secret=cookieKey)
            return redirect('/account')
    else:
        return template('signin', error=True)
@get('/signin')
def display_signin_get(db):
    userId = request.get_cookie("id", secret=cookieKey)
    if userId:
        return redirect('/account')
    else:
        return template('signin', error=False)

### Account page. Actions:
#@get('/account')
#### - Use post data to build account details page, include edit details button
#### - Send user to sign in page if not signed in
#### - Let user edit details, send users to same page via post request with new data
@get('/account')
def display_account_details(db):
    idIfSignedIn = request.get_cookie("id", secret=cookieKey)
    if not idIfSignedIn:
        return redirect('/signin')
    else:
        # Account Details
        thisUser = User(idIfSignedIn, db)
        # Access Log
        accessQueryResult = db.execute("""
                        SELECT BookDetail.bookName, BookDetail.id, PastAccess.dateAccessed, BookDetail.url
                        FROM PastAccess
                        INNER JOIN BookDetail
                        ON PastAccess.bookId = BookDetail.id
                        WHERE PastAccess.userId = ?
                        ORDER BY PastAccess.dateAccessed DESC
                        LIMIT 5
                        """, (idIfSignedIn,)).fetchall()
        accessLog = [{
            "bookname": bookName,
            "url": f"/resource/{resourceId}" if url else None,
            "date": time.strftime("%H:%M %d %B %Y", time.localtime(t))
            }
            for bookName, resourceId, t, url in accessQueryResult]
        # Active Loan Details
        loanQueryResult = db.execute("""
                        SELECT BookDetail.bookName, Loan.hardCopyId, Loan.dataBorrowed, Loan.dateDue FROM Loan
                        INNER JOIN HardCopy ON Loan.hardCopyId = HardCopy.id
                        INNER JOIN BookDetail ON HardCopy.bookId = BookDetail.id
                        WHERE borrowerId = ? AND dateReturned IS NULL
                        ORDER BY Loan.dateDue ASC
                        """, (idIfSignedIn,)).fetchall()
        activeLoans = [{
            "book_title": book_name,
            "copy_id": copy_id,
            "date_borrowed": dbdate_to_date(date_borrowed),
            "date_due": dbdate_to_date(date_due)
        }
        for book_name, copy_id, date_borrowed, date_due in loanQueryResult]

        return template('account', user=thisUser, accesslog=accessLog, active_loans=activeLoans, today=date.today())

@post('/account') # For if user has updated their details
def update_account_details(db):
    id = request.get_cookie("id", secret=cookieKey)
    if not id:
        return redirect('/signin')
    else:
        thisUser = User(id, db)
        thisUser.setGenDetails(db, request.forms)
        # Could just use the info we already have to render the page, but redirect to GET keeps it consistent if we make changes
        return redirect('/account')

### Sign-up page - DONE. Actions: 
#### - Send new user details via post request to confirmation page
@get('/signup')
def display_signup():
    userId = request.get_cookie("id", secret=cookieKey)
    if userId:
        return redirect('/account')
    else:
        errorVal = False
        if 'error' in request.query:
            errorVal = True if str(request.query['error']) == 'True' else False
        return template('signup', error=errorVal)

### Confirm sign-up page - DONE. Actions: 
#### - Send new user back to sign in page where they can use their new details
@post('/confirmation')
def display_confirmation(db):
    newUserId = verify_signup(request.forms, db)
    # verify_signup returns false if there is already an account associated with this library card number
    if newUserId == False:
        return redirect('/signup?error=True')
    else:
        newUser = User(newUserId, db)
        return template('confirmation', user=newUser)
# Redirect to home if anyone tries to access this page via get request
@get('/confirmation')
def redirect_confirmation(db):
    return redirect('/')

### Sign-out page - DONE. Actions: 
#### - Sign user out
@get('/signout')
def display_signout():
    isSignedIn = request.get_cookie("id", secret=cookieKey)
    if isSignedIn:
        response.delete_cookie("id")
        return template('signout')
    else:
        return redirect('/')

### Search page. Actions:
#### - Send form data via get request to same location, use this to display results
#### - Send get request to individual item pages depending on which result user selects
@get('/search')
def display_search(db):
    buttonText, signOutBtn = signin_status()
    # If a search hasn't been carried out yet, return empty page
    if 'searchdata' not in request.params:
        return template('search', buttontext=buttonText, signout=signOutBtn)
    # Otherwise, deal with the form data. NOTE: need to add validation here ideally
    else:
        detail = request.query['searchdata']
        detailType = request.query['field']     
        words = tuple(request.query['searchdata'].split())  # Split searchdata into its constituent words
        if words == []:                        # Empty query: return all
            results = db.execute("SELECT id FROM BookDetail").fetchall()
        else:
            results = ordered_results(detail, detailType, db)
        return template('search', buttontext=buttonText, signout=signOutBtn, request=request, results=[Book(row['id'], db) for row in results])

### Book pages. Actions:
#### Eventually: show how many copies of the book in question are available
#### Eventually: allow users to make reservations
@get('/book/<bookId>')
def display_book_page(db, bookId):
    buttonText, signOutBtn = signin_status()
    thisBook = Book(bookId, db)
    return template('book', book=thisBook, buttontext=buttonText, signout=signOutBtn)

### Contact page
@get('/contact')
def display_contact():
    bt, s = signin_status()
    return template('contact', buttontext=bt, signout=s)

@get('/resource/<resourceId:int>')
def track_resource_access(db, resourceId):
    # Redirect if not signed in
    idIfSignedIn = request.get_cookie("id", secret=cookieKey)
    if not idIfSignedIn:
        return redirect('/signin')
    # Redirect if no online resource available
    buttonText, signOutBtn = signin_status()
    resourceQueryResponse = db.execute("SELECT url, bookName FROM BookDetail WHERE id = ?", (resourceId,)).fetchone()
    if not resourceQueryResponse:
        return template('error', errormessage="Resource not found.", backButton=True, buttontext=buttonText, signout=signOutBtn)
    if not resourceQueryResponse[0]:
        errorMessageTail = " is not currently available online."
        return template('error', emphdetails=resourceQueryResponse[1], errormessage=errorMessageTail, backButton=True, buttontext=buttonText, signout=signOutBtn)
    # Otherwise record access and redirect to resource
    db.execute("INSERT INTO PastAccess (userID, bookID, dateAccessed) VALUES (?,?,?)", (idIfSignedIn, resourceId, calendar.timegm(time.localtime())))
    redirect(resourceQueryResponse[0])

### Librarians: different user details page, but same actions
#@get('/secretlibrarianroute/account')

### Librarians: extended search page. Same actions
#@get('/secretlibrarianroute/search')

### Librarians: page for adding books. Actions:
#### - Send new book details via post request to same location, add details to database
#@get('/secretlibrarianroute/inventory')

run(host='localhost', port=8080, debug=True)