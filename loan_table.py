from classes_and_functions import today_date, calculate_due_date

class ValidationError:

    def __init__(self, message):
        self.message = message

def get_current_loan_status(db, copy_id):
    return db.execute("""
        SELECT borrowerId, dateBorrowed, dateDue
        FROM Loan
        WHERE hardCopyId = ?        -- this book
        AND   dateReturned IS NULL  -- not returned
        """, (copy_id,)).fetchone()

def get_user_loan_count(db, user_id):
    return db.execute("""
        SELECT COUNT(*)
        FROM Loan
        WHERE borrowerId = ?        -- borrowed by this user 
        AND   dateReturned IS NULL  -- not returned
        """, (user_id,)).fetchone()[0]

def get_user_related_copy_count(db, user_id, copy_id):
    return db.execute("""
        SELECT COUNT(*) FROM Loan
        INNER JOIN HardCopy ON Loan.hardCopyId = HardCopy.id
        WHERE HardCopy.bookId = (SELECT bookId FROM HardCopy WHERE id = ?)  -- Same book (in the abstract, not hard copy)
            AND   borrowerId  = ?                                           -- borrowed by this user
            AND   dateReturned IS NULL                                      -- not returned
        """, (copy_id, user_id)).fetchone()[0]

def issue_copy_to_user(db, user_id, copy_id, due_date):
    db.execute(f"""
        INSERT INTO Loan (borrowerId, hardCopyId, dateBorrowed, dateDue)
        VALUES (?, ?, ?, ?)
        """, (user_id, copy_id, today_date(), due_date))

def renew_copy(db, copy_id, renew_date):
    db.execute(f"""
        UPDATE Loan
        SET dateDue = ?
        WHERE hardCopyId = ?        -- this book
        AND   dateReturned IS NULL  -- not returned
        """, (renew_date, copy_id))

def return_copy(db, copy_id):
    db.execute(f"""
        UPDATE Loan
        SET dateReturned = ?
        WHERE hardCopyId = ?        -- this book
        AND   dateReturned IS NULL  -- not returned
        """, (today_date(), copy_id))