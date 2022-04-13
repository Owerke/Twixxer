# TypedDict is a pre-made dictionary that follows the same structure everywhere
from typing import TypedDict

class Jwt_data(TypedDict):
    """This is a user object. All users has to have the same structure as this object."""
    id: str
    username: str
    email: str
    iat: int
