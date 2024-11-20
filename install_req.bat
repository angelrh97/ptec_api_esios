python -m pip install --trusted-host pypi.org -U pip
python -m pip install --trusted-host pypi.org -U virtualenv
python -m virtualenv "%~dp0.venv"
call "%~dp0.venv\Scripts\activate.bat"
python -m pip install --trusted-host pypi.org -r requirements.txt
@echo off
echo.
echo.
echo Installation finished
pause