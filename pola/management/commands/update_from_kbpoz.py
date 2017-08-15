from django.core.management.base import BaseCommand

from pola.logic_workers import update_from_kbpoz


class Command(BaseCommand):
    help = 'Updates products according to KBPOZ database'

    def add_arguments(self, parser):
        parser.add_argument('db_filename')

    def handle(self, *args, **options):
        update_from_kbpoz(options["db_filename"])
