@echo off

echo Running on Virtual Environment...
call .venv\Scripts\activate.bat

echo Running Script...
python app.py

pause