from bottle import get, static_file

## This might not be needed at all
# @get("/static/<content>")
# def get_static_content(content):
#   return static_file(content, root="./static")

# Server the app.css file
@get("/static/app.css")
def get_app_css():
  return static_file("app.css", root="./")


# Server the entire js folder
@get("/static/js/<content>")
def get_static_js_content(content):
  return static_file(content, root="./static/js")

# Server the entire images folder
@get("/static/images/<content>")
def get_static_js_content(content):
  return static_file(content, root="./static/images")

# Server the profile pictures
@get("/static/images/profiles/<content>")
def get_static_js_content(content):
  return static_file(content, root="./static/images/profiles")



# Serve fontawesome webfonts
@get("/static/fontawesome/webfonts/<content>")
def get_font_awesome_webfonts(content):
  return static_file(content, root="./static/fontawesome/webfonts")

# Serve fontawesome CSS
@get("/static/fontawesome/css/<content>")
def get_font_awesome_css(content):
  return static_file(content, root="./static/fontawesome/css")
