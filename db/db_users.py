"""
Database queries that is related to Users.

This file interacts directly with the database, so if you need to fo any database interaction, you do it here.
"""

# All these imported modules are coded in this project
from models.user import User
import common
import db.db as Db

def get_users():
    """Get all users. Returns a `List[User]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute("SELECT * FROM users")
        # Fetch all data (from the cursor)
        results = cur.fetchall()

        # If there are no results, we just return an empty List
        if not results:
            print("No results found")
            return []

        # Create an empty list where we store all results
        users = []
        # Go through all results, and create a User (from `/models/user.py`) object
        for result in results:
            # Creating User object
            user: User = {
                'id': result["id"],
                'username': result["username"],
                'firstname': result["firstname"],
                'lastname': result["lastname"],
                'email': result["email"],
                'password': result["password"],
                'created': result["created"]
            }
            # Add this user to the List
            users.append(user)

        # Return the list of users
        return users

    # If any error happened, then just return an empty list, and print the error
    except Exception as e:
        print(e)
        return []

def get_user_by_username(username: str):
    """Get a single user by Username. Returns a `User` object."""
    try:
        db = Db._db_connect(common.DB_NAME)
        cur = db.cursor()
        # Run query
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        # Only fetch one single result, because usernames should be unique.
        result = cur.fetchone()

        # If there are no results, we just return None
        if not result:
            print(f"No results found for user {username}")
            return None

        # Create a user object with all the details
        user: User = {
            'id': result["id"],
            'username': result["username"],
            'firstname': result["firstname"],
            'lastname': result["lastname"],
            'email': result["email"],
            'password': result["password"],
            'created': result["created"]
        }
        # Return the User object
        return user

    # If any error happened, print the error and return None.
    except Exception as e:
        print(e)
        return None

def get_user_by_email(email: str):
    """Get a single user by Email. Returns a `User` object."""
    try:
        db = Db._db_connect(common.DB_NAME)
        cur = db.cursor()
        # Run query
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        # Only fetch one single result, because usernames should be unique.
        result = cur.fetchone()

        # If there are no results, we just return None
        if not result:
            print(f"No results found for user {email}")
            return None

        # Create a user object with all the details
        user: User = {
            'id': result["id"],
            'username': result["username"],
            'firstname': result["firstname"],
            'lastname': result["lastname"],
            'email': result["email"],
            'password': result["password"],
            'created': result["created"]
        }
        # Return the User object
        return user

    # If any error happened, print the error and return None.
    except Exception as e:
        print(e)
        return None


def create_user(user: User):
    """Create a user in the database based on a `User` object. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the User object.
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user["id"], user["username"], user["firstname"], user["lastname"], user["email"], user["password"], user["created"]))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def create_user_by_properties(id: str, username: str, firstname: str, lastname: str, email: str, password: str, created: str):
    """Create a user in the database by individual properties. Returns `True` if successful, `False` if it failed."""
    user: User = {
        "id": id,
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": password,
        "created": created
    }
    return create_user(user)

def change_user_details(username: str, new_firstname: str, new_lastname: str, new_email: str):
    """Update user details. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the user with 'username'.
        cur.execute("""UPDATE users
                    SET
                        firstname = ?,
                        lastname = ?,
                        email = ?
                    WHERE username = ?;
                    """,
                    (new_firstname, new_lastname, new_email, username))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def change_user_password(username: str, new_password: str):
    """Change user password. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the User object.
        cur.execute("""UPDATE users
                    SET password = ?
                    WHERE username = ?;
                    """,
                    (new_password, username))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False
