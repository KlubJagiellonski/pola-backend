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

from pola.openfoodfacts.loading import (
    CSV_HEADERS,
    CSV_URL,
    INDEX_URL,
    OPTIONAL_CSV_COLUMNS,
)
from pola.openfoodfacts.models import LoadRun, Product, ProductNext

INDEX_TEXT = 'openfoodfacts_products_100_200.json.gz\n' 'openfoodfacts_products_200_300.json.gz\n'


class ImportOpenFoodFactsTests(TestCase):
    def test_full_import_swaps_rows_and_sets_cursor(self):
        with self._full_files(
            [
                self._csv_row(code='5900000000011', product_name='Oat milk', energy='12.5', allergens='milk, gluten'),
                self._csv_row(code='5900000000028', product_name='Bread "rye"', energy='250'),
            ]
        ) as paths:
            call_command(
                'import_openfoodfacts_full',
                csv=paths['csv'],
                index=paths['index'],
            )

        oat = Product.objects.get(code='5900000000011')
        bread = Product.objects.get(code='5900000000028')
        self.assertEqual(oat.product_name, 'Oat milk')
        self.assertEqual(oat.energy_kcal, Decimal('12.5000'))
        self.assertEqual(oat.allergens_tags, 'milk, gluten')
        self.assertIsNone(oat.ecoscore_grade)
        self.assertEqual(oat.brands_tags, 'en:oatly')
        self.assertEqual(bread.product_name, 'Bread "rye"')
        self.assertEqual(ProductNext.objects.count(), 0)
        run = LoadRun.objects.get()
        self.assertEqual(run.mode, LoadRun.Mode.FULL)
        self.assertEqual(run.status, LoadRun.Status.SUCCESS)
        self.assertEqual(run.delta_end_unix, 300)
        self.assertEqual(run.row_count, 2)
        self.assertEqual(run.sha256, paths['digest'])

    def test_downloaded_csv_imports_without_a_checksum_file(self):
        with self._full_files([self._csv_row(code='5900000000011', product_name='Oat milk')]) as paths:

            def fetch(url: str, dest: Path, **_kwargs: object) -> None:
                if url == CSV_URL:
                    dest.write_bytes(Path(paths['csv']).read_bytes())
                    return
                if url == INDEX_URL:
                    dest.write_bytes(Path(paths['index']).read_bytes())
                    return
                raise AssertionError(f'unexpected download: {url}')

            with mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=fetch):
                call_command('import_openfoodfacts_full')

        self.assertEqual(Product.objects.get().product_name, 'Oat milk')
        run = LoadRun.objects.get()
        self.assertEqual(run.status, LoadRun.Status.SUCCESS)
        self.assertEqual(run.sha256, paths['digest'])

    def test_null_bytes_in_csv_text_are_removed(self):
        with self._full_files([self._csv_row(code='5900000000011', product_name='Oat\x00milk')]) as paths:
            call_command('import_openfoodfacts_full', csv=paths['csv'], index=paths['index'])

        self.assertEqual(Product.objects.get().product_name, 'Oatmilk')

    def test_out_of_range_nutrient_is_left_empty(self):
        with self._full_files(
            [self._csv_row(code='5900000000011', product_name='Oat milk', energy='14232696253056200')]
        ) as paths:
            call_command('import_openfoodfacts_full', csv=paths['csv'], index=paths['index'])

        product = Product.objects.get()
        self.assertEqual(product.product_name, 'Oat milk')
        self.assertIsNone(product.energy_kcal)

    def test_duplicate_codes_keep_the_first_row(self):
        with self._full_files(
            [
                self._csv_row(code='30383354190402', product_name='First'),
                self._csv_row(code='30383354190402', product_name='Second'),
            ]
        ) as paths:
            call_command('import_openfoodfacts_full', csv=paths['csv'], index=paths['index'])

        self.assertEqual(Product.objects.get().product_name, 'First')
        self.assertEqual(LoadRun.objects.get().row_count, 1)

    def test_database_size_guard_refuses_the_swap(self):
        Product.objects.create(code='keep', product_name='stay')
        with self._full_files([self._csv_row(code='5900000000011', product_name='Replacement')]) as paths:
            with self.assertRaisesRegex(CommandError, 'left in place'):
                call_command(
                    'import_openfoodfacts_full',
                    csv=paths['csv'],
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
                    {'product_name': 'skip-me'},
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

    def test_full_import_with_no_products_leaves_the_live_table(self):
        Product.objects.create(code='keep', product_name='stay')
        with self._full_files([self._csv_row(code=' ', product_name='Nope')]) as paths:
            with self.assertRaisesRegex(CommandError, 'no products'):
                call_command('import_openfoodfacts_full', csv=paths['csv'], index=paths['index'])

        self.assertEqual(Product.objects.get().product_name, 'stay')
        self.assertFalse(LoadRun.objects.exists())

    def test_csv_and_index_must_be_passed_together(self):
        with self.assertRaisesRegex(CommandError, 'together'):
            call_command('import_openfoodfacts_full', csv='products.csv.gz')
        with self.assertRaisesRegex(CommandError, 'together'):
            call_command('import_openfoodfacts_full', index='index.txt')

    def test_delta_already_applied_records_zero_rows(self):
        self._cursor(300)
        Product.objects.create(code='keep', product_name='stay')
        with self._delta_dir() as directory:
            call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        self.assertEqual(Product.objects.get().product_name, 'stay')
        run = LoadRun.objects.order_by('id').last()
        self.assertEqual(run.row_count, 0)
        self.assertEqual(run.delta_end_unix, 300)
        self.assertEqual(run.status, LoadRun.Status.SUCCESS)

    def test_missing_delta_file_is_recorded(self):
        self._cursor(100)
        with self._delta_dir() as directory:
            with self.assertRaisesRegex(CommandError, 'Missing delta file'):
                call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        run = LoadRun.objects.get(status=LoadRun.Status.FAILED)
        self.assertIn('Missing delta file', run.error)

    def test_empty_delta_file_records_zero_rows(self):
        self._cursor(100)
        with self._delta_dir() as directory:
            empty = gzip.compress(b'\n')
            (directory / 'openfoodfacts_products_100_200.json.gz').write_bytes(empty)
            (directory / 'openfoodfacts_products_200_300.json.gz').write_bytes(empty)
            call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        counts = list(
            LoadRun.objects.filter(mode=LoadRun.Mode.DELTA, status=LoadRun.Status.SUCCESS)
            .order_by('id')
            .values_list('row_count', flat=True)
        )
        self.assertEqual(counts, [0, 0])

    def test_invalid_delta_json_is_recorded(self):
        self._cursor(200)
        with self._delta_dir() as directory:
            (directory / 'openfoodfacts_products_200_300.json.gz').write_bytes(gzip.compress(b'{\n'))
            with self.assertRaisesRegex(CommandError, 'Invalid delta JSON'):
                call_command('import_openfoodfacts_delta', index=directory / 'index.txt', delta_dir=directory)

        self.assertTrue(LoadRun.objects.filter(status=LoadRun.Status.FAILED).exists())

    def test_delta_fetches_the_index_when_it_is_not_local(self):
        self._cursor(300)
        with (
            mock.patch('pola.openfoodfacts.loading.fetch_text', return_value=INDEX_TEXT) as fetch_text,
            mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=AssertionError('csv downloaded')),
        ):
            call_command('import_openfoodfacts_delta')

        fetch_text.assert_called_once_with(INDEX_URL)
        run = LoadRun.objects.order_by('id').last()
        self.assertEqual(run.row_count, 0)
        self.assertEqual(run.status, LoadRun.Status.SUCCESS)

    def test_delta_download_reads_the_official_url(self):
        self._cursor(100)

        def fetch(url: str, dest: Path, **_kwargs: object) -> None:
            if url.endswith('openfoodfacts_products_100_200.json.gz'):
                payload = '{"code": "111", "product_name": "from-url"}\n'
            elif url.endswith('openfoodfacts_products_200_300.json.gz'):
                payload = '{"code": "111", "product_name": "from-second-url"}\n'
            else:
                raise AssertionError(url)
            dest.write_bytes(gzip.compress(payload.encode()))

        with self._delta_dir() as directory:
            with mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=fetch):
                call_command('import_openfoodfacts_delta', index=directory / 'index.txt')

        self.assertEqual(Product.objects.get().product_name, 'from-second-url')

    def test_delta_download_failure_is_recorded(self):
        self._cursor(100)
        with self._delta_dir() as directory:
            with mock.patch('pola.openfoodfacts.loading.fetch_bytes', side_effect=OSError('disk')):
                with self.assertRaises(OSError):
                    call_command('import_openfoodfacts_delta', index=directory / 'index.txt')

        run = LoadRun.objects.get(status=LoadRun.Status.FAILED)
        self.assertIn('disk', run.error)

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

    def _csv_row(self, *, code: str, product_name: str, energy: str = '', allergens: str = '') -> dict[str, str]:
        row = {header: '' for column, header in CSV_HEADERS.items() if column not in OPTIONAL_CSV_COLUMNS}
        row['code'] = code
        row['product_name'] = product_name
        row['brands_tags'] = 'en:oatly'
        row['energy-kcal_100g'] = energy
        row['allergens'] = allergens
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
            fieldnames=[header for column, header in CSV_HEADERS.items() if column not in OPTIONAL_CSV_COLUMNS],
            delimiter='\t',
            lineterminator='\n',
            extrasaction='ignore',
        )
        writer.writeheader()
        writer.writerows(self.rows)
        csv_path.write_bytes(gzip.compress(buffer.getvalue().encode()))
        digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
        index_path = self.directory / 'index.txt'
        index_path.write_text(INDEX_TEXT, encoding='utf-8')
        self.paths = {'csv': csv_path, 'index': index_path, 'digest': digest}
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
