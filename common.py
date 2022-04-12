import sqlite3

API_PREFIX = "api"

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"

JWT_SECRET = "9OzAdFhiJ44vUzK5ikTlflOgztgi45yft3C7VTK6ND2mTEhl9a"

DB_NAME = "database.sqlite"

def create_json_from_sqlite_result(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def _db_connect(db_name):
    db = sqlite3.connect(db_name)
    db.row_factory = create_json_from_sqlite_result
    return db

sessions = {
    } #creating a key that contains the uuid and it will point to a dictionary where i keep the user data. the session is a dictionary here where we have keys =uuid,  and values = dictionary.

users123 =[
    {
        "id": "1",
        "firstname": "Andor",
        "lastname": "Nagy",
        "email": "a@a.com",
        "password": "pass1"
    }
]
