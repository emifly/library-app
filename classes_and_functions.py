from datetime import date

## Classes and Functions
class User:
    def __init__(self, id, db):
        self.id = id
        self.populate(db)
    def populate(self, db):
        self.GenUserRow = db.execute("SELECT * FROM GenUser WHERE id = ?", (self.id,)).fetchone()
        self.PublicUserRow = db.execute("SELECT * FROM PublicUser WHERE userId = ?", (self.id,)).fetchone()
    def getGenDetail(self, detail):
        return self.GenUserRow[detail]
    def getPublicDetail(self, detail):
        return self.PublicUserRow[detail]
    def setGenDetail(self, db, detail, value):
        keys = self.GenUserRow.keys()
        if detail in keys:
            query = "UPDATE GenUser SET " + detail + " = ? WHERE id = ?"
            db.execute(query, (value, self.id))
        db.execute("UPDATE GenUser SET ? = ? WHERE id = ?", (detail, value, self.id))
        # Could handle invalid inputs if necessary
    def setGenDetails(self, db, formObj):
        keys = self.GenUserRow.keys()
        for key in keys:
            if key in formObj.keys():
                query = "UPDATE GenUser SET " + key + " = ? WHERE id = ?"
                db.execute(query, (formObj.get(key), self.id))

class Book:
    def __init__(self, id, db):
        self.id = id
        self.populate(db)
    def populate(self, db):
        self.BookDetailRow = db.execute("SELECT * FROM BookDetail WHERE id = ?", (self.id,)).fetchone()
        self.AuthorRows = db.execute("SELECT * FROM Author INNER JOIN BookDetailAuthor ON authorId = Author.id WHERE bookId = ?", (self.id,)).fetchall()
        self.authorString = compile_authors_string([row['name'] for row in self.AuthorRows])
        self.onlineLink = f"/resource/{self.id}" if self.BookDetailRow['url'] else None
    def getBookDetail(self, detail):
        return self.BookDetailRow[detail]

def compile_authors_string(authorNames):
    authorsString = ""
    for i in range(0, len(authorNames)):
        if i < len(authorNames) - 2:
            authorsString += authorNames[i] + ", "
        elif i == len(authorNames) - 2:
            authorsString += authorNames[i] + " and "
        else:
            authorsString += authorNames[i]
    return authorsString

def return_purpose_text(requestObj):
    if 'origin' in requestObj.params:
        origin = requestObj.query['origin']
        if origin == 'account':
            return " to view your account"
        elif origin == 'resource':
            return " to access this resource"
        else:
            return ""

def ordered_results(requestObj, db):
    detail = requestObj.query['searchdata']
    detailType = requestObj.query['field']
    words = detail.split()          # Split searchdata into its constituent words
    if words == []:                 # Empty query should return all books
        results = db.execute("SELECT id FROM BookDetail").fetchall()
    if detailType == "Title":
        # Priority: anything that matches detail exactly > anything that contains detail > anything that partially matches detail
        checkerValues = [detail, detail]
        queryString = "SELECT id, CASE WHEN (bookName = ?) THEN 10 ELSE 0 END + \
            CASE WHEN (bookName LIKE '%' || ? || '%') THEN 5 ELSE 0 END"
        for i in range(1, len(words)):
            queryString += " + CASE WHEN (bookName LIKE '%' || ? || '%') THEN 1 ELSE 0 END"
            checkerValues.append(words[i])
        queryString += " ratingSum FROM BookDetail WHERE ratingSum > "
        queryString += str(1 if len(words) < 4 else len(words) - 2) + " ORDER BY ratingSum DESC"
        results = db.execute(queryString, tuple(checkerValues)).fetchall()
    else:
        checkerValues = [detail, detail]
        queryString = "SELECT BookDetail.id, CASE WHEN (Author.name = ?) THEN 10 ELSE 0 END + \
            CASE WHEN (Author.name LIKE '%' || ? || '%') THEN 5 ELSE 0 END"
        for i in range(1, len(words)):
            queryString += " + CASE WHEN (Author.name LIKE '%' || ? || '%') THEN 1 ELSE 0 END"
            checkerValues.append(words[i])
        queryString += " ratingSum FROM BookDetail INNER JOIN BookDetailAuthor ON BookDetail.id = bookId \
            INNER JOIN Author ON Author.id = authorId WHERE ratingSum > "
        queryString += str(1 if len(words) < 4 else len(words) - 2)
        queryString += " GROUP BY BookDetail.id ORDER BY ratingSum DESC"
        results = db.execute(queryString, tuple(checkerValues)).fetchall()
    return results

def verify_form(formObj, db):
    fname = formObj.get('firstName')
    lname = formObj.get('lastName')
    email = formObj.get('emailAddr')
    pcode = formObj.get('postcode')
    cardNo = formObj.get('cardNo')
    idRow = db.execute("SELECT * FROM GenUser WHERE (firstName, lastName, emailAddr, postcode) = (?, ?, ?, ?)", (fname, lname, email, pcode)).fetchone()
    if idRow == None:
        return True
    else:
        id = idRow[0]
        publicIdRow = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardNo,)).fetchone()
        if publicIdRow == None:
            return False
        elif publicIdRow['userId'] == id:
            return id
        else:
            return False

def verify_signup(formObj, db):
    fname = formObj.get('firstName')
    lname = formObj.get('lastName')
    email = formObj.get('emailAddr')
    pcode = formObj.get('postcode')
    cardNo = formObj.get('cardNo')
    # Check if there is already an account associated with this library card number
    check = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardNo,)).fetchone()
    if check != None:
        return False
    else:
        db.execute("INSERT INTO GenUser (firstName, lastName, emailAddr, postcode) VALUES (?, ?, ?, ?);", (fname, lname, email, pcode))
        # Get row id of newly added GenUser row to use as foreign key in PublicUser table
        newRowId = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        dateEntry = int(date.today().strftime('%Y%m%d'))
        db.execute("INSERT INTO PublicUser (cardNo, regDate, userId) VALUES (?, ?, ?);", (cardNo, dateEntry, newRowId))
        return newRowId

def calculate_due_date(numDays):
    """
    Represented as the "proleptic Gregorian ordinal". Basically the number of days since a date way in the past.

    Examples:
        if numDays=0, then the book is due before the coming midnight.
        if numDays=1, then the book should be returned the following day (or the day it was taken out).
        if numdays=7, then the last day for returning will be the same day of the week as it was taken out.
    """
    return numDays + date.toordinal(date.today())

def today_date():
    return date.toordinal(date.today())

def dbdate_to_date(dbDate):
    return date.fromordinal(dbDate)