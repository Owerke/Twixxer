import re
from models.jwt import Jwt_data
from models.user import User
# import db.db_users as Db_users # SQLIte
import db.mysql_users as Db_users # MySQL
import time
import jwt
import common
import base64

def password_authenticate(username: str, password: str):
    """Authenticate a user with username and password. Returns True if it's valid (authenticated), False if it's not."""
    user: User = Db_users.get_user_by_username(username)
    if not user or not user["password"] or not user["username"]:
        return False
    if user["password"] == password:
        return True
    return False

def create_jwt_with_data(jwt_data: Jwt_data):
    encoded_jwt = jwt.encode(jwt_data, common.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def create_jwt(id: str, username: str, email: str):
    """Create a JWT for a specific user"""
    data: Jwt_data = {
        "id": id,
        "username": username,
        "email": email,
        "iat" : int(time.time())
    }
    return create_jwt_with_data(data)

def create_jwt_for_user(user: User):
    """Create a JWT for a specific user"""
    return create_jwt(user["id"], user["username"], user["email"])

def decode_jwt(jwt_token: str):
    """
    Decode a JWT, and return the data in it if it's valid. If it's not valid, return None.

    It also checks if the user is actually in the database or not.
    """
    try:
        data: Jwt_data = jwt.decode(jwt_token, common.JWT_SECRET, algorithms=["HS256"])
        user: User = Db_users.get_user_by_username(data["username"])
        # if we get a user from the database, and we have a jwt, and the user id in both are the same
        if user and data and user["id"] == data["id"]:
            # we authenticate successfully
            return data
        return None
    except:
        return None

def parse_jwt_header(header: str):
    """Remove the Bearer text from the authentication header string. Return a raw (but still encoded) JWT."""
    if not header:
        return None
    # We get something like this: Bearer bGciOiJIUzI1NiJ9.eyJpZCI6IjZiYzA1MjRkLWJjMDgtMTFlYy1hNzNhLTU4MDBlMzdkNjhjYyIsInVzZXJuYW1lIjo
    # We need to remove the the "Bearer " from the beginning of the token.

    # Remove text from the beginning of a string https://stackoverflow.com/a/16891427
    return re.sub(r'^{0}'.format(re.escape("Bearer ")), '', header)

def parse_basic_auth_header(header: str):
    """
    Remove the Basic text from the authentication header string, decode the base64 encoded text,
    and then return the username/password combination in a dictionary.
    """
    if not header:
        return None
    # We get something liek this: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
    # We need to remove the "Basic " part, and base64 decode it, and then then we get the "username:password" combo.
    # Then we need to split the text into "username" and "password".

    # Remove text from the beginning of a string https://stackoverflow.com/a/16891427
    base64_credentials = re.sub(r'^{0}'.format(re.escape("Basic ")), '', header)
    # Decode base64 https://stackoverflow.com/a/50602520
    credentials = base64.b64decode(base64_credentials).decode('utf-8')
    # https://www.w3schools.com/python/ref_string_split.asp
    parts = credentials.split(":")
    # Make a credentials dictionary to easier handling
    credentials = dict(username=parts[0], password=parts[1])
    return credentials
