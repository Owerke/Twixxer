from typing import List
from bottle import get, view, response, request, redirect
import common
import authentication
import db.db_users as Db_users
import db.db_tweets as Db_tweets
import db.db as db
from models.user import User
from models.tweet import Tweet


@get("/")
@view("feed")
def get_feed():
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/login")
    jwt_data = authentication.decode_jwt(jwt)

    user: User = Db_users.get_user_by_email(jwt_data["email"])
    if not user:
        return redirect("/login")
    user["password"] = "" # We don't want to send the passowrd to the user, so we just make it empty

    tweets: List[Tweet] = Db_tweets.get_tweets()
    tabs: List[tabs] = db.tabs
    items: List[items]= db.items
    trends: List[trends] = db.trends
    return dict(user=user,tweets=tweets,tabs=tabs, items=items, trends=trends)
