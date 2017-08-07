from django.core.urlresolvers import reverse, reverse_lazy
from test_plus.test import TestCase

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
