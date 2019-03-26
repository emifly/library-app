def upgrade(conn):
    # Change PastLoan table to Loan
    conn.execute("DROP TABLE PastLoan;")

    conn.execute('''CREATE TABLE IF NOT EXISTS Loan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrowerId INTEGER NOT NULL,
        hardCopyId INTEGER NOT NULL,

        dataBorrowed INTEGER NOT NULL,
        dateDue INTEGER NOT NULL,
        dateReturned INTEGER,
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