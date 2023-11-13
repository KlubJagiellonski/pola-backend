from bs4 import BeautifulSoup
from django.test import override_settings
from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from reportlab.graphics import renderPM
from reversion.models import Version
from test_plus.test import TestCase
from webtest import Upload

from pola.company.factories import BrandFactory, CompanyFactory
from pola.company.models import Brand, Company
from pola.product.factories import ProductFactory
from pola.product.images import Barcode
from pola.product.models import Product
from pola.tests.test_views import PermissionMixin
from pola.users.factories import StaffFactory, UserFactory


def get_dummy_image(code="123", width=300):
    barcode = Barcode.get_barcode(code, width)
    data = renderPM.drawToString(barcode, fmt='PNG')
    return data


class TemplateUsedMixin:
    def test_template_used(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class CompanyInstanceMixin:
    def setUp(self):
        super().setUp()
        self.instance = CompanyFactory()

    def test_contains_official_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.instance.official_name)


class BrandInstanceMixin:
    def setUp(self):
        super().setUp()
        self.company_instance = CompanyFactory()
        self.brand_instance = BrandFactory(company=self.company_instance)

    def test_contains_official_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.brand_instance.common_name)


class TestCompanyCreateView(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:create')
    template_name = 'company/company_form.html'


class TestCompanyCreateFromKRSView(PermissionMixin, TemplateUsedMixin, WebTestMixin, TestCase):
    url = reverse_lazy('company:create_from_krs')
    template_name = 'company/company_from_krs.html'


class TestCompanyUpdate(CompanyInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_form.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})


class TestCompanyUpdateWeb(WebTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.instance = CompanyFactory(name="company_name")
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})
        self.user = StaffFactory()

    def test_form_success(self):
        page = self.app.get(self.url, user=self.user)
        page.form['official_name'] = "New name"
        page.form['commit_desc'] = "Commit description"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        versions = Version.objects.get_for_object(self.instance)
        self.assertEqual(versions[0].revision.comment, "Commit description")
        self.assertEqual(versions[0].revision.user, self.user)
        self.assertEqual(self.instance.official_name, "New name")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_commit_desc_required(self):
        page = self.app.get(self.url, user=self.user)
        page.form['official_name'] = "New name"
        page = page.form.submit()

        self.assertContains(page, "This field is required.")

        page.form['commit_desc'] = "AAA"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_readonly_fields(self):
        page = self.app.get(self.url, user=self.user)
        self.assertEqual(page.form['name'].attrs['disabled'], 'true')

        page.form['name'] = "789789789"
        page.form['commit_desc'] = "Commit desc"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, "company_name")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_readonly_fields222(self):
        random_image = get_dummy_image()

        page = self.app.get(self.url, user=self.user)

        page.form['logotype'] = Upload('filename.jpg', random_image, 'image/jpeg')
        page.form['commit_desc'] = "Commit desc"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        self.assertIn("http://minio:9000", self.instance.logotype.url)


class TestConcurencyComapnyUpdate(TestCase):
    user_factory = UserFactory

    def setUp(self):
        super().setUp()
        self.instance = CompanyFactory()

    def test_restrictions(self):
        user1 = self.make_user('u1', perms=['company.view_company', 'company.change_company'])
        user2 = self.make_user('u2', perms=['company.view_company', 'company.change_company'])
        url = reverse('company:edit', kwargs={'pk': self.instance.pk})

        with self.login(username=user1.username):
            response = self.get(url)
            self.response_200(response)

        with self.login(username=user2.username):
            response = self.get(url)
            self.response_302(response)


class TestCompanyDeleteView(CompanyInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_confirm_delete.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:delete', kwargs={'pk': self.instance.pk})

    def test_object_delete(self):
        self.login()
        self.client.post(self.url)
        self.assertFalse(Company.objects.filter(pk=self.instance.pk).exists())


class TestCompanyDetailView(CompanyInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_detail.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:detail', kwargs={'pk': self.instance.pk})

    def test_should_products_be_sorted(self):
        self.login()
        p1 = ProductFactory(company=self.instance, query_count=100)
        p2 = ProductFactory(company=self.instance, query_count=50)
        p3 = ProductFactory(company=self.instance, query_count=75)

        resp = self.client.get(self.url)
        doc = BeautifulSoup(resp.content, 'html.parser')
        product_names = [d.text for d in doc.select("#company-table tr td:nth-child(1) > a")]
        self.assertEqual([str(p1), str(p3), str(p2)], product_names)


class TestCompanyListView(PermissionMixin, TemplateUsedMixin, WebTestMixin, TestCase):
    url = reverse_lazy('company:list')
    template_name = 'company/company_filter.html'

    def test_empty(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, "Nie znaleziono producentów spełniających zadane kryteria")

    def test_filled(self):
        products = CompanyFactory.create_batch(100)
        page = self.app.get(self.url, user=self.user)
        # self.assertTrue("1 z 4" in page)
        self.assertTrue(str(products[-1]) in page)
        page2 = page.click("Następne")
        page2.click("Poprzednie")


class CompanyAutocomplete(PermissionMixin, TestCase):
    url = reverse_lazy('company:company-autocomplete')


class TestBrandDeleteView(BrandInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/brand_confirm_delete.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:brand-delete', kwargs={'pk': self.brand_instance.pk})

    def test_object_delete(self):
        product_instance = ProductFactory(brand=self.brand_instance)
        self.login()
        self.client.post(self.url)
        self.assertFalse(Brand.objects.filter(pk=self.brand_instance.pk).exists())
        self.assertTrue(Company.objects.filter(pk=self.brand_instance.company.pk).exists())
        self.assertTrue(Product.objects.filter(pk=product_instance.pk).exists())
