from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from report.factories import AttachmentFactory, ReportFactory
from report.models import Report


class DeleteEmptyReportsTestCase(TestCase):
    def test_keep_ai_pics_with_files(self):
        report = ReportFactory()
        AttachmentFactory(report=report)

        self.assertEqual(Report.objects.count(), 1)

        call_command('delete_empty_reports', '10')

        self.assertEqual(Report.objects.count(), 1)

    def test_remove_empty_report_without_files(self):
        report = ReportFactory(description='')
        attachment = AttachmentFactory(report=report)
        attachment.attachment.delete()

        self.assertEqual(Report.objects.count(), 1)

        call_command('delete_empty_reports', '10')

        self.assertEqual(Report.objects.count(), 0)

    def test_keep_non_report_without_files(self):
        report = ReportFactory(description='TEST')
        attachment = AttachmentFactory(report=report)
        attachment.attachment.delete()

        self.assertEqual(Report.objects.count(), 1)

        call_command('delete_empty_reports', '10')

        self.assertEqual(Report.objects.count(), 1)

    def test_keep_untouched_old_files(self):
        report = ReportFactory()
        report.created_at = timezone.now() - timedelta(days=30)
        report.save()
        attachment = AttachmentFactory(report=report)
        attachment.attachment.delete()

        self.assertEqual(Report.objects.count(), 1)

        call_command('delete_empty_reports', '1')

        self.assertEqual(Report.objects.count(), 1)
