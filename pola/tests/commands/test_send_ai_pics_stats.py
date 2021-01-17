from unittest import TestCase

from django.core.management import call_command


class SendAiPicsStatsTestCase(TestCase):
    def test_run_command(self):
        call_command('send_ai_pics_stats')
