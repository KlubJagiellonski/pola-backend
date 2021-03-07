import sys
from datetime import timedelta

from boto.s3.connection import Bucket
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from pola.s3 import create_s3_connection
from report.models import Attachment


class Command(BaseCommand):
    help = 'Deletes empty reports'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        print('Loading list of S3 files')
        conn = create_s3_connection()
        bucket = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)

        s3_files = set()
        for key in bucket.list():
            s3_files.add(key.name)

        print(f'Loaded {len(s3_files)} S3 files')

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = Attachment.objects.select_related('report').filter(report__created_at__gte=startdate)
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
