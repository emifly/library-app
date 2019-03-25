def upgrade(conn):
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
        name TEXT
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

def downgrade(conn):
    sql = """
        DROP TABLE PastAccess;
        DROP TABLE PastLoan;
        DROP TABLE BookDetailAuthor;
        DROP TABLE HardCopyPublisher;
        DROP TABLE OnlineResourcePublisher;
        DROP TABLE BookDetailClassification;
        DROP TABLE Author;
        DROP TABLE Publisher;
        DROP TABLE Classification;
        DROP TABLE OnlineResource;
        DROP TABLE HardCopy;
        DROP TABLE BookDetail;
        DROP TABLE PublicUser;
        DROP TABLE Librarian;
        DROP TABLE GenUser;
    """
    conn.execute(sql)
    conn.commit()