from bottle import get,post, redirect, response, request, view, HTTPResponse
import common
import authentication
# import db.db_users as Db_users # SQLite
import db.mysql_users as Db_users # MySQL
from models.user import User
from models.jwt import Jwt_data
import re

@get("/login")
@view("login")
def get_login():
    # if there is a JWT set, just log them in anyway
    jwt = request.get_cookie(common.JWT_COOKIE) # extract the user session id from cookie
    if jwt:
        jwt_data: Jwt_data = authentication.decode_jwt(jwt)
        if Db_users.get_user_by_email(jwt_data["email"]):
            return redirect("/")



@post("/login") #this is where to login take place
def post_login():
    if not request.forms.get("user_email"):
        return redirect("/login?error=email")

    if not re.match(common.REGEX_EMAIL, request.forms.get("user_email")):
        return redirect("/login?error=email")


    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")

    user: User = Db_users.get_user_by_email(user_email)
    if not user:
        # User is not found in the database
        return redirect ("/login")

    if user_email == user["email"] and user_password == user["password"]:
        encoded_jwt = authentication.create_jwt_for_user(user)
        response.set_cookie(common.JWT_COOKIE, encoded_jwt) #this user id session will be passed to the cookie
        return redirect ("/")

    return redirect("/login")
