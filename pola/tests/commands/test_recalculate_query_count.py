from unittest import TestCase

from django.core.management import call_command


class RecalculateQueryCountTestCase(TestCase):
    def test_run_command(self):
        call_command('recalculate_query_count')
