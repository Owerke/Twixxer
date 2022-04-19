"""
Generic database queries, like initializing the database (create all tables).
"""
from datetime import datetime
import sqlite3
import uuid

# All these imported modules are coded in this project
import db.db_users as Db_users
import db.db_tweets as Db_tweets
import common

def create_json_from_sqlite_result(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def _db_connect(db_name):
    db = sqlite3.connect(db_name)
    db.row_factory = create_json_from_sqlite_result
    return db

def initialize_database():
    """
    Set up the database for usage. Create tables, and if necessary, even populate them.

    This could be done in a separate SQL file too, but if we do it here, then we don't need to manually do anything.
    """

    db = _db_connect(common.DB_NAME)
    cur = db.cursor()

    # Create Users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (
                    "id" TEXT NOT NULL PRIMARY KEY,
                    "username" TEXT NOT NULL UNIQUE,
                    "firstname" TEXT,
                    "lastname" TEXT,
                    "email" TEXT NOT NULL UNIQUE,
                    "password" TEXT,
                    "created" TEXT NOT NULL,
                    "picture_path" TEXT
                );
                ''')
    # Create Tweets table
    cur.execute('''CREATE TABLE IF NOT EXISTS tweets
                (
                    "id" TEXT NOT NULL PRIMARY KEY,
                    "username" TEXT NOT NULL,
                    "content" TEXT,
                    "banner_id" TEXT,
                    "created" TEXT NOT NULL,
                    FOREIGN KEY(username) REFERENCES users(username)
                );
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

    Db_tweets.create_tweet_by_properties(str(uuid.uuid1()), "elonmusk", "We now accept dogecoin at Tesla", "", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    Db_tweets.create_tweet_by_properties(str(uuid.uuid1()), "elonmusk", "We no longer accept dogecoin at Tesla", "", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    Db_tweets.create_tweet_by_properties(str(uuid.uuid1()), "daddybezos", "I am going into space.", "", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    Db_tweets.create_tweet_by_properties(str(uuid.uuid1()), "elonmusk", "And now I am rich.", "", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))
    Db_tweets.create_tweet_by_properties(str(uuid.uuid1()), "daddybezos", "I came back from space.", "", datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"))

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
items = [
    {"img":"/static/images/elonmusk.jpg", "title":"Elon Musk", "user_name":"elonmusk"},
    {"img":"/static/images/daddybezos.jpg", "title":"Daddy Bezos", "user_name":"daddybezos"},
    {"img":"/static/images/pinkbanana.jpg", "title":"Pink BaNaNa", "user_name":"pinkbanana"},
]

trends = [
    {"category": "Music", "title": "We Won", "tweets_counter": "135K"},
    {"category": "Pop", "title": "Blue Ivy", "tweets_counter": "40k"},
    {"category": "Trending in US", "title": "Denim Day", "tweets_counter": "40k"},
    {"category": "Ukraine", "title": "Ukraine", "tweets_counter": "20k"},
    {"category": "Russia", "title": "Russia", "tweets_counter": "10k"},
]
