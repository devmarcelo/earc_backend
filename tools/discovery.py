#!/usr/bin/env python
# tools/discovery.py
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDES = {".git", ".idea", ".vscode", "node_modules", "venv", ".venv", "__pycache__", "migrations", "static", "dist", "build"}

# 1) Padrões de interesse
PATTERNS = {
    "RLS/DB context": r"ROW LEVEL SECURITY|pg_policies|policy|current_setting\(|set_config\(|SET LOCAL|search_path|SET\s+search_path",
    "Tenancy (app)": r"\btenant(_id)?\b|request\.tenant|Tenant(Context|Middleware)|Subdomain|django[-_]?tenants|tenant_schemas",
    "RBAC/Perms": r"\bMembership\b|role(s)?\b|HasPermission|permission_classes|IsAuthenticatedOr|Owner|Admin|Member|Viewer",
    "Auditoria/ReqID": r"Audit(Event)?|X-Request-ID|Request-Id|structlog|Sentry|Breadcrumb|audit",
    "Throttle/Lockout": r"throttle|SimpleRateThrottle|AXES|user_login_failed|lockout|ratelimit|django-ratelimit",
    "DRF/Segurança": r"REST_FRAMEWORK|DEFAULT_AUTHENTICATION_CLASSES|DEFAULT_PERMISSION_CLASSES|CORS|CSRF|TRUSTED_ORIGINS",
    "DB/Pool/Caches": r"DATABASES|DATABASE_ROUTERS|PGBOUNCER|CONN_MAX_AGE|CACHES|Redis|CELERY|BROKER_URL|RESULT_BACKEND",
}

def iter_files():
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        parts = set(p.parts)
        if parts & EXCLUDES: continue
        if p.suffix.lower() not in {".py", ".ini", ".cfg", ".toml", ".env", ".yaml", ".yml"} and p.name != "settings.py":
            continue
        yield p

def scan():
    print(f"# Root: {ROOT}\n")
    for name, pat in PATTERNS.items():
        rx = re.compile(pat, re.I)
        print(f"=== {name} ===")
        hits = 0
        for f in iter_files():
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    snippet = line.strip()
                    print(f"{f.relative_to(ROOT)}:{i}: {snippet}")
                    hits += 1
        if not hits:
            print("(sem ocorrências)")
        print()
    # 2) Extra: extrair seções do settings.py
    sfile = next((p for p in iter_files() if p.name == "settings.py"), None)
    if sfile:
        print("=== SETTINGS SNAPSHOT ===")
        text = sfile.read_text(encoding="utf-8", errors="ignore")
        def grab(title, rx):
            m = re.search(rx, text, re.S|re.I)
            print(f"\n# {title}\n{(m.group(0).strip() if m else '(não encontrado)')}\n")
        grab("DATABASES", r"DATABASES\s*=\s*\{.*?\}\s*")
        grab("DATABASE_ROUTERS", r"DATABASE_ROUTERS\s*=\s*\[.*?\]")
        grab("INSTALLED_APPS", r"INSTALLED_APPS\s*=\s*\[.*?\]")
        grab("MIDDLEWARE", r"MIDDLEWARE\s*=\s*\[.*?\]")
        grab("REST_FRAMEWORK", r"REST_FRAMEWORK\s*=\s*\{.*?\}")
        grab("CACHES", r"CACHES\s*=\s*\{.*?\}")
        grab("AUTH", r"(AUTH_USER_MODEL|AUTHENTICATION_BACKENDS).*(\n.*){0,20}")
    else:
        print("=== SETTINGS SNAPSHOT ===\n(settings.py não encontrado)")
    print("\n# Fim")
if __name__ == "__main__":
    scan()
