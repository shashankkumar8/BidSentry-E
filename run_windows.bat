@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Creating Python virtual environment...
  py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
if not exist .env (
  echo Could not create .env. Please copy .env.example to .env manually.
  pause
  exit /b 1
)
echo.
echo IMPORTANT: Edit .env and add your TinyFish API key for live mode.
echo The sample mode works without a key and is clearly labeled synthetic.
echo.
start "BidSentry" http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
