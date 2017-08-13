# -*- coding: utf-8 -*-

from django.core.validators import ValidationError
from django.db import connection, models
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from reversion import revisions as reversion

from pola.concurency import concurency


class IntegerRangeField(models.IntegerField):

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(models.IntegerField, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class CompanyQuerySet(models.query.QuerySet):

    def get_or_create(self, commit_desc=None, commit_user=None,
                      *args, **kwargs):
        if not commit_desc:
            return super(CompanyQuerySet, self).get_or_create(*args, **kwargs)

        with reversion.create_revision(manage_manually=True, atomic=True):
            obj, created = super(CompanyQuerySet, self).get_or_create(*args, **kwargs)
            if created:
                reversion.set_comment(commit_desc)
                reversion.set_user(commit_user)
                reversion.add_to_revision(obj)
            return obj, created


@reversion.register
@python_2_unicode_compatible
class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, null=True, blank=True,
                            db_index=True,
                            verbose_name=_(u"Nazwa (pobrana z ILiM)"))
    official_name = models.CharField(max_length=128, blank=True, null=True,
                                     verbose_name=_(u"Nazwa rejestrowa"))
    common_name = models.CharField(max_length=128, blank=True,
                                   verbose_name=_(u"Nazwa dla użytkownika"))

    plCapital = IntegerRangeField(
        verbose_name=_(u"Udział polskiego kapitału"),
        min_value=0, max_value=100, null=True, blank=True)
    plWorkers = IntegerRangeField(
        verbose_name=_(u"Miejsce produkcji"), min_value=0,
        max_value=100, null=True, blank=True,
        choices=((0, _(u"0 - Nie produkuje w Polsce")),
                 (100, _(u"100 - Produkuje w Polsce"))))
    plRnD = IntegerRangeField(
        verbose_name=_(u"Miejsca pracy w BiR w Polsce"), min_value=0,
        max_value=100, null=True, blank=True,
        choices=((0, _(u"0 - Nie tworzy miejsc pracy w BiR Polsce")),
                 (100, _(u"100 - Tworzy miejsca pracy w BiR w Polsce"))))
    plRegistered = IntegerRangeField(
        verbose_name=_(u"Miejsce rejestracji"), min_value=0, max_value=100,
        null=True, blank=True,
        choices=((0, _(u"0 - Firma zarejestrowana za granicą")),
                 (100, _(u"100 - Firma zarejestrowana w Polsce"))))
    plNotGlobEnt = IntegerRangeField(
        verbose_name=_(u"Struktura kapitałowa"), min_value=0,
        max_value=100, null=True, blank=True,
        choices=((0, _(u"0 - Firma jest częścią zagranicznego koncernu")),
                 (100,
                  _(u"100 - Firma nie jest częścią zagranicznego koncernu"))))

    description = models.TextField(
        _(u"Opis producenta"), null=True, blank=True)
    sources = models.TextField(_(u"Źródła"), null=True, blank=True)

    verified = models.BooleanField(default=False,
                                   verbose_name=_("Dane zweryfikowane"),
                                   choices=((True, _("Tak")),
                                            (False, _("Nie"))))

    Editor_notes = models.TextField(
        _(u"Notatki redakcji (nie pokazujemy użytkownikom)"), null=True,
        blank=True)

    plCapital_notes = models.TextField(
        _(u"Więcej nt. udziału polskiego kapitału"), null=True, blank=True)
    plWorkers_notes = models.TextField(
        _(u"Więcej nt. miejsca produkcji"), null=True, blank=True)
    plRnD_notes = models.TextField(
        _(u"Więcej nt. miejsc pracy w BiR"), null=True, blank=True)
    plRegistered_notes = models.TextField(
        _(u"Więcej nt. miejsca rejestracji"), null=True, blank=True)
    plNotGlobEnt_notes = models.TextField(
        _(u"Więcej nt. struktury kapitałowej"), null=True, blank=True)

    nip = models.CharField(max_length=10, db_index=True, null=True,
                           blank=True, verbose_name=_(u"NIP/Tax ID"))
    address = models.TextField(null=True, blank=True,
                               verbose_name=_(u"Adres"))
    query_count = models.PositiveIntegerField(null=False, default=0, db_index=True)

    objects = CompanyQuerySet.as_manager()

    def increment_query_count(self):
        with connection.cursor() as cursor:
            cursor.execute(
                'update company_company set query_count = query_count +1 '
                'where id=%s', [self.id])

    @staticmethod
    def recalculate_query_count():
        with connection.cursor() as cursor:
            cursor.execute(
                'update company_company set query_count = '
                '(select coalesce(sum(query_count),0) '
                'from product_product '
                'where product_product.company_id=company_company.id)')

    def to_dict(self):
        dict = model_to_dict(self)
        return dict

    def get_absolute_url(self):
        return reverse('company:detail', args=[self.pk])

    def locked_by(self):
        return concurency.locked_by(self)

    def __str__(self):
        return self.common_name or self.official_name or self.name

    def js_plCapital_notes(self):
        return '' if not self.plCapital_notes else\
            self.plCapital_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plWorkers_notes(self):
        return '' if not self.plWorkers_notes else\
            self.plWorkers_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plRnD_notes(self):
        return '' if not self.plRnD_notes else\
            self.plRnD_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plRegistered_notes(self):
        return '' if not self.plRegistered_notes else\
            self.plRegistered_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plNotGlobEnt_notes(self):
        return '' if not self.plNotGlobEnt_notes else\
            self.plNotGlobEnt_notes.replace('\n', '\\n').replace('\r', '\\r')

    def get_sources(self, raise_exp=True):
        ret = {}
        if not self.sources:
            return ret

        lines = self.sources.splitlines()
        for line in lines:
            line = line.strip()
            if line == u'':
                continue
            s = line.split(u'|')
            if s.__len__() != 2:
                if raise_exp:
                    raise ValidationError(u'Pole >Źródła< powinno składać się '
                                          u'linii zawierających tytuł odnośnika'
                                          u' i odnośnik odzielone znakiem | (pipe)')
                else:
                    continue
            if s[0] in ret:
                if raise_exp:
                    raise ValidationError(u'Tytuł odnośnika >{}< występuje'
                                          u' więcej niż raz'.format(s[0]))
                else:
                    continue
            ret[s[0]] = s[1]

        return ret

    def clean(self, *args, **kwargs):
        if self.verified:
            YOU_CANT_SET_VERIFIED = u'Nie możesz oznaczyć producenta jako ' \
                u'zweryfikowany jeśli pole >{}< jest nieustalone'
            if self.plCapital is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.
                                      format(u'udział kapitału polskiego'))
            if self.plWorkers is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.
                                      format(u'miejsce produkcji'))
            if self.plRnD is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.
                                      format('wysokopłatne miejsca pracy'))
            if self.plRegistered is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.
                                      format(u'miejsce rejestracji'))
            if self.plNotGlobEnt is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.
                                      format(u'struktura kapitałowa'))
            self.get_sources()

        super(Company, self).clean(*args, **kwargs)

    def save(self, commit_desc=None, commit_user=None, *args, **kwargs):
        self.full_clean()
        if not commit_desc:
            return super(Company, self).save(*args, **kwargs)

        with reversion.create_revision(manage_manually=True, atomic=True):
            obj = super(Company, self).save(*args, **kwargs)
            reversion.set_comment(commit_desc)
            reversion.set_user(commit_user)
            reversion.add_to_revision(obj)
            return obj

    class Meta:
        verbose_name = _(u"Producent")
        verbose_name_plural = _(u"Producenci")
        ordering = ['-created_at']
