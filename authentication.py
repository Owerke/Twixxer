import re
from models.jwt import Jwt_data
from models.user import User
import db.db_users as Db_users
import time
import jwt
import common

def create_jwt_with_data(jwt_data: Jwt_data):
    encoded_jwt = jwt.encode(jwt_data, common.JWT_SECRET, algorithm="HS256")
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
    """Remove the Bearer header from the authentication header string."""
    # We get something like this: Bearer bGciOiJIUzI1NiJ9.eyJpZCI6IjZiYzA1MjRkLWJjMDgtMTFlYy1hNzNhLTU4MDBlMzdkNjhjYyIsInVzZXJuYW1lIjo
    # We need to remove the the "Bearer " from the beginning of the token.
    if not header:
        return None

    return re.sub(r'^{0}'.format(re.escape("Bearer ")), '', header)
