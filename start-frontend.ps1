# Start Frontend Server
Write-Host "Starting Interview Practice Partner Frontend on port 3001..." -ForegroundColor Cyan
Set-Location "c:\Users\dell6\OneDrive\Desktop\Eightfold.ai\frontend"
$env:PORT = "3001"
npm start
