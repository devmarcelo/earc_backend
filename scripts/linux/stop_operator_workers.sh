#!/usr/bin/env bash
set -Eeuo pipefail
APP_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

stop_one() {
  local name="$1" pidfile="$2" timeout="${3:-10}"
  if [[ ! -f "$pidfile" ]]; then
    echo "[$name] PID file not found ($pidfile) — nothing to stop."
    return 0
  fi
  local pid
  pid="$(cat "$pidfile" 2>/dev/null || true)"
  if [[ -z "$pid" ]]; then
    echo "[$name] PID file empty — removing."
    rm -f "$pidfile"
    return 0
  fi

  if ps -p "$pid" >/dev/null 2>&1; then
    echo "[$name] Stopping PID $pid (TERM)..."
    kill "$pid" 2>/dev/null || true
    for i in $(seq 1 "$timeout"); do
      if ! ps -p "$pid" >/dev/null 2>&1; then
        echo "[$name] Stopped."
        rm -f "$pidfile"
        return 0
      fi
      sleep 1
    done
    echo "[$name] Still running, sending KILL..."
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$pidfile"
    echo "[$name] Killed."
  else
    echo "[$name] No running process for PID $pid — cleaning up PID file."
    rm -f "$pidfile"
  fi
}

stop_one "scheduler_worker" ".pid_scheduler_worker" 10
stop_one "ai_worker"        ".pid_ai_worker"        10
