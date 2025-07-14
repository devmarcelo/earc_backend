# core/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from django.db import models
from .middleware import get_current_user, get_current_tenant

def get_all_tenant_aware_models():
    """
    Retorna todos os modelos que herdam de TenantAwareModel.
    """
    from .models import TenantAwareModel
    tenant_aware_models = []
    
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if issubclass(model, TenantAwareModel) and model is not TenantAwareModel:
                tenant_aware_models.append(model)
    
    return tenant_aware_models

@receiver(pre_save)
def set_audit_fields(sender, instance, **kwargs):
    """
    Signal para preencher automaticamente os campos de auditoria (created_by, updated_by e tenant)
    em todos os modelos que herdam de TenantAwareModel.
    """
    from .models import TenantAwareModel
    
    if not issubclass(sender, TenantAwareModel) or sender is TenantAwareModel:
        return
    
    current_user = get_current_user()
    current_tenant = get_current_tenant()

    # Preenche o tenant_id se disponível
    if current_tenant and hasattr(instance, 'tenant') and not instance.tenant_id:
        instance.tenant = current_tenant
    
    if not current_user or getattr(current_user, 'is_anonymous', False):
        return
    
    # Se é uma nova instância (sem ID), preenche created_by
    if not instance.pk and hasattr(instance, 'created_by') and not instance.created_by_id:
        instance.created_by = current_user
    
    # Sempre atualiza updated_by em qualquer operação de salvamento
    if hasattr(instance, 'updated_by') and not instance.updated_by_id:
        instance.updated_by = current_user
