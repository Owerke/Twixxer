from datetime import datetime
import json
from typing import List
import uuid
from bottle import get, view, run, post, request
import common
from models.user import User
import db.db_users

@get(f"/{common.API_PREFIX}/users")
def get_users():
    users: List[User] = db.db_users.get_users();
    return json.dumps(users)

@get(f"/{common.API_PREFIX}/user/<username>")
def get_users(username):
    users: List[User] = db.db_users.get_user_by_username(username);
    return json.dumps(users)

@post(f"/{common.API_PREFIX}/users")
def create_user():
    user: User = {
            "username": request.json.get("username"),
            "id" : str(uuid.uuid1()),
            "firstname": request.json.get("firstname"),
            "lastname": request.json.get("lastname"),
            "password": request.json.get("password"),
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }


    db.db_users.create_user(user)
    return None
