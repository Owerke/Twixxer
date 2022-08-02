"""
Database queries that is related to Follows.

This file interacts directly with the database, so if you need to fo any database interaction, you do it here.
"""

# All these imported modules are coded in this project
from models.follow import Follow
from models.user import User
import common
import db.db as Db

def get_followings_for_user(username: str):
    """Get all followed users for a certain user. Returns a `List[str]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute('''
                        SELECT
                            followed_user.id as id,
                            followed_user.username as username,
                            followed_user.firstname as firstname,
                            followed_user.lastname as lastname,
                            followed_user.email as email,
                            followed_user.created as created,
                            followed_user.picture_path as picture_path
                        FROM follows
                            JOIN users AS follower_user ON follows.follower_id = follower_user.id
                            JOIN users AS followed_user ON follows.followed_id = followed_user.id
                        WHERE
                            follower_id=?
                    ''', (username,))
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
                'password': "",
                'created': result["created"],
                'picture_path': result['picture_path']
            }
            # Add this user to the List
            users.append(user)

        # Return the list of users
        return users

    # If any error happened, then just return an empty list, and print the error
    except Exception as e:
        print(e)
        return []

def get_followers_for_user(username: str):
    """Get all users that are following the user. Returns a `List[str]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute('''
                        SELECT
                            follower_user.id as id,
                            follower_user.username as username,
                            follower_user.firstname as firstname,
                            follower_user.lastname as lastname,
                            follower_user.email as email,
                            follower_user.created as created,
                            follower_user.picture_path as picture_path
                        FROM follows
                            JOIN users AS follower_user ON follows.follower_id = follower_user.id
                            JOIN users AS followed_user ON follows.followed_id = followed_user.id
                        WHERE
                            followed_id=?
                    ''', (username,))
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
                'password': "",
                'created': result["created"],
                'picture_path': result['picture_path']
            }
            # Add this user to the List
            users.append(user)

        # Return the list of users
        return users

    # If any error happened, then just return an empty list, and print the error
    except Exception as e:
        print(e)
        return []

def get_if_user_is_followed(follower_id: str, followed_id: str):
    """Get all users that are following the user. Returns a `List[str]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute('''
                        SELECT *
                        FROM follows
                        WHERE
                            follower_id=?
                        AND
                            followed_id=?
                    ''', (follower_id, followed_id))
        # Fetch all data (from the cursor)
        results = cur.fetchall()

        # If there are no results, we return False
        if not results:
            print("No results found")
            return False

        # If we found a match, we return True
        return True

    # If any error happened, then just return False
    except Exception as e:
        print(e)
        return False

def create_following(follow: Follow):
    """Create a follow."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the User object.
        cur.execute("INSERT INTO follows VALUES (NULL, ?, ?)", (follow["follower_id"], follow["followed_id"]))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def create_following_by_properties(follower_id: str, followed_id: str):
    """Create a follow."""
    follow: Follow = {
        "follower_id": follower_id,
        "followed_id": followed_id
    }
    return create_following(follow)

def delete_following(follower_id: str, followed_id: str):
    """Delete a follow. Unfollow someone"""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details.
        cur.execute("""DELETE FROM follows
                    WHERE follower_id = ?
                    AND
                    followed_id = ?
                    ;
                    """,
                    (follower_id, followed_id)
                    )
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False
