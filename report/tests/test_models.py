from unittest import TestCase

from pola.users.factories import UserFactory
from report.factories import ReportFactory, ResolvedReportFactory
from report.models import Report


class TestReportQuerySet(TestCase):
    def test_only_open(self):
        self.assertTrue(Report.objects.only_open().filter(pk=ReportFactory().pk).exists())
        self.assertFalse(Report.objects.only_open().filter(pk=ResolvedReportFactory().pk).exists())

    def test_only_resolved(self):
        self.assertFalse(Report.objects.only_resolved().filter(pk=ReportFactory().pk).exists())
        self.assertTrue(Report.objects.only_resolved().filter(pk=ResolvedReportFactory().pk).exists())

    def test_resolve(self):
        user = UserFactory()

        ReportFactory.create_batch(4)
        Report.objects.resolve(user)

        self.assertEqual(Report.objects.filter(resolved_by=user).count(), 4)
