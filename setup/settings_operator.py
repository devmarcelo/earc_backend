import os
from pathlib import Path

# NÃO importe o settings base dos tenants para evitar carregar django-tenants sem querer.
# Re-declare o essencial aqui (DB/REST/logging herdados você pode puxar pontualmente depois).

BASE_DIR = Path(__file__).resolve().parents[1]
DEBUG = os.getenv("OP_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("OP_SECRET_KEY", "change-me-operator-secret-key")

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

ALLOWED_HOSTS = os.getenv("OP_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Banco: o MESMO do projeto, mas com search_path fixo "public,ai"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "earc_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {
            "options": "-c search_path=public,ai"
        },
        "CONN_MAX_AGE": 60,
    }
}

INSTALLED_APPS = [
    # Django core
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps do Operator (todos no public/ai)
    "ops_accounts",   # OperatorUser
    "scheduler",      # seu core_scheduler, renomeado aqui para evitar colisão
    "ai",             # schema ai + tables (event, recommendation)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.operator_urls"  # arquivo mínimo de urls, logo abaixo
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [str(BASE_DIR / "operator_templates")],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "setup.wsgi.application"

AUTH_USER_MODEL = "ops_accounts.OperatorUser"

STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("OP_STATIC_ROOT", str(BASE_DIR / "static_operator"))

SESSION_COOKIE_NAME = "op_sessionid"
CSRF_COOKIE_NAME   = "op_csrftoken"

# Logging básico (ajuste se quiser)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
