"""
Database queries that is related to Tweets.
"""
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
        # Go through all results, and create a tweet  (from `/models/tweet.py`) object
        for result in results:
            # Creating tweet object
            tweet: Tweet = {
                'id': result["id"],
                'username': result["username"],
                'content': result["content"],
                'created': result["created"],
                'picture_path': result['picture_path']
            }
            # Add this tweet to the List
            tweets.append(tweet)

        # Return the list of tweet
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
        cur.execute("SELECT * FROM tweets WHERE username=? ORDER BY created DESC;", (username,))
        # Fetch all data (from the cursor)
        results = cur.fetchall()

        # If there are no results, we just return an empty List
        if not results:
            print("No results found")
            return []

        # Create an empty list where we store all results
        tweets = []
        # Go through all results, and create a Tweet (from `/models/tweet.py`) object
        for result in results:
            # Creating Tweet object
            tweet: Tweet = {
                'id': result["id"],
                'username': result["username"],
                'content': result["content"],
                'created': result["created"],
                'picture_path': result['picture_path']
            }
            # Add this tweet to the List
            tweets.append(tweet)

        # Return the list of tweet
        return tweets

    # If any error happened, print the error and return None.
    except Exception as e:
        print(e)
        return None

def get_tweet_by_id(tweet_id: str):
    """Get a single tweet by id. Returns a `tweet` object."""
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
            'content': result["content"],
            'created': result["created"],
            'picture_path': result['picture_path']
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
        cur.execute("INSERT INTO tweets VALUES (?, ?, ?, ?, ?)", (tweet["id"], tweet["username"], tweet["content"], tweet["created"], tweet["picture_path"]))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def create_tweet_by_properties(id: str, username: str, content: str, created: str, picture_path: str = ""):
    """Create a tweet in the database by individual properties. Returns `True` if successful, `False` if it failed."""
    tweet: Tweet = {
        "id": id,
        "username": username,
        "content": content,
        "created": created,
        "picture_path": picture_path
    }
    return create_tweet(tweet)

def change_tweet_content(tweet_id: str, new_content: str):
    """Update the content of a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the tweet with the new content.
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

def change_tweet_picture(tweet_id: str, new_picture_path: str):
    """Update the picture (path) of a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We update the tweet with the new content.
        cur.execute("""UPDATE tweets
                    SET
                        picture_path = ?
                    WHERE id = ?;
                    """,
                    (new_picture_path, tweet_id))
        # Save changes (basically actually execute the insert query)
        db.commit()
        # Return True if everything is good. (if not, then it will throw an exception)
        return True
    # In case of error, just return False
    except Exception as e:
        print(e)
        return False

def delete_tweet(tweet_id: str):
    """Delete a tweet. Returns `True` if successful, `False` if it failed."""
    try:
        # Connect to database
        db = Db._db_connect(common.DB_NAME)
        # Get the cursor (that will execute the query)
        cur = db.cursor()
        # Execute query with the values from the details. We delete the tweet.
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

#TODO change tweet image? WHAT IS THE SET CONTENT ?
