from django.test import override_settings
from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from reversion.models import Version
from test_plus.test import TestCase

from company.factories import CompanyFactory
from pola.tests.test_views import PermissionMixin
from pola.users.factories import StaffFactory
from product.factories import ProductFactory
from product.models import Product


class TemplateUsedMixin:
    def test_template_used(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class InstanceMixin:
    def setUp(self):
        super().setUp()
        self.instance = ProductFactory()

    def test_contains_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.instance.name)


class TestProductDetailView(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_detail.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('product:detail', args=[self.instance.code])


class TestProductListView(PermissionMixin, WebTestMixin, TestCase):
    url = reverse_lazy('product:list')
    template_name = 'product/product_filter.html'

    def test_empty(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, "Nic nie znaleziono")

    def test_filled(self):
        products = ProductFactory.create_batch(100)
        page = self.app.get(self.url, user=self.user)
        # self.assertTrue("1 z 4" in page)
        self.assertTrue(str(products[-1]) in page)
        page2 = page.click("Następne")
        page2.click("Poprzednie")


class TestProductCreate(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('product:create')
    template_name = 'product/product_form.html'


class TestProductUpdate(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_update_form.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('product:edit', args=[self.instance.code])


class TestProductUpdateWeb(WebTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.instance = ProductFactory(code="123")
        self.url = reverse('product:edit', args=[self.instance.code])
        self.user = StaffFactory()

    def test_form_success(self):
        page = self.app.get(self.url, user=self.user)
        page.form['name'] = "New name"
        page.form['commit_desc'] = "Commit description"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        versions = Version.objects.get_for_object(self.instance)
        self.assertEqual(versions[0].revision.comment, "Commit description")
        self.assertEqual(versions[0].revision.user, self.user)
        self.assertEqual(self.instance.name, "New name")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_commit_desc_required(self):
        page = self.app.get(self.url, user=self.user)
        page.form['name'] = "New name"
        page = page.form.submit()

        self.assertContains(page, "This field is required.")

        page.form['commit_desc'] = "AAA"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())


class TestProductDeleteView(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_detail.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('product:delete', args=[self.instance.code])

    def test_success_delete(self):
        self.login()
        resp = self.post(self.url, follow=True)
        self.assertRedirects(resp, expected_url=reverse('product:list'))
        self.assertContains(resp, "Product deleted!")
        self.assertFalse(Product.objects.filter(pk=self.instance.pk).exists())


class TestProductHistoryView(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_history.html'

    def setUp(self):
        super().setUp()
        self.url = reverse('product:view-history', args=[self.instance.code])


class TestProductGetImage(PermissionMixin, TestCase):
    url = reverse_lazy('product:image')

    def setUp(self):
        super().setUp()
        self.instance = ProductFactory()
        self.url = reverse("product:image", args=[self.instance.code])

    def test_valid_content_type(self):
        self.login()
        resp = self.client.get(self.url)
        content_type = resp['Content-Type']
        self.assertEqual(content_type, "image/png")


class TestProductAutocomplete(PermissionMixin, TestCase):
    url = reverse_lazy('product:product-autocomplete')

    def test_filters(self):
        self.login()
        ProductFactory(id=1, name="A1")
        ProductFactory(id=2, name="A2", company=CompanyFactory(name="PrefixB2"))
        ProductFactory(id=3, name="A3", company=CompanyFactory(official_name="B3Suffix"))
        ProductFactory(id=4, name="A4", company=CompanyFactory(common_name="PefixB4Suffix"))

        response = self.client.get("{}?q={}".format(self.url, "A1"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('1', 'A1')]))

        response = self.client.get("{}?q={}".format(self.url, "B2"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('2', 'A2')]))

        response = self.client.get("{}?q={}".format(self.url, "B3"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('3', 'A3')]))

        response = self.client.get("{}?q={}".format(self.url, "B4"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('4', 'A4')]))

    def _get_expected_result(self, elements):
        return {
            'pagination': {'more': False},
            'results': [{'text': o[1], 'selected_text': o[1], 'id': o[0]} for o in elements],
        }


class TestUrls(TestCase):
    def test_should_render_url(self):
        self.assertEqual("/cms/product/create", reverse('product:create'))
        self.assertEqual("/cms/product/create-bulk", reverse('product:create-bulk'))
        self.assertEqual("/cms/product/product-autocomplete/", reverse('product:product-autocomplete'))
        self.assertEqual("/cms/product/123/image", reverse('product:image', args=[123]))
        self.assertEqual("/cms/product/123/edit", reverse('product:edit', args=[123]))
        self.assertEqual("/cms/product/123/delete", reverse('product:delete', args=[123]))
        self.assertEqual("/cms/product/123/history", reverse('product:view-history', args=[123]))
        self.assertEqual("/cms/product/123/", reverse('product:detail', args=[123]))
        self.assertEqual("/cms/product/", reverse('product:list'))
