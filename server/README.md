**If you simply want to start the server you do so by first activating your virtual environment (with the commands further down) and then 
starting the server in the command line with:**
`python run.py`

If you dont have a already have a virtual environment you will need to set one up

**Create a virtual environment in the server folder:**

On windows:
`py -3 -m venv venv`

On linux:
`python3 -m venv venv`

**Activate the environment:**

On windows:
`venv\Scripts\activate`

On linux:
`. venv/bin/activate`

**After activating the environment you need to install the needed packages that exist requirements.txt**

`pip install -r requirements.txt`

**If this is the first time running the server on your virtual environment you will need to set the flask application variable.**

On windows the command is: ``set FLASK_APP=visualize`` (There can be no spaces around the '=' sign for any of the set/export commands)

On linux the command is: ``export FLASK_APP=visualize``


**The server can be run in 3  different working environments: testing, development and production depending on what you aim to achieve. You change between the working environments with the following commands:**

On windows the commands are:
`set FLASK_ENV=testing`, `set FLASK_ENV=development` and `set FLASK_ENV=production` respectively

On linux the commands are:
`export FLASK_ENV=testing`, `export FLASK_ENV=development` and `export FLASK_ENV=production` respectively

The development environment gives access to the debugger and is recommended in most cases.

Afterwards you just run the server with `python run.py`. 
If the server is local it will (most likely) be hosted on http://127.0.0.1:5000/ (The adress is also shown in the terminal)

**If you install any new packages with `pip install` during your work you will need to update the requirements.txt file.**

You do this with the command `pip freeze > requirements.txt` in the server folder.

**If you want to test the database in the python terminal there are some commands that will need to be done since the server is
using an application factory.**

`from visualize import create_app`

`app = create_app()`

`app.app_context().push()`

After this you can then import and create the database with:

`from visualize.models import db`

`db.create_all()`

You are thereafter free to import and  start testing with any tables from `visualize.models`.

