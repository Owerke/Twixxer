import imp
from typing import List
from bottle import get, view, request, redirect, response, post
import common
import db.db_users as Db_users
import db.db_tweets as Db_tweets
from models.user import User
from models.tweet import Tweet

@get("/profile/<username>")
@view("profile")
def get_user_profile(username):
    user: User = Db_users.get_user_by_username(username)
    tweets: List[Tweet] = Db_tweets.get_tweets_for_user_by_username(username)
    # TODO: proper profile pic
    return dict(user=user, tweets=tweets, profile_pic="/static/images/placeholder.png")
