$ErrorActionPreference = "Stop"
$PSScriptRootPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $PSScriptRootPath "..")

function Status-One([string]$Name, [string]$PidFile) {
  if (Test-Path $PidFile) {
    $pid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($pid) {
      $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
      if ($null -ne $proc) {
        Write-Host "[$Name] RUNNING  pid=$pid  name=$($proc.ProcessName)"
      } else {
        Write-Host "[$Name] NOT RUNNING  (stale PID file: $PidFile)"
      }
    } else {
      Write-Host "[$Name] NOT RUNNING  (empty PID file)"
    }
  } else {
    Write-Host "[$Name] NOT RUNNING  (no PID file)"
  }
}

Status-One "scheduler_worker" ".pid_scheduler_worker"
Status-One "ai_worker"        ".pid_ai_worker"
