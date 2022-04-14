"""
Generic database queries, like initializing the database (create all tables).
"""
from datetime import datetime
import uuid

# All these imported modules are coded in this project
import db.db_users as Db_users
import common

def initialize_database():
    """
    Set up the database for usage. Create tables, and if necessary, even populate them.

    This could be done in a separate SQL file too, but if we do it here, then we don't need to manually do anything.
    """

    db = common._db_connect(common.DB_NAME)
    cur = db.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (
                    "id" text,
                    "username" text,
                    "firstname" text,
                    "lastname" text,
                    "email" text,
                    "password" text,
                    "created" text
                )
                ''')
    # Save (commit) the changes
    db.commit()

    db.close()

# Create some test data for development
def create_dummy_data():
    """Create some dummy data for easier testing. If the data is already there, don't create it"""

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
