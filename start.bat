cd frontend
cd app
start cmd /k "npm start"
cd ..
cd ..
cd server
CALL venv\Scripts\activate
set FLASK_ENV=development
python run.py