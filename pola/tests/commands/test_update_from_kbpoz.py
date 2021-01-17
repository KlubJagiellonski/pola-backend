from tempfile import NamedTemporaryFile
from unittest import TestCase

from django.core.management import call_command


class UpdateFromKbpozTestCase(TestCase):
    def test_run_command(self):
        with NamedTemporaryFile() as tmp_file:
            call_command('update_from_kbpoz', tmp_file.name)
