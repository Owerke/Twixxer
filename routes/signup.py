from datetime import date, datetime
import uuid
from bottle import get,post, redirect, response, request, view
import common
import db.db_users as Db_users
from models.user import User
from models.jwt import Jwt_data

@get("/signup")
@view("signup")
def get_signup():
    return


@post("/signup")
def post_signup():
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    user_firstname = request.forms.get("user_firstname")
    user_lastname = request.forms.get("user_lastname")
    user_username = request.forms.get("user_username")

    user: User = Db_users.get_user_by_email(user_email)
    if user:
        # User is found in the database, so we redirect them to login
        return redirect ("/login")

    user = {
        "id": str(uuid.uuid1()),
        "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"),
        "email": user_email,
        "firstname": user_firstname,
        "lastname": user_lastname,
        "password": user_password,
        "username": user_username
    }
    # Create user in database
    Db_users.create_user(user)
    # Create a token for it for automatic login
    encoded_jwt = common.create_jwt_for_user(user)
    # Set JWT for auto login
    response.set_cookie(common.JWT_COOKIE, encoded_jwt)
    return redirect ("/login")
