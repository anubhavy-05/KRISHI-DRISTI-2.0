# PowerShell Script to Start Krishi Drishti System
Write-Host "=========================================="
Write-Host "Starting Krishi Drishti System"
Write-Host "=========================================="
Write-Host ""

# Change to project directory
Set-Location "C:\Users\ay840\Downloads\KRISHI-DRISTI-2.0"

# Kill existing processes
Write-Host "Stopping any existing servers..."
Get-Process | Where-Object {$_.MainWindowTitle -like "*Krishi*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait a bit
Start-Sleep -Seconds 2

# Start Backend
Write-Host "Starting Backend API..."
$backend = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\ay840\Downloads\KRISHI-DRISTI-2.0'; .venv\Scripts\python.exe backend\app.py" -PassThru
Write-Host "Backend started (PID: $($backend.Id))"

# Wait for backend to initialize
Start-Sleep -Seconds 5

# Start Dashboard
Write-Host "Starting Dashboard..."
$dashboard = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\ay840\Downloads\KRISHI-DRISTI-2.0'; .venv\Scripts\python.exe -m streamlit run frontend\dashboard.py --server.headless true" -PassThru
Write-Host "Dashboard started (PID: $($dashboard.Id))"

# Wait a bit
Start-Sleep -Seconds 3

# Open browser
Write-Host ""
Write-Host "Opening browser..."
Start-Process "http://localhost:8501"

Write-Host ""
Write-Host "=========================================="
Write-Host "System Running!"
Write-Host "=========================================="
Write-Host "Backend:   http://localhost:8000/docs"
Write-Host "Dashboard: http://localhost:8501"
Write-Host ""
Write-Host "Keep the PowerShell windows OPEN!"
Write-Host "Press any key to exit this window..."
Write-Host "=========================================="
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
