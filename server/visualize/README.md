This folder contains most of the logic behind the server.

The folders **admin,** **user,** **main** and **approver** are blueprints for the url routes. They contain the views that are specified for their class. If the url of the server is http://127.0.0.1:5000/  the routes would be:

**main:** http://127.0.0.1:5000/

**admin:** http://127.0.0.1:5000/admin/

**user:** http://127.0.0.1:5000/user/

**approver:** http://127.0.0.1:5000/approver/

The `__init__.py` file creates the application and loads the specified config files from the server folder.

The `model.py` file contains the strukture of the database as well as the db object connecting to the actuall database.