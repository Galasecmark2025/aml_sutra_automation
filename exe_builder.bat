@echo off

echo Running on Virtual Environment...
call .venv\Scripts\activate.bat

echo Building EXE...
pyinstaller --onefile --windowed --clean --name "AML_Automation" app.py

pause
