import sys
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from pola.management.command_utils import load_s3_files_list
from pola.report.models import Attachment


class Command(BaseCommand):
    help = 'Deletes empty reports'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        print('Loading list of S3 files')
        s3_files = load_s3_files_list(settings.AWS_STORAGE_BACKEND_BUCKET_NAME)

        print(f'Loaded {len(s3_files)} S3 files')

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = Attachment.objects.select_related('report').filter(report__created__gte=startdate)
        for attachment in attachments:
            if attachment.attachment not in s3_files:
                attachment.delete()
                sys.stdout.write('-')
            else:
                sys.stdout.write('+')
            sys.stdout.flush()

        print('Deleting empty reports')
        with connection.cursor() as cursor:
            cursor.execute(
                "delete from report_report WHERE "
                "(description is NULL or description = '') AND "
                "(select count(*) from report_attachment where report_id=report_report.id) =0"
            )
