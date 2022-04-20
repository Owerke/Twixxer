"""
The Users API.

This API handles all interactions with User objects, and exposes them both as a function, and as an HTTP route/endpoint.
"""
from datetime import datetime
import json
from typing import List
import uuid
from bottle import route, get, post, delete, request, HTTPResponse, response

# All these imported modules are coded in this project
import common
from models.tweet import Tweet
from models.jwt import Jwt_data
import authentication
import db.db_tweets as Db_tweets

@get(f"/api/tweets")
def get_tweets():
    """HTTP GET: Get All Tweets"""
    ####### Authentication - only allow this if you have a valid JWT ###########
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    ############################################################################


    # Get all tweets from the database
    tweets: List[Tweet] = Db_tweets.get_tweets();
    # Convert the users into a JSON string, and return that string
    return HTTPResponse(status=200, body=json.dumps(tweets))

@get(f"/api/tweets/<username>")
def get_tweets_for_user_by_username(username):
    """HTTP GET: Get tweets by username"""
    ####### Authentication - only allow this if you have a valid JWT ###########
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    ############################################################################


    # Query the database "layer" (which will actually get the data from the database) and get the tweets from the user
    tweets: List[Tweet] = Db_tweets.get_tweets_for_user_by_username(username);
    # If we can't find the user, return a 404 code. Otherwise return the user object
    if not tweets:
        return HTTPResponse(status=404, body="This user does not have tweets")

    return HTTPResponse(status=200, body=json.dumps(tweets))

@get(f"/api/tweet/<id>")
def get_tweets_by_id(id):
    """HTTP GET: Get tweet by id"""
    ####### Authentication - only allow this if you have a valid JWT ###########
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    ############################################################################


    # Query the database "layer" (which will actually get the data from the database) and get the tweets from the user
    tweets: List[Tweet] = Db_tweets.get_tweet_by_id(id);
    # If we can't find the user, return a 404 code. Otherwise return the user object
    if not tweets:
        return HTTPResponse(status=404, body="This tweet does not exist")

    return HTTPResponse(status=200, body=json.dumps(tweets))



# This may not be used at all, but we won't delete it, just in case.
@post(f"/api/tweet")
def create_tweet():
    ####### Authentication - only allow this if you have a valid JWT ###########
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
    ############################################################################

    # Create the user object from the JSON info
    tweet: Tweet = {
            # A user can only create tweet in its own name, so we use the JWT to have the user's username
            "username": token["username"],
            # Generate UUID
            "id" : str(uuid.uuid1()),
            "content": request.json.get("content"),
            # Creation time is the always current time (when this function runs)
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }

    if not common.is_tweet_valid(tweet["content"]):
        return HTTPResponse(status=500)

    # Create the user in the database, using the `db` methods
    result = Db_tweets.create_tweet(tweet)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)

    return HTTPResponse(status=200, body=tweet)

@delete(f"/api/tweet/<tweet_id>")
def delete_tweet(tweet_id):
    """HTTP POST: Create tweet using HTTP POST and its JSON body."""
    ####### Authentication - only allow this if you have a valid JWT ###########
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    ############################################################################

    tweet: Tweet = Db_tweets.get_tweet_by_id(tweet_id)
    # If we can't find tweet, return 404
    if not tweet:
        return HTTPResponse(status=404, body="Can't find tweet")

    # the tweet's owner can delete the tweet, or the "admin" user
    if tweet["username"] != token["username"] and token["username"] != "admin":
        return HTTPResponse(status=403, body="You don't have permission to delete someone else's tweet")

    # Delete tweet
    result = Db_tweets.delete_tweet(tweet_id)

    # If we can't delete it, return error 500
    if not result:
        return HTTPResponse(status=500)

    return HTTPResponse(status=200, body="Tweet deleted")

@route(f"/api/tweet", method='PATCH')
def edit_tweet():
    """HTTP POST: Create tweet using HTTP POST and its JSON body."""
    ####### Authentication - only allow this if you have a valid JWT ###########
    auth_token = request.headers.get('Authorization', None)
    auth_token = authentication.parse_jwt_header(auth_token)
    # if the token is empty, then reject.
    if not auth_token:
        return HTTPResponse(status=401, body="Unathorized")
    token: Jwt_data = authentication.decode_jwt(auth_token)
    # if the token is not valid, then reject
    if not token:
        return HTTPResponse(status=401, body="Unathorized")
    ############################################################################

    # We expect something like this to recieve in the json from javascript:
    # {
    #     "id": "xxxxxxx-xxxxxxxx-xxxxxxx"
    #     "content": "xxxxxxxx"
    # }

    # Read tweet id and content from HTTP Body
    tweet_id = request.json.get("id")
    tweet_content = request.json.get("content")

    # Validate tweet (between 1 and 100 characters)
    if not common.is_tweet_valid(tweet_content):
        return HTTPResponse(status=500)

    # If the user tries to edit another user's tweet, we reject it.
    tweet: Tweet = Db_tweets.get_tweet_by_id(request.json.get("id"))
    if tweet["username"] != token["username"]:
        return HTTPResponse(status=403, body="Forbidden")

    result = False

    # We only edit content if we get a new content
    if tweet_content:
        result = Db_tweets.change_tweet_content(tweet_id, tweet_content)

    # Get the updated tweet by ID
    tweet: Tweet = Db_tweets.get_tweet_by_id(tweet_id)

    # If we can't create it, return error 500
    if not result:
        return HTTPResponse(status=500)

    return HTTPResponse(status=200, body=tweet)
