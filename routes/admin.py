from bottle import get, view, response, request, redirect
import common
import authentication

# import db.db_users as Db_users # SQLite
import db.mysql_users as Db_users # MySQL
from models.user import User

@get("/admin")
@view("admin")
def get_admin():
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: #if the user session id is not there, we redirect the user to the login
        return redirect("/login")
    jwt_data = authentication.decode_jwt(jwt)
    user: User = Db_users.get_user_by_email(jwt_data["email"])
    if not user:
        return redirect("/login")

    # Only the admin can login.
    if user["username"] != "admin":
        return redirect("/login")

    user["password"] = "" # We don't want to send the passowrd to the user, so we just make it empty
    return dict(user=user)


#this must be standalone page, with all the users and tweets on it
