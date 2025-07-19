# core/social/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from core.handlers.response import error_response

class NoSignupSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adapter Allauth que BLOQUEIA o signup automático via social login.
    Permite login Google apenas para usuários já cadastrados e ativos.
    Retorna resposta de erro 100% padronizada com o restante da API.
    """
    def is_open_for_signup(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        User = get_user_model()
        user_exists = User.objects.filter(email=email, is_active=True).exists()

        if user_exists:
            return True
        
        response = error_response(
            errors={"email": "Usuário não encontrado ou não vinculado a nenhum tenant ativo."},
            message="Email não autorizado ou não cadastrado no sistema.",
            status=403,
            trace_id=getattr(request, "request_id", None)
        )
        raise ImmediateHttpResponse(response)
