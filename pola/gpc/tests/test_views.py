from django.test import override_settings
from django.urls import reverse, reverse_lazy
from django_webtest import WebTestMixin
from test_plus.test import TestCase

from pola.tests.test_views import PermissionMixin

from .. import factories


class TemplateUsedMixin:
    url = None
    template_name = None

    def test_template_used(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class InstanceMixin:
    factory = None

    def setUp(self):
        super().setUp()
        self.instance = self.factory()

    def test_contains_instance_details(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, str(self.instance))
        self.assertContains(resp, self.instance.code)


class RelatedInstanceMixin(InstanceMixin):
    related_factory = None

    def setUp(self):
        super().setUp()
        self.instance = self.factory()
        self.related_instance = self.related_factory(parent=self.instance)

    def test_contains_code(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, str(self.related_instance))
        self.assertContains(resp, self.related_instance.code)


class ListViewMixin:
    url = None
    template_name = None

    def test_empty(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, "Nic nie znaleziono")

    def test_filled(self):
        items = factories.GPCBrickFactory.create_batch(100)
        page = self.app.get(self.url, user=self.user)
        self.assertIn(items[-1].code, page)
        page2 = page.click("Następne")
        page2.click("Poprzednie")


class UpdateViewMixin:
    factory = None
    url = None

    def setUp(self):
        super().setUp()
        self.instance = self.factory(alias="test-alias")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_view(self):
        self.login()
        page = self.client.get(self.url)
        self.assertContains(page, 'test-alias')

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_success_submit(self):
        self.login()
        page = self.client.post(
            self.url,
            data={
                'alias': "new-alias",
                'action': 'Save',
            },
        )

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()

        self.assertEqual(self.instance.alias, "new-alias")


class TestGPCBrickDetailView(PermissionMixin, InstanceMixin, TestCase):
    template_name = 'gpc/gpcbrick_detail.html'
    factory = factories.GPCBrickFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:brick-detail', args=[self.instance.code])


class TestGPCBrickListView(PermissionMixin, ListViewMixin, WebTestMixin, TestCase):
    url = reverse_lazy('gpc:brick-list')
    template_name = 'gpc/gpcbrick_filter.html'
    factory = factories.GPCBrickFactory


class TestGPCBrickUpdateView(PermissionMixin, UpdateViewMixin, TestCase):
    factory = factories.GPCBrickFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:brick-edit', args=[self.instance.code])


class TestGPCClassDetailView(PermissionMixin, RelatedInstanceMixin, TestCase):
    template_name = 'gpc/gpcclass_detail.html'
    factory = factories.GPCClassFactory
    related_factory = factories.GPCBrickFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:class-detail', args=[self.instance.code])


class TestGPCClassListView(PermissionMixin, ListViewMixin, WebTestMixin, TestCase):
    url = reverse_lazy('gpc:class-list')
    template_name = 'gpc/gpcclass_filter.html'
    factory = factories.GPCClassFactory


class TestGPCClassUpdateView(PermissionMixin, UpdateViewMixin, TestCase):
    factory = factories.GPCClassFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:class-edit', args=[self.instance.code])


class TestGPCFamilyDetailView(PermissionMixin, RelatedInstanceMixin, TestCase):
    template_name = 'gpc/gpcfamily_detail.html'
    factory = factories.GPCFamilyFactory
    related_factory = factories.GPCClassFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:family-detail', args=[self.instance.code])


class TestGPCFamilyListView(PermissionMixin, ListViewMixin, WebTestMixin, TestCase):
    url = reverse_lazy('gpc:family-list')
    template_name = 'gpc/gpcfamily_filter.html'
    factory = factories.GPCFamilyFactory


class TestGPCFamilyUpdateView(PermissionMixin, UpdateViewMixin, TestCase):
    factory = factories.GPCFamilyFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:family-edit', args=[self.instance.code])


class TestGPCSegmentDetailView(PermissionMixin, RelatedInstanceMixin, TestCase):
    template_name = 'gpc/gpcsegment_detail.html'
    factory = factories.GPCSegmentFactory
    related_factory = factories.GPCFamilyFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:segment-detail', args=[self.instance.code])


class TestGPCSegmentListView(PermissionMixin, ListViewMixin, WebTestMixin, TestCase):
    url = reverse_lazy('gpc:segment-list')
    template_name = 'gpc/gpcsegment_filter.html'
    factory = factories.GPCSegmentFactory


class TestGPCSegmentUpdateView(PermissionMixin, UpdateViewMixin, TestCase):
    factory = factories.GPCSegmentFactory

    def setUp(self):
        super().setUp()
        self.url = reverse('gpc:segment-edit', args=[self.instance.code])
