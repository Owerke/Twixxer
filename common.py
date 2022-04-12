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

'''this stuff for the voices feed look

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

people = [
  {"src": "stephie.png", "name": "Stephie Jensen", "handle": "@sjensen"},
  {"src": "monk.jpg", "name": "Adrian Monk", "handle": "@detective :)"},
  {"src": "kevin.jpg", "name": "Kevin Hart", "handle": "@miniRock"}
]

trends = [
  {"category": "Music", "title": "We Won", "tweets_counter": "135K"},
  {"category": "Pop", "title": "Blue Ivy", "tweets_counter": "40k"},
  {"category": "Trending in US", "title": "Denim Day", "tweets_counter": "40k"},
  {"category": "Ukraine", "title": "Ukraine", "tweets_counter": "20k"},
  {"category": "Russia", "title": "Russia", "tweets_counter": "10k"},
]

tweets = [
  {"id":"1", "src":"6.jpg", "user_first_name":"Barack", "user_last_name":"Obama", "user_name":"barackobama", "date":"Feb 20", "text":"The Ukrainian people need our help. If you’re looking for a way to make a difference, here are some organizations doing important work.", "image":"1.jpg"},
  {"id":"2", "src":"2.jpg", "user_first_name":"Elon", "user_last_name":"Musk", "user_name":"joebiden", "date":"Mar 3", "text":"Richard Hunt is one of the greatest artists Chicago has ever produced, and I couldn’t be prouder that his “Book Bird” sculpture will live outside of the newest @ChiPubLibbranch at the Obama Presidential Center. I hope it inspires visitors for years to come."},
  {"id":"3", "src":"3.jpg", "user_first_name":"Joe Biden", "user_last_name":"Biden", "user_name":"elonmusk", "date":"Mar 7", "text":"Last year has been the best year for manufacturing jobs and trucking jobs since 1994."},
  {"id":"4", "src":"6.jpg", "user_first_name":"Barack", "user_last_name":"Obama", "user_name":"barackobama", "date":"Feb 20", "text":"The Ukrainian people need our help. If you’re looking for a way to make a difference, here are some organizations doing important work.", "image":"1.jpg"},
  {"id":"5", "src":"2.jpg", "user_first_name":"Elon", "user_last_name":"Musk", "user_name":"joebiden", "date":"Mar 3", "text":"Richard Hunt is one of the greatest artists Chicago has ever produced, and I couldn’t be prouder that his “Book Bird” sculpture will live outside of the newest @ChiPubLibbranch at the Obama Presidential Center. I hope it inspires visitors for years to come."},
  {"id":"6", "src":"3.jpg", "user_first_name":"Joe Biden", "user_last_name":"Biden", "user_name":"elonmusk", "date":"Mar 7", "text":"Last year has been the best year for manufacturing jobs and trucking jobs since 1994."},
  {"id":"7", "src":"6.jpg", "user_first_name":"Barack", "user_last_name":"Obama", "user_name":"barackobama", "date":"Feb 20", "text":"The Ukrainian people need our help. If you’re looking for a way to make a difference, here are some organizations doing important work.", "image":"1.jpg"},
  {"id":"8", "src":"2.jpg", "user_first_name":"Elon", "user_last_name":"Musk", "user_name":"joebiden", "date":"Mar 3", "text":"Richard Hunt is one of the greatest artists Chicago has ever produced, and I couldn’t be prouder that his “Book Bird” sculpture will live outside of the newest @ChiPubLibbranch at the Obama Presidential Center. I hope it inspires visitors for years to come."},
  {"id":"9", "src":"3.jpg", "user_first_name":"Joe Biden", "user_last_name":"Biden", "user_name":"elonmusk", "date":"Mar 7", "text":"Last year has been the best year for manufacturing jobs and trucking jobs since 1994."},
  {"id":"10", "src":"6.jpg", "user_first_name":"Barack", "user_last_name":"Obama", "user_name":"barackobama", "date":"Feb 20", "text":"The Ukrainian people need our help. If you’re looking for a way to make a difference, here are some organizations doing important work.", "image":"1.jpg"},
  {"id":"11", "src":"2.jpg", "user_first_name":"Elon", "user_last_name":"Musk", "user_name":"joebiden", "date":"Mar 3", "text":"Richard Hunt is one of the greatest artists Chicago has ever produced, and I couldn’t be prouder that his “Book Bird” sculpture will live outside of the newest @ChiPubLibbranch at the Obama Presidential Center. I hope it inspires visitors for years to come."},
  {"id":"12", "src":"3.jpg", "user_first_name":"Joe Biden", "user_last_name":"Biden", "user_name":"elonmusk", "date":"Mar 7", "text":"Last year has been the best year for manufacturing jobs and trucking jobs since 1994."},
]

items = [
  {"img":"bbc.png", "title":"BBC News", "user_name":"bbcworld"},
  {"img":"biden.jpg", "title":"Joe Biden", "user_name":"joebiden"},
  {"img":"harris.jpg", "title":"Vice President", "user_name":"vp"},
]'''
