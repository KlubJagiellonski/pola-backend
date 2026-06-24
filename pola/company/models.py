import textwrap

from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from django.core.validators import ValidationError
from django.db import connection, models
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from model_utils.models import TimeStampedModel
from reversion import revisions as reversion
from storages.backends.s3boto3 import S3Boto3Storage

from pola.concurency import concurency
from pola.logic_score import get_pl_score


class IntegerRangeField(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(models.IntegerField, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CompanyQuerySet(models.query.QuerySet):
    def get_or_create(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super().get_or_create(*args, **kwargs)

        with reversion.create_revision(manage_manually=True, atomic=True):
            obj, created = super().get_or_create(*args, **kwargs)
            if created:
                reversion.set_comment(commit_desc)
                reversion.set_user(commit_user)
                reversion.add_to_revision(obj)
            return obj, created


@reversion.register
class Company(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        unique=False,
        verbose_name=_("Nazwa (pobrana z ILiM)"),
    )
    official_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Nazwa rejestrowa"))
    common_name = models.CharField(max_length=255, blank=True, verbose_name=_("Nazwa dla użytkownika"))

    plCapital = IntegerRangeField(
        verbose_name=_("Udział polskiego kapitału"), min_value=0, max_value=100, null=True, blank=True
    )
    plWorkers = IntegerRangeField(
        verbose_name=_("Miejsce produkcji"),
        min_value=0,
        max_value=100,
        null=True,
        blank=True,
        choices=((0, _("0 - Nie produkuje w Polsce")), (100, _("100 - Produkuje w Polsce"))),
    )
    plRnD = IntegerRangeField(
        verbose_name=_("Miejsca pracy w BiR w Polsce"),
        min_value=0,
        max_value=100,
        null=True,
        blank=True,
        choices=(
            (0, _("0 - Nie tworzy miejsc pracy w BiR Polsce")),
            (100, _("100 - Tworzy miejsca pracy w BiR w Polsce")),
        ),
    )
    plRegistered = IntegerRangeField(
        verbose_name=_("Miejsce rejestracji"),
        min_value=0,
        max_value=100,
        null=True,
        blank=True,
        choices=(
            (0, _("0 - Firma zarejestrowana za granicą")),
            (100, _("100 - Firma zarejestrowana w Polsce")),
        ),
    )
    plNotGlobEnt = IntegerRangeField(
        verbose_name=_("Struktura kapitałowa"),
        min_value=0,
        max_value=100,
        null=True,
        blank=True,
        choices=(
            (0, _("0 - Firma jest częścią zagranicznego koncernu")),
            (100, _("100 - Firma nie jest częścią zagranicznego koncernu")),
        ),
    )

    description = models.TextField(_("Opis producenta"), null=True, blank=True)
    sources = models.TextField(_("Źródła"), null=True, blank=True)

    verified = models.BooleanField(
        default=False, verbose_name=_("Dane zweryfikowane"), choices=((True, _("Tak")), (False, _("Nie")))
    )

    Editor_notes = models.TextField(_("Notatki redakcji (nie pokazujemy użytkownikom)"), null=True, blank=True)

    plCapital_notes = models.TextField(_("Więcej nt. udziału polskiego kapitału"), null=True, blank=True)
    plWorkers_notes = models.TextField(_("Więcej nt. miejsca produkcji"), null=True, blank=True)
    plRnD_notes = models.TextField(_("Więcej nt. miejsc pracy w BiR"), null=True, blank=True)
    plRegistered_notes = models.TextField(_("Więcej nt. miejsca rejestracji"), null=True, blank=True)
    plNotGlobEnt_notes = models.TextField(_("Więcej nt. struktury kapitałowej"), null=True, blank=True)

    nip = models.CharField(max_length=10, db_index=True, null=True, blank=True, verbose_name=_("NIP/Tax ID"))
    address = models.TextField(null=True, blank=True, verbose_name=_("Adres"))
    query_count = models.PositiveIntegerField(null=False, default=0, db_index=True)

    logotype = ResizedImageField(
        _("Logotyp"),
        upload_to='logo/%Y/%m/%d',
        size=[None, 200],
        null=True,
        blank=True,
        force_format='PNG',
        storage=S3Boto3Storage(
            querystring_auth=False,
            bucket_name=settings.AWS_STORAGE_COMPANY_LOGOTYPE_BUCKET_NAME,
            region_name='eu-central-1',
            default_acl=None,
        ),
    )
    official_url = models.URLField(
        _("Link do strony firmy"),
        null=True,
        blank=True,
    )

    is_friend = models.BooleanField(
        default=False, verbose_name=_("Przyjaciel Poli"), choices=((True, _("Tak")), (False, _("Nie")))
    )
    display_brands_in_description = models.BooleanField(
        default=False,
        verbose_name=_("Wyświetlaj informacje o markach w opisie"),
        choices=((True, _("Tak")), (False, _("Nie"))),
    )

    objects = CompanyQuerySet.as_manager()

    @property
    def pl_score(self):
        return get_pl_score(self)

    def increment_query_count(self):
        with connection.cursor() as cursor:
            cursor.execute('update company_company set query_count = query_count +1 where id=%s', [self.id])

    def recalculate_query_count_for_company(self):
        """Recalculate the query_count for the specific company."""
        with connection.cursor() as cursor:
            cursor.execute(
                textwrap.dedent(
                    """
                UPDATE company_company AS c
                SET query_count = (
                  SELECT coalesce(sum(p.query_count), 0)
                  FROM product_product AS p
                  WHERE p.company_id = %s
                )
                WHERE c.id = %s
                """
                ),
                [self.id, self.id],
            )

    @staticmethod
    def recalculate_query_count():
        with connection.cursor() as cursor:
            cursor.execute(
                textwrap.dedent(
                    """
                UPDATE company_company
                SET query_count =
                  (SELECT coalesce(sum(query_count), 0)
                   FROM product_product
                   WHERE company_company.id = product_product.company_id)
                """
                )
            )

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
        return '' if not self.plCapital_notes else self.plCapital_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plWorkers_notes(self):
        return '' if not self.plWorkers_notes else self.plWorkers_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plRnD_notes(self):
        return '' if not self.plRnD_notes else self.plRnD_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plRegistered_notes(self):
        return '' if not self.plRegistered_notes else self.plRegistered_notes.replace('\n', '\\n').replace('\r', '\\r')

    def js_plNotGlobEnt_notes(self):
        return '' if not self.plNotGlobEnt_notes else self.plNotGlobEnt_notes.replace('\n', '\\n').replace('\r', '\\r')

    def get_sources(self, raise_exp=True):
        ret = {}
        if not self.sources:
            return ret

        lines = self.sources.splitlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            s = line.split('|')
            if s.__len__() != 2:
                if raise_exp:
                    raise ValidationError(
                        'Pole >Źródła< powinno składać się '
                        'linii zawierających tytuł odnośnika'
                        ' i odnośnik odzielone znakiem | (pipe)'
                    )
                else:
                    continue
            if s[0] in ret:
                if raise_exp:
                    raise ValidationError(f'Tytuł odnośnika >{s[0]}< występuje więcej niż raz')
                else:
                    continue
            ret[s[0]] = s[1]

        return ret

    def clean(self, *args, **kwargs):
        if self.verified:
            YOU_CANT_SET_VERIFIED = 'Nie możesz oznaczyć producenta jako zweryfikowany jeśli pole >{}< jest nieustalone'
            if self.plCapital is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.format('udział kapitału polskiego'))
            if self.plWorkers is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.format('miejsce produkcji'))
            if self.plRnD is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.format('wysokopłatne miejsca pracy'))
            if self.plRegistered is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.format('miejsce rejestracji'))
            if self.plNotGlobEnt is None:
                raise ValidationError(YOU_CANT_SET_VERIFIED.format('struktura kapitałowa'))
            self.get_sources()

        super().clean(*args, **kwargs)

    def save(self, commit_desc=None, commit_user=None, *args, **kwargs):
        self.full_clean()
        if not commit_desc:
            super().save(*args, **kwargs)
            return

        with reversion.create_revision(manage_manually=True, atomic=True):
            super().save(*args, **kwargs)
            reversion.set_comment(commit_desc)
            reversion.set_user(commit_user)
            reversion.add_to_revision(self)

    class Meta:
        verbose_name = _("Producent")
        verbose_name_plural = _("Producenci")
        ordering = ['-created']
        permissions = (
            # ("view_company", "Can see all company"),
            # ("add_company", "Can add a new company"),
            # ("change_company", "Can edit the company"),
            # ("delete_company", "Can delete the company"),
        )
        indexes = [BrinIndex(fields=['created'], pages_per_range=16)]


class BrandQuerySet(models.query.QuerySet):
    def get_or_create(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super().get_or_create(*args, **kwargs)

        with reversion.create_revision(manage_manually=True, atomic=True):
            obj, created = super().get_or_create(*args, **kwargs)
            if created:
                reversion.set_comment(commit_desc)
                reversion.set_user(commit_user)
                reversion.add_to_revision(obj)
            return obj, created


@reversion.register
class Brand(TimeStampedModel):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Nazwa marki (na podstawie ILiM)"),
    )
    common_name = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Nazwa dla użytkownika"))
    objects = BrandQuerySet.as_manager()
    logotype = ResizedImageField(
        _("Logotyp"),
        upload_to='brand-logotype/%Y/%m/%d',
        size=[None, 200],
        null=True,
        blank=True,
        force_format='PNG',
        storage=S3Boto3Storage(
            querystring_auth=False,
            bucket_name=settings.AWS_STORAGE_COMPANY_LOGOTYPE_BUCKET_NAME,
            region_name='eu-central-1',
        ),
    )
    website_url = models.CharField(
        max_length=128, null=False, blank=False, verbose_name=_("URL marki"), default="example.pl"
    )

    def __str__(self):
        return self.common_name or self.name

    def get_absolute_url(self):
        return reverse('company:brand-detail', args=[self.pk])

    class Meta:
        verbose_name = _("Marka")
        verbose_name_plural = _("Marki")
        ordering = ['-name']
        permissions = (
            # ("view_brand", "Can see all brands"),
        )
