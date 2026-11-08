Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Launching AegisTrust - AI Threat & Digital Trust Intelligence" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='backend'; .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Starting React Frontend on http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  AegisTrust is launching in two dedicated terminal sessions!" -ForegroundColor Green
Write-Host "  - Backend Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  - Frontend Cyber UI:    http://localhost:3000" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Green

