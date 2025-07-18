# core/utils/security.py

import logging
from django.core.cache import cache

logger = logging.getLogger("core.security")

MAX_REFRESH_ATTEMPTS = 5
BLOCK_TIME_SECONDS = 60 * 10  # 10 minutos

def _make_token_key(token, tenant):
    """
    Gera a chave única de tentativas para um token de refresh por tenant.
    """
    return f"refresh_attempts:{tenant.schema_name if tenant else 'public'}:{token}"

def register_token_attempt(token, tenant, success):
    """
    Incrementa tentativas de uso do refresh token e bloqueia após muitas falhas.
    Limpa as tentativas em caso de sucesso.
    Loga tentativas e bloqueios para auditoria.
    """
    key = _make_token_key(token, tenant)
    if success:
        cache.delete(key)
        logger.info(f"Refresh token liberado após sucesso | Tenant={getattr(tenant, 'schema_name', 'public')} | Token={token}")
    else:
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, BLOCK_TIME_SECONDS)
        logger.warning(f"Tentativa falha de refresh | Tenant={getattr(tenant, 'schema_name', 'public')} | Token={token} | Attempts={attempts}")
        if attempts >= MAX_REFRESH_ATTEMPTS:
            cache.set(f"{key}:blocked", True, BLOCK_TIME_SECONDS)
            logger.error(f"Refresh token BLOQUEADO por brute force | Tenant={getattr(tenant, 'schema_name', 'public')} | Token={token} | Attempts={attempts}")

def is_token_blocked(token, tenant):
    """
    Verifica se o token de refresh está bloqueado por excesso de tentativas.
    """
    key = _make_token_key(token, tenant)
    blocked = cache.get(f"{key}:blocked", False)
    if blocked:
        logger.warning(f"Tentativa de uso de token bloqueado | Tenant={getattr(tenant, 'schema_name', 'public')} | Token={token}")
    return blocked
