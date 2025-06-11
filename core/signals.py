# core/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from django.db import models
from .middleware import get_current_user

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
    Signal para preencher automaticamente os campos de auditoria (created_by e updated_by)
    em todos os modelos que herdam de TenantAwareModel.
    """
    from .models import TenantAwareModel
    
    if not issubclass(sender, TenantAwareModel) or sender is TenantAwareModel:
        return
    
    current_user = get_current_user()
    
    if not current_user:
        return
    
    # Se é uma nova instância (sem ID), preenche created_by
    if not instance.pk and hasattr(instance, 'created_by'):
        instance.created_by = current_user
    
    # Sempre atualiza updated_by em qualquer operação de salvamento
    if hasattr(instance, 'updated_by'):
        instance.updated_by = current_user
