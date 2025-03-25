from unittest import TestCase, mock

import pytest
from django.core.management import call_command


class SendAiPicsStatsTestCase(TestCase):
    @mock.patch('pola.slack.send_ai_pics_stats')
    @pytest.mark.django_db
    def test_run_command(self, mock_send_ai_pics_stats):
        call_command('send_ai_pics_stats')
        mock_send_ai_pics_stats.assert_called_once_with(
            'W ciągu ostatniej doby użytkownicy Poli przysłali 0 zdjęć w 0 sesjach dla 0 produktów.'
        )
