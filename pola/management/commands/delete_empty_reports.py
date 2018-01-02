from django.core.management.base import BaseCommand, CommandError
from boto.s3.connection import S3Connection, Bucket, Key
from django.conf import settings
from report.models import Report, Attachment
from sets import Set
from django.db import connection
from datetime import datetime, timedelta
from django.utils import timezone
import sys

class Command(BaseCommand):
    help = 'Deletes empty reports'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        print('Loading list of S3 files')

        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)

        s3_files = Set()
        for key in bucket.list():
            s3_files.add(key.name)

        print('Loaded {} S3 files'.format(len(s3_files)))

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = Attachment.objects.select_related('report')\
            .filter(report__created_at__gte=startdate)
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
