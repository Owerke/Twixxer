"""Follow model. It's used to follow other users."""
# TypedDict is a pre-made dictionary that follows the same structure everywhere
from typing import TypedDict

class Follow(TypedDict):
    """This is a follow object. Every follow will have this structure"""
    id: str
    follower_id: str
    followed_id: str
