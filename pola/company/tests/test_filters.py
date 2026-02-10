from django.urls import reverse
from test_plus.test import TestCase

from pola.company.factories import CompanyFactory
from pola.users.factories import StaffFactory


class TestCompanyListFilters(TestCase):
    def setUp(self):
        super().setUp()
        self.user = StaffFactory()
        self.client.login(username=self.user.username, password='pass')
        self.url = reverse('company:list')

    def test_filter_has_official_url_true(self):
        # Companies with and without website
        with_site = CompanyFactory(official_name='WithSite', official_url='https://example.com')
        without_site_none = CompanyFactory(official_name='NoSiteNone', official_url=None)
        without_site_empty = CompanyFactory(official_name='NoSiteEmpty', official_url='')

        resp = self.client.get(self.url, {'has_official_url': 'True'})

        self.assertContains(resp, str(with_site))
        self.assertNotContains(resp, str(without_site_none))
        self.assertNotContains(resp, str(without_site_empty))

    def test_filter_has_official_url_false(self):
        with_site = CompanyFactory(official_name='WithSite', official_url='https://example.com')
        without_site_none = CompanyFactory(official_name='NoSiteNone', official_url=None)
        without_site_empty = CompanyFactory(official_name='NoSiteEmpty', official_url='')

        resp = self.client.get(self.url, {'has_official_url': 'False'})

        self.assertNotContains(resp, str(with_site))
        self.assertContains(resp, str(without_site_none))
        self.assertContains(resp, str(without_site_empty))

    def test_filter_has_logotype_true(self):
        # Company with logo
        logo_company = CompanyFactory(official_name='HasLogo')
        # Set the file name directly to avoid storage I/O in tests
        logo_company.logotype = 'company-logotype/2024/01/01/logo.png'
        logo_company.save()

        # Companies without logo (None and empty string)
        no_logo_none = CompanyFactory(official_name='NoLogoNone')
        no_logo_empty = CompanyFactory(official_name='NoLogoEmpty')
        no_logo_empty.logotype = ''
        no_logo_empty.save()

        resp = self.client.get(self.url, {'has_logotype': 'True'})

        self.assertContains(resp, str(logo_company))
        self.assertNotContains(resp, str(no_logo_none))
        self.assertNotContains(resp, str(no_logo_empty))

    def test_filter_has_logotype_false(self):
        logo_company = CompanyFactory(official_name='HasLogo')
        logo_company.logotype = 'company-logotype/2024/01/01/logo.png'
        logo_company.save()

        no_logo_none = CompanyFactory(official_name='NoLogoNone')
        no_logo_empty = CompanyFactory(official_name='NoLogoEmpty')
        no_logo_empty.logotype = ''
        no_logo_empty.save()

        resp = self.client.get(self.url, {'has_logotype': 'False'})

        self.assertNotContains(resp, str(logo_company))
        self.assertContains(resp, str(no_logo_none))
        self.assertContains(resp, str(no_logo_empty))
