import csv
import gzip
import io
import os
import tempfile
from pathlib import Path
from unittest import mock

from django.core.management.base import CommandError
from django.test import SimpleTestCase

from pola.openfoodfacts.loading import (
    CSV_HEADERS,
    OPTIONAL_CSV_COLUMNS,
    PRODUCT_COLUMNS,
    DeltaFile,
    ProjectedCopy,
    column_text,
    decimal_text,
    download_directory,
    encode_copy_field,
    image_from_document,
    int_text,
    iter_documents,
    nutrient_value,
    parse_index,
    primary_key_name,
    row_from_csv,
    row_from_document,
    tags_value,
    text_value,
)


class ParseIndexTests(SimpleTestCase):
    def test_blank_lines_are_skipped_and_files_are_ordered(self):
        files = parse_index('\nopenfoodfacts_products_200_300.json.gz\n \nopenfoodfacts_products_100_200.json.gz\n')
        self.assertEqual([item.start for item in files], [100, 200])
        self.assertEqual(
            files[0].url,
            'https://static.openfoodfacts.org/data/delta/openfoodfacts_products_100_200.json.gz',
        )
        self.assertEqual(files[0], DeltaFile('openfoodfacts_products_100_200.json.gz', 100, 200))

    def test_unexpected_line_is_rejected(self):
        with self.assertRaisesRegex(CommandError, 'Unexpected delta index line'):
            parse_index('nope\n')

    def test_empty_index_is_rejected(self):
        with self.assertRaisesRegex(CommandError, 'Delta index is empty'):
            parse_index('\n \n')


class ValueTests(SimpleTestCase):
    def test_text_and_tags(self):
        self.assertIsNone(text_value(None))
        self.assertIsNone(text_value(['a']))
        self.assertIsNone(text_value({'a': 1}))
        self.assertIsNone(text_value(' \x00 '))
        self.assertEqual(text_value(' a\x00b '), 'ab')
        self.assertIsNone(tags_value([]))
        self.assertIsNone(tags_value(['', ' ']))
        self.assertEqual(tags_value([' en:a ', '', 'en:b']), 'en:a,en:b')
        self.assertEqual(tags_value(' en:a '), 'en:a')

    def test_numbers(self):
        self.assertIsNone(decimal_text(None))
        self.assertIsNone(decimal_text(['1']))
        self.assertIsNone(decimal_text(''))
        self.assertIsNone(decimal_text('nope'))
        self.assertIsNone(decimal_text('Infinity'))
        self.assertIsNone(decimal_text('-10000000000'))
        self.assertEqual(decimal_text(' -1.5 '), '-1.5')
        self.assertIsNone(int_text(None, limit=10))
        self.assertIsNone(int_text(['1'], limit=10))
        self.assertIsNone(int_text(' \x00 ', limit=10))
        self.assertIsNone(int_text('nope', limit=10))
        self.assertIsNone(int_text('NaN', limit=10))
        self.assertIsNone(int_text('11', limit=10))
        self.assertEqual(int_text(' 3.9 ', limit=10), '3')

    def test_nutrients_images_and_columns(self):
        self.assertIsNone(nutrient_value({}, 'fat'))
        self.assertEqual(nutrient_value({'nutriments': {'fat_100g': 1}}, 'fat'), 1)
        self.assertEqual(nutrient_value({'nutriments': 'nope', 'fat_100g': 2}, 'fat'), 2)
        self.assertEqual(nutrient_value({'nutriments': {}, 'fat_100g': 3}, 'fat'), 3)
        self.assertEqual(image_from_document({'image_url': ' https://a ', 'image_front_url': 'https://b'}), 'https://a')
        self.assertEqual(image_from_document({'image_front_url': ' https://b '}), 'https://b')
        self.assertEqual(image_from_document({'image_front_small_url': 'https://c'}), 'https://c')
        self.assertIsNone(image_from_document({}))
        self.assertIsNone(column_text('product_name', {'a': 1}))
        self.assertEqual(column_text('nova_group', '4'), '4')
        self.assertIsNone(column_text('energy_kcal', 'Infinity'))
        self.assertEqual(column_text('brands_tags', ['en:a']), 'en:a')

    def test_rows_and_copy_encoding(self):
        self.assertIsNone(row_from_csv({'code': '  '}))
        self.assertIsNone(row_from_document({'product_name': 'x'}))
        headers = [header for column, header in CSV_HEADERS.items() if column not in OPTIONAL_CSV_COLUMNS]
        csv_row = {header: '' for header in headers}
        csv_row['code'] = '1'
        csv_row['product_name'] = 'Name'
        self.assertEqual(row_from_csv(csv_row)[0], '1')
        values = row_from_document(
            {
                'code': '1',
                'product_name': ['nope'],
                'image_front_small_url': 'https://c',
                'energy-kcal_100g': '5',
                'nova_group': '99999999999',
            }
        )
        columns = list(PRODUCT_COLUMNS)
        self.assertEqual(values[columns.index('code')], '1')
        self.assertIsNone(values[columns.index('product_name')])
        self.assertEqual(values[columns.index('image_url')], 'https://c')
        self.assertEqual(values[columns.index('energy_kcal')], '5')
        self.assertIsNone(values[columns.index('nova_group')])
        self.assertEqual(encode_copy_field(None), r'\N')
        self.assertEqual(encode_copy_field(r'\N'), '"\\N"')
        self.assertEqual(encode_copy_field('a\tb'), '"a\tb"')
        self.assertEqual(encode_copy_field('a\nb'), '"a\nb"')
        self.assertEqual(encode_copy_field('a\rb'), '"a\rb"')
        self.assertEqual(encode_copy_field('a"b'), '"a""b"')
        self.assertEqual(encode_copy_field('plain'), 'plain')


class DocumentTests(SimpleTestCase):
    def test_json_lines_and_arrays(self):
        self.assertEqual(list(iter_documents('')), [])
        self.assertEqual(list(iter_documents(' \n')), [])
        documents = list(iter_documents('\n{"code": "1"}\n\n'))
        self.assertEqual(documents, [{'code': '1'}])
        self.assertEqual(list(iter_documents('[{"code": "2"}]')), [{'code': '2'}])
        with self.assertRaisesRegex(CommandError, 'non-object'):
            list(iter_documents('[1]'))
        with self.assertRaisesRegex(CommandError, 'not an object'):
            list(iter_documents('1\n'))
        with self.assertRaisesRegex(CommandError, 'Invalid delta JSON on line 1'):
            list(iter_documents('{\n'))


class ProjectedCopyTests(SimpleTestCase):
    def test_uncompressed_csv_skips_blank_and_duplicate_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'products.csv'
            fieldnames = [header for column, header in CSV_HEADERS.items() if column not in OPTIONAL_CSV_COLUMNS]
            blank = {name: '' for name in fieldnames}
            first = {name: '' for name in fieldnames}
            first['code'] = '1'
            first['product_name'] = 'a\tb"c'
            duplicate = {name: '' for name in fieldnames}
            duplicate['code'] = '1'
            duplicate['product_name'] = 'second'
            literal = {name: '' for name in fieldnames}
            literal['code'] = r'\N'
            literal['product_name'] = 'literal'
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames, delimiter='\t', lineterminator='\n')
            writer.writeheader()
            writer.writerows([blank, first, duplicate, literal])
            path.write_text(buffer.getvalue(), encoding='utf-8')
            with ProjectedCopy(path) as source:
                payload = source.read(1) + source.read(1) + source.read(None)
                self.assertEqual(source.read(-1), b'')
            self.assertEqual(source.row_count, 2)
            text = payload.decode()
            self.assertIn('"a\tb""c"', text)
            self.assertNotIn('second', text)
            self.assertIn('"\\N"', text)

    def test_missing_columns_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'products.csv.gz'
            path.write_bytes(gzip.compress(b'code\tproduct_name\n1\tMilk\n'))
            with self.assertRaisesRegex(CommandError, 'missing columns'):
                with ProjectedCopy(path):
                    pass


class DownloadDirectoryTests(SimpleTestCase):
    def test_cache_directory_comes_from_the_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'cache'
            with mock.patch.dict(os.environ, {'OPENFOODFACTS_CACHE_DIR': str(target)}):
                self.assertEqual(download_directory(), target)
            self.assertTrue(target.is_dir())

    def test_cache_directory_defaults_to_temp(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop('OPENFOODFACTS_CACHE_DIR', None)
            path = download_directory()
        self.assertEqual(path, Path(tempfile.gettempdir()) / 'openfoodfacts')


class PrimaryKeyTests(SimpleTestCase):
    def test_primary_key_name(self):
        with mock.patch('pola.openfoodfacts.loading.connection') as connection:
            cursor = connection.cursor.return_value.__enter__.return_value
            cursor.fetchone.return_value = None
            with self.assertRaisesRegex(CommandError, 'has no primary key'):
                primary_key_name('product')
            cursor.fetchone.return_value = ('bad-name',)
            with self.assertRaisesRegex(CommandError, 'Unexpected primary key'):
                primary_key_name('product')
            cursor.fetchone.return_value = ('product_pkey',)
            self.assertEqual(primary_key_name('product'), 'product_pkey')
