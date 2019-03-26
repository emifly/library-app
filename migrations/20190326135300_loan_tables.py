def upgrade(conn):
    conn.execute("DROP TABLE PastLoan;")
    print("bbb")

    conn.commit()

    

def downgrade(conn):
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


    conn.commit()