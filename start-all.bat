@echo off
echo ========================================
echo Starting DataOps Inspector Application
echo ========================================

echo.
echo 1. Starting Proxy Server (Port 3001)...
start "Proxy Server" cmd /k "cd backend && python proxy_server.py"

echo.
echo 2. Starting Frontend Server (Port 3004)...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo 3. Waiting for servers to start...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo Application URLs:
echo ========================================
echo Frontend: http://localhost:3004
echo Proxy API: http://localhost:3001
echo Health Check: http://localhost:3001/health
echo ========================================
echo.
echo Press any key to exit this window...
pause 