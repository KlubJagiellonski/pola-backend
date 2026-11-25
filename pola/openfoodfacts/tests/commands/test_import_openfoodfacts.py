import csv
import gzip
import hashlib
import io
import json
from decimal import Decimal
from pathlib import Path
from unittest import mock

from django.core.management import CommandError, call_command
from django.test import TestCase
from django.utils import timezone

from pola.openfoodfacts.loading import CSV_BASENAME, CSV_HEADERS
from pola.openfoodfacts.models import LoadRun, Product, ProductNext

INDEX_TEXT = 'openfoodfacts_products_100_200.json.gz\n' 'openfoodfacts_products_200_300.json.gz\n'


class ImportOpenFoodFactsTests(TestCase):
    def test_full_import_swaps_rows_and_sets_cursor(self):
        with self._full_files(
            [
                self._csv_row(code='5900000000011', product_name='Oat milk', energy='12.5'),
                self._csv_row(code='5900000000028', product_name='Bread "rye"', energy='250'),
            ]
        ) as paths:
            call_command(
                'import_openfoodfacts_full',
                csv=paths['csv'],
                checksum=paths['checksum'],
                index=paths['index'],
            )

        oat = Product.objects.get(code='5900000000011')
        bread = Product.objects.get(code='5900000000028')
        self.assertEqual(oat.product_name, 'Oat milk')
        self.assertEqual(oat.energy_kcal, Decimal('12.5000'))
        self.assertEqual(oat.brands_tags, 'en:oatly')
        self.assertEqual(bread.product_name, 'Bread "rye"')
        self.assertEqual(ProductNext.objects.count(), 0)
        run = LoadRun.objects.get()
        self.assertEqual(run.mode, LoadRun.Mode.FULL)
        self.assertEqual(run.status, LoadRun.Status.SUCCESS)
        self.assertEqual(run.delta_end_unix, 300)
        self.assertEqual(run.row_count, 2)
        self.assertEqual(run.sha256, paths['digest'])

    def test_checksum_mismatch_leaves_the_live_table_untouched(self):
        Product.objects.create(code='keep', product_name='stay')
        with self._full_files([self._csv_row(code='5900000000011', product_name='Replacement')]) as paths:
            paths['checksum'].write_text(f'{"0" * 64}  {CSV_BASENAME}\n', encoding='utf-8')
            with self.assertRaisesRegex(CommandError, 'SHA256 mismatch'):
                call_command(
                    'import_openfoodfacts_full',
                    csv=paths['csv'],
                    checksum=paths['checksum'],
                    index=paths['index'],
                )

        self.assertEqual(Product.objects.get().product_name, 'stay')
        self.assertFalse(LoadRun.objects.filter(status=LoadRun.Status.SUCCESS).exists())

    def test_database_size_guard_refuses_the_swap(self):
        Product.objects.create(code='keep', product_name='stay')
        with self._full_files([self._csv_row(code='5900000000011', product_name='Replacement')]) as paths:
            with self.assertRaisesRegex(CommandError, 'left in place'):
                call_command(
                    'import_openfoodfacts_full',
                    csv=paths['csv'],
                    checksum=paths['checksum'],
                    index=paths['index'],
                    max_database_bytes=1,
                )

        self.assertEqual(Product.objects.get().product_name, 'stay')
        self.assertEqual(ProductNext.objects.count(), 0)
        self.assertFalse(LoadRun.objects.filter(status=LoadRun.Status.SUCCESS).exists())

    def test_delta_files_upsert_in_order(self):
        self._cursor(100)
        Product.objects.create(code='111', product_name='old')
        with self._delta_dir() as directory:
            self._write_delta(
                directory / 'openfoodfacts_products_100_200.json.gz',
                [
                    {'code': '111', 'product_name': 'from-first'},
                    {'code': '222', 'product_name': 'created', 'brands_tags': ['en:a', 'en:b']},
                ],
            )
            self._write_delta(
                directory / 'openfoodfacts_products_200_300.json.gz',
                [
                    {
                        'code': '111',
                        'product_name': 'from-second',
                        'nutriments': {'energy-kcal_100g': 12.5, 'fat_100g': 1},
                        'nova_group': 3,
                        'last_modified_t': 99,
                        'image_front_url': 'https://img.example/a.jpg',
                    }
                ],
                as_array=True,
            )
            call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        updated = Product.objects.get(code='111')
        created = Product.objects.get(code='222')
        self.assertEqual(updated.product_name, 'from-second')
        self.assertEqual(updated.energy_kcal, Decimal('12.5000'))
        self.assertEqual(updated.fat, Decimal('1.0000'))
        self.assertEqual(updated.nova_group, 3)
        self.assertEqual(updated.last_modified_t, 99)
        self.assertEqual(updated.image_url, 'https://img.example/a.jpg')
        self.assertEqual(created.product_name, 'created')
        self.assertEqual(created.brands_tags, 'en:a,en:b')
        self.assertEqual(
            LoadRun.objects.filter(status=LoadRun.Status.SUCCESS).order_by('id').last().delta_end_unix,
            300,
        )

    def test_missing_cursor_fails_without_downloading(self):
        with (
            mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=AssertionError('network used')),
            mock.patch('pola.openfoodfacts.loading.fetch_text', side_effect=AssertionError('network used')),
            mock.patch('pola.openfoodfacts.loading.import_full', side_effect=AssertionError('csv loaded')),
        ):
            with self.assertRaisesRegex(CommandError, 'import_openfoodfacts_full'):
                call_command('import_openfoodfacts_delta')

        self.assertFalse(LoadRun.objects.filter(status=LoadRun.Status.SUCCESS).exists())

    def test_broken_cursor_fails_without_loading_the_csv(self):
        self._cursor(50)
        Product.objects.create(code='keep', product_name='stay')
        with self._delta_dir() as directory:
            self._write_delta(
                directory / 'openfoodfacts_products_100_200.json.gz',
                [{'code': '999', 'product_name': 'should-not-load'}],
            )
            with (
                mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=AssertionError('network used')),
                mock.patch('pola.openfoodfacts.loading.fetch_text', side_effect=AssertionError('network used')),
                mock.patch('pola.openfoodfacts.loading.import_full', side_effect=AssertionError('csv loaded')),
            ):
                with self.assertRaisesRegex(CommandError, '14-day delta chain was missed'):
                    call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        self.assertEqual(Product.objects.get().product_name, 'stay')
        self.assertFalse(Product.objects.filter(code='999').exists())

    def _cursor(self, delta_end_unix: int) -> None:
        now = timezone.now()
        LoadRun.objects.create(
            started_at=now,
            finished_at=now,
            mode=LoadRun.Mode.FULL,
            source_url='test',
            sha256='abc',
            delta_end_unix=delta_end_unix,
            row_count=1,
            status=LoadRun.Status.SUCCESS,
        )

    def _csv_row(self, *, code: str, product_name: str, energy: str = '') -> dict[str, str]:
        row = {header: '' for header in CSV_HEADERS.values()}
        row['code'] = code
        row['product_name'] = product_name
        row['brands_tags'] = 'en:oatly'
        row['energy-kcal_100g'] = energy
        return row

    def _full_files(self, rows: list[dict[str, str]]):
        return _FullFiles(rows)

    def _delta_dir(self):
        return _DeltaDir()

    def _write_delta(self, path: Path, documents: list[dict[str, object]], *, as_array: bool = False) -> None:
        if as_array:
            payload = json.dumps(documents)
        else:
            payload = ''.join(json.dumps(document) + '\n' for document in documents)
        path.write_bytes(gzip.compress(payload.encode()))


class _FullFiles:
    def __init__(self, rows: list[dict[str, str]]) -> None:
        self.rows = rows
        self.directory: Path | None = None

    def __enter__(self) -> dict[str, object]:
        import tempfile

        self._owned = tempfile.TemporaryDirectory()
        self.directory = Path(self._owned.name)
        csv_path = self.directory / 'products.csv.gz'
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=list(dict.fromkeys(CSV_HEADERS.values())),
            delimiter='\t',
            lineterminator='\n',
            extrasaction='ignore',
        )
        writer.writeheader()
        writer.writerows(self.rows)
        csv_path.write_bytes(gzip.compress(buffer.getvalue().encode()))
        digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        checksum_path = self.directory / 'gz-sha256sum'
        checksum_path.write_text(f'{digest}  {CSV_BASENAME}\n', encoding='utf-8')
        index_path = self.directory / 'index.txt'
        index_path.write_text(INDEX_TEXT, encoding='utf-8')
        self.paths = {'csv': csv_path, 'checksum': checksum_path, 'index': index_path, 'digest': digest}
        return self.paths

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._owned.cleanup()


class _DeltaDir:
    def __enter__(self) -> Path:
        import tempfile

        self._owned = tempfile.TemporaryDirectory()
        directory = Path(self._owned.name)
        (directory / 'index.txt').write_text(INDEX_TEXT, encoding='utf-8')
        return directory

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._owned.cleanup()
