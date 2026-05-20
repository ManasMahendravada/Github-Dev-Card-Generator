@echo off
echo =============================================
echo    GitHub Dev Card Generator - Startup
echo =============================================
echo.

cd /d "C:\Users\MANAS\Downloads\github-dev-card-generator-v3\github-dev-card-generator\backend"

echo Installing requirements...
python -m pip install fastapi uvicorn httpx python-dotenv aiofiles pydantic --quiet
echo Done.
echo.

echo Server starting at http://127.0.0.1:8080
echo Open frontend\index.html in your browser once you see "Application startup complete"
echo Press CTRL+C to stop the server.
echo.

python -m uvicorn main:app --reload --port 8080
pause