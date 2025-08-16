#!/usr/bin/env bash
set -Eeuo pipefail

# Raiz do projeto (pasta acima de scripts/)
APP_DIR="$(cd -- "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-setup.settings}
export DJANGO_ENV=${DJANGO_ENV:-dev}
export PORT_TENANT=${PORT_TENANT:-8000}
export WEB_WORKERS=${WEB_WORKERS:-3}

mkdir -p logs

echo "[tenant] applying tenant migrations..."
python manage.py makemigrations || true
python manage.py migrate_schemas --tenant --noinput

if [[ "$DJANGO_ENV" == "dev" ]]; then
  echo "[tenant] starting Django dev server at 0.0.0.0:${PORT_TENANT}"
  (python manage.py runserver 0.0.0.0:${PORT_TENANT} >> logs/tenant_web.log 2>&1) & echo $! > .pid_tenant_web
  echo "[tenant] pid $(cat .pid_tenant_web)"
  wait   # remove esta linha se não quiser bloquear o terminal
else
  if ! command -v gunicorn >/dev/null 2>&1; then
    echo "[tenant] gunicorn not found. Install with: pip install gunicorn" >&2
    exit 1
  fi
  echo "[tenant] starting gunicorn at 0.0.0.0:${PORT_TENANT} (workers=${WEB_WORKERS})"
  exec gunicorn setup.wsgi:application \
       --bind 0.0.0.0:${PORT_TENANT} \
       --workers ${WEB_WORKERS} \
       --pid .pid_tenant_web \
       --access-logfile logs/tenant_access.log \
       --error-logfile logs/tenant_error.log
fi
