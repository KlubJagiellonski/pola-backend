import textwrap

from django.test import override_settings
from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from parameterized import parameterized
from reversion.models import Version
from test_plus.test import TestCase

from company.factories import CompanyFactory
from pola.tests.test_views import PermissionMixin
from product.factories import ProductFactory
from product.forms import AddBulkProductForm
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


class TestProductUpdateWeb(PermissionMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.instance = ProductFactory(code="123")
        self.company = CompanyFactory()
        self.url = reverse('product:edit', args=[self.instance.code])

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_view(self):
        self.login()
        page = self.client.get(self.url)
        self.assertContains(page, 'commit_desc')
        self.assertContains(page, 'name')

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_success_submit(self):
        self.login()
        page = self.client.post(
            self.url,
            data={
                'code': self.instance.code,
                'name': "New name",
                'company': self.company.pk,
                'commit_desc': "Commit description",
                'action': 'Save',
            },
        )

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()

        versions = Version.objects.get_for_object(self.instance)
        self.assertEqual(versions[0].revision.comment, "Commit description")
        self.assertEqual(versions[0].revision.user, self.user)
        self.assertEqual(self.instance.name, "New name")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_commit_desc_required(self):
        self.login()
        page = self.client.post(
            self.url,
            data={
                'code': self.instance.code,
                'name': "New name",
                'company': self.company.pk,
                'commit_desc': "",
                'action': 'Save',
            },
        )

        self.assertContains(page, "This field is required.")


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

        response = self.client.get(f"{self.url}?q=A1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('1', 'A1')]))

        response = self.client.get(f"{self.url}?q=B2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('2', 'A2')]))

        response = self.client.get(f"{self.url}?q=B3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('3', 'A3')]))

        response = self.client.get(f"{self.url}?q=B4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self._get_expected_result([('4', 'A4')]))

    def _get_expected_result(self, elements):
        return {
            'pagination': {'more': False},
            'results': [{'text': o[1], 'selected_text': o[1], 'id': o[0]} for o in elements],
        }


class TestProductBulkCreate(PermissionMixin, WebTestMixin, TestCase):
    url = reverse_lazy('product:create-bulk')

    def setUp(self):
        super().setUp()
        self.company = CompanyFactory()

    def test_display_form_on_get(self):
        self.login()
        page = self.client.get(self.url, user=self.user)
        self.assertIsInstance(page.context['form'], AddBulkProductForm)
        self.assertIn('<form  class="form-horizontal"', page.rendered_content)

    def test_display_should_save_new_product(self):
        self.login()
        page = self.client.post(
            self.url,
            user=self.user,
            data={'company': self.company.pk, 'rows': "name\tcode\nP1\t123\nP2\t456"},
            follow=True,
        )
        messages = list(page.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertTrue(Product.objects.filter(company__id=self.company.pk, name="P1", code=123).exists())
        self.assertTrue(Product.objects.filter(company__id=self.company.pk, name="P2", code=456).exists())
        self.assertEqual(messages[0].message, 'Zapisano 2 produktów,\n')

    def test_display_should_dont_update_duplicates(self):
        self.login()
        p = Product(name="P1", code=123, company=self.company)
        p.save()
        self.client.post(self.url, user=self.user, data={'company': self.company.pk, 'rows': "name\tcode\nXXXXX\t123"})
        self.assertTrue(Product.objects.filter(company__id=self.company.pk, name="P1", code=123).exists())

    @parameterized.expand(
        [
            ("\nXXXXX\t123", ['Następujące kolumny są wymagane: code, name. Aktualne kolumny: []']),
            (
                "coOOde\tname\n123\tAA",
                ["Następujące kolumny są wymagane: code, name. Aktualne kolumny: ['coOOde', 'name']"],
            ),
            (
                "name\tcode\n\t123\nP2\t456",
                ["Nieprawidlowe wiersz - Linia 2 - Puste kolumny: {'name': '', 'code': '123'}"],
            ),
            (
                "name\tcode\n\t123\nP2\t",
                [
                    "Nieprawidlowe wiersz - Linia 2 - Puste kolumny: {'name': '', 'code': '123'}",
                    "Nieprawidlowe wiersz - Linia 3 - Puste kolumny: {'name': 'P2', 'code': ''}",
                ],
            ),
            (
                textwrap.dedent(
                    """\
                    code,name
                    5903548005092DDD,Amarantus ekspandowany BIO
                    """,
                ),
                [
                    "Nieprawidlowe wiersz - Linia 2 - Kod musi zawierać tylko cyfry: {'code': '5903548005092DDD', "
                    "'name': 'Amarantus ekspandowany BIO'}"
                ],
            ),
        ]
    )
    def test_malformed_csv_file(self, current_input, expected_rows_errors):
        self.login()
        Product(name="P1", code=123).save()
        page = self.client.post(self.url, user=self.user, data={'company': self.company.pk, 'rows': current_input})
        self.assertEqual(page.context['form'].errors['rows'], expected_rows_errors)

    def test_duplicate_code(self):
        self.login()
        p = Product(name="P1", code=123, company=self.company)
        p.save()

        response = self.client.post(
            self.url, user=self.user, data={'company': self.company.pk, 'rows': "name\tcode\nP1\t123"}, follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].message, 'Nie udało się zapisać 1 produktów.\nNiepowodzenia: P1 (123)')

    def test_unknown_company(self):
        self.login()
        Product(name="P1", code=123).save()
        response = self.client.post(
            self.url, user=self.user, data={'company': self.company.pk, 'rows': "name\tcode\nP1\t123"}, follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].message, 'Zapisano 1 produktów,\n')

    def test_unknown_name(self):
        self.login()
        Product(name=None, code=123).save()
        response = self.client.post(
            self.url, user=self.user, data={'company': self.company.pk, 'rows': "name\tcode\nP1\t123"}, follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].message, 'Zapisano 1 produktów,\n')

    def test_unknown_company_and_name(self):
        self.login()
        Product(name=None, code=123).save()
        response = self.client.post(
            self.url, user=self.user, data={'company': self.company.pk, 'rows': "name\tcode\nP1\t123"}, follow=True
        )
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual(messages[0].message, 'Zapisano 1 produktów,\n')


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
