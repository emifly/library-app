def upgrade(conn):
    # We are no longer going to use OnlineResource
    conn.execute('DROP TABLE OnlineResource;')

    # Add some dummy online resources
    conn.execute('ALTER TABLE BookDetail ADD url TEXT;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Philosopher%27s_Stone" WHERE id = 1;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Chamber_of_Secrets" WHERE id = 2;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Prisoner_of_Azkaban" WHERE id = 3;')

    # Add some dummy access records
    conn.execute("""INSERT INTO PastAccess (userID, bookID, dateAccessed) VALUES
        (1, 1, 1553621057),
        (1, 3, 1553620057),
        (2, 2, 1553621125)""")

    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")