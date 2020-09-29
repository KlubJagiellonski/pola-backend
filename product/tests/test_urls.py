from django.urls import reverse
from test_plus import TestCase


class TestUrls(TestCase):
    def test_should_render_url(self):
        self.assertEqual("/cms/product/create", reverse('product:create'))
        self.assertEqual("/cms/product/product-autocomplete/", reverse('product:product-autocomplete'))
        self.assertEqual("/cms/product/123/image", reverse('product:image', args=[123]))
        self.assertEqual("/cms/product/123/edit", reverse('product:edit', args=[123]))
        self.assertEqual("/cms/product/123/delete", reverse('product:delete', args=[123]))
        self.assertEqual("/cms/product/123/history", reverse('product:view-history', args=[123]))
        self.assertEqual("/cms/product/123/", reverse('product:detail', args=[123]))
        self.assertEqual("/cms/product/", reverse('product:list'))
