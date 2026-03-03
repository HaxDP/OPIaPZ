$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$spec = Join-Path $root "TaskBoard.spec"
$dist = Join-Path $root "dist"
$saveFile = Join-Path $dist "tasks.json"

if (-not (Test-Path $python)) {
    throw "Python executable not found: $python"
}

Write-Output "Stopping running TaskBoard/Flet processes (if any)..."
Get-Process TaskBoard, flet -ErrorAction SilentlyContinue | Stop-Process -Force

try {
    & $python -m PyInstaller --noconfirm $spec
}
catch {
    $message = $_.Exception.Message
    if ($message -match "Access is denied" -or $message -match "WinError 5") {
        Write-Output "Build file lock detected. Retrying once in 2 seconds..."
        Start-Sleep -Seconds 2
        Get-Process TaskBoard, flet -ErrorAction SilentlyContinue | Stop-Process -Force
        & $python -m PyInstaller --noconfirm $spec
    }
    else {
        throw
    }
}

if (-not (Test-Path $dist)) {
    New-Item -ItemType Directory -Path $dist | Out-Null
}

if (-not (Test-Path $saveFile)) {
    Set-Content -Path $saveFile -Value "[]" -Encoding utf8
}

Write-Output "Build complete. Output files:"
Get-ChildItem $dist | Select-Object Name, Length | Format-Table -AutoSize
