from django.core.management.base import BaseCommand
from ai.jobs import process_ai_events

class Command(BaseCommand):
    help = "Processa eventos AI uma única vez."
    def add_arguments(self, parser):
        parser.add_argument("--batch", type=int, default=50)
    def handle(self, *args, **opts):
        n = process_ai_events(batch_size=opts["batch"])
        self.stdout.write(self.style.SUCCESS(f"Processados: {n}"))
