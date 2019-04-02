class GenUser():
    def __init__(self, db, id):
        db_data = db.execute("""
            SELECT *
            FROM GenUser 
            LEFT JOIN PublicUser
            ON GenUser.id = PublicUser.userId
            WHERE GenUser.id = ?
            """, (id,)).fetchone()
        self.id = id
        self.first_name = db_data["firstName"]
        self.middle_names = db_data["middleNames"]
        self.last_name = db_data["lastName"]
        self.date_of_birth = db_data["dateOfBirth"]
        self.email_address = db_data["emailAddr"]
        self.phone_number_1_type = db_data["phoneNo1Type"]
        self.phone_number_1 = db_data["phoneNo1"]
        self.phone_number_2_type = db_data["phoneNo2Type"]
        self.phone_number_2 = db_data["phoneNo2"]
        self.address_line_1 = db_data["addrLine1"]
        self.address_line_2 = db_data["addrLine2"]
        self.town = db_data["townCity"]
        self.postcode = db_data["postcode"]


    def update(self, form):
        for key, value in form.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self, db):
        db.execute("""
        UPDATE GenUser
        SET (firstName, middleNames, lastName, dateOfBirth, emailAddr,
            phoneNo1Type, phoneNo1, phoneNo2Type, phoneNo2, addrLine1,
            addrLine2, townCity, postcode)
            =
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        WHERE id = ?
        """, (self.first_name, self.middle_names, self.last_name, self.date_of_birth, \
            self.email_address, self.phone_number_1_type, self.phone_number_1, \
            self.phone_number_2_type, self.phone_number_2, self.address_line_1, \
            self.address_line_2, self.town, self.postcode, self.id))
        

class PublicUser(GenUser):

    def __init__(self, db, id):
        super().__init__(db, id)
        db_data = db.execute("""
            SELECT *
            FROM PublicUser 
            WHERE userId = ?
            """, (id,)).fetchone()
        self.card_number = db_data["cardNo"]
        self.reg_date = db_data["regDate"]

    def save(self, db):
        super().save(db)
