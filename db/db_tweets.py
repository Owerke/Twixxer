"""
Database queries that is related to Tweets.
"""

# All these imported modules are coded in this project
from re import T
from models.tweet import Tweet
import common
import db.db as Db

def get_tweets():
    """Get all tweets. Returns a `List[Tweet]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute("SELECT * FROM tweets ORDER BY created DESC;")
        # Fetch all data (from the cursor)
        results = cur.fetchall()

        # If there are no results, we just return an empty List
        if not results:
            print("No results found")
            return []

        # Create an empty list where we store all results
        tweets = []
        # Go through all results, and create a User (from `/models/tweet.py`) object
        for result in results:
            # Creating User object
            tweet: Tweet = {
                'id': result["id"],
                'username': result["username"],
                'banner_id': result["banner_id"],
                'content': result["content"],
                'created': result["created"]
            }
            # Add this user to the List
            tweets.append(tweet)

        # Return the list of users
        return tweets

    # If any error happened, then just return an empty list, and print the error
    except Exception as e:
        print(e)
        return []

def get_tweets_for_user_by_username(username: str):
    """Get all Tweets for a single User. Returns a `List[Tweet]` object."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Create a cursor that will execute a query
        cur = db.cursor()
        # Execute query (using the cursor)
        cur.execute("SELECT * FROM tweets WHERE username=?", (username,))
        # Fetch all data (from the cursor)
        results = cur.fetchall()

        # If there are no results, we just return an empty List
        if not results:
            print("No results found")
            return []

        # Create an empty list where we store all results
        tweets = []
        # Go through all results, and create a User (from `/models/tweet.py`) object
        for result in results:
            # Creating User object
            tweet: Tweet = {
                'id': result["id"],
                'username': result["username"],
                'banner_id': result["banner_id"],
                'content': result["content"],
                'created': result["created"]
            }
            # Add this user to the List
            tweets.append(tweet)

        # Return the list of users
        return tweets

    # If any error happened, print the error and return None.
    except Exception as e:
        print(e)
        return None

def get_tweet_by_id(tweet_id: str):
    """Get a single user by Username. Returns a `User` object."""
    try:
        db = Db._db_connect(common.DB_NAME)
        cur = db.cursor()
        # Run query
        cur.execute("SELECT * FROM tweets WHERE id=?", (tweet_id,))
        # Only fetch one single result, because ids should be unique.
        result = cur.fetchone()

        # If there are no results, we just return None
        if not result:
            print(f"No tweet found for {tweet_id}")
            return None

        # Create a tweet object with all the details
        tweet: Tweet = {
            'id': result["id"],
            'username': result["username"],
            'banner_id': result["banner_id"],
            'content': result["content"],
            'created': result["created"]
        }
        # Return the Tweet object
        return tweet
    # If any error happened, print the error and return None.
    except Exception as e:
        print(e)
        return None

def create_tweet(tweet: Tweet):
    """Create a tweet in the database based on a `Tweet` object. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the User object.
        cur.execute("INSERT INTO tweets VALUES (?, ?, ?, ?, ?)", (tweet["id"], tweet["username"], tweet["content"], tweet["banner_id"], tweet["created"]))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def create_tweet_by_properties(id: str, username: str, content: str, banner_id: str, created: str):
    """Create a user in the database by individual properties. Returns `True` if successful, `False` if it failed."""
    tweet: Tweet = {
        "id": id,
        "username": username,
        "content": content,
        "banner_id": banner_id,
        "created": created
    }
    return create_tweet(tweet)

def change_tweet_content(tweet_id: str, new_content: str):
    """Update the content of a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the user with 'username'.
        cur.execute("""UPDATE tweets
                    SET
                        content = ?
                    WHERE id = ?;
                    """,
                    (new_content, tweet_id))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def change_tweet_banner_id(tweet_id: str, new_banner_id: str):
    """Update the banner_id of a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the user with 'username'.
        cur.execute("""UPDATE tweets
                    SET
                        banner_id = ?,
                    WHERE tweet_id = ?;
                    """,
                    (new_banner_id, tweet_id))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def set_tweet_banner(tweet_id, banner):
    # TODO: do functionality for uploading and saving tweet banner
    return None

def delete_tweet(tweet_id: str):
    """Delete a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the user with 'username'.
        cur.execute("""DELETE FROM tweets
                    WHERE id = ?;
                    """,
                    (tweet_id,)
                    )
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False
