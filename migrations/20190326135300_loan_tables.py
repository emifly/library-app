def upgrade(conn):
    conn.execute("DROP TABLE PastLoan;")

    conn.execute('''CREATE TABLE IF NOT EXISTS Loan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrowerId INTEGER NOT NULL,
        hardCopyId INTEGER NOT NULL,

        borrowDate INTEGER NOT NULL,
        dueDate INTEGER NOT NULL,
        returnDate INTEGER,
            FOREIGN KEY (borrowerId) REFERENCES PublicUser(id),
            FOREIGN KEY (hardCopyId) REFERENCES HardCopy(id)
    );''')

    conn.commit()


def downgrade(conn):
    conn.execute("DROP TABLE Loan;")

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