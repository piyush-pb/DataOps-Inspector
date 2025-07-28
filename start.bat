@echo off
echo Starting DataOps Inspector Platform...
echo.

echo Building and starting services with Docker Compose...
docker-compose up --build -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo.
echo DataOps Inspector is starting up!
echo.
echo Services:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - API Documentation: http://localhost:8000/docs
echo - Database: localhost:5432
echo.
echo Sample data file: sample_data.csv
echo.
echo Press any key to view logs...
pause > nul

docker-compose logs -f 