from datetime import datetime
from typing import Dict, TypedDict

class User(TypedDict):
    id: str
    username: str
    firstname: str
    lastname: str
    password: str
    created: str
