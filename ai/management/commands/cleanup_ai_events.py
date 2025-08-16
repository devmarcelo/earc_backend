from django.core.management.base import BaseCommand
from ai.jobs import cleanup_events

class Command(BaseCommand):
    help = "Limpa eventos AI: destrava processing e remove errors >24h."

    def add_arguments(self, parser):
        parser.add_argument("--batch", type=int, default=2000)

    def handle(self, *args, **opts):
        n = cleanup_events(batch_size=opts["batch"])
        self.stdout.write(self.style.SUCCESS(f"Eventos removidos/ajustados: {n}"))
