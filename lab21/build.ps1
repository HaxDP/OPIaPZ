$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$spec = Join-Path $root "TaskBoard.spec"
$dist = Join-Path $root "dist"
$saveFile = Join-Path $dist "tasks.json"

if (-not (Test-Path $python)) {
    throw "Python executable not found: $python"
}

& $python -m PyInstaller --noconfirm $spec

if (-not (Test-Path $dist)) {
    New-Item -ItemType Directory -Path $dist | Out-Null
}

if (-not (Test-Path $saveFile)) {
    Set-Content -Path $saveFile -Value "[]" -Encoding utf8
}

Write-Output "Build complete. Output files:"
Get-ChildItem $dist | Select-Object Name, Length | Format-Table -AutoSize
