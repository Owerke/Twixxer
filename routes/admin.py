from bottle import get, view, response, request, redirect
import common
import db.db_users as Db_users
from models.user import User

@get("/admin")
@view("admin")
def get_admin():
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: #if the user session id is not there, we redirect the user to the login
        return redirect("/login")
    jwt_data = common.decode_jwt(jwt)
    user: User = Db_users.get_user_by_email(jwt_data["email"])
    if not user:
        return redirect("/login")
    user["password"] = "" # We don't want to send the passowrd to the user, so we just make it empty
    return dict(user=user)


#this must be standalone page, with all the users and tweets on it
