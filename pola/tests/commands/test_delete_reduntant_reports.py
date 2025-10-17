from unittest import TestCase

import pytest
from django.core.management import call_command


class DeleteRedundantProductsTestCase(TestCase):
    @pytest.mark.django_db
    def test_run_command(self):
        call_command('delete_reduntant_reports', '10')
