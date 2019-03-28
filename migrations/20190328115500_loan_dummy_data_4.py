def upgrade(conn):

    conn.execute("""INSERT INTO HardCopy (bookId) VALUES
            (4), (4),
            (5), (5), (5),
            (6),
            (7), (7),
            (8),
            (9)""")


    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")