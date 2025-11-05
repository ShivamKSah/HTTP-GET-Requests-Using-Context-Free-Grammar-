@echo off
echo Starting CFG Validator Backend...
cd backend
start "CFG Backend" py app.py
echo Backend started on http://localhost:5000

echo.
echo Starting CFG Validator Frontend...
cd ../frontend
start "CFG Frontend" npm run dev
echo Frontend will start on http://localhost:5173

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to continue...
pause