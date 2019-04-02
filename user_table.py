class User:
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
        self.card_number = db_data["cardNo"]
        self.reg_date = db_data["regDate"]
    # def set_GenUser_detail(self, db, detail, value):
    #     keys = self.GenUser_row.keys()
    #     if detail in keys:
    #         query = "UPDATE GenUser SET " + detail + " = ? WHERE id = ?"
    #         db.execute(query, (value, self.id))
    #     db.execute("UPDATE GenUser SET ? = ? WHERE id = ?", (detail, value, self.id))
    #     # Could handle invalid inputs if necessary
    # def set_GenUser_details(self, db, form_obj):
    #     keys = self.GenUser_row.keys()
    #     for key in keys:
    #         if key in form_obj.keys():
    #             query = "UPDATE GenUser SET " + key + " = ? WHERE id = ?"
    #             db.execute(query, (form_obj.get(key), self.id))