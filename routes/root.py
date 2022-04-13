from bottle import get,post, redirect, response, request, view
import common
import db.db_users as Db_Users
from models.user import User
from models.jwt import Jwt_data

# @get("/")
# @view("login")
# def get_login():
#     # if there is a JWT set
#     jwt = request.get_cookie(common.JWT_COOKIE) # extract the user session id from cookie
#     if not jwt:
#         return redirect("/login")

#     jwt_data: Jwt_data = common.decode_jwt(jwt)
#     if Db_Users.get_user_by_email(jwt_data["email"]):
#         return redirect("/admin")

#     return redirect("/login")
