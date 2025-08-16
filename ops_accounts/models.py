import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models import Q, UniqueConstraint
from .managers import OperatorUserManager

class OperatorUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = OperatorUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "operator_user"
        constraints = [
            UniqueConstraint(
                fields=["is_superuser"],
                condition=Q(is_superuser=True),
                name="uq_ops_single_superuser",
            )
        ]
