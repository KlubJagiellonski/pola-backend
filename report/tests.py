# coding=utf-8
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.encoding import force_text
from django_webtest import WebTestMixin
from test_plus.test import TestCase

from pola.users.factories import StaffFactory, UserFactory
from report.factories import ReportFactory, ResolvedReportFactory
from report.models import Report


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
        self.instance = ReportFactory()

    def test_contains_official_name(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, force_text(self.instance))


class ReportListViewTestCase(PermissionMixin, TemplateUsedMixin, InstanceMixin, WebTestMixin, TestCase):
    url = reverse_lazy('report:list')
    template_name = 'report/report_filter.html'

    # def test_empty(self):
    #     self.login()
    #     resp = self.client.get(self.url)
    #     self.assertContains(resp, "Nie znaleziono zgłoszeń spełniających te kryteria")
    #
    def test_filled(self):
        products = ReportFactory.create_batch(100)
        page = self.app.get(self.url, user=self.user)
        self.assertTrue("1 z 5" in page)
        self.assertTrue(str(products[-1]) in page)
        page2 = page.click("Następne")
        page2.click("Poprzednie")


class ReportAdvancedListViewTestCase(PermissionMixin, TemplateUsedMixin, WebTestMixin, TestCase):
    url = reverse_lazy('report:advanced')
    template_name = 'report/report_filter_adv.html'

    def test_massive_resolve(self):
        reports = ReportFactory.create_batch(10)

        self.login()
        self.client.post(reverse('report:advanced'), {
            'report_to_resolve': map(lambda d: d.pk, reports)
        })

        self.assertEqual(len(Report.objects.only_resolved()), 10)

    def test_empty(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, "Nie znaleziono zgłoszeń spełniających te kryteria")

    def test_filled(self):
        products = ReportFactory.create_batch(100)
        page = self.app.get(self.url, user=self.user)
        # self.assertTrue("1 z 4" in str(page))
        self.assertTrue(str(products[-1]) in page)
        page2 = page.click("Następne")
        page2.click("Poprzednie")


class ReportDeleteViewTestCase(PermissionMixin, TemplateUsedMixin, InstanceMixin, TestCase):
    template_name = 'report/report_confirm_delete.html'

    def setUp(self):
        super(ReportDeleteViewTestCase, self).setUp()
        self.url = reverse('report:delete', kwargs={'pk': self.instance.pk})

    def test_resolve_action(self):
        self.login()
        self.client.post(self.url)
        self.assertFalse(Report.objects.filter(pk=self.instance.pk).exists())


class ReportDetailViewTestCase(PermissionMixin, TemplateUsedMixin, InstanceMixin, TestCase):
    template_name = 'report/report_detail.html'

    def setUp(self):
        super(ReportDetailViewTestCase, self).setUp()
        self.url = reverse('report:detail', kwargs={'pk': self.instance.pk})


class ReportResolveViewTestCase(PermissionMixin, TemplateUsedMixin, InstanceMixin, TestCase):
    template_name = 'report/report_resolve.html'

    def setUp(self):
        super(ReportResolveViewTestCase, self).setUp()
        self.url = reverse('report:resolve', kwargs={'pk': self.instance.pk})

    def test_resolve_action(self):
        self.login()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('report:detail', kwargs={'pk': self.instance.pk}))
        self.assertEqual(Report.objects.get(pk=self.instance.pk).status(), Report.RESOLVED)


class ReportQuerySetTestCase(TestCase):

    def test_only_open(self):
        self.assertTrue(Report.objects.only_open().filter(pk=ReportFactory().pk).exists())
        self.assertFalse(Report.objects.only_open().filter(pk=ResolvedReportFactory().pk).exists())

    def test_only_resolved(self):
        self.assertFalse(Report.objects.only_resolved().filter(pk=ReportFactory().pk).exists())
        self.assertTrue(Report.objects.only_resolved().filter(pk=ResolvedReportFactory().pk).exists())

    def test_resolve(self):
        user = UserFactory()

        ReportFactory.create_batch(4)
        Report.objects.resolve(user)

        self.assertEqual(Report.objects.filter(resolved_by=user).count(), 4)







