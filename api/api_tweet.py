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
from models.jwt import Jwt_data
import authentication
import db.db_tweets as Db_tweets

@get(f"/api/tweets")
def get_tweets():
    """HTTP GET: Get All Tweets"""
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")

    # Get all tweets from the database
    tweets: List[Tweet] = Db_tweets.get_tweets();
    # Convert the users into a JSON string, and return that string
    return HTTPResponse(status=200, body=json.dumps(tweets))

@get(f"/api/tweets/<username>")
def get_tweets_for_user_by_username(username):
    """HTTP GET: Get tweets by username"""
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")

    # Query the database "layer" (which will actually get the data from the database) and get the tweets from the user
    tweets: List[Tweet] = Db_tweets.get_tweets_for_user_by_username(username);
    # If we can't find the user, return a 404 code. Otherwise return the user object
    if not tweets:
        return HTTPResponse(status=404, body="This user does not have tweets")

    return HTTPResponse(status=200, body=json.dumps(tweets))


# This may not be used at all, but we won't delete it, just in case.
@post(f"/api/tweet")
def create_tweet():
    """HTTP POST: Create tweet using HTTP POST and its JSON body."""
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")

    # Create the user object from the JSON info
    tweet: Tweet = {
            # A user can only create tweet in its own name, so we use the JWT to have the user's username
            "username": token["username"],
            # Generate UUID
            "id" : str(uuid.uuid1()),
            "content": request.json.get("content"),
            "banner_id":request.json.get("banner_id"),
            # Creation time is the always current time (when this function runs)
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }
    # Create the user in the database, using the `db` methods
    result = Db_tweets.create_tweet(tweet)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)

    return HTTPResponse(status=200, body=tweet)
