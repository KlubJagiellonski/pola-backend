from django.core.urlresolvers import reverse, reverse_lazy
from mock import patch
from test_plus.test import TestCase


from mojepanstwo_api2.krs import CompanyInfo
from company.factories import CompanyFactory
from company.forms import CompanyCreateFromKRSForm
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
    def test_existings_compnay_in_db(self):
        CompanyFactory(nip=123)
        r = [
            CompanyInfo(**{
                "id": 1,
                "nazwa": "AA",
                "nazwa_skrocona": "BB",
                "nip": "123",
                "adres":"AAAA",
                "liczba_wspolnikow": 3,
                "score": "333",
                "url": ""
            })
        ]
        with patch('mojepanstwo_api2.krs.Krs.get_companies') as mock_tool:
            mock_tool.return_value = r
            data = {'is_krs' : '1', 'no': 123}
            form = CompanyCreateFromKRSForm(data=data)
            self.assertFalse(form.is_valid())

    def test_multiple_company(self):
        r = [
            CompanyInfo(**{
                "id": 1,
                "nazwa": "AA",
                "nazwa_skrocona": "BB",
                "nip": "123",
                "adres":"AAAA",
                "liczba_wspolnikow": 3,
                "score": "333",
                "url": ""
            }),
            CompanyInfo(**{
                "id": 1,
                "nazwa": "AA",
                "nazwa_skrocona": "BB",
                "nip": "321",
                "adres": "AAAA",
                "liczba_wspolnikow": 3,
                "score": "333",
                "url": ""
            }),
        ]
        with patch('mojepanstwo_api2.krs.Krs.get_companies') as mock_tool:
            mock_tool.return_value = r
            data = {'is_krs' : '1', 'no': 123}
            form = CompanyCreateFromKRSForm(data=data)
            self.assertFalse(form.is_valid())

    def test_no_company_in_remote_api(self):
        r = []
        with patch('mojepanstwo_api2.krs.Krs.get_companies') as mock_tool:
            mock_tool.return_value = r
            data = {'is_krs' : '1', 'no': 123}
            form = CompanyCreateFromKRSForm(data=data)
            self.assertFalse(form.is_valid())

    def test_success(self):
        r = [
            CompanyInfo(**{
                "id": 1,
                "nazwa": "AA",
                "nazwa_skrocona": "BB",
                "nip": "123",
                "adres":"AAAA",
                "liczba_wspolnikow": 3,
                "score": "333",
                "url": ""
            })
        ]
        with patch('mojepanstwo_api2.krs.Krs.get_companies') as mock_tool:
            mock_tool.return_value = r
            data = {'is_krs' : '1', 'no': 123}
            form = CompanyCreateFromKRSForm(data=data)
            self.assertTrue(form.is_valid())

    def test_success_by_nip(self):
        r = [
            CompanyInfo(**{
                "id": 1,
                "nazwa": "AA",
                "nazwa_skrocona": "BB",
                "nip": "123",
                "adres":"AAAA",
                "liczba_wspolnikow": 3,
                "score": "333",
                "url": ""
            })
        ]
        with patch('mojepanstwo_api2.krs.Krs.get_companies') as mock_tool:
            mock_tool.return_value = r
            data = {'is_krs' : '0', 'no': 123}
            form = CompanyCreateFromKRSForm(data=data)
            self.assertTrue(form.is_valid())
