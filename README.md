# Twixxer

Final exam project for web development.

Running the program (from PowerShell):

```
python -m venv .
```

```
./Scripts/Activate.ps1
```

```
pip3 install -r requirements.txt
```

```
./Scripts/python.exe app.py
```

## Project structure

For easier code overview and structing, we separated the code into different files and folders.

### Project folders

- `/api/`
  - The `api` folder contains all API related code. Each file (eg. `api_users.py`) contains API routes and functions for a specific area of the application. For example all user interaction related routes (query users, create users, modify user data, etc.) is stored in the `api_users.py` file.
- `/models/`
  - The `models` folder contains typed dictionaries to help in the creation of consistent data structures (dictionaries). Everything here is a template for some object, like a user (which has properties like username, ID, password, etc.)
- `/db/`
  - The `db` folder contains functions that are used to interact with the database. If any code needs to query something from the database, instead of directly accessing the DB, it calls functions from this folder instead. This way if there is any change in how we interact with the database, only code in this folder will be affected, everything else is the same.

### Notable files

- `/app.py`
  - Main application, this is where the web server is being run from. It only contains minimal code that imports and runs the app
- `/common.py`
  - A global variables files that can be used in any module. It stores things like database name, JWT secret, some and some common functions.
