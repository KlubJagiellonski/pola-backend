import os
from unittest import mock

from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from test_plus.test import TestCase

from pola.models import AppConfiguration
from pola.users.factories import StaffFactory


class PermissionMixin:
    def setUp(self):
        super().setUp()
        self.user = StaffFactory()

    def login(self, username=None):
        self.client.login(username=username or self.user.username, password='pass')

    def test_anonymous_denied(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)


class TemplateUsedMixin:
    def test_template_used(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class TestFrontPageView(TemplateUsedMixin, PermissionMixin, TestCase):
    url = reverse_lazy('home-cms')
    template_name = 'pages/home-cms.html'

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestStatsPageView(TemplateUsedMixin, PermissionMixin, TestCase):
    url = reverse_lazy('home-stats')
    template_name = 'pages/home-stats.html'

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestEditorsStatsPageView(TemplateUsedMixin, PermissionMixin, TestCase):
    url = reverse_lazy('home-editors-stats')
    template_name = 'pages/home-editors-stats.html'

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestAdminStatsPageView(TemplateUsedMixin, PermissionMixin, TestCase):
    url = reverse_lazy('home-admin-stats')
    template_name = 'pages/home-admin-stats.html'

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestSelectLang(TemplateUsedMixin, PermissionMixin, TestCase):
    url = reverse_lazy('select_lang')
    template_name = 'pages/lang-cms.html'

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestReleaseView(TemplateUsedMixin, TestCase):
    url = reverse_lazy('release')
    template_name = 'pages/release-info.html'

    def test_display_unknown_release(self):
        with mock.patch.dict('os.environ', RELEASE_SHA='VALUE'):
            del os.environ['RELEASE_SHA']
            resp = self.client.get(self.url)
            self.assertContains(resp, 'Unknown')

    def test_display_known_release(self):
        with mock.patch.dict('os.environ', RELEASE_SHA='9e905684bb2cf6bdf074224e50d1c58e43740bba'):
            resp = self.client.get(self.url)
            self.assertContains(resp, '9e905684bb2cf6bdf074224e50d1c58e43740bba')
            self.assertContains(resp, 'KlubJagiellonski/pola-backend')

    def test_return_json(self):
        with mock.patch.dict('os.environ', RELEASE_SHA='9e905684bb2cf6bdf074224e50d1c58e43740bba'):
            resp = self.client.get(self.url, HTTP_CONTENT_TYPE='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['Content-Type'], 'application/json')
            self.assertEqual(list(resp.json().keys()), ['release_sha', 'release_link'])


class TestAppConfigurationUpdateView(TemplateUsedMixin, PermissionMixin, TestCase):
    template_name = 'pages/app_config_form.html'
    url = reverse_lazy('app-config')

    def test_template_used(self):
        self.login()
        super().test_template_used()


class TestAppConfigurationUpdate(WebTestMixin, TestCase):
    url = reverse_lazy('app-config')

    def setUp(self):
        super().setUp()
        self.user = StaffFactory()

    def test_form_success(self):
        page = self.app.get(self.url, user=self.user)
        page.form['donate_url'] = "http://example.com"
        page.form['donate_text'] = "DONATE-TEXT"

        page = page.form.submit(name='action')
        self.assertRedirects(page, reverse('home-cms'))
        instance = AppConfiguration.objects.first()
        self.assertEqual(instance.donate_url, "http://example.com")
        self.assertEqual(instance.donate_text, "DONATE-TEXT")
