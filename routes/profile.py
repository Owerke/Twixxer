import imghdr
import imp
import os
from typing import List
from unittest.mock import patch
from bottle import get, view, request, redirect, response, post
import common
# import db.db_users as Db_users # SQLite
import db.mysql_users as Db_users # MySQL
# import db.db_tweets as Db_tweets # SQLite
import db.mysql_tweets as Db_tweets # MySQL
# import db.db as db # SQLite
import db.mysql_db as db # MySQL
from models.user import User
from models.tweet import Tweet
from models.jwt import Jwt_data
import authentication

@get("/profile/<username>")
@view("profile")
def get_user_profile(username):
    # Authentication: only logged in users can view
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/login")
    jwt_data = authentication.decode_jwt(jwt)
    user: User = Db_users.get_user_by_username(jwt_data["username"])
    if not user:
        return redirect("/login")
    # ################################

    user: User = Db_users.get_user_by_username(username)
    tweets: List[Tweet] = Db_tweets.get_tweets_for_user_by_username(username)
    # TODO: proper profile pic
    tabs: List[tabs] = db.tabs
    items: List[items]= db.items
    trends: List[trends] = db.trends
    return dict(user=user, tweets=tweets, tabs=tabs, items=items, trends=trends, profile_pic="/static/images/placeholder.png")


@get("/profile/<username>/edit")
@view("edit_profile")
def get_edit_user_profile(username):
    # Authentication: only logged in users can view
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/")
    jwt_data: Jwt_data = authentication.decode_jwt(jwt)
    if username != jwt_data["username"]:
        return redirect("/")
    # Check if the user is in the database too
    user: User = Db_users.get_user_by_username(jwt_data["username"])
    if not user:
        return redirect("/")
    # ################################

    # TODO: dynamic profile pic
    return dict(user=user, profile_pic="/static/images/placeholder.png")


@post("/profile/<username>")
def patch_edit_user_profile(username):
    # Authentication: only logged in users can view
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/")
    jwt_data: Jwt_data = authentication.decode_jwt(jwt)
    if username != jwt_data["username"]:
        return redirect("/")
    # Check if the user is in the database too
    user: User = Db_users.get_user_by_username(jwt_data["username"])
    if not user:
        return redirect("/")
    # ################################

    new_user_email = request.forms.get("user_email")
    new_user_firstname = request.forms.get("user_firstname")
    new_user_lastname = request.forms.get("user_lastname")

    if not common.is_email_valid(new_user_email):
        return redirect("/signup?error=bad email")

    result = Db_users.change_user_details(user["username"], new_user_firstname, new_user_lastname, new_user_email)

    return redirect(f'/profile/{user["username"]}/edit')

@post("/profile/<username>/password")
def post_edit_user_password(username):
    # Authentication: only logged in users can view
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/")
    jwt_data: Jwt_data = authentication.decode_jwt(jwt)
    # the user can only edit its own profile (so it has to own the correct JWT)
    if username != jwt_data["username"]:
        return redirect("/")
    # Check if the user is in the database too
    user: User = Db_users.get_user_by_username(jwt_data["username"])
    if not user:
        return redirect("/")
    # ################################

    if not common.is_password_valid(new_user_password):
        return redirect(f'/profile/{user["username"]}/edit/error=bad password')


    new_user_password = request.forms.get("user_password")
    result = Db_users.change_user_password(user["username"], new_user_password)

    return redirect(f'/profile/{user["username"]}/edit')


@post("/profile/<username>/picture")
def post_edit_user_picture(username):
    # Authentication: only logged in users can view
    response.set_header("Cache-Control", "no-cache, no-store, must-revaildate")
    jwt = request.get_cookie(common.JWT_COOKIE) #from the cookie we extract the user session id
    if not jwt: # if the user session id is not there, we redirect the user to the login
        return redirect("/")
    jwt_data: Jwt_data = authentication.decode_jwt(jwt)
    # the user can only edit its own profile (so it has to own the correct JWT)
    if username != jwt_data["username"]:
        return redirect("/")
    # Check if the user is in the database too
    user: User = Db_users.get_user_by_username(jwt_data["username"])
    if not user:
        return redirect("/")
    # #############################

    # Upload files: https://bottlepy.org/docs/dev/tutorial.html#file-uploads
    save_path = "./static/images/profiles"

    image = request.files.get('upload')
    file_name, file_extension = os.path.splitext(image.filename) # .png .jpeg .jpg

    # overwrite jpg to jpeg so imghdr will pass validation
    if file_extension == ".jpg": file_extension = ".jpeg"
    # Validate extension
    if file_extension not in (".png", ".jpeg", ".jpg"):
        return "image not allowed"

    # Create new image name
    image_name = f"{user['id']}{file_extension}"
    image_full_path = f"{save_path}/{image_name}"

    try:
        os.remove(image_full_path)
    except:
        print("Does not need to remove pic")
    # Save the image
    image.save(image_full_path)

    # Make sure that the image is actually a valid image
    # by reading its mime type
    print("imghdr.what", imghdr.what(image_full_path))   # imghdr.what png
    print("file_extension", file_extension) # file_extension .png

    imghdr_extension = imghdr.what(image_full_path)
    if file_extension != f".{imghdr_extension}":
        print("mmm... suspicious ... it is not really an image")
        # remove the invalid image from the folder
        os.remove(image_full_path)
        return "mmm...got you! It was not an image"

    Db_users.change_user_picture_path(user["username"], image_name)

    return redirect(f'/profile/{user["username"]}/edit')
