"""Main app file, this is where the whole application runs"""
from bottle import default_app, run
# All these imported modules are coded in this project
import db.db as db

import api.api_users
import api.api_tweet
import api.api_email

import routes.static
import routes.feed
import routes.admin
import routes.signup
import routes.login
import routes.logout
import routes.profile


# Initialize and populate the database
db.initialize_database()
db.create_dummy_data()

try:
    # Try to run the Bottle application as production on PythonAnywhere
    import production
    application = default_app()
except Exception as ex:

    # Run the Bottle application as dev
    print("Server running on development")
    run(host="127.0.0.1", port=6969, debug=True, reloader=True, server="paste")
