def upgrade(conn):

    conn.execute("""
        INSERT INTO GenUser (firstName, lastName, emailAddr, townCity, postcode) VALUES
            ('Emily', 'F', 'e.f@something.com', 'London', 'AB1 2CD'),
            ('Robin', 'H', 'r.h@something.com', 'London', 'AB1 2CD'),
            ('Stefan', 'C', 's.c@something.com', 'London', 'AB1 2CD'),
            ('Rohit', 'G', 'r.g@something.com', 'London', 'EF3 4GH'),
            ('Filipp', 'L', 'f.l@something.com', 'London', 'IJ5 6KL'),
            ('Holly', 'K', 'h.k@something.com', 'London', 'MN7 8OP'),
            ('Rebecca', 'C', 'r.c@something.com', 'London', 'QR9 10ST')""")

    conn.execute("""INSERT INTO PublicUser (cardNo, regDate, userId) VALUES
            ('1111', 20190325, 1),
            ('1112', 20190325, 2),
            ('1113', 20190325, 3),
            ('1114', 20190325, 4),
            ('1115', 20190325, 5),
            ('1116', 20190325, 6),
            ('1117', 20190325, 7)""")

    conn.execute("""INSERT INTO BookDetail (bookName) VALUES
            ('Harry Potter 1'),
            ('Harry Potter 2'),
            ('Harry Potter 3'),
            ('1984'),
            ('Animal Farm'),
            ('Middlemarch'),
            ('Lord of the Rings'),
            ('Fab book with two authors'),
            ('Amazing book with three authors')""")

    conn.execute("""INSERT INTO Author (name) VALUES
            ('J. K. Rowling'),
            ('George Orwell'),
            ('George Eliot'),
            ('J. R. R. Tolkien'),
            ('Fab author 1'),
            ('Fab amazing author 2'),
            ('Amazing author 3'),
            ('Amazing author 4')""")

    conn.execute("""INSERT INTO Publisher (name, city) VALUES
            ('William Blackwood and Sons', 'Edinburgh'),
            ('Bloomsbury', 'London'),
            ('Allen & Unwin', 'Sydney'),
            ('Fab publisher 1', 'Birmingham'),
            ('Amazing publisher 2', 'Reading')""")

    conn.execute("""INSERT INTO BookDetailAuthor (bookId, authorId, orderPos) VALUES
            (1, 1, 1),
            (2, 1, 1),
            (3, 1, 1),
            (4, 2, 1),
            (5, 2, 1),
            (6, 3, 1),
            (7, 4, 1),
            (8, 5, 1),
            (8, 6, 2),
            (9, 6, 1),
            (9, 7, 2),
            (9, 8, 3)""")

    conn.commit()

def downgrade(conn):
    # Need to work out if this is correct
    sql = """
        DELETE FROM BookDetailAuthor;
        DELETE FROM Author;
        DELETE FROM Publisher;
        DELETE FROM BookDetail;
        DELETE FROM PublicUser;
        DELETE FROM GenUser;
    """
    conn.execute(sql)
    conn.commit()