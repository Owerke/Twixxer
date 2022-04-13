"""Main app file, this is where the whole application runs"""
from datetime import datetime
import uuid
from bottle import default_app, delete, get, post, request, response, run, static_file, view

# All these imported modules are coded in this project
import common
import models.user as User

import routes.root
import routes.admin
import routes.signup
import routes.login
import routes.logout

import api.api_users

import db.db_users as Db_users

##############################


    # return #dict(tabs=common.tabs, tweets=common.tweets, trends=common.trends, items=common.items)
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


# TODO: Might be nice to move it somewhere else.
def create_dummy_data():
    """Create some dummy data for easier testing. If the data is already there, don't create it"""

    # FIXME: there is some bug with it, and it creates it anyway. Also use the API, not the DB.
    if not Db_users.get_user_by_username("elonmusk"):
        Db_users.create_user_by_properties(str(uuid.uuid1()), "elonmusk", "Elon", "Musk", "elon@tesla.com", "teslaisawesome", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    else:
        print("Elon is already in the database")

    if not Db_users.get_user_by_username("daddybezos"):
        Db_users.create_user_by_properties(str(uuid.uuid1()), "daddybezos", "Jeff", "Bezos", "bezos@amazon.com", "iaminspace", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    else:
        print("Bezos is already in the database")

    if not Db_users.get_user_by_username("andor123"):
        Db_users.create_user_by_properties(str(uuid.uuid1()), "andor123", "Andor", "Nagy", "a@a.com", "pass1", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    else:
        print("Andor is already in the database")



# Initialize and populate the database
initialize_database()
create_dummy_data()

# Run the Bottle application
run(host='127.0.0.1', port=6969, debug=True, reloader=True)
