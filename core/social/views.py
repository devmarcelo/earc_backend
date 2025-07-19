# core/social/views.py

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
