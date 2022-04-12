from bottle import get,post, redirect, response, request, view
import jwt
import common
import uuid


@get("/login")
@view("login")
def _():
    ''' encoded_jwt = request.get_cookie("jwt")
    # Checking if there is an exsisting cookie containing a user
    if encoded_jwt:
        decoded_jwt = jwt.decode(encoded_jwt, common.JWT_SECRET, algorithms=["HS256"])
        user_session_id = decoded_jwt["user_session_id"]

        # If user exists in the sessions list redirect to the feed view
        if user_session_id in common.sessions:
            return redirect("/voices_index")'''
    return

@post("/login") #this is where to login take place
def _():
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    for user in common.users123: #made a new one in common.py
        if user_email == user["email"] and user_password == user["password"]:
            user_session_id = str(uuid.uuid4()) #generating the uuid4 for the user
            common.sessions[user_session_id] = user #creating the key userid session id, this key will point to the user object. it will be the user itself
            print(common.sessions)
            response.set_cookie("user_session_id", user_session_id) #this user id session will be passed to the cookie
            return redirect ("/admin")
    return redirect ("/login")

'''@get("/logout")
@view("logout")
def _():
    user_session_id = request.get_cookie("user_session_id") #extract the user session id from cookie
    common.sessions.pop(user_session_id) #removing it from the session dictionary
    return redirect("/login")'''
