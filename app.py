# Configuration
db_file = 'librarytest.db'

# Database Seeding
import sqlite3
conn = sqlite3.connect(db_file)

conn.execute('''CREATE TABLE IF NOT EXISTS GenUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    middleNames TEXT,
    lastName TEXT NOT NULL,
    dateOfBirth INTEGER,            -- Format: ?
    emailAddr TEXT NOT NULL,        -- Important
    phoneNo1 TEXT,
    phoneNo1Type TEXT,              -- Can be user defined - suggest home/mobile/work
    phoneNo2 TEXT,
    phoneNo2Type TEXT,              -- Can be user defined - suggest home/mobile/work
    addrLine1 TEXT,
    addrLine2 TEXT,
    townCity TEXT,
    postcode TEXT NOT NULL          -- Important
        -- librarian and/or normal user: from PublicUser, Librarian
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS PublicUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cardNo TEXT NON NULL,           -- Possibility of integration with card number generation?
    regDate INTEGER,                -- Format: ?
        -- current loan info: from HardCopy
        -- past use info: from join table with HardCopy and OnlineResource
    userId INTEGER NOT NULL,
        FOREIGN KEY (userId) REFERENCES GenUser(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Librarian (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        -- What kind of thing would be useful for a librarian's account?
    userId INTEGER NOT NULL,
        FOREIGN KEY (userId) REFERENCES GenUser(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS BookDetail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookName TEXT NOT NULL,
        -- author: from Author
        -- publisher: in HardCopy or OnlineResource, from Publisher
    yearPublished INTEGER,
    isbn TEXT,
        -- classification: from Classification
    classmark TEXT
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS OnlineResource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libraryId TEXT,                 -- Could be used if library has pre-existing ID system
        -- publisher: from Publisher (different editions may have different publishers?)
    status INTEGER DEFAULT 1,       -- Status codes: 0 = unavailable, 1 = available
    purchaseDate INTEGER,           -- Format: ?
    renewalFreq INTEGER,            -- Status codes? Days?
    bookId INTEGER NOT NULL,
        FOREIGN KEY (bookId) REFERENCES BookDetail(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS HardCopy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libraryId TEXT,                 -- Could be used if library has pre-existing ID system
        -- publisher: from Publisher (different editions may have different publishers?)
    status INTEGER DEFAULT 1,       -- Status codes: ***
    purchaseDate INTEGER,           -- Format: ?
    loanLength INTEGER NOT NULL,    -- Status codes? Days?
    condition INTEGER DEFAULT 0,    -- Status codes: 0 = fine, 1 = worn/damaged, 2 = very poor
    bookId INTEGER NOT NULL,
    borrowerId INTEGER,             -- Current borrower
        FOREIGN KEY (bookId) REFERENCES BookDetail(id),
        FOREIGN KEY (borrowerId) REFERENCES GenUser(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstNames TEXT,
    lastName TEXT
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Publisher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    city TEXT
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Classification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT,
    code TEXT
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS BookDetailAuthor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookId INTEGER NOT NULL,
    authorId INTEGER NOT NULL,
    orderPos INTEGER DEFAULT 10,    -- Will use to list authors in the right order
        FOREIGN KEY (bookId) REFERENCES BookDetail(id),
        FOREIGN KEY (authorId) REFERENCES Author(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS HardCopyPublisher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookId INTEGER NOT NULL,
    publisherId INTEGER NOT NULL,
        FOREIGN KEY (bookId) REFERENCES HardCopy(id),
        FOREIGN KEY (publisherId) REFERENCES Publisher(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS OnlineResourcePublisher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookId INTEGER NOT NULL,
    publisherId INTEGER NOT NULL,
        FOREIGN KEY (bookId) REFERENCES OnlineResource(id),
        FOREIGN KEY (publisherId) REFERENCES Publisher(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS BookDetailClassification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookId INTEGER NOT NULL,
    classId INTEGER NOT NULL,
    orderPos INTEGER DEFAULT 10,    -- Will use to list classifications order inputted
        FOREIGN KEY (bookId) REFERENCES BookDetail(id),
        FOREIGN KEY (classId) REFERENCES Classification(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS PastLoan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    bookId INTEGER NOT NULL,
    dateBorrowed INTEGER,           -- Format: ?
    dateReturned INTEGER,           -- Format: ?
    wasOverdue INTEGER,             -- Status codes: 0 = not overdue, 1 = overdue
        FOREIGN KEY (userId) REFERENCES PublicUser(id),
        FOREIGN KEY (bookId) REFERENCES HardCopy(id)
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS PastAccess (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    bookId INTEGER NOT NULL,
    dateAccessed INTEGER,           -- Format: ?
        FOREIGN KEY (userId) REFERENCES PublicUser(id),
        FOREIGN KEY (bookId) REFERENCES OnlineResource(id)
);''')

conn.commit()

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
        return template('account', firstname=fname, lastname=lname, email=email, postcode=pcode)

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
#### - Send get request to individual item pages via get request based on what happens when
@get('/search')
def display_search(db):
    results = []
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    return template('search', searchpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn, results=results)

### Contact page
@get('/contact')
def display_contact():
    buttonText = "My account" if request.get_cookie("id", secret=cookieKey) else "Sign in"
    signOutBtn = True if request.get_cookie("id", secret=cookieKey) else False
    return template('contact', contactpage=True, dispsignin=True, buttontext=buttonText, signout=signOutBtn)

### Librarians: different user details page, but same actions
#@get('/secretlibrarianroute/search')

### Librarians: extended search page. Same actions
#@get('/secretlibrarianroute/account')

### Librarians: page for adding books. Actions:
#### - Send new book details via post request to same location, add details to database
#@get('/secretlibrarianroute/inventory')

'''

### To do: add books. EXAMPLE: /add/book?name=A%20Fun%20Story
@get('/add/book')
def table_add(db):
    return ""

'''

run(host='localhost', port=8080, debug=True)