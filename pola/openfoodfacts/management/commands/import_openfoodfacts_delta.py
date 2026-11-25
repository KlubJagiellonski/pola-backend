from pathlib import Path

from django.core.management.base import BaseCommand

from pola.openfoodfacts.loading import import_delta


class Command(BaseCommand):
    help = 'Apply Open Food Facts delta files newer than the stored cursor. Does not download the full CSV.'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--index', type=Path, default=None)
        parser.add_argument('--delta-dir', type=Path, default=None)

    def handle(self, *args, **options) -> None:
        runs = import_delta(index_path=options['index'], delta_dir=options['delta_dir'])
        applied = [run for run in runs if run.row_count]
        self.stdout.write(f'Applied {len(applied)} delta file(s). Cursor is {runs[-1].delta_end_unix}.')
