# Visual1ze - A graphical solution to facility access management

Visual1ze is a visual web-interface prototype for facility access-control management. It simplifies the process of viewing, giving and revoking access to rooms. The interface allows users to manage their access directly using a map of the facility.

There are 3 roles in the system listed below in order of ascending possibilities: 
* reader (can only see its own accesses and require new);
* approver (process the incoming requirements);
* admin (can create new users and access groups, etc).


## Content

This system consists of 3 building blocks: 
1. Backend-server constructed with the Python library **Flask**. This lies under the project folder `server`.
2. Frontend-server constructed with the Javascript library **React**. This lies under the project folder `frontend`.
3. Database constructed in **SQLite**. This also lies under the project folder `server`.

## Prerequisites

Visual1ze requires the following software to run. Install them before continuing to Installation.

* [Node.js](https://nodejs.org/en/)
* [Python 3](https://www.python.org/downloads/) or later version

## Installation

Follow these 4 steps to install the system:

#### 1. Clone the repository

Clone the repository into your PC (running Windows 10) with e.g. `git clone https://gitlab.liu.se/tddd96-grupp1/huvudprojekt.git`

#### 2. Install the frontend-server

Navigate to the folder `frontend/app`. Open a command prompt and run: `npm install`. This will install all the needed dependencies. 

#### 3. Install the backend-server

Navigate to `server/`. All the needed Python modules are listed in `server/requirements.txt`. Install all the listed Python modules using pip by running: `pip install -r requirements.txt`.

#### 4. Construct the database

Navigate to `server/script`. Run the script to create a SQLite database by typing in the command prompt: `python3 create_db_data.py`. This database will show upp as a file named `app.db` inside the `server` folder.

## Usage

In order to run the program, both the web-server and the backend-server must be running at the same time. Do the following in two different command prompts:

1. Run: `python3 run.py` inside the folder `server/script`. This starts the backend-server. 
2. Run: `npm start` inside the folder `frontend/app`. This will automatically open the login-page of Visual1ze in your web-browser.

For demonstration purposes there exists three default users with login credentials `a@a.a` (reader), `b@b.b` (approver), and `c@c.c` (admin), each with the password `abcABC123`.

#### Screenshots

Here are screenshots of the system running:

* [Login-page](screenshots/inlogg.PNG), 
* [Reader page](screenshots/reader.PNG), 
* [Approver page](screenshots/approver.PNG), 
* [Admin page](screenshots/admin.PNG), 
* [Create user](screenshots/create-user.PNG), 
* [Request form](screenshots/requestform.PNG), 
* [Creating access groups](screenshots/access_group.PNG).

## Authors

This project was developed by a group of 8 students at Linköping University for a software engineering bachelor project. 

The authors are: Matheus Bernat, Johan Ehinger, Jesper Jensen, Ludvig Joborn, Gustav Malmström, Anders Ryefalk, Mårten Walter and Johannes Wilson.

## License

MIT license. 

## Acknowledgments

Special thanks to Linköping university and to those who bought fika.
