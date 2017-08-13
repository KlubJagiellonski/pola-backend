from django.core.urlresolvers import reverse_lazy
from test_plus.test import TestCase

from pola.users.factories import StaffFactory


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
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class HomeTestCase(TemplateUsedMixin, TestCase):
    url = reverse_lazy('home')
    template_name = 'index.html'


class SelectLangTestCase(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('select_lang')
    template_name = 'pages/lang-cms.html'

    def test_template_used(self):
        self.login()
        super(SelectLangTestCase, self).test_template_used()


class AboutTestCase(TemplateUsedMixin, TestCase):
    url = reverse_lazy('about')
    template_name = 'pages/about.html'


class FaviconsTestCase(TestCase):
    def test_redirect_happens(self):
        from config.urls import FAVICON_FILES
        for filename in FAVICON_FILES:
            resp = self.client.get('/' + filename, follow=False)
            self.assertEqual(resp.status_code, 301, "Invalid redirect status code")
