@echo off
echo ========================================
echo   DataOps Inspector - Local Development
echo ========================================
echo.

echo 🚀 Starting local development environment...
echo.

echo 📦 Installing Python dependencies...
pip install flask flask-cors

echo.
echo 🔧 Starting Flask API server on port 8000...
start "DataOps Inspector API" cmd /k "python local-server.py"

echo.
echo ⏳ Waiting for API server to start...
timeout /t 3 /nobreak > nul

echo.
echo 🌐 Starting React development server on port 3000...
start "DataOps Inspector Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ Local development environment started!
echo.
echo 📍 API Server: http://localhost:8000
echo 🌐 Frontend: http://localhost:3000
echo 💚 Health Check: http://localhost:8000/health
echo.
echo Press any key to exit this launcher...
pause > nul 