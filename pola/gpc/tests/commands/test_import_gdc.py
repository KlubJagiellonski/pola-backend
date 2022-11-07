import re
from pathlib import Path

from django.core.management import CommandError, call_command
from django.test import TestCase

from pola.gpc import models

FIXTURE_DIR = Path(__file__).absolute().parents[2] / "fixtures"
if not FIXTURE_DIR.exists():
    raise Exception("Directory not exists: " + str(FIXTURE_DIR))


class ImportGDCTestCase(TestCase):
    def test_invalid_file(self):
        with self.assertRaisesRegex(
            CommandError,
            re.escape(
                "Error: argument xml_filepath: can't open '/invalid-file.xml': "
                "[Errno 2] No such file or directory: '/invalid-file.xml'"
            ),
        ):
            call_command('import_gdc', '/invalid-file.xml')

    def test_should_import_may_data_file(self):
        fixture_file = FIXTURE_DIR / "GPC_as_of-May_2021_GDSN_v20210723_PL.xml"

        self.assertEqual(models.GPCSegment.objects.count(), 0)
        self.assertEqual(models.GPCFamily.objects.count(), 0)
        self.assertEqual(models.GPCClass.objects.count(), 0)
        self.assertEqual(models.GPCBrick.objects.count(), 0)

        call_command('import_gdc', fixture_file, "--noinput")

        self.assertEqual(models.GPCSegment.objects.count(), 41)
        self.assertEqual(models.GPCFamily.objects.count(), 149)
        self.assertEqual(models.GPCClass.objects.count(), 919)
        self.assertEqual(models.GPCBrick.objects.count(), 5153)
