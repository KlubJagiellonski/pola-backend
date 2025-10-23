from django.test import TestCase
from django.urls import reverse


class TestHome(TestCase):
    def test_should_render_urls(self):
        self.assertEqual("/", reverse("index"))
        self.assertEqual("/cms/", reverse("home-cms"))
        self.assertEqual("/cms/stats", reverse("home-stats"))
        self.assertEqual("/cms/editors-stats", reverse("home-editors-stats"))
        self.assertEqual("/cms/admin-stats", reverse("home-admin-stats"))
        self.assertEqual("/cms/lang/", reverse("select_lang"))
