import calendar, time

def get_user_access_log(db, user_id):
    return db.execute("""
        SELECT BookDetail.bookName, BookDetail.id, PastAccess.dateAccessed, BookDetail.url
        FROM PastAccess
        INNER JOIN BookDetail
        ON PastAccess.bookId = BookDetail.id
        WHERE PastAccess.userId = ?
        ORDER BY PastAccess.dateAccessed DESC
        LIMIT 5
        """, (user_id,)).fetchall()

def record_user_access(db, user_id, resource_id):
    db.execute("""
    INSERT INTO PastAccess (userID, bookID, dateAccessed)
    VALUES (?,?,?)""", (user_id, resource_id, calendar.timegm(time.localtime())))