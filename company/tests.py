from django.core.urlresolvers import reverse, reverse_lazy
from test_plus.test import TestCase

from company.factories import CompanyFactory
from company.models import Company
from pola.users.factories import StaffFactory, UserFactory


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
        self.instance = CompanyFactory()

    def test_contains_official_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.instance.official_name)


class CompanyCreatelViewTestCase(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:create')
    template_name = 'company/company_form.html'


class CompanyCreateFromKRSViewTestCase(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:create_from_krs')
    template_name = 'company/company_from_krs.html'


class CompanyUpdateTestCase(InstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:edit')
    template_name = 'company/company_form.html'

    def setUp(self):
        super(CompanyUpdateTestCase, self).setUp()
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})


class CompanyDeleteViewTestCase(InstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_confirm_delete.html'

    def setUp(self):
        super(CompanyDeleteViewTestCase, self).setUp()
        self.url = reverse('company:delete', kwargs={'pk': self.instance.pk})

    def test_object_delete(self):
        self.login()
        self.client.post(self.url)
        self.assertFalse(Company.objects.filter(pk=self.instance.pk).exists())


class CompanyDetailViewTestCase(InstanceMixin, PermissionMixin, TemplateUsedMixin, TestCase):
    template_name = 'company/company_detail.html'

    def setUp(self):
        super(CompanyDetailViewTestCase, self).setUp()
        self.url = reverse('company:detail', kwargs={'pk': self.instance.pk})


class CompanyListViewTestCase(PermissionMixin, TemplateUsedMixin, TestCase):
    url = reverse_lazy('company:list')
    template_name = 'company/company_filter.html'

