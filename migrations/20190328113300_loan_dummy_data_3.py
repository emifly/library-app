def upgrade(conn):

    conn.execute("""INSERT INTO HardCopy (bookId) VALUES
            (1),
            (2),
            (3),
            (2),
            (3),
            (3)""")


    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")