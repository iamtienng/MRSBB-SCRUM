from flask import Blueprint, request

from model.User import User
from config import db

from datetime import datetime

import json
from bson.objectid import ObjectId

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/jwt/verify/", methods=['POST'])
def verify_auth():
    data = request.get_json()
    jwtQuery = db['access'].find({"token": data['token']})
    if(jwtQuery.count() > 0):
        if datetime.now().timestamp().__int__() < jwtQuery[0]['expires_at']:
            return "", 200
    return "", 401


@auth_bp.route("/users/me/", methods=['GET'])
def load_user():
    data = request.headers.get('Authorization')[4:]
    jwtQuery = db['access'].find({"token": data})
    if(jwtQuery.count() > 0):
        if datetime.now().timestamp().__int__() < jwtQuery[0]['expires_at']:
            user = User()
            user.get_info_from_db(db, jwtQuery[0]['user_id'])
            return json.dumps(user.get_info()), 200
    return "", 401


# login function
@auth_bp.route("/jwt/create/", methods=['POST'])
def login():
    userdata = request.get_json()
    user = User()
    user.email = userdata['email']
    user.password = userdata['password']
    result = user.login(db)
    if result == False:
        return "Login failed", 401
    else:
        return result, 200


@auth_bp.route("/users/", methods=['POST'])
def signup():
    userdata = request.get_json()
    user = User()
    user.name = userdata['first_name']
    user.surname = userdata['last_name']
    user.email = userdata['email']
    user.password = userdata['password']
    user.gender = userdata['gender']
    user.birth_date = userdata['birth_date']

    if userdata['password'] != userdata['re_password']:
        return "Passwords do not match", 401
    elif user.register(db) == False:
        return "Signup failed", 401
    else:
        return user.register(db), 200
