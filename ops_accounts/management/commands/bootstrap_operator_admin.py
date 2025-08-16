from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Create the initial Operator admin user (only one superuser allowed)."

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--name", default="SysAdmin")

    def handle(self, *args, **opts):
        User = get_user_model()
        email, pwd, name = opts["email"].strip().lower(), opts["password"], opts["name"]
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Operator admin already exists: {email}"))
            return
        if User.objects.filter(is_superuser=True).exists():
            raise CommandError("There is already an operator superuser. Only one is allowed.")
        try:
            u = User.objects.create_superuser(email=email, password=pwd, name=name)
        except IntegrityError:
            raise CommandError("DB constraint prevented another superuser.")
        self.stdout.write(self.style.SUCCESS(f"Operator admin created: {u.email}"))
