from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class GPCSegment(models.Model):
    code = models.CharField(max_length=255, null=False, verbose_name="Kod")
    text = models.CharField(max_length=255, null=False, verbose_name="Nazwa kategorii")
    definition = models.TextField(null=True, verbose_name="Nazwa kategorii")
    active = models.BooleanField(null=True)

    alias = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nazwa alternatywna")

    class Meta:
        verbose_name = _("GPC Segment")
        verbose_name_plural = _("GPC Segmenty")
        db_table = 'gpc_segment'
        ordering = ['-code']

    def get_absolute_url(self):
        return reverse('gpc:segment-detail', args=[self.code])

    def __str__(self):
        return self.alias or self.text


class GPCFamily(models.Model):
    parent = models.ForeignKey(GPCSegment, null=False, blank=False, verbose_name="Segment", on_delete=models.CASCADE)
    code = models.CharField(max_length=32, null=False, verbose_name="Kod")
    text = models.CharField(max_length=255, null=False, verbose_name="Nazwa rodziny")
    definition = models.TextField(null=True, verbose_name="Opis rodziny")
    active = models.BooleanField(null=True)

    alias = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nazwa alternatywna")

    class Meta:
        verbose_name = _("GPC Rodzina")
        verbose_name_plural = _("GPC Rodziny")
        db_table = 'gpc_family'
        ordering = ['-code']

    def get_absolute_url(self):
        return reverse('gpc:family-detail', args=[self.code])

    def __str__(self):
        return self.alias or self.text


class GPCClass(models.Model):
    parent = models.ForeignKey(GPCFamily, null=False, blank=False, verbose_name="Segment", on_delete=models.CASCADE)
    code = models.CharField(max_length=32, null=False, verbose_name="Kod")
    text = models.CharField(max_length=255, null=False, verbose_name="Nazwa klasy")
    definition = models.TextField(null=True, verbose_name="Opis klasy")
    active = models.BooleanField(null=True)

    alias = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nazwa alternatywna")

    class Meta:
        verbose_name = _("GPC Klasa")
        verbose_name_plural = _("GPC Klasy")
        db_table = 'gpc_class'
        ordering = ['-code']

    def get_absolute_url(self):
        return reverse('gpc:class-detail', args=[self.code])

    def __str__(self):
        return self.alias or self.text


class GPCBrick(models.Model):
    parent = models.ForeignKey(GPCClass, null=False, blank=False, verbose_name="Class", on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=False, verbose_name="Kod", db_index=True)
    text = models.CharField(max_length=255, null=False, verbose_name="Nazwa brick")
    definition = models.TextField(null=True, verbose_name="Opis brick")
    definitionExcludes = models.TextField(null=True, verbose_name="Opis wykluczeń")
    active = models.BooleanField(null=True)

    alias = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nazwa alternatywna")

    class Meta:
        verbose_name = _("GPC Brick")
        verbose_name_plural = _("GPC Bricks")
        db_table = 'gpc_brick'
        ordering = ['-code']

    def get_absolute_url(self):
        return reverse('gpc:brick-detail', args=[self.code])

    def __str__(self):
        return self.alias or self.text
