"""
The Users API.

This API handles all interactions with User objects, and exposes them both as a function, and as an HTTP route/endpoint.
"""
from datetime import datetime
import json
from typing import List
import uuid
from bottle import get, post, request, HTTPResponse, response

# All these imported modules are coded in this project
import common
from models.tweet import Tweet
import db.db_tweets

@get(f"/api/tweets")
def get_tweets():
    """HTTP GET: Get All Tweets"""
    # TODO: you need to login to see tweets

    # Get all tweets from the database
    tweets: List[Tweet] = db.db_tweets.get_tweets();
    # Convert the users into a JSON string, and return that string
    return json.dumps(tweets)

@get(f"/api/tweets/<username>")
def get_tweets_for_user_by_username(username):
    """HTTP GET: Get tweets by username"""
    # Query the database "layer" (which will actually get the data from the database) and get the tweets from the user
    tweets: Tweet = db.db_tweets.get_tweets_for_user_by_username(username); #???????
    # If we can't find the user, return a 404 code. Otherwise return the user object
    if not tweets:
        return HTTPResponse(status=404, body="This user does not have tweets")
    # TODO If there are tweets, return tweets
    return tweets

# This may not be used at all, but we won't delete it, just in case.
@post(f"/api/tweet")
def create_tweet():
    """HTTP POST: Create tweet using HTTP POST and its JSON body."""

    # Create the user object from the JSON info
    tweet: Tweet = {
            "username": request.json.get("username"),
            # Generate UUID
            "id" : str(uuid.uuid1()),
            "content": request.json.get("content"),
            "banner_id":request.json.get("banner_id"),
            # Creation time is the always current time (when this function runs)
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }
    # Create the user in the database, using the `db` methods
    result = db.db_tweets.create_tweet(tweet)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)
    # TODO: If result, then return the tweet
