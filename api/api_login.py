from bottle import get,post, redirect, response, request, view
import jwt
import common
import uuid
import db.db_users


@get("/login")
@view("login")
def _():
    return

@get("/admin")
@view("admin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    user_session_id = request.get_cookie("user_session_id") #from the cookie we extract the user session id
    if user_session_id not in common.sessions: #if the user session id is not there, we redirect the user to the login
        return redirect("/login")
    user = common.sessions[user_session_id] #extract the user, from the session
    return dict(user=user) #return the user to the view.

@get("/logout")
@view("logout")
def _():
    user_session_id = request.get_cookie("user_session_id") #extract the user session id from cookie
    common.sessions.pop(user_session_id) #removing it from the session dictionary
    return redirect("/login")


@post("/login") #this is where to login take place
def _():
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    for user in common.users123:
        if user_email == user["email"] and user_password == user["password"]:
            user_session_id = str(uuid.uuid4())
            common.sessions[user_session_id] = user
            print(common.sessions)
            response.set_cookie("user_session_id", user_session_id) #this user id session will be passed to the cookie
            return redirect ("/voices_index")
    return redirect ("/login")
