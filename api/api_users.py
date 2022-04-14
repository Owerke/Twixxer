"""
The Users API.

This API handles all interactions with User objects, and exposes them both as a function, and as an HTTP route/endpoint.
"""
from datetime import datetime
import json
from typing import List
import uuid
from bottle import get, post, request

# All these imported modules are coded in this project
import common
from models.user import User
import db.db_users

@get(f"/api/users")
def get_users():
    """HTTP GET: Get All Users"""

    # Get all users from the database
    users: List[User] = db.db_users.get_users();
    # Convert the users into a JSON string, and return that string
    return json.dumps(users)

@get(f"/api/user/<username>")
def get_user(username):
    """HTTP GET: Get user by username"""

    # Query the database "layer" (which will actually get the data from the database) and get the user
    user: User = db.db_users.get_user_by_username(username);
    return json.dumps(user)

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
    db.db_users.create_user(user)
    # Remove password before returning it
    user["password"] = "****"
    return user
