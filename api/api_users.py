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
import common
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
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"),
            "picture_path": ""
        }

    if not common.is_username_valid(user["username"]):
        return HTTPResponse(status=500)
    if not common.is_password_valid(user["password"]):
        return HTTPResponse(status=500)
    if not common.is_email_valid(user["email"]):
        return HTTPResponse(status=500)

    # Create the user in the database, using the `db` methods
    result = Db_users.create_user(user)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)

    # Remove password before returning it
    user["password"] = "****"
    return HTTPResponse(status=200, body=user)

# This is basically only for testing JWT authentication
@post(f"/api/jwt-test")
def jwt_auth_test():
    """Test a JWT, and if it's valid, return the user object it belongs to."""
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
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

@post(f"/api/authenticate")
def basic_authenticate():
    """Use HTTP basic authentication (username:password) to generate a JWT."""
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
    auth_token = request.headers.get('Authorization', None)
    credentials = authentication.parse_basic_auth_header(auth_token)

    # if either the username or the password is empty, then unathorize
    if not credentials["username"] or not credentials["password"]:
        return HTTPResponse(status=401, body="Unathorized")
    # We try to authenticate the user. if it's not successful, then we are unauthorized
    authenticated = authentication.password_authenticate(credentials["username"], credentials["password"])
    if not authenticated:
        return HTTPResponse(status=401, body="Unathorized")

    # Create a JWT for the user
    user = Db_users.get_user_by_username(credentials["username"])
    encoded_jwt = authentication.create_jwt_for_user(user)
    # Return JWT
    return HTTPResponse(status=200, body=encoded_jwt)
