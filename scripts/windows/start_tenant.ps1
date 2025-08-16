Param(
  [int]$Port = $(if ($env:PORT_TENANT) { [int]$env:PORT_TENANT } else { 8000 })
)

$ErrorActionPreference = "Stop"
$PSScriptRootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $PSScriptRootPath "..")

if (-not $env:DJANGO_SETTINGS_MODULE) { $env:DJANGO_SETTINGS_MODULE = "setup.settings" }
if (-not $env:DJANGO_ENV) { $env:DJANGO_ENV = "dev" }

New-Item -ItemType Directory -Force -Path "logs" | Out-Null

Write-Host "[tenant] applying tenant migrations..."
python manage.py makemigrations | Out-Null
python manage.py migrate_schemas --tenant --noinput

if ($env:DJANGO_ENV -eq "dev") {
  Write-Host "[tenant] starting Django dev server at 0.0.0.0:$Port"
  $proc = Start-Process -FilePath "python" -ArgumentList @("manage.py","runserver","0.0.0.0:$Port") `
         -PassThru -NoNewWindow -RedirectStandardOutput "logs\tenant_web.log" `
         -RedirectStandardError "logs\tenant_web.err.log"
  $proc.Id | Out-File -FilePath ".pid_tenant_web" -Encoding ascii -Force
  Wait-Process -Id $proc.Id   # (opcional; remova se quiser voltar ao prompt)
}
else {
  $waitress = Get-Command "waitress-serve" -ErrorAction SilentlyContinue
  if (-not $waitress) {
    Write-Host "[tenant] waitress-serve not found. Install with: pip install waitress" -ForegroundColor Yellow
    exit 1
  }
  Write-Host "[tenant] starting waitress at 0.0.0.0:$Port"
  $proc = Start-Process -FilePath "waitress-serve" -ArgumentList @("--listen=0.0.0.0:$Port","setup.wsgi:application") `
         -PassThru -NoNewWindow -RedirectStandardOutput "logs\operator_web.log" `
         -RedirectStandardError "logs\operator_web.err.log"
  $proc.Id | Out-File -FilePath ".pid_operator_web" -Encoding ascii -Force
}
