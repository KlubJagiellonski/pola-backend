from django.core.files.temp import NamedTemporaryFile
from django.core.management import call_command
from django.test import TestCase


class ImportBrandsTestCase(TestCase):
    def test_run_command(self):
        with NamedTemporaryFile() as tmp_file:
            call_command('import_brands', tmp_file.name)
