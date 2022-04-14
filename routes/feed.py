from typing import List
from bottle import get, view, response, request, redirect
import common
import authentication
import db.db_users as Db_users
import db.db_tweets as Db_tweets
from models.user import User
from models.tweet import Tweet

tabs = [
    {"icon": "fas fa-home fa-fw", "title": "Home", "id":"home"},
    {"icon": "fas fa-hashtag fa-fw", "title": "Explore", "id": "explore"},
    {"icon": "far fa-bell fa-fw", "title": "Notifications", "id": "notifications"},
    {"icon": "far fa-envelope fa-fw", "title": "Messages", "id": "messages"},
    {"icon": "far fa-bookmark fa-fw", "title": "Bookmarks", "id": "bookmarks"},
    {"icon": "fas fa-clipboard-list fa-fw", "title": "Lists", "id": "lists"},
    {"icon": "far fa-user fa-fw", "title": "Profile", "id": "profile"},
    {"icon": "fas fa-ellipsis-h fa-fw", "title": "More", "id": "more"}
]

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
    return dict(user=user, tabs=tabs, tweets=tweets)


#this must be standalone page, with all the users and tweets on it
