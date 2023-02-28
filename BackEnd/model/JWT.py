import jwt
from uuid import uuid4
from datetime import datetime, timedelta
from config import secret_key


class JWT:
    token = ""
    token_type = ""
    created_at = ""
    expires_at = ""
    user_id = ""
    jti = ""

    def __init__(self, user_id, token_type):
        self.created_at = self.create_created_at()
        self.expires_at = self.create_expires_at()
        self.user_id = user_id
        self.jti = uuid4().hex
        self.token_type = token_type
        self.token = self.create_jwt_token()

    def create_created_at(self):
        return datetime.now().timestamp().__int__()

    def create_expires_at(self):
        return (datetime.now()+timedelta(days=1)).timestamp().__int__()

    def create_jwt_token(self):
        return jwt.encode({
            "token_type": self.token_type,
            "exp": self.expires_at,
            "jti": self.jti,
            "user_id": self.user_id
        }, secret_key, algorithm='HS256')

    def store_token(self, mongoDatabase):
        jwtCollection = mongoDatabase[self.token_type]
        jwtDocument = jwtCollection.find({"token": self.token})
        if jwtDocument.count() == 0:
            jwtCollection.insert_one({
                "token": self.token,
                "created_at": self.created_at,
                "expires_at": self.expires_at,
                "user_id": self.user_id,
                "jti": self.jti
            })
            return True
        return False

    def get_token(self):
        return self.token
