from datetime import date

class Book:
    def __init__(self, id, db):
        self.id = id
        self.populate(db)
    def populate(self, db):
        self.BookDetail_row = db.execute("SELECT * FROM BookDetail WHERE id = ?", (self.id,)).fetchone()
        self.Author_rows = db.execute("SELECT * FROM Author INNER JOIN BookDetailAuthor ON authorId = Author.id WHERE bookId = ?", (self.id,)).fetchall()
        self.authors_string = compile_authors_string([row['name'] for row in self.Author_rows])
        self.online_link = f"/resource/{self.id}" if self.BookDetail_row['url'] else None
    def get_book_detail(self, detail):
        return self.BookDetail_row[detail]


def compile_authors_string(author_names):
    authors_string = ""
    for i in range(0, len(author_names)):
        if i < len(author_names) - 2:
            authors_string += author_names[i] + ", "
        elif i == len(author_names) - 2:
            authors_string += author_names[i] + " and "
        else:
            authors_string += author_names[i]
    return authors_string


def return_purpose_text(request_obj):
    if 'origin' in request_obj.params:
        origin = request_obj.query['origin']
        if origin == 'account':
            return " to view your account"
        elif origin == 'resource':
            return " to access this resource"
        else:
            return ""


def ordered_results(request_obj, db):
    detail = request_obj.query['searchdata']
    detail_type = request_obj.query['field']
    words = detail.split()          # Split searchdata into its constituent words
    if words == []:                 # Empty query should return all books
        results = db.execute("SELECT id FROM BookDetail").fetchall()
    if detail_type == "Title":
        # Priority: anything that matches detail exactly > anything that contains detail > anything that partially matches detail
        checker_values = [detail, detail]
        query_string = "SELECT id, CASE WHEN (bookName = ?) THEN 10 ELSE 0 END + \
            CASE WHEN (bookName LIKE '%' || ? || '%') THEN 5 ELSE 0 END"
        for i in range(1, len(words)):
            query_string += " + CASE WHEN (bookName LIKE '%' || ? || '%') THEN 1 ELSE 0 END"
            checker_values.append(words[i])
        query_string += " ratingSum FROM BookDetail WHERE ratingSum > "
        query_string += str(1 if len(words) < 4 else len(words) - 2) + " ORDER BY ratingSum DESC"
        results = db.execute(query_string, tuple(checker_values)).fetchall()
    else:
        checker_values = [detail, detail]
        query_string = "SELECT BookDetail.id, CASE WHEN (Author.name = ?) THEN 10 ELSE 0 END + \
            CASE WHEN (Author.name LIKE '%' || ? || '%') THEN 5 ELSE 0 END"
        for i in range(1, len(words)):
            query_string += " + CASE WHEN (Author.name LIKE '%' || ? || '%') THEN 1 ELSE 0 END"
            checker_values.append(words[i])
        query_string += " ratingSum FROM BookDetail INNER JOIN BookDetailAuthor ON BookDetail.id = bookId \
            INNER JOIN Author ON Author.id = authorId WHERE ratingSum > "
        query_string += str(1 if len(words) < 4 else len(words) - 2)
        query_string += " GROUP BY BookDetail.id ORDER BY ratingSum DESC"
        results = db.execute(query_string, tuple(checker_values)).fetchall()
    return results


def verify_form(form_obj, db):
    fname = form_obj.get('firstName')
    lname = form_obj.get('lastName')
    email = form_obj.get('emailAddr')
    pcode = form_obj.get('postcode')
    cardno = form_obj.get('cardNo')
    id_row = db.execute("SELECT * FROM GenUser WHERE (firstName, lastName, emailAddr, postcode) = (?, ?, ?, ?)", (fname, lname, email, pcode)).fetchone()
    if id_row == None:
        return False
    else:
        id = id_row[0]
        public_id_row = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardno,)).fetchone()
        if public_id_row == None:
            return False
        elif public_id_row['userId'] == id:
            return id
        else:
            return False

def verify_signup(form_obj, db):
    fname = form_obj.get('firstName')
    lname = form_obj.get('lastName')
    email = form_obj.get('emailAddr')
    pcode = form_obj.get('postcode')
    cardno = form_obj.get('cardNo')
    # Check if there is already an account associated with this library card number
    check_existing = db.execute("SELECT * FROM PublicUser WHERE (cardNo) = (?)", (cardno,)).fetchone()
    if check_existing != None:
        return False
    else:
        db.execute("INSERT INTO GenUser (firstName, lastName, emailAddr, postcode) VALUES (?, ?, ?, ?);", (fname, lname, email, pcode))
        # Get row id of newly added GenUser row to use as foreign key in PublicUser table
        new_row_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        date_entry = int(date.today().strftime('%Y%m%d'))
        db.execute("INSERT INTO PublicUser (cardNo, regDate, userId) VALUES (?, ?, ?);", (cardno, date_entry, new_row_id))
        return new_row_id



# Simple functions that could be inlined but useful if database date format changes later
def calculate_due_date(num_days):
    """
    Represented as the "proleptic Gregorian ordinal". Basically the number of days since a date way in the past.

    Examples:
        if num_days=0, then the book is due before the coming midnight.
        if num_days=1, then the book should be returned the following day (or the day it was taken out).
        if numdays=7, then the last day for returning will be the same day of the week as it was taken out.
    """
    return num_days + date.toordinal(date.today())

def today_date():
    return date.toordinal(date.today())

def dbdate_to_date(db_date):
    return date.fromordinal(db_date)