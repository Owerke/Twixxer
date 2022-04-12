"""Main app file, this is where the whole application runs"""
from datetime import datetime
import uuid
from bottle import default_app, delete, get, post, request, response, run, static_file, view
import common
# All these imported modules are coded in this project
import api.api_admin
import api.api_users
import api.api_login
import api.api_logout
import common
import models.user as User
import db.db_users as Db_users

##############################
@get("/")
@view("login")
def _():
    return #dict(tabs=common.tabs, tweets=common.tweets, trends=common.trends, items=common.items)
##############################

# #these stuff for the voices main
# @get("/app.css")
# def _():
#     return static_file("app.css", root=".")

# ##############################
# @get("script/app.js")
# def _():
#     return static_file("app.js", root=".")

# ##############################
# @get("script/validator.js")
# def _():
#     return static_file("validator.js", root=".")

# ##############################
# @get("/images/<image_name>")
# def _(image_name):
#     return static_file(image_name, root="./images")
# ##############################


# TODO: Might be nice to move it somewhere else.
def create_dummy_data():
    """Create some dummy data for easier testing. If the data is already there, don't create it"""

    # FIXME: there is some bug with it, and it creates it anyway. Also use the API, not the DB.
    if not Db_users.get_user_by_username("elonmusk"):
        user1: User = {
            "username": "elonmusk",
            "id" : str(uuid.uuid1()),
            "firstname": "Elon",
            "lastname": "Must",
            "email": "elon@tesla.com",
            "password": "teslaisawesome",
            "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }
        Db_users.create_user(user1)
    else:
        print("Elon is already in the database")


    if not Db_users.get_user_by_username("daddybezos"):
        user2: User = {
                "username": "daddybezos",
                "id" : str(uuid.uuid1()),
                "firstname": "Jeff",
                "lastname": "Bezos",
                "email": "bezos@amazon.com",
                "password": "iaminspace",
                "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")

        }
        Db_users.create_user(user2)
    else:
        print("Bezos is already in the database")


def initialize_database():
    """
    Set up the database for usage. Create tables, and if necessary, even populate them.

    This could be done in a separate SQL file too, but if we do it here, then we don't need to manually do anything.
    """

    db = common._db_connect(common.DB_NAME)
    cur = db.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id text, username text, firstname text, lastname text, email text,  "password" text, created text)''')
    # Save (commit) the changes
    db.commit()

    db.close()

# Initialize and populate the database
initialize_database()
create_dummy_data()

# Run the Bottle application
run(host='127.0.0.1', port=6969, debug=True, reloader=True)
