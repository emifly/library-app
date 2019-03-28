from datetime import date

def upgrade(conn):

    conn.execute(f"""INSERT INTO Loan (borrowerId, hardCopyId, dataBorrowed, dateDue) VALUES
        (1, 3, {date(2019, 3, 27).toordinal()}, {date(2019, 4, 10).toordinal()}), -- on loan
        (1, 2, {date(2018, 3, 27).toordinal()}, {date(2018, 4, 10).toordinal()}), -- overdue

        (2, 7, {date(2019, 3, 27).toordinal()}, {date(2019, 4, 10).toordinal()}), -- on loan
        (2, 9, {date(2019, 3, 28).toordinal()}, {date(2019, 4, 11).toordinal()}) -- on loan
        """)

    conn.execute(f"""INSERT INTO Loan (borrowerId, hardCopyId, dataBorrowed, dateDue, dateReturned) VALUES
        (1, 1, {date(2019, 2, 20).toordinal()}, {date(2019, 3, 6).toordinal()}, {date(2019, 3, 1).toordinal()}) -- returned
        """)

    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")