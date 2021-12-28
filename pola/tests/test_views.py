import os
from unittest import mock

from django.urls import reverse_lazy
from test_plus.test import TestCase

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
