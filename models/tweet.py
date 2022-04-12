"""Users model. It's used to help create User objects everywhere else."""
# TypedDict is a pre-made dictionary that follows the same structure everywhere
from typing import TypedDict

class User(TypedDict):
    """This is a user object. All users has to have the same structure as this object."""
    id: str
    username: str
    created: str
