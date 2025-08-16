$ErrorActionPreference = "Stop"
$PSScriptRootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $PSScriptRootPath "..")

function Stop-One([string]$Name, [string]$PidFile) {
  if (-not (Test-Path $PidFile)) {
    Write-Host "[$Name] PID file not found ($PidFile) — nothing to stop."
    return
  }
  $procId = Get-Content $PidFile -ErrorAction SilentlyContinue
  if (-not $procId) {
    Write-Host "[$Name] PID file empty — removing."
    Remove-Item -Force $PidFile
    return
  }
  $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
  if ($null -ne $proc) {
    Write-Host "[$Name] Stopping PID $procId ..."
    try {
      Stop-Process -Id $procId
      Start-Sleep -Seconds 2
      if (Get-Process -Id $procId -ErrorAction SilentlyContinue) {
        Write-Host "[$Name] Still running, force stopping..."
        Stop-Process -Id $procId -Force
      }
    } catch { }
    if (-not (Get-Process -Id $procId -ErrorAction SilentlyContinue)) {
      Write-Host "[$Name] Stopped."
      Remove-Item -Force $PidFile
    } else {
      Write-Host "[$Name] Unable to stop PID $procId. Check manually."
    }
  } else {
    Write-Host "[$Name] No running process for PID $procId — cleaning up PID file."
    Remove-Item -Force $PidFile
  }
}

Stop-One "scheduler_worker" ".pid_scheduler_worker"
Stop-One "ai_worker"        ".pid_ai_worker"
