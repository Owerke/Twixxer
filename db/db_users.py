from datetime import datetime
import json
from typing import List
from models.user import User
import common

def get_users():
    try:
        db = common._db_connect(common.DB_NAME)
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        results = cur.fetchall()

        if not results:
            print("No results")
            # We did not find anything at all
            return []

        users = []
        for result in results:
            user: User = {
                'id': result["id"],
                'username': result["username"],
                'firstname': result["firstname"],
                'lastname': result["lastname"],
                'password': result["password"],
                'created': result["created"]
            }
            users.append(user)

        return users

    except Exception as e:
        print(e)
        return None

def get_user_by_username(username: str):
    try:
        db = common._db_connect(common.DB_NAME)
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cur.fetchone()

        if not result:
            print("No results")
            # We did not find anything at all
            return None

        user: User = {
            'id': result["id"],
            'username': result["username"],
            'firstname': result["firstname"],
            'lastname': result["lastname"],
            'password': result["password"],
            'created': result["created"]
        }
        print(user)
        return user

    except Exception as e:
        print(e)
        return None


def create_user(user: User):
    try:
        db = common._db_connect(common.DB_NAME)
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user["id"], user["username"], user["firstname"], user["lastname"], user["password"], user["created"]))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
