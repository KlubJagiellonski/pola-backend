from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from pola.ai_pics.models import AIAttachment
from pola.gcs import get_bucket


class Command(BaseCommand):
    help = 'Deletes empty AI pics'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        bucket = get_bucket(settings.GCS_AI_PICS_BUCKET_NAME)
        gcs_files = {blob.name for blob in bucket.list_blobs()}

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = AIAttachment.objects.select_related('ai_pics').filter(ai_pics__created__gte=startdate)
        for attachment in attachments:
            if attachment.attachment.name not in gcs_files:
                print(attachment.attachment)
                attachment.delete()

        with connection.cursor() as cursor:
            cursor.execute(
                'delete from ai_pics_aipics WHERE '
                '(select count(*) from ai_pics_aiattachment where ai_pics_id=ai_pics_aipics.id) =0'
            )
