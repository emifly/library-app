def upgrade(conn):
    # We are no longer going to use OnlineResource
    conn.execute('DROP TABLE OnlineResource;')

    # Add some dummy onine resources
    conn.execute('ALTER TABLE BookDetail ADD url TEXT;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Philosopher%27s_Stone" WHERE id = 1;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Chamber_of_Secrets" WHERE id = 2;')
    conn.execute('UPDATE BookDetail SET url = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Prisoner_of_Azkaban" WHERE id = 3;')

    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")