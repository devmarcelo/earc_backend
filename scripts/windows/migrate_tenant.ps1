$env:DJANGO_SETTINGS_MODULE = "setup.settings"
python manage.py makemigrations
python manage.py migrate_schemas --tenant
