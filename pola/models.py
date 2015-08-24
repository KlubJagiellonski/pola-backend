from os.path import basename
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Product
# from django.core.urlresolvers import reverse


class Report(models.Model):
    product = models.ForeignKey(Product)
    client = models.CharField(max_length=40,
                              blank=True, null=True, default=None)
    desciption = models.TextField()


class Query(models.Model):
    client = models.CharField(max_length=40,
                              blank=True, null=True, default=None)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)


class ReportAttachment(models.Model):
    report = models.ForeignKey(Report)
    attachment = models.FileField(
        upload_to="reports/%Y/%m/%d", verbose_name=_("File"))

    @property
    def filename(self):
        return basename(self.attachment.name)

    def __unicode__(self):
        return "%s" % (self.filename)

    def get_absolute_url(self):
        return self.attachment.url

    class Meta:
        abstract = True
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
