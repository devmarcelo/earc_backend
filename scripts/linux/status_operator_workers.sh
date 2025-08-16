#!/usr/bin/env bash
set -Eeuo pipefail
APP_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

status_one() {
  local name="$1" pidfile="$2"
  if [[ -f "$pidfile" ]]; then
    local pid
    pid="$(cat "$pidfile" 2>/dev/null || true)"
    if [[ -n "$pid" && "$(ps -p "$pid" -o pid= 2>/dev/null | xargs)" == "$pid" ]]; then
      local cmd
      cmd="$(ps -p "$pid" -o comm= 2>/dev/null || echo '?')"
      echo "[$name] RUNNING  pid=$pid  cmd=$cmd"
    else
      echo "[$name] NOT RUNNING  (stale PID file: $pidfile)"
    fi
  else
    echo "[$name] NOT RUNNING  (no PID file)"
  fi
}

status_one "scheduler_worker" ".pid_scheduler_worker"
status_one "ai_worker"        ".pid_ai_worker"
