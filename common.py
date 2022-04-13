import sqlite3
import time
from models.user import User
from models.jwt import Jwt_data
import jwt

API_PREFIX = "api"

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"

JWT_SECRET = "9OzAdFhiJ44vUzK5ikTlflOgztgi45yft3C7VTK6ND2mTEhl9a"
JWT_COOKIE = "user_session_jwt"

DB_NAME = "database.sqlite"

def create_json_from_sqlite_result(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def _db_connect(db_name):
    db = sqlite3.connect(db_name)
    db.row_factory = create_json_from_sqlite_result
    return db

def create_jwt_with_data(jwt_data: Jwt_data):
    encoded_jwt = jwt.encode(jwt_data, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def create_jwt(id: str, username: str, email: str):
    data: Jwt_data = {
        "id": id,
        "username": username,
        "email": email,
        "iat" : int(time.time())
    }
    return create_jwt_with_data(data)

def create_jwt_for_user(user: User):
    return create_jwt(user["id"], user["username"], user["email"])

def decode_jwt(jwt_token: str):
    data: Jwt_data = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    return data
