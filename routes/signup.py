from datetime import date, datetime
import uuid
from bottle import get,post, redirect, response, request, view
import common
import authentication
# import db.db_users as Db_users # SQLite
import db.mysql_users as Db_users # MySQL
from models.user import User
from models.jwt import Jwt_data
import api.api_email

import re

@get("/signup")
@view("signup")
def get_signup():
    # Get error parameters from URL (eg.: http://127.0.0.1:6969/signup?error=username-occupied)
    error = request.params.get('error', "")

    # if we can't get it, that means no error has occured
    if not error:
        return dict(error="")

    # Error message is the one we display to the user
    error_message: str = ""

    # different error scenarios
    if error == "email-occupied":
        error_message = "Email is already occupied"
    elif error == "username-occupied":
        error_message = "Username is already occupied"
    else:
        error_message = "Unknown error occured"

    # display the error message in the HTML
    return dict(error=error_message)


@post("/signup")
def post_signup():
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    user_firstname = request.forms.get("user_firstname")
    user_lastname = request.forms.get("user_lastname")
    user_username = request.forms.get("user_username")

    if not user_firstname or not user_lastname:
        return redirect("/signup?error=missing input")

    if not common.is_email_valid(user_email):
        return redirect("/signup?error=bad email")
    if not common.is_password_valid(user_password):
        return redirect("/signup?error=bad password")
    if not common.is_username_valid(user_username):
        return redirect("/signup?error=bad username")

    # We don't validate first and lastname, so Elon Musk's kid can also register :)

    # Check if email is occupied
    user: User = Db_users.get_user_by_email(user_email)
    if user:
        # User is found in the database, so we redirect them to login
        return redirect("/signup?error=email-occupied")
    # Check if username is occupied
    user: User = Db_users.get_user_by_username(user_username)
    if user:
        # User is found in the database, so we redirect them to login
        return redirect("/signup?error=username-occupied")

    user = {
        "id": str(uuid.uuid1()),
        "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"),
        "email": user_email,
        "firstname": user_firstname,
        "lastname": user_lastname,
        "password": user_password,
        "username": user_username,
        "picture_path": ""
    }
    # Create user in database

    result = Db_users.create_user(user)
    if not result:
        print("Something went wrong")
        return redirect("/signup?error")

    # Create a token for it for automatic login
    encoded_jwt = authentication.create_jwt_for_user(user)
    # Set JWT for auto login
    response.set_cookie(common.JWT_COOKIE, encoded_jwt)
    # Send simple welcome signup email
    api.api_email.send_signup_email()
    return redirect ("/login")
