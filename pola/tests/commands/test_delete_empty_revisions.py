from unittest import TestCase

from django.core.management import call_command


class DeleteEmptyRevisionsTestCase(TestCase):
    def test_run_command(self):
        call_command('delete_empty_revisions', '10')
