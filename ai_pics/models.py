from os.path import basename

from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from storages.backends.s3boto3 import S3Boto3Storage

from product.models import Product


class AIPics(models.Model):
    STATES = (
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
        ('unknown', 'Unknown'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.CharField(max_length=40, blank=False, null=False, verbose_name=_('Zgłaszający'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Utworzone'))

    original_width = models.IntegerField(null=False)
    original_height = models.IntegerField(null=False)

    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

    device_name = models.CharField(max_length=100)
    flash_used = models.BooleanField(null=True)
    was_portrait = models.BooleanField(null=True)

    is_valid = models.BooleanField(null=True)

    def attachment_count(self):
        return self.attachment_set.count()

    def get_absolute_url(self):
        return reverse('ai_pics:detail', args=[self.pk])

    @property
    def state(self):
        if self.is_valid is None:
            return 'unknown'
        if self.is_valid:
            return 'valid'
        return 'invalid'

    @state.setter
    def state(self, value):
        if value == 'valid':
            self.is_valid = True
            return
        if value == 'invalid':
            self.is_valid = False
            return
        self.is_valid = None

    class Meta:
        verbose_name = _("AIPics")
        verbose_name_plural = _("AIPics")
        permissions = (
            # ("view_aipics", "Can see all AIPics"),
            # ("add_aipics", "Can add a new AIPics"),
            # ("change_aipics", "Can edit the AIPics"),
            # ("delete_aipics", "Can delete the AIPics"),
        )
        indexes = [BrinIndex(fields=['created_at'], pages_per_range=16)]


class AIAttachment(models.Model):
    ai_pics = models.ForeignKey(AIPics, on_delete=models.CASCADE)
    file_no = models.IntegerField(null=False, default=0)
    attachment = models.FileField(
        upload_to="ai/%Y/%m/%d",
        verbose_name=_("File"),
        storage=S3Boto3Storage(bucket_name=settings.AWS_STORAGE_BUCKET_AI_NAME),
    )

    @property
    def filename(self):
        return basename(self.attachment.name)

    def __str__(self):
        return f"{self.filename}"

    def get_absolute_url(self):
        return self.attachment.url

    class Meta:
        verbose_name = _("AIPics's attachment")
        verbose_name_plural = _("AIPics's attachments")
        permissions = (
            # ("view_aiattachment", "Can see all AIAttachment"),
            # ("add_aiattachment", "Can add a new AIAttachment"),
            # ("change_aiattachment", "Can edit the AIAttachment"),
            # ("delete_aiattachment", "Can delete the AIAttachment"),
        )
