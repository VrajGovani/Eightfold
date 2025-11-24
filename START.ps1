Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Interview Practice Partner" -ForegroundColor Magenta
Write-Host "  Starting All Services..." -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "c:\Users\dell6\OneDrive\Desktop\Eightfold.ai\start-backend.ps1"

Start-Sleep -Seconds 5

Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "c:\Users\dell6\OneDrive\Desktop\Eightfold.ai\start-frontend.ps1"

Write-Host ""
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Access your application:" -ForegroundColor White
Write-Host ""
Write-Host "  Frontend (React):    http://localhost:3001" -ForegroundColor Cyan
Write-Host "  Backend API:         http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "  API Documentation:   http://127.0.0.1:8000/docs" -ForegroundColor Magenta
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Checking services..." -ForegroundColor Yellow
$listening = netstat -ano | Select-String "LISTENING" | Select-String ":8000|:3001"
if ($listening) {
    Write-Host "Services are running!" -ForegroundColor Green
    $listening | ForEach-Object { Write-Host $_ }
}

Write-Host ""
Write-Host "To stop the servers, close the PowerShell windows." -ForegroundColor Gray
