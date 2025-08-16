#!/usr/bin/env bash
set -Eeuo pipefail
APP_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

PORT_TENANT="${PORT_TENANT:-8000}"
PORT_OPERATOR="${PORT_OPERATOR:-8010}"

kill_by_pidfile() {
  local name="$1" pidfile="$2" timeout="${3:-10}"
  if [[ ! -f "$pidfile" ]]; then
    echo "[$name] no PID file ($pidfile)"
    return 0
  fi
  local pid; pid="$(cat "$pidfile" 2>/dev/null || true)"
  if [[ -z "$pid" ]]; then
    echo "[$name] empty PID file; removing"
    rm -f "$pidfile"; return 0
  fi
  if ps -p "$pid" >/dev/null 2>&1; then
    echo "[$name] TERM $pid..."
    kill "$pid" 2>/dev/null || true
    for i in $(seq 1 "$timeout"); do
      ps -p "$pid" >/dev/null 2>&1 || { echo "[$name] stopped"; rm -f "$pidfile"; return 0; }
      sleep 1
    done
    echo "[$name] KILL $pid..."
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$pidfile"
  else
    echo "[$name] not running (stale PID); removing"
    rm -f "$pidfile"
  fi
}

kill_by_port() {
  local name="$1" port="$2"
  echo "[$name] trying port kill :$port"
  if command -v lsof >/dev/null 2>&1; then
    local pids; pids="$(lsof -ti :$port || true)"
    for pid in $pids; do
      echo "[$name] TERM pid=$pid (lsof)"
      kill "$pid" 2>/dev/null || true
      sleep 1
      kill -9 "$pid" 2>/dev/null || true
    done
  elif command -v fuser >/dev/null 2>&1; then
    fuser -k "$port"/tcp 2>/dev/null || true
  else
    echo "[$name] neither lsof nor fuser found; skip port kill"
  fi
}

echo "[stop-all] stopping operator workers..."
./scripts/stop_operator_workers.sh 2>/dev/null || true

echo "[stop-all] stopping operator web..."
kill_by_pidfile "operator_web" ".pid_operator_web"
kill_by_port    "operator_web" "$PORT_OPERATOR"

echo "[stop-all] stopping tenant web..."
kill_by_pidfile "tenant_web" ".pid_tenant_web"
kill_by_port    "tenant_web" "$PORT_TENANT"

echo "[stop-all] done."
