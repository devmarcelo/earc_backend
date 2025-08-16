#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-setup.settings_operator}
export DJANGO_ENV=${DJANGO_ENV:-dev}
export PORT_OPERATOR=${PORT_OPERATOR:-8010}
export WEB_WORKERS=${WEB_WORKERS:-2}
export SCHEDULER_ENABLED=${SCHEDULER_ENABLED:-false}
export AI_WORKER_ENABLED=${AI_WORKER_ENABLED:-false}

mkdir -p logs

echo "[operator] applying public migrations..."
python manage.py makemigrations operator core_scheduler || true
python manage.py migrate --noinput

# Start workers (em background) se habilitados
if [[ "${SCHEDULER_ENABLED}" == "true" ]]; then
  echo "[operator] starting scheduler_worker (loop)..."
  (python manage.py scheduler_worker --loop >> logs/scheduler_worker.log 2>&1) & echo $! > .pid_scheduler_worker
fi

if [[ "${AI_WORKER_ENABLED}" == "true" ]]; then
  echo "[operator] starting ai_worker (loop)..."
  (python manage.py ai_worker --loop >> logs/ai_worker.log 2>&1) & echo $! > .pid_ai_worker
fi

if [[ "$DJANGO_ENV" == "dev" ]]; then
  echo "[operator] starting Django dev server at 0.0.0.0:${PORT_OPERATOR}"
  (python manage.py runserver 0.0.0.0:${PORT_OPERATOR} >> logs/operator_web.log 2>&1) & echo $! > .pid_operator_web
  echo "[operator] pid $(cat .pid_operator_web)"
  wait   # remova se não quiser bloquear
else
  if ! command -v gunicorn >/dev/null 2>&1; then
    echo "[operator] gunicorn not found. Install with: pip install gunicorn" >&2
    exit 1
  fi
  echo "[operator] starting gunicorn at 0.0.0.0:${PORT_OPERATOR} (workers=${WEB_WORKERS})"
  exec gunicorn setup.wsgi:application \
       --bind 0.0.0.0:${PORT_OPERATOR} \
       --workers ${WEB_WORKERS} \
       --pid .pid_operator_web \
       --access-logfile logs/operator_access.log \
       --error-logfile logs/operator_error.log
fi
