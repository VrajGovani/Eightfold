# Start Backend Server
Write-Host "Starting Interview Practice Partner Backend..." -ForegroundColor Green
Set-Location "c:\Users\dell6\OneDrive\Desktop\Eightfold.ai\backend"
$env:PYTHONPATH = "c:\Users\dell6\OneDrive\Desktop\Eightfold.ai\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
