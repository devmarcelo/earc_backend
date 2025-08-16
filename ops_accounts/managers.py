from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

class OperatorUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.last_login = timezone.now()
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_active", True)
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_active", True)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        if self.model.objects.filter(is_superuser=True).exists():
            raise ValueError("There is already an operator superuser. Only one is allowed.")
        return self._create_user(email, password, **extra)
