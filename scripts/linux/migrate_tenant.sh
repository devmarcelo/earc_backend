#!/usr/bin/env bash
set -euo pipefail
export DJANGO_SETTINGS_MODULE=setup.settings

# Se você adicionou/alterou models em TENANT_APPS, gere migrations
python manage.py makemigrations || true

# Aplica migrations nos schemas de TENANTS (não mexe no public)
python manage.py migrate_schemas --tenant
