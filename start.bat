@echo off
echo ========================================
echo Fog Computing Simulator - Startup
echo ========================================
echo.
echo This will start BOTH backend and frontend servers
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.
echo Press any key to start...
pause >nul

echo.
echo Starting Backend Server...
start "Backend API" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Dev Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Close the command windows to stop the servers.
echo.
pause


