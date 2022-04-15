from bottle import get, static_file

## This might not be needed at all
# @get("/static/<content>")
# def get_static_content(content):
#   return static_file(content, root="./static")

# Server the app.css file
@get("/static/app.css")
def get_app_css():
  return static_file("app.css", root="./")

# Server the entire tweet banners folder
@get("/static/tweet-banners/<content>")
def get_tweet_banners(content):
  return static_file(content, root="./static/tweet-banners")

# Server the entire js folder
@get("/static/js/<content>")
def get_static_js_content(content):
  return static_file(content, root="./static/js")

# Server the entire js folder
@get("/static/images/<content>")
def get_static_js_content(content):
  return static_file(content, root="./static/images")
