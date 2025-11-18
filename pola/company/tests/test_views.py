import environ
from bs4 import BeautifulSoup
from django.test import override_settings
from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from reversion.models import Version
from test_plus.test import TestCase
from webtest import Upload

from pola.company.factories import BrandFactory, CompanyFactory
from pola.company.models import Brand, Company
from pola.product.factories import ProductFactory
from pola.product.models import Product
from pola.tests.test_utils import get_dummy_image
from pola.tests.test_views import PermissionMixin
from pola.users.factories import StaffFactory, UserFactory


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

    def test_form_success(self):
        self.login()
        post_data = {
            "name": "",
            "official_name": "Test Company",
            "common_name": "Nazwa dla uzytkownika",
            "is_friend": "False",
            "display_brands_in_description": "False",
            "plCapital": "100",
            "plWorkers": "100",
            "plRnD": "100",
            "plRegistered": "100",
            "plNotGlobEnt": "100",
            "description": "",
            "sources": "",
            "verified": "False",
            "Editor_notes": "",
            "nip": "",
            "address": "",
            "logotype": "",
            "official_url": "",
            "commit_desc": "Opis zmiany",
            "brand_set-TOTAL_FORMS": "3",
            "brand_set-INITIAL_FORMS": "0",
            "brand_set-MIN_NUM_FORMS": "0",
            "brand_set-MAX_NUM_FORMS": "1000",
            "brand_set-__prefix__-name": "",
            "brand_set-__prefix__-common_name": "",
            "brand_set-__prefix__-company": "",
            "brand_set-__prefix__-id": "",
            "brand_set-__prefix__-DELETE": "on",
            "brand_set-0-name": "Test Brand",
            "brand_set-0-common_name": "Nazwa dla uzytkownika marki",
            "brand_set-0-company": "",
            "brand_set-0-id": "",
            "brand_set-1-name": "",
            "brand_set-1-common_name": "",
            "brand_set-1-company": "",
            "brand_set-1-id": "",
            "brand_set-2-name": "",
            "brand_set-2-common_name": "",
            "brand_set-2-company": "",
            "brand_set-2-id": "",
            "action": "Save",
        }
        response = self.client.post(self.url, post_data)

        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Brand.objects.count(), 1)
        company = Company.objects.first()
        self.assertEqual(company.official_name, 'Test Company')
        self.assertEqual(Brand.objects.first().name, 'Test Brand')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, company.get_absolute_url())


class TestCompanyCreateFromKRSView(PermissionMixin, TemplateUsedMixin, WebTestMixin, TestCase):
    url = reverse_lazy('company:create_from_krs')
    template_name = 'company/company_from_krs.html'


class TestCompanyUpdateView(CompanyInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_form.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})

    def test_form_success_with_formset(self):
        self.brand_instance = BrandFactory(company=self.instance)
        self.login()

        initial_form_data = {
            "name": self.instance.name,
            "official_name": self.instance.official_name,
            "common_name": self.instance.common_name,
            "is_friend": "False",
            "display_brands_in_description": "False",
            "plCapital": "",
            "plWorkers": "",
            "plRnD": "",
            "plRegistered": "",
            "plNotGlobEnt": "",
            "description": self.instance.description,
            "sources": "",
            "verified": "False",
            "Editor_notes": "",
            "nip": "",
            "address": "",
            "logotype": "",
            "official_url": "",
            "commit_desc": "",
            "brand_set-TOTAL_FORMS": "4",
            "brand_set-INITIAL_FORMS": "1",
            "brand_set-MIN_NUM_FORMS": "0",
            "brand_set-MAX_NUM_FORMS": "1000",
            "brand_set-0-name": self.brand_instance.name,
            "brand_set-0-common_name": self.brand_instance.common_name,
            "brand_set-0-company": str(self.instance.pk),
            "brand_set-0-id": str(self.brand_instance.pk),
            "brand_set-1-name": "",
            "brand_set-1-common_name": "",
            "brand_set-1-company": str(self.instance.pk),
            "brand_set-1-id": "",
            "brand_set-2-name": "",
            "brand_set-2-common_name": "",
            "brand_set-2-company": str(self.instance.pk),
            "brand_set-2-id": "",
            "brand_set-3-name": "",
            "brand_set-3-common_name": "",
            "brand_set-3-company": str(self.instance.pk),
            "brand_set-3-id": "",
            "action": "Save",
        }

        # Update company data
        post_data = initial_form_data.copy()
        post_data['official_name'] = post_data['official_name'] + "_updated"

        # Set change description
        post_data['commit_desc'] = 'Commit message'

        # Update brand data
        post_data['brand_set-0-name'] = post_data['brand_set-0-name'] + "_updated"
        post_data['brand_set-0-common_name'] = post_data['brand_set-0-common_name'] + "_updated"

        # Add new brand using dynamic formset
        post_data.update(
            {
                "brand_set-4-name": "New brand - name",
                "brand_set-4-common_name": "New brand - common-name",
                "brand_set-4-company": str(self.instance.pk),
                "brand_set-4-id": "",
            }
        )
        post_data["brand_set-TOTAL_FORMS"] = str(int(post_data["brand_set-TOTAL_FORMS"]) + 1)

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.instance.get_absolute_url())

        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Brand.objects.count(), 2)

        company = Company.objects.first()
        company.refresh_from_db()

        self.assertTrue(
            company.official_name.endswith('_updated'), f"{company.official_name!r} does not end with '_updated'"
        )

        existing_brand = Brand.objects.get(pk=self.brand_instance.pk)
        self.assertTrue(
            existing_brand.name.endswith('_updated'), f"{existing_brand.name!r} does not end with '_updated'"
        )
        self.assertTrue(
            existing_brand.common_name.endswith('_updated'),
            f"{existing_brand.common_name!r} does not end with '_updated'",
        )

        new_brand = Brand.objects.filter(company=company).exclude(pk=self.brand_instance.pk).first()
        self.assertEqual(new_brand.name, "New brand - name")
        self.assertEqual(new_brand.common_name, "New brand - common-name")


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
    def test_form_logotype_field(self):
        random_image = get_dummy_image()

        page = self.app.get(self.url, user=self.user)

        page.form['logotype'] = Upload('filename.jpg', random_image, 'image/jpeg')
        page.form['commit_desc'] = "Commit desc"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        self.assertIn(environ.Env().str('POLA_APP_AWS_S3_ENDPOINT_URL'), self.instance.logotype.url)


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

    def test_query_count_should_Be_visible(self):
        self.login()
        p1 = ProductFactory(company=self.instance, query_count=100)
        p2 = ProductFactory(company=self.instance, query_count=50)
        p3 = ProductFactory(company=self.instance, query_count=75)

        resp = self.client.get(self.url)
        doc = BeautifulSoup(resp.content, 'html.parser')
        product_names = [d.text for d in doc.select("#company-table tr td:nth-child(1) > a")]
        self.assertEqual([str(p1), str(p3), str(p2)], product_names)


class CompanyDetailCompanyCardViewTests(TestCase):

    def setUp(self):
        super().setUp()
        self.user = StaffFactory()
        self.client.login(username=self.user.username, password='pass')
        self.company = Company.objects.create(
            name='Test Company',
            verified=True,
            plCapital=100,
            plWorkers=100,
            plRnD=100,
            plRegistered=100,
            plNotGlobEnt=100,
        )
        # Assuming Product model and Company have a relationship
        self.products = [
            Product.objects.create(company=self.company, code='ABC123', query_count=100),
            Product.objects.create(company=self.company, code='XYZ789', query_count=200),
        ]
        self.url = reverse('company:detail', kwargs={'pk': self.company.pk})

    def test_verified_company_with_products_and_100_score(self):
        response = self.client.get(self.url)

        self.assertIn('company_card', response.context_data)
        company_card = response.context_data['company_card']
        self.assertEqual(company_card.pl_score, 100)
        self.assertEqual(company_card.product_count, 2)
        self.assertEqual(company_card.product_query_count, 300)
        self.assertEqual(company_card.most_popular_code, 'XYZ789')

    def test_verified_company_with_products_and_non_100_score(self):
        self.company.plWorkers = 0
        self.company.save()

        response = self.client.get(self.url)

        self.assertIn('company_card', response.context_data)
        company_card = response.context_data['company_card']
        self.assertEqual(company_card.pl_score, 70)

    def test_verified_company_no_products(self):
        # Clear products for this test
        Product.objects.filter(company=self.company).delete()

        response = self.client.get(self.url)

        self.assertIn('company_card', response.context_data)
        company_card = response.context_data['company_card']
        self.assertEqual(company_card.product_count, 0)
        self.assertEqual(company_card.product_query_count, 0)
        self.assertIsNone(company_card.most_popular_code)

    def test_unverified_company(self):
        self.company.verified = False
        self.company.save()

        response = self.client.get(self.url)

        self.assertNotIn('company_card', response.context_data)


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


class TestBrandDetailView(BrandInstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/brand_detail.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('company:brand-detail', kwargs={'pk': self.brand_instance.pk})

    def test_should_products_be_sorted(self):
        self.login()
        ProductFactory(company=self.company_instance, query_count=100, brand=self.brand_instance)
        ProductFactory(company=self.company_instance, query_count=50, brand=self.brand_instance)
        ProductFactory(company=self.company_instance, query_count=75, brand=self.brand_instance)

        resp = self.client.get(self.url)
        doc = BeautifulSoup(resp.content, 'html.parser')
        total_query_count = next(iter(doc.select("[data-testid]"))).text
        self.assertEqual(total_query_count, str(100 + 50 + 75))


class TestCompanyMergeView(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:merge')
    template_name = 'company/company_merge.html'

    def test_filter_by_name(self):
        self.login()
        c1 = CompanyFactory(name='Alpha Sp. z o.o.')
        c2 = CompanyFactory(name='Beta SA')
        c3 = CompanyFactory(name='Gamma LLC')
        resp = self.client.get(self.url, {'q': 'Alp'})
        self.assertContains(resp, str(c1))
        self.assertNotContains(resp, str(c2))
        self.assertNotContains(resp, str(c3))

    def test_filter_by_all_name_fields_and_unique(self):
        self.login()
        # Matches via official_name
        c_off = CompanyFactory(name='x1', official_name='Mega Delta', common_name='')
        # Matches via common_name
        c_com = CompanyFactory(name='x2', official_name='', common_name='SuperMega Epsilon')
        # Matches via name
        c_name = CompanyFactory(name='Mega Zeta', official_name='', common_name='')
        # Does not match
        c_other = CompanyFactory(name='Other Inc', official_name='Other Official', common_name='Other Common')

        resp = self.client.get(self.url, {'q': 'Mega'})

        # Found across all three fields
        self.assertContains(resp, str(c_off))
        self.assertContains(resp, str(c_com))
        self.assertContains(resp, str(c_name))
        # Non-matching company excluded
        self.assertNotContains(resp, str(c_other))

    def test_merge_success(self):
        self.login()
        target = CompanyFactory(common_name='Target')
        other1 = CompanyFactory(common_name='Other1')
        other2 = CompanyFactory(common_name='Other2')
        p1 = ProductFactory(company=other1)
        p2 = ProductFactory(company=other2)
        b1 = BrandFactory(company=other1)
        b2 = BrandFactory(company=other2)

        resp = self.client.post(self.url, {'selected': [str(target.id), str(other1.id), str(other2.id)]})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, target.get_absolute_url())

        # Products moved to target
        p1.refresh_from_db()
        p2.refresh_from_db()
        self.assertEqual(p1.company_id, target.id)
        self.assertEqual(p2.company_id, target.id)

        # Brands moved to target
        b1.refresh_from_db()
        b2.refresh_from_db()
        self.assertEqual(b1.company_id, target.id)
        self.assertEqual(b2.company_id, target.id)

        # Other companies deleted
        self.assertFalse(Company.objects.filter(id__in=[other1.id, other2.id]).exists())

    def test_merge_requires_two_selected(self):
        self.login()
        only = CompanyFactory()
        resp = self.client.post(self.url, {'selected': [str(only.id)]})
        # Should render page with error and not redirect
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Zaznacz co najmniej dwóch producentów')

    def test_merge_recalculates_query_count(self):
        self.login()
        target = CompanyFactory(common_name='Target')
        other1 = CompanyFactory(common_name='Other1')
        other2 = CompanyFactory(common_name='Other2')
        # existing product on target
        ProductFactory(company=target, query_count=2)
        # products to be moved
        ProductFactory(company=other1, query_count=3)
        ProductFactory(company=other2, query_count=7)

        resp = self.client.post(self.url, {'selected': [str(target.id), str(other1.id), str(other2.id)]})
        self.assertEqual(resp.status_code, 302)

        target.refresh_from_db()
        self.assertEqual(target.query_count, 2 + 3 + 7)

    def test_merge_selects_best_target_not_first(self):
        self.login()
        # Poorly filled company (few scored fields set)
        poor = CompanyFactory(name="", official_name="", common_name="", description="")
        # Well-filled company should be chosen as target regardless of order
        best = CompanyFactory(
            address="Some address",
            plCapital=100,
            plCapital_notes="note",
            plRnD=100,
            plRnD_notes="note",
            plWorkers=100,
            plWorkers_notes="note",
            plNotGlobEnt=100,
            plNotGlobEnt_notes="note",
            plRegistered=100,
            plRegistered_notes="note",
            description="desc",
        )

        # First selected is the poorer record, but view should pick 'best'
        resp = self.client.post(self.url, {'selected': [str(poor.id), str(best.id)]})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, best.get_absolute_url())
