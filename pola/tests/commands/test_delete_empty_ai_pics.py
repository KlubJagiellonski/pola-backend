from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from ai_pics.factories import AIAttachmentFactory, AIPicsFactory
from ai_pics.models import AIAttachment, AIPics


class DeleteEmptyAiPicsTestCase(TestCase):
    def test_keep_ai_pics_with_files(self):
        ai_pics = AIPicsFactory()
        AIAttachmentFactory(ai_pics=ai_pics)

        self.assertEqual(AIPics.objects.count(), 1)

        call_command('delete_empty_ai_pics', '10')

        self.assertEqual(AIPics.objects.count(), 1)

    def test_remove_ai_pics_without_files(self):
        ai_pics: AIPics = AIPicsFactory()
        ai_attachment: AIAttachment = AIAttachmentFactory(ai_pics=ai_pics)
        ai_attachment.attachment.delete()
        self.assertEqual(AIPics.objects.count(), 1)

        call_command('delete_empty_ai_pics', '10')

        self.assertEqual(AIPics.objects.count(), 0)

    def test_keep_untouched_old_files(self):
        created_at = timezone.now() - timedelta(days=30)
        ai_pics: AIPics = AIPicsFactory()
        ai_pics.created_at = created_at
        ai_pics.save()

        ai_attachment: AIAttachment = AIAttachmentFactory(ai_pics=ai_pics)
        ai_attachment.attachment.delete()
        self.assertEqual(AIPics.objects.count(), 1)

        call_command('delete_empty_ai_pics', '1')

        self.assertEqual(AIPics.objects.count(), 1)
