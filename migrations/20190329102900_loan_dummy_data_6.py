from datetime import date

def upgrade(conn):

    conn.execute(f"""INSERT INTO Loan (borrowerId, hardCopyId, dateBorrowed, dateDue) VALUES
        (1,15, {date(2018, 12, 24).toordinal()}, {date(2019, 3, 29).toordinal()}) -- on loan
        """)

    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")