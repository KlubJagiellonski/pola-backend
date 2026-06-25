from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from pola.ai_pics.models import AIAttachment
from pola.management.command_utils import load_s3_files_list


class Command(BaseCommand):
    help = 'Deletes empty AI pics'

    def add_arguments(self, parser):
        parser.add_argument('no_of_days_back')

    def handle(self, *args, **options):
        s3_files = load_s3_files_list(settings.AWS_STORAGE_AI_PICS_BUCKET_NAME)

        startdate = timezone.now() - timedelta(days=int(options["no_of_days_back"]))
        attachments = AIAttachment.objects.select_related('ai_pics').filter(ai_pics__created__gte=startdate)
        for attachment in attachments:
            if attachment.attachment not in s3_files:
                print(attachment.attachment)
                attachment.delete()

        with connection.cursor() as cursor:
            cursor.execute(
                'delete from ai_pics_aipics WHERE '
                '(select count(*) from ai_pics_aiattachment where ai_pics_id=ai_pics_aipics.id) =0'
            )
