"""
The Users API.

This API handles all interactions with User objects, and exposes them both as a function, and as an HTTP route/endpoint.
"""
from datetime import datetime
import json
from models.jwt import Jwt_data
from typing import List
import uuid
from bottle import get, post, request, HTTPResponse

# All these imported modules are coded in this project
import authentication
from models.user import User
import db.db_users as Db_users

@get(f"/api/users")
def get_users():
    """HTTP GET: Get All Users"""
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")

    # Get all users from the database
    users: List[User] = Db_users.get_users();
    # Convert the users into a JSON string, and return that string
    return json.dumps(users)

@get(f"/api/user/<username>")
def get_user(username):
    """HTTP GET: Get user by username"""
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")

    # Query the database "layer" (which will actually get the data from the database) and get the user
    user: User = Db_users.get_user_by_username(username);
    # If we can't find the user, return a 404 code. Otherwise return the user object
    if not user:
        return HTTPResponse(status=404, body="User not found")

    # Remove password before returning it (so people can't just get it)
    user["password"] = "****"
    return HTTPResponse(status=200, body=user)

# This may not be used at all, but we won't delete it, just in case.
@post(f"/api/user")
def create_user():
    """HTTP POST: Create user using HTTP POST and its JSON body."""

    # Create the user object from the JSON info
    user: User = {
            "username": request.json.get("username"),
            # Generate UUID
            "id" : str(uuid.uuid1()),
            "firstname": request.json.get("firstname"),
            "lastname": request.json.get("lastname"),
            "email": request.json.get("email"),
            "password": request.json.get("password"),
            # Creation time is the always current time (when this function runs)
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }
    # Create the user in the database, using the `db` methods
    result = Db_users.create_user(user)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)

    # Remove password before returning it
    user["password"] = "****"
    return HTTPResponse(status=200, body=user)

# This is basically only for testing authentication
@post(f"/api/auth-test")
def auth_user_test():
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)

    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")

    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    # if the token is valid, then return user details
    user: User = Db_users.get_user_by_username(token["username"])
    user["password"] = "****"
    return HTTPResponse(status=200, body=user)
