import re

API_PREFIX = "api"

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^.{4,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"

JWT_SECRET = "9OzAdFhiJ44vUzK5ikTlflOgztgi45yft3C7VTK6ND2mTEhl9a"
JWT_COOKIE = "user_session_jwt"

MY_SQL_CONNECTION = "localhost"
MY_SQL_USERNAME = "root"
MY_SQL_PASSWORD = ""
DB_NAME = "twixxer"

SENDGRID_API_KEY="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"

def is_email_valid(email):
    is_valid = re.match(REGEX_EMAIL, email)
    if is_valid:
        return True
    return False

def is_tweet_valid(tweet):
    if len(tweet) <= 100 and len(tweet) > 0:
        return True
    return False

def is_username_valid(username):
    is_valid = re.match(REGEX_USERNAME, username)
    if is_valid:
        return True
    return False

def is_password_valid(password):
    is_valid = re.match(REGEX_PASSWORD, password)
    if is_valid:
        return True
    return False
