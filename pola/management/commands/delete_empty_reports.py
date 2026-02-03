import sys
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from pola.gcs import get_bucket
from pola.report.models import Attachment


class Command(BaseCommand):
    help = 'Deletes empty reports'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        print('Loading list of GCS files')
        bucket = get_bucket(settings.GCS_BACKEND_BUCKET_NAME)
        gcs_files = {blob.name for blob in bucket.list_blobs()}

        print(f'Loaded {len(gcs_files)} GCS files')

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = Attachment.objects.select_related('report').filter(report__created__gte=startdate)
        for attachment in attachments:
            if attachment.attachment.name not in gcs_files:
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
