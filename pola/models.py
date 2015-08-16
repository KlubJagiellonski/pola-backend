from django.db import models
from os.path import basename
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
from product.models import Product
# from django.core.urlresolvers import reverse


class Client(models.Model):
    pass

    def to_dict(self):
        dict = model_to_dict(self)
        return dict


class Report(models.Model):
    barcode = models.ForeignKey(Product)
    client = models.ForeignKey(Client)
    desciption = models.TextField()


class Query(models.Model):
    client = models.ForeignKey(Client)
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
