from datetime import timedelta

from boto.s3.connection import Bucket
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from ai_pics.models import AIAttachment
from pola.s3 import create_s3_connection


class Command(BaseCommand):
    help = 'Deletes empty AI pics'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        conn = create_s3_connection()
        bucket = Bucket(conn, name=settings.AWS_STORAGE_BUCKET_AI_NAME)

        s3_files = set()
        for key in bucket.list():
            s3_files.add(key.name)

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = AIAttachment.objects.select_related('ai_pics').filter(ai_pics__created_at__gte=startdate)
        for attachment in attachments:
            if attachment.attachment not in s3_files:
                print(attachment.attachment)
                attachment.delete()

        with connection.cursor() as cursor:
            cursor.execute(
                'delete from ai_pics_aipics WHERE '
                '(select count(*) from ai_pics_aiattachment where ai_pics_id=ai_pics_aipics.id) =0'
            )
