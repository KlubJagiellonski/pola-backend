from unittest import TestCase

import pytest
from django.core.management import call_command


class DeleteEmptyRevisionsTestCase(TestCase):
    @pytest.mark.django_db
    def test_run_command(self):
        call_command('delete_empty_revisions', '10')
