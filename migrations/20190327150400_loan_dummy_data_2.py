def upgrade(conn):

    conn.execute('UPDATE BookDetail SET url = NULL WHERE id = 3;')

    conn.execute('''DROP TABLE IF EXISTS HardCopy''')

    conn.execute('''
        CREATE TABLE HardCopy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookId INTEGER NOT NULL,
                FOREIGN KEY (bookId) REFERENCES BookDetail(id)
        )
    ''')

    conn.commit()


def downgrade(conn):
    print("Sorry downgrade not implemented")