from api.utils import correct_nip
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import model_to_dict
from simple_history.models import HistoricalRecords


class Company(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    made_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         verbose_name="Made in Poland (0-100%)")
    made_in_poland_info = models.TextField(blank=True)
    capital_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)],
                                            verbose_name="Capital in Poland (0-100%)")
    capital_in_poland_info = models.TextField(blank=True)
    taxes_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)],
                                          verbose_name="Taxes paid in Poland (0-100%)")
    taxes_in_poland_info = models.TextField(blank=True)
    krs_url = models.URLField(null=True, blank=True)
    nip = models.CharField(null=True, blank=True, max_length=12)
    regon = models.CharField(null=True, blank=True, max_length=14)
    address_city = models.CharField(null=True, blank=True, max_length=255)
    address_country = models.CharField(null=True, blank=True, max_length=255)
    address_post_city = models.CharField(null=True, blank=True, max_length=255)
    address_post_code = models.CharField(null=True, blank=True, max_length=10)
    address_street_and_number = models.CharField(null=True, blank=True, max_length=255)
    history = HistoricalRecords()

    def fill_from_gs1(self, gs1OwnerInfo):
        self.name = gs1OwnerInfo['Name']
        self.nip = gs1OwnerInfo['NIP']
        self.regon = gs1OwnerInfo['REGON']

        gs1OwnerAddressInfo = gs1OwnerInfo['Address'] if ('Address' in gs1OwnerInfo) else None
        if gs1OwnerAddressInfo:
            self.address_city = gs1OwnerAddressInfo["City"]
            self.address_country = gs1OwnerAddressInfo["Country"]
            self.address_post_city = gs1OwnerAddressInfo["PostCity"]
            self.address_post_code = gs1OwnerAddressInfo["PostCode"]
            self.address_street_and_number = gs1OwnerAddressInfo["StreetAndNumber"]

    @classmethod
    def find_by_gs1_owner_info(cls, gs1OwnerInfo):
        nip = gs1OwnerInfo['NIP']
        name = gs1OwnerInfo['Name']
        regon = gs1OwnerInfo['REGON']
        results = cls.nip_filter(nip) | cls.name_filter(name) | cls.regon_filter(regon)
        return results[0] if results else None

    @classmethod
    def nip_filter(cls, nip):
        return Company.objects.filter(nip=correct_nip(nip)) if nip else Company.objects.none()

    @classmethod
    def name_filter(cls, name):
        return Company.objects.filter(name=name) if name else Company.objects.none()

    @classmethod
    def regon_filter(cls, regon):
        return Company.objects.filter(regon=regon) if regon else Company.objects.none()


class Product(models.Model):
    barcode = models.CharField(max_length=13, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True)
    made_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         verbose_name="Made in Poland (0-100%)")
    made_in_poland_info = models.TextField(blank=True)
    image = models.TextField(null=True, blank=True)
    gs1_code_type = models.CharField(null=True, blank=True, max_length=255)
    gs1_country = models.CharField(null=True, blank=True, max_length=8)
    gs1_country_name = models.CharField(null=True, blank=True, max_length=255)
    gs1_pool = models.CharField(null=True, blank=True, max_length=255)
    gs1_responsible_entity = models.CharField(null=True, blank=True, max_length=255)
    gs1_status = models.CharField(null=True, blank=True, max_length=255)
    gs1_www = models.URLField(null=True, blank=True)
    number_of_api_calls = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()

    def fill_from_gs1_product_info(self, gs1ProductInfo):
        self.name = gs1ProductInfo['Name']
        self.description = gs1ProductInfo['Description']
        image = gs1ProductInfo['Image']
        self.image = image if image else gs1ProductInfo['BigImage']

    def fill_from_gs1_info(self, gs1Information):
        self.gs1_code_type = gs1Information['CodeType']
        self.gs1_country = gs1Information['Country']
        self.gs1_country_name = gs1Information['CountryName']
        self.gs1_pool = gs1Information['Pool']
        self.gs1_responsible_entity = gs1Information['ResponsibleEntity']
        self.gs1_status = gs1Information['Status']
        self.gs1_www = gs1Information['Www']

    def dict_representation(self):
        dictSelf = model_to_dict(self)
        dictCompany = model_to_dict(self.company) if self.company else None
        dictSelf['company'] = dictCompany
        return dictSelf



