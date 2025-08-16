Param(
  [int]$TenantPort   = $(if ($env:PORT_TENANT) { [int]$env:PORT_TENANT } else { 8000 }),
  [int]$OperatorPort = $(if ($env:PORT_OPERATOR) { [int]$env:PORT_OPERATOR } else { 8010 })
)
$ErrorActionPreference = "Stop"
$PSScriptRootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $PSScriptRootPath "..")

function Stop-ByPidFile([string]$Name, [string]$PidFile) {
  if (-not (Test-Path $PidFile)) { Write-Host "[$Name] no PID file ($PidFile)"; return }
  $procId = Get-Content $PidFile -ErrorAction SilentlyContinue
  if (-not $procId) { Write-Host "[$Name] empty PID file; removing"; Remove-Item -Force $PidFile; return }
  $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
  if ($null -ne $proc) {
    Write-Host "[$Name] Stopping PID $procId ..."
    try {
      Stop-Process -Id $procId -ErrorAction SilentlyContinue
      Start-Sleep -Seconds 2
      if (Get-Process -Id $procId -ErrorAction SilentlyContinue) {
        Write-Host "[$Name] Force stopping..."
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
      }
    } catch { }
    if (-not (Get-Process -Id $procId -ErrorAction SilentlyContinue)) {
      Write-Host "[$Name] Stopped."
      Remove-Item -Force $PidFile
    } else {
      Write-Host "[$Name] Unable to stop PID $procId; check manually."
    }
  } else {
    Write-Host "[$Name] Not running (stale PID); removing"
    Remove-Item -Force $PidFile
  }
}

function Stop-ByPort([string]$Name, [int]$Port) {
  try {
    $procIds = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
               Select-Object -ExpandProperty OwningProcess -Unique
    if ($procIds) {
      foreach ($procId in $procIds) {
        Write-Host "[$Name] Stopping PID $procId (port $Port) ..."
        Stop-Process -Id $procId -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
      }
    } else {
      Write-Host "[$Name] No process bound to port $Port"
    }
  } catch {
    Write-Host "[$Name] Could not query port $($Port): $($_.Exception.Message)"
  }
}

Write-Host "[stop-all] stopping operator workers..."
powershell -ExecutionPolicy Bypass -File "scripts\stop_operator_workers.ps1" | Out-Null

Write-Host "[stop-all] stopping operator web..."
Stop-ByPidFile "operator_web" ".pid_operator_web"
Stop-ByPort    "operator_web" $OperatorPort

Write-Host "[stop-all] stopping tenant web..."
Stop-ByPidFile "tenant_web" ".pid_tenant_web"
Stop-ByPort    "tenant_web" $TenantPort

Write-Host "[stop-all] done."
