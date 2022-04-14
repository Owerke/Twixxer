"""Tweet model. It's used to help create Tweet objects everywhere else."""
# TypedDict is a pre-made dictionary that follows the same structure everywhere
from typing import TypedDict

class Tweet(TypedDict):
    """This is a tweet object. Every tweet will have this structure"""
    id: str
    username: str
    content: str
    banner_id: str
    created: str
