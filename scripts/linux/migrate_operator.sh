#!/usr/bin/env bash
set -euo pipefail
export DJANGO_SETTINGS_MODULE=setup.settings_operator

python manage.py makemigrations operator_console core_scheduler || true
python manage.py migrate
# python manage.py bootstrap_operator_admin --email you@domain.com --password 'StrongPass!' --name 'SysAdmin'
