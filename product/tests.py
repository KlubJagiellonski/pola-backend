from django.core.urlresolvers import reverse, reverse_lazy
from django.test import override_settings
from django_webtest import WebTestMixin
from reversion.models import Version
from test_plus.test import TestCase

from company.factories import CompanyFactory
from pola.users.factories import StaffFactory
from product.factories import ProductFactory


class PermissionMixin(object):
    def setUp(self):
        super(PermissionMixin, self).setUp()
        self.user = StaffFactory()

    def login(self, username=None):
        self.client.login(username=username or self.user.username, password='pass')

    def test_anonymous_denied(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)


class TemplateUsedMixin(object):
    def test_template_used(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class InstanceMixin(object):
    def setUp(self):
        super(InstanceMixin, self).setUp()
        self.instance = ProductFactory()

    def test_contains_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.instance.name)


class ProductCreateTestCase(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('product:create')
    template_name = 'product/product_form.html'


class ProductGetImageTestCase(PermissionMixin, TestCase):
    url = reverse_lazy('product:image')

    def setUp(self):
        super(ProductGetImageTestCase, self).setUp()
        self.instance = ProductFactory()
        self.url = reverse("product:image", args=[self.instance.code])

    def test_valid_content_type(self):
        self.login()
        resp = self.client.get(self.url)
        content_type = resp['Content-Type']
        self.assertEqual(content_type, "image/png")


class ProductUpdateTestCase(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_update_form.html'

    def setUp(self):
        super(ProductUpdateTestCase, self).setUp()
        self.url = reverse('product:edit', args=[self.instance.code])


class ProductUpdateWebTestCase(WebTestMixin, TestCase):
    def setUp(self):
        super(ProductUpdateWebTestCase, self).setUp()
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

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_readonly_fields(self):
        page = self.app.get(self.url, user=self.user)
        self.assertEqual(page.form['code'].attrs['disabled'], 'true')

        page.form['code'] = "789789789"
        page.form['commit_desc'] = "Commit desc"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.code, "123")


class ProductHistoryViewTestCase(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_history.html'

    def setUp(self):
        super(ProductHistoryViewTestCase, self).setUp()
        self.url = reverse('product:view-history', args=[self.instance.code])


class ProductDetailViewTestCase(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'product/product_detail.html'

    def setUp(self):
        super(ProductDetailViewTestCase, self).setUp()
        self.url = reverse('product:detail', args=[self.instance.code])


class ProductListViewTestCase(PermissionMixin, InstanceMixin, TestCase):
    url = reverse_lazy('product:list')
    template_name = 'product/product_filter.html'


class ProductAutocompleteTestCase(PermissionMixin, TestCase):
    url = reverse_lazy('product:product-autocomplete')

    def test_filters(self):
        self.login()
        ProductFactory(id=1, name="A1")
        ProductFactory(id=2, name="A2", company=CompanyFactory(name="PrefixB2"))
        ProductFactory(id=3, name="A3", company=CompanyFactory(official_name="B3Suffix"))
        ProductFactory(id=4, name="A4", company=CompanyFactory(common_name="PefixB4Suffix"))

        response = self.client.get("%s?q=%s" % (self.url, "A1"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self._get_expected_result([('1', 'A1')])
        )

        response = self.client.get("%s?q=%s" % (self.url, "B2"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self._get_expected_result([('2', 'A2')])
        )

        response = self.client.get("%s?q=%s" % (self.url, "B3"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self._get_expected_result([('3', 'A3')])
        )

        response = self.client.get("%s?q=%s" % (self.url, "B4"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self._get_expected_result([('4', 'A4')])
        )

    def _get_expected_result(self, elements):
        return {
            'pagination':
                {'more': False},
            'results':
                [{'text': o[1], 'id': o[0]} for o in elements]
        }
