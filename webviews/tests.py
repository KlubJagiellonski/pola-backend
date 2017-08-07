from django.core.urlresolvers import reverse_lazy
from test_plus.test import TestCase


class TemplateUsedMixin(object):
    def test_template_used(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class WebViewsAboutTestCase(TemplateUsedMixin, TestCase):
    template_name = 'about.html'
    url = reverse_lazy('webviews:about')


class WebViewsMethodTestCase(TemplateUsedMixin, TestCase):
    template_name = 'method.html'
    url = reverse_lazy('webviews:method')


class WebViewsKjTestCase(TemplateUsedMixin, TestCase):
    template_name = 'kj.html'
    url = reverse_lazy('webviews:kj')


class WebViewsTeamTestCase(TemplateUsedMixin, TestCase):
    template_name = 'team.html'
    url = reverse_lazy('webviews:team')


class WebViewsPartnersTestCase(TemplateUsedMixin, TestCase):
    template_name = 'partners.html'
    url = reverse_lazy('webviews:partners')


