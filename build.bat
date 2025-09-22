@echo off

REM Full-Stack ELD Application Build Script for Windows

echo 🚛 Building ELD Assessment Application...

REM Build React Frontend
echo 📦 Building React Frontend...
cd frontend
call npm install
call npm run build
cd ..

REM Setup Django Backend
echo 🐍 Setting up Django Backend...
cd driver_truck
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

echo ✅ Build complete!
echo.
echo 🚀 To run the application:
echo Backend: cd driver_truck ^&^& python manage.py runserver
echo Frontend: cd frontend ^&^& npm run dev
echo.
echo 🌐 Access:
echo React UI: http://localhost:3000
echo Django API: http://localhost:8000

pause