from unittest import TestCase

import pytest
from django.core.management import call_command


class RequeryAllCodesTestCase(TestCase):
    @pytest.mark.django_db
    def test_run_command(self):
        call_command('requery_all_codes')
