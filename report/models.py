# -*- coding: utf-8 -*-

import re
import reversion
from os.path import basename
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from datetime import datetime
from babel.dates import format_timedelta
from django.utils import timezone


class ReportQuerySet(models.QuerySet):
    def only_open(self):
        return (self.filter(resolved_at__isnull=True)
                    .filter(resolved_by__isnull=True))

    def only_resolved(self):
        return (self.filter(resolved_at__isnull=False)
                    .filter(resolved_by__isnull=False))

    def resolve(self, user):
        return self.update(resolved_at=timezone.now(),
                           resolved_by=user)


class Report(models.Model):
    product = models.ForeignKey(Product, null=True)
    client = models.CharField(max_length=40, blank=True, null=True,
                              default=None, verbose_name=_(u'Zgłaszający'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Utworzone'))
    resolved_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name=_('Rozpatrzone'))
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    blank=True,
                                    verbose_name=_('Rozpatrzone przez'))
    description = models.TextField(verbose_name=_('Opis'))
    objects = ReportQuerySet.as_manager()

    def status(self):
        if self.resolved_at is not None:
            return self.RESOLVED

        if self.resolved_by is not None:
            return self.RESOLVED

        return self.OPEN

    def resolve(self, user, commit=True):
        self.resolved_at = timezone.now()
        self.resolved_by = user
        if commit:
            self.save()

    def get_absolute_url(self):
        return reverse('report:detail', args=[self.pk])

    def __unicode__(self):
        return self.description[:40] or "None"

    def get_timedelta(self):
        return format_timedelta(timezone.now()-self.created_at, locale='pl_PL')

    def attachment_count(self):
        return self.attachment_set.count()

    OPEN = 1
    RESOLVED = 2

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class Attachment(models.Model):
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
        verbose_name = _("Report's attachment")
        verbose_name_plural = _("Report's attachments")


# Command in reversion description.
COMMAND_REGEXP = re.compile(r'(?P<command>\w+)\s?\#(?P<pk>[0-9]+)', re.I)


def on_revision_commit(instances, revision, **kwargs):
    comment = revision.comment
    search = COMMAND_REGEXP.search(comment)
    if not search:
        return

    command = search.group('command')
    pk = search.group('pk')

    if command.lower() == 'close':
        handle_command_close(revision, command, pk)

reversion.post_revision_commit.connect(on_revision_commit)


def handle_command_close(revision, command, pk):
    report = Report.objects.only_open().get(pk=pk)

    if report:
        report.resolve(revision.user)
