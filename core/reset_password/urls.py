from django.urls import path
from .views import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path("reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
