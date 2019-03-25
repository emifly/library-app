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
from bottle import get, post, run, debug, install, request, response, redirect, template, static_file
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
install(message_plugin)
install(SQLitePlugin(dbfile=db_file))
cookieKey = "1234567890987654321"

## Routes
### Static files - DONE
@get('/static/<file:path>')
def serve_static(file):
    return static_file(file, root='./static')

### Homepage - DONE
@get('/')
def display_homepage():
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    return template('index', indexpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn)

### Sign-in page - DONE. Actions:
#### - Validate user details and send them via post request to their account page
@post('/signin')
def display_signin_post(db):
    # Check if user is signed in. (Not quite taking my security as seriously as I should be...)
    userId = request.get_cookie("id", secret=cookieKey)
    if userId:
        return redirect('/account')
    else:
        # Check if there is the expected post data
        if 'firstName' in request.forms:
            fname = request.forms.get('firstName')
            lname = request.forms.get('lastName')
            email = request.forms.get('emailAddr')
            pcode = request.forms.get('postcode')
            cardNo = request.forms.get('cardNo')
            # Check if they made an error filling in the form
            idRow = db.execute("SELECT * FROM GenUser WHERE (firstName, lastName, emailAddr, postcode) = (?, ?, ?, ?)", (fname, lname, email, pcode)).fetchone()
            if idRow == None:
                # No row with the right details was found, so display error
                return template('signin', error=True)
            else:
                id = idRow[0]
                publicIdRow = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardNo,)).fetchone()
                # Check if there is an entry in PublicUser corresponding to the id
                if publicIdRow == None:
                    return template('signin', error=True)
                else:
                    # If there is an entry, work out if their personal details match their library card number
                    userId = publicIdRow['userId']
                    if userId == id:
                        response.set_cookie("id", str(id), secret=cookieKey)
                        return redirect('/account')
                    # Otherwise, there was a conflict in the details, so display error
                    else:
                        return template('signin', error=True)                
        # Would be strange not to have any relevant post data, but if so, serve empty form as normal
        else:
            return template('signin', error=True)
@get('/signin')
def display_signin_get(db):
    # Check if user already signed in
    userId = request.get_cookie("id", secret=cookieKey)
    # If yes, redirect to account page
    if userId:
        return redirect('/account')
    # If no, serve empty form as normal
    else:
        return template('signin', error=False)

### Account page. Actions:
#@get('/account')
#### - Use post data to build account details page, include edit details button
#### - Send user to sign in page if not signed in
#### - Let user edit details, send users to same page via post request with new data
@get('/account')
def display_account_details(db):
    # Check if signed in. If yes, continue. Otherwise, redirect to sign-in page
    isSignedIn = request.get_cookie("id", secret=cookieKey)
    if not isSignedIn:
        return redirect('/signin')
    else:
        userInfo = db.execute("SELECT * FROM GenUser WHERE (id) = (?)", (isSignedIn,)).fetchone()
        fname = userInfo['firstName']
        lname = userInfo['lastName']
        email = userInfo['emailAddr']
        pcode = userInfo['postcode']
        return template('account', firstname=fname, lastname=lname, email=email, postcode=pcode, signout=True)
@post('/account') # For if user has updated their details
def update_account_details(db):
    # User should definitely be signed in to have reached this page via post, but check anyway
    id = request.get_cookie("id", secret=cookieKey)
    if not id:
        return redirect('/signin')
    else:
        # Check form data
        fname = request.forms.get('firstName')
        lname = request.forms.get('lastName')
        email = request.forms.get('emailAddr')
        pcode = request.forms.get('postcode')
        # NOTE - this line needs checking after the JavaScript is in place
        db.execute("UPDATE GenUser SET (firstName, lastName, emailAddr, postcode) VALUES (?, ?, ?, ?) WHERE (id) = (?);", (fname, lname, email, pcode, id))
        # Could just use the info we already have to render the page, but redirect to GET keeps it consistent if we make changes
        return redirect('/account')

### Sign-up page - DONE. Actions: 
#### - Send new user details via post request to confirmation page
@get('/signup')
def display_signup():
    # Check if user already signed up
    userId = request.get_cookie("id", secret=cookieKey)
    # If yes, redirect to account page
    if userId:
        return redirect('/account')
    # Otherwise, display sign up page as normal
    else:
        errorVal = False
        if 'error' in request.query:
            errorVal = True if str(request.query['error']) == 'True' else False
        return template('signup', error=errorVal)

### Confirm sign-up page - DONE. Actions: 
#### - Send new user back to sign in page where they can use their new details
@post('/confirmation')
def display_confirmation(db):
    fname = request.forms.get('firstName')
    lname = request.forms.get('lastName')
    email = request.forms.get('emailAddr')
    pcode = request.forms.get('postcode')
    cardNo = request.forms.get('cardNo')
    # Check if there is already an account associated with this library card number
    check = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardNo,)).fetchone()
    if check != None:
        return redirect('/signup?error=True')
    else:
        # Add details to database
        db.execute("INSERT INTO GenUser (firstName, lastName, emailAddr, postcode) VALUES (?, ?, ?, ?);", (fname, lname, email, pcode))
        # Get row id of newly added GenUser row to use as foreign key in PublicUser table
        newRowId = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        dateEntry = int(date.today().strftime('%Y%m%d'))
        db.execute("INSERT INTO PublicUser (cardNo, regDate, userId) VALUES (?, ?, ?);", (cardNo, dateEntry, newRowId))
        return template('confirmation', firstName=fname)
# Redirect to home if anyone tries to access this page via get request
@get('/confirmation')
def redirect_confirmation(db):
    return redirect('/')

### Sign-out page - DONE. Actions: 
#### - Sign user out
@get('/signout')
def display_signout():
    isSignedIn = request.get_cookie("id", secret=cookieKey)
    # If signed in, sign out and display confirmation that this has happened
    if isSignedIn:
        response.delete_cookie("id")
        return template('signout')
    # Otherwise, redirect to home
    else:
        return redirect('/')

### Search page. Actions:
#### - Send form data via get request to same location, use this to display results
#### - Send get request to individual item pages depending on which result user selects
@get('/search')
def display_search(db):
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    # If a search hasn't been carried out yet, return empty page
    if 'searchdata' not in request.params:
        return template('search', searchpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn)
    # Otherwise, deal with the form data. NOTE: need to add validation here
    else:
        detail = request.query['searchdata']
        detailType = request.query['field']
        if detailType == "Title":       # Title
            results = db.execute("SELECT * FROM BookDetail WHERE bookName LIKE '%' || (?) || '%'", (detail,)).fetchall()
        elif detailType == "Author":    # Author
            names = detail.split()      # Split the query by spaces if necessary
            searchValues = tuple(names)
            # Find the ids of authors that could work
            buildQuery = "SELECT id FROM Author WHERE name LIKE '%' || (?) || '%'"
            for i in range(1, len(names)):  # Add extra query lines if multiple words in user input
                buildQuery += " AND name LIKE '%' || (?) || '%'"
            if len(names) < 2:  # Make sure to cover case where there's only one search word
                authorIds = db.execute(buildQuery, (detail,)).fetchall()
            else:
                authorIds = db.execute(buildQuery, searchValues).fetchall()
            # Find the bookIds of matching rows in the BookDetailAuthor join table
            buildQuery = "SELECT bookId FROM BookDetailAuthor WHERE (authorId = ?)"
            for i in range(1, len(authorIds)):
                buildQuery += " OR (authorId = ?)"
            # STILL TO DO: run query
            # STILL TO DO: Find the details of matching books in BookDetail table
        return template('search', searchpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn, results=results)

### Book pages. Actions:
#### Eventually: show how many copies of the book in question are available
#### Eventually: allow users to make reservations
@get('/book/<id>')
def display_book_page(db, id):
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    bookName = db.execute("SELECT bookName FROM BookDetail WHERE id = ?", (id,)).fetchone()[0]
    authorId = db.execute("SELECT authorId FROM BookDetailAuthor WHERE bookId = ?", (id,)).fetchall() # Each row represents an author
    authorNames = []
    for i in range(0, len(authorId)):   # For each author, get their first and last name
        currentName = db.execute("SELECT name FROM Author WHERE id = ?", (authorId[i][0],)).fetchone()[0]
        authorNames.append(currentName)
    authorsString = ""
    for i in range(0, len(authorNames)):    # Could move this part into a separate function for clarity
        if i < len(authorNames) - 2:
            authorsString += authorNames[i] + ", "
        elif i == len(authorNames) - 2:
            authorsString += authorNames[i] + " and "
        else:
            authorsString += authorNames[i]
    return template('book', book=bookName, authors=authorsString, dispsignin=True, buttontext=buttonText, signout=signOutBtn)

### Contact page
@get('/contact')
def display_contact():
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    return template('contact', contactpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn)

### Librarians: different user details page, but same actions
#@get('/secretlibrarianroute/account')

### Librarians: extended search page. Same actions
#@get('/secretlibrarianroute/search')

### Librarians: page for adding books. Actions:
#### - Send new book details via post request to same location, add details to database
#@get('/secretlibrarianroute/inventory')

run(host='localhost', port=8080, debug=True)