Param(
  [int]$Port = $(if ($env:PORT_OPERATOR) { [int]$env:PORT_OPERATOR } else { 8010 })
)

$ErrorActionPreference = "Stop"
$PSScriptRootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $PSScriptRootPath "..")

if (-not $env:DJANGO_SETTINGS_MODULE) { $env:DJANGO_SETTINGS_MODULE = "setup.settings_operator" }
if (-not $env:DJANGO_ENV) { $env:DJANGO_ENV = "dev" }
if (-not $env:SCHEDULER_ENABLED) { $env:SCHEDULER_ENABLED = "false" }
if (-not $env:AI_WORKER_ENABLED) { $env:AI_WORKER_ENABLED = "false" }

New-Item -ItemType Directory -Force -Path "logs" | Out-Null

Write-Host "[operator] applying public migrations..."
python manage.py makemigrations operator core_scheduler | Out-Null
python manage.py migrate --noinput

# Start workers (background) se habilitados
# scheduler
if ($env:SCHEDULER_ENABLED -eq "true") {
  Write-Host "[operator] starting scheduler_worker (loop)..."
  $p = Start-Process -FilePath "python" -ArgumentList @("manage.py","scheduler_worker","--loop") `
        -PassThru -NoNewWindow -RedirectStandardOutput "logs\scheduler_worker.log" `
        -RedirectStandardError "logs\scheduler_worker.err.log"
  $p.Id | Out-File -FilePath ".pid_scheduler_worker" -Encoding ascii -Force
}

# ai_worker
if ($env:AI_WORKER_ENABLED -eq "true") {
  Write-Host "[operator] starting ai_worker (loop)..."
  $p = Start-Process -FilePath "python" -ArgumentList @("manage.py","ai_worker","--loop") `
        -PassThru -NoNewWindow -RedirectStandardOutput "logs\ai_worker.log" `
        -RedirectStandardError "logs\ai_worker.err.log"
  $p.Id | Out-File -FilePath ".pid_ai_worker" -Encoding ascii -Force
}

if ($env:DJANGO_ENV -eq "dev") {
  Write-Host "[operator] starting Django dev server at 0.0.0.0:$Port"
  python manage.py runserver 0.0.0.0:$Port
} else {
  $waitress = Get-Command "waitress-serve" -ErrorAction SilentlyContinue
  if (-not $waitress) {
    Write-Host "[operator] waitress-serve not found. Install with: pip install waitress" -ForegroundColor Yellow
    exit 1
  }
  Write-Host "[operator] starting waitress at 0.0.0.0:$Port"
  waitress-serve --listen=0.0.0.0:$Port setup.wsgi:application
}
