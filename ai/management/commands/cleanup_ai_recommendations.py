from django.core.management.base import BaseCommand
from ai.jobs import cleanup_recommendations

class Command(BaseCommand):
    help = "Remove recomendações 'new' com mais de 24h."

    def add_arguments(self, parser):
        parser.add_argument("--batch", type=int, default=2000)

    def handle(self, *args, **opts):
        n = cleanup_recommendations(batch_size=opts["batch"])
        self.stdout.write(self.style.SUCCESS(f"Recomendações removidas: {n}"))
