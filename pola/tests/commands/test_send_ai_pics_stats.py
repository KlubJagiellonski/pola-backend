import importlib
from unittest import mock

import pytest
from django.core.management import call_command
from django.test import TestCase


@pytest.mark.django_db
class SendAiPicsStatsTestCase(TestCase):
    def test_run_command(self):
        command_module = importlib.import_module('pola.management.commands.send_ai_pics_stats')
        with mock.patch.object(command_module, 'send_ai_pics_stats') as mock_send_ai_pics_stats:
            call_command('send_ai_pics_stats')
            mock_send_ai_pics_stats.assert_called_once_with(
                'W ciągu ostatniej doby użytkownicy Poli przysłali 0 zdjęć w 0 sesjach dla 0 produktów.'
            )
