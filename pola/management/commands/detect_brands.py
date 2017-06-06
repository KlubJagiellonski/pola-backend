from django.core.management.base import BaseCommand, CommandError
from pola.logic_brands import detect_brands

class Command(BaseCommand):
    help = 'Detects brands from product names'

    def handle(self, *args, **options):
        detect_brands()
