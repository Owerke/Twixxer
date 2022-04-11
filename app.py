from datetime import datetime
import uuid
from bottle import get, view, run
import api.api_users
import common
import models.user as User
import db.db_users as Db_users

@get("/")
@view("index")
def _():
    return "Hello World"


def create_dummy_data():
    if not Db_users.get_user_by_username("ElonMusk123"):
        user1: User = {
            "username": "ElonMusk123",
            "id" : str(uuid.uuid1()),
            "firstname": "Elon",
            "lastname": "Must",
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
                "password": "iaminspace",
                "created": datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        }
        Db_users.create_user(user2)
    else:
        print("bezos is already in the database")


def initialize_database():
    db = common._db_connect(common.DB_NAME)
    cur = db.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id text, username text, firstname text, lastname text, "password" text, created text)''')
    # Save (commit) the changes
    db.commit()

    db.close()


initialize_database()
create_dummy_data()

run(host='localhost', port=6969)
