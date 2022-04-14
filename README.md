# Twixxer

Final exam project for web development. This is where you can find installation guides, and basic information about the project.

## Running the program

Requirements:
- Python 3+ (with pip)
- Node.js 16+ (with npm)

### Run the Python Bottle application

Running the program (from PowerShell on Windows):

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

### Install and run TailwindCSS

**Installation:** Open up a terminal and enter the following commands:  
*Note: requires NodeJS and npm to be installed*

```
cd tailwindcss
npm install -d tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init
```

**Run as development:** To develop tailwind, use the following command:

```
npx tailwindcss -i tailwindcss.css -o ../app.css --watch
```

**Run as final version:** To ship a final version of the tailwind CSS (minified) for your website, use the following command:

```
npx tailwindcss -i tailwindcss.css -o ../final.css --minify
```

## Project structure

For easier code overview and structing, we separated the code into different files and folders.

### Project folders

- `/routes/`
  - The `routes` folder contains Bottle routes that are displaying server-side rendered HTML pages, and does the main backend programming logic. This is where the majority of the application (backend) is running.
- `/api/`
  - The `api` folder contains all API related code. Each file (eg. `api_users.py`) contains API routes and functions for a specific area of the application. For example all user interaction related routes (query users, create users, modify user data, etc.) is stored in the `api_users.py` file. Only the frontend javascript should interact with this. It was needed to separate javascript HTTP queries from the Bottle routes.
- `/models/`
  - The `models` folder contains typed dictionaries (`TypedDict`) to help in the creation of consistent data structures (dictionaries). Everything here is a template for some object, like a user (which has properties like username, ID, password, etc.)
- `/db/`
  - The `db` folder contains functions that are used to interact with the database. If any code needs to query something from the database, instead of directly accessing the DB, it calls functions from this folder instead. This way if there is any change in how we interact with the database, only code in this folder will be affected, everything else is the same.
- `/js/`
  - The `js` folder contains all javascript code for the application.
- `/views/`
  - The `views` folder contains the HTML codes and templates that will make this app work in a browser :)

### Notable files

- `/app.py`
  - Main application, this is where the web server is being run from. It only contains minimal code that imports and runs the app
- `/common.py`
  - A global variables files that can be used in any module. It stores things like database name, JWT secret, some and some common functions.
- `/database.sqlite`
  - This is the database. Only the methods in the `/db/` folder are using this file, but it is essential for the entire application.
