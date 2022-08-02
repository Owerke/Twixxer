# Twixxer

Final exam project for web development. This is where you can find installation guides, and basic information about the project.

## Running the program

Requirements:
- Python 3+ (with pip)
- Node.js 16+ (with npm)

### Run the Python Bottle application

Running the program (from PowerShell on Windows):

Create a new Python VENV:
```
python -m venv .
```

Activate the Python VENV:
```
./Scripts/Activate.ps1
```

Install all Python packages from the requirements.txt file (all python packages you need should be in this file).  
_(Might need to run this twice, Bottle does not want to install sometimes)_
```
pip3 install -r requirements.txt
```

Run the application using the VENV Python app.
```
python app.py
```


### Install and run TailwindCSS

**Installation:** Open up a terminal and enter the following commands (only need to do it once):  
*Note: requires NodeJS and npm to be installed*

```
cd tailwindcss
npm install -d tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init
```

**Run as development:** To develop tailwind, use the following command:

```
cd tailwindcss
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
- `/views/`
  - The `views` folder contains the HTML codes and templates that will make this app work in a browser :)
- `/static/`
  - The `static` folder is used to serve CSS, JS, and other assets to the frontend. The `routes/static.py` bottle route is serving all content from here.
- `/static/js/`
  - The `js` folder contains all javascript code for the application. It has to be served statically, otherwise the frontend can't recognize it.

### Notable files

- `/app.py`
  - Main application, this is where the web server is being run from. It only contains minimal code that imports and runs the app
- `/common.py`
  - A global variables files that can be used in any module. It stores things like database name, JWT secret, some and some common functions.
- `/authentication.py`
  - Contains all authentication related Python code that is used in various places.
- `/database.sqlite`
  - This is the database. Only the methods in the `/db/` folder are using this file, but it is essential for the entire application.

# Project information

## Requirements

### Mandatory

Every part that you should have a SPA can be done as a normal page, this means reloading the UI

**A user must be able to:**

- [x] Sign Up
  - A simple page that redirects somewhere. You can also just make it a SPA if wanted
- [x] Sign In / login
  - A simple page that redirects somewhere. You can also just make it a SPA if wanted
- [x] Logout
  - Simple page or SPA if you want to
- [x] Use a session
  - You can do this in the login
- [x] Use a JWT
  - You can implement this as part of the cookie in the session
- [x] Tweet
  - It is a SPA, the page should not reload
- [x] Delete tweet
  - It is a SPA, the page should not reload
- [x] Update tweet
  - It is a SPA, the page should not reload
- [x] See pages from other users
  - A simple page that doesn't have to be a SPA, but you can if you want to
- [x] Must be able to upload an image somewhere in the system

**System must:**

- [x] Admin panel
  - This is a "stand-alone" feature. This means that it doesn't have to be part of the twitter application, but can be a whole different solution. The administrator can see all tweets and delete them if wanted. It is a SPA, so deleting a tweet doesn't reload the whole page.
- [x] Choose 1 extra functionality that you find challenging/interesting in twitter and implement it (email sending, update profile, using databases)
- [x] look like twitter using any CSS library or plain CSS.
  - We use tailwind, so welcome to do it https://www.youtube.com/watch?v=YTdE7nYMJis&t=1s
- [x] Have back-end validation
- [x] Have front-end validation
  - Use any library you want, or create your own
- [x] Keep the data in lists and/or dictionaries. I suggest you use SQLite
- [ ] Uploaded to PythonAnywhere
  - https://youtu.be/HW8QoyP0pBE?t=30
- [x] Use proper HTTP methods: GET, POST, PUT, DELETE
- [x] Use proper status codes: 20x, 30x, 40x, 50x
- [x] Use try-except
- [x] Use regular expressions when needed

### Optional 

- [x] Optional - Send an email when the user creates an account (Sign up). This feature may or may not work in PythonAnywhere. If it fails on PythonAnywhere, just make sure you can send the email from localhost/127.0.0.1
- [x] Update user profile
- [x] Use a database if you want to, this is optional
- [ ] Follow someone - It is a SPA, the page should not reload
