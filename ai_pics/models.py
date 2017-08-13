# -*- coding: utf-8 -*-

from os.path import basename

from babel.dates import format_timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from product.models import Product


class AIPics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.CharField(max_length=40, blank=False, null=False,
                              verbose_name=_(u'Zgłaszający'))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Utworzone'))

    original_width = models.IntegerField(null=False)
    original_height = models.IntegerField(null=False)

    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

    device_name = models.CharField(max_length=100)
    flash_used = models.NullBooleanField()
    was_portrait = models.NullBooleanField()

    is_valid = models.NullBooleanField()

    def attachment_count(self):
        return self.attachment_set.count()

    def get_timedelta(self):
        return format_timedelta(timezone.now() - self.created_at,
                                locale='pl_PL')

    class Meta:
        verbose_name = _("AIPics")
        verbose_name_plural = _("AIPics")


@python_2_unicode_compatible
class AIAttachment(models.Model):
    ai_pics = models.ForeignKey(AIPics, on_delete=models.CASCADE)
    file_no = models.IntegerField(null=False, default=0)
    attachment = models.FileField(
        upload_to="ai/%Y/%m/%d", verbose_name=_("File"))

    @property
    def filename(self):
        return basename(self.attachment.name)

    def __str__(self):
        return "%s" % (self.filename)

    def get_absolute_url(self):
        return 'https://{}.s3.amazonaws.com/{}'.format(
            settings.AWS_STORAGE_BUCKET_AI_NAME, self.attachment)

    class Meta:
        verbose_name = _("AIPics's attachment")
        verbose_name_plural = _("AIPics's attachments")
