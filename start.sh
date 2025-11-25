#!/bin/bash

echo "========================================"
echo "Fog Computing Simulator - Startup"
echo "========================================"
echo ""
echo "Starting Backend Server..."
cd backend
python3 app.py &
BACKEND_PID=$!

sleep 3

echo "Starting Frontend Server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Both servers are running!"
echo "========================================"
echo ""
echo "Backend: http://localhost:5000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait


