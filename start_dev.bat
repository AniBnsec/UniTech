@echo off
echo ======================================================================
echo   Launching AegisTrust - AI Threat & Digital Trust Intelligence
echo ======================================================================
echo.

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "AegisTrust Backend (FastAPI)" cmd /k "call venv\Scripts\activate.bat && set PYTHONPATH=backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Vite Frontend on http://localhost:3000 ...
start "AegisTrust Frontend (Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================================
echo   AegisTrust is starting up!
echo   - Backend Swagger Docs: http://127.0.0.1:8000/docs
echo   - Frontend Cyber UI:    http://localhost:3000
echo ======================================================================
pause
