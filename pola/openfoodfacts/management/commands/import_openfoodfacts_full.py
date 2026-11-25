from pathlib import Path

from django.core.management.base import BaseCommand

from pola.openfoodfacts.loading import MAX_DATABASE_BYTES, import_full


class Command(BaseCommand):
    help = 'Download the Open Food Facts CSV once, load openfoodfacts.product, and set the delta cursor.'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--csv', type=Path, default=None)
        parser.add_argument('--checksum', type=Path, default=None)
        parser.add_argument('--index', type=Path, default=None)
        parser.add_argument('--max-database-bytes', type=int, default=MAX_DATABASE_BYTES)

    def handle(self, *args, **options) -> None:
        run = import_full(
            csv_path=options['csv'],
            checksum_path=options['checksum'],
            index_path=options['index'],
            max_database_bytes=options['max_database_bytes'],
        )
        self.stdout.write(
            f'Loaded {run.row_count} products into openfoodfacts.product. Delta cursor is {run.delta_end_unix}.'
        )
