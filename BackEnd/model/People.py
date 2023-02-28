from security.CryptoTools import md5
from security.RegexTools import isEmailValid
from model.JWT import JWT

import json
from bson.objectid import ObjectId


class People:
    id = 0
    name = ""
    surname = ""
    password = ""
    email = ""
    type = ""
    gender = ""
    birth_date = ""

    def login(self, mongoDatabase):
        mongoCollection = mongoDatabase[self.type]
        if isEmailValid(self.email) and len(self.password) > 5:
            myDoc = mongoCollection.find({"email": self.email})
            if(myDoc.count() > 0):
                encryptedPassword = self.password
                for i in range(0, 10):
                    encryptedPassword = md5(encryptedPassword)
                if encryptedPassword == myDoc[0]['password']:
                    refreshJWT = JWT(myDoc[0]['_id'].__str__(), "refresh")
                    accessJWT = JWT(myDoc[0]['_id'].__str__(), "access")
                    if refreshJWT.store_token(mongoDatabase) and accessJWT.store_token(mongoDatabase):
                        return json.dumps({
                            "refresh": refreshJWT.get_token(),
                            "access": accessJWT.get_token()
                        })
        return False

    def register(self, mongoDatabase):
        mongoCollection = mongoDatabase[self.type]
        if isEmailValid(self.email) and len(self.password) > 5:
            myDoc = mongoCollection.find({"email": self.email})
            if(myDoc.count() == 0):
                # find the max id
                self.id = 6040
                encryptedPassword = self.password
                for i in range(0, 10):
                    encryptedPassword = md5(encryptedPassword)
                mongoCollection.insert_one({
                    "name": self.name,
                    "surname": self.surname,
                    "email": self.email,
                    "password": encryptedPassword,
                    "id": self.id,
                    "gender": self.gender,
                    "birth_date": self.birth_date
                })
                return json.dumps(self.get_info())
            else:
                return "Email already exists"
        return False

    def get_info(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "gender": self.gender,
            "birth_date": self.birth_date,
            "id": self.id,
            "email": self.email
        }

    def get_info_from_db(self, mongoDatabase, idObj):
        mongoCollection = mongoDatabase[self.type]
        mongoDoc = mongoCollection.find({"_id": ObjectId(idObj)})
        if (mongoDoc.count() > 0):
            self.id = mongoDoc[0]['id']
            self.name = mongoDoc[0]['name']
            self.surname = mongoDoc[0]['surname']
            self.email = mongoDoc[0]['email']
            self.gender = mongoDoc[0]['gender']
            self.birth_date = mongoDoc[0]['birth_date']
