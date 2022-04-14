API_PREFIX = "api"

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"

JWT_SECRET = "9OzAdFhiJ44vUzK5ikTlflOgztgi45yft3C7VTK6ND2mTEhl9a"
JWT_COOKIE = "user_session_jwt"

DB_NAME = "database.sqlite"
