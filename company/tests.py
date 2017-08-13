from django.core.urlresolvers import reverse, reverse_lazy
from django.test import override_settings
from django_webtest import WebTestMixin
from mock import patch
from reversion.models import Version
from test_plus.test import TestCase

from company.factories import CompanyFactory
from company.forms import CompanyCreateFromKRSForm
from company.models import Company
from mojepanstwo_api2.krs import CompanyInfo
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
    template_name = 'company/company_form.html'

    def setUp(self):
        super(CompanyUpdateTestCase, self).setUp()
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})


class CompanyUpdateWebTestCase(WebTestMixin, TestCase):
    def setUp(self):
        super(CompanyUpdateWebTestCase, self).setUp()
        self.instance = CompanyFactory(name="company_name")
        self.url = reverse('company:edit', kwargs={'pk': self.instance.pk})
        self.user = StaffFactory()

    def test_form_success(self):
        page = self.app.get(self.url, user=self.user)
        page.form['official_name'] = "New name"
        page.form['commit_desc'] = "Commit description"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        versions = Version.objects.get_for_object(self.instance)
        self.assertEqual(versions[0].revision.comment, "Commit description")
        self.assertEqual(versions[0].revision.user, self.user)
        self.assertEqual(self.instance.official_name, "New name")

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_commit_desc_required(self):
        page = self.app.get(self.url, user=self.user)
        page.form['official_name'] = "New name"
        page = page.form.submit()

        self.assertContains(page, "This field is required.")

        page.form['commit_desc'] = "AAA"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())

    @override_settings(LANGUAGE_CODE='en-EN')
    def test_form_readonly_fields(self):
        page = self.app.get(self.url, user=self.user)
        self.assertEqual(page.form['name'].attrs['disabled'], 'true')

        page.form['name'] = "789789789"
        page.form['commit_desc'] = "Commit desc"
        page = page.form.submit()

        self.assertRedirects(page, self.instance.get_absolute_url())
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, "company_name")


class ConcurencyComapnyUpdateTestCase(TestCase):
    user_factory = UserFactory

    def setUp(self):
        super(ConcurencyComapnyUpdateTestCase, self).setUp()
        self.instance = CompanyFactory()

    def test_restrictions(self):
        user1 = self.make_user('u1')
        user2 = self.make_user('u2')
        url = reverse('company:edit', kwargs={'pk': self.instance.pk})

        with self.login(username=user1.username):
            response = self.get(url)
            self.response_200(response)

        with self.login(username=user2.username):
            response = self.get(url)
            self.response_302(response)


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


class CompanyCreateFromKRSFormTestCase(TestCase):

    @patch('mojepanstwo_api2.krs.Krs.get_companies')
    def test_existings_compnay_in_db(self, mock_tool):
        CompanyFactory(nip=123)
        mock_tool.return_value = [self._get_mock()]
        data = {'is_krs' : '1', 'no': 123}
        form = CompanyCreateFromKRSForm(data=data)
        self.assertFalse(form.is_valid())

    @patch('mojepanstwo_api2.krs.Krs.get_companies')
    def test_multiple_company(self, mock_tool):
        mock_tool.return_value = [
            self._get_mock(),
            self._get_mock(),
        ]
        data = {'is_krs' : '1', 'no': 123}
        form = CompanyCreateFromKRSForm(data=data)
        self.assertFalse(form.is_valid())

    @patch('mojepanstwo_api2.krs.Krs.get_companies')
    def test_no_company_in_remote_api(self, mock_tool):
        mock_tool.return_value = []
        data = {'is_krs' : '1', 'no': 123}
        form = CompanyCreateFromKRSForm(data=data)
        self.assertFalse(form.is_valid())

    @patch('mojepanstwo_api2.krs.Krs.get_companies')
    def test_success(self, mock_tool):
        mock_tool.return_value = [self._get_mock()]
        data = {'is_krs' : '1', 'no': 123}
        form = CompanyCreateFromKRSForm(data=data)
        self.assertTrue(form.is_valid())

    @patch('mojepanstwo_api2.krs.Krs.get_companies')
    def test_success_by_nip(self, mock_tool):
        mock_tool.return_value = [self._get_mock()]
        data = {'is_krs' : '0', 'no': 123}
        form = CompanyCreateFromKRSForm(data=data)
        self.assertTrue(form.is_valid())

    def _get_mock(self):
        data = {
            "id": 1,
            "nazwa": "AA",
            "nazwa_skrocona": "BB",
            "nip": "123",
            "adres": "AAAA",
            "liczba_wspolnikow": 3,
            "score": "333",
            "url": ""
        }
        return CompanyInfo(**data)


class CompanyAutocomplete(PermissionMixin, TestCase):
    url = reverse_lazy('company:company-autocomplete')
