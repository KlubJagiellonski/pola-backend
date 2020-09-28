from django.urls import reverse_lazy
from test_plus.test import TestCase


class TemplateUsedMixin:
    def test_template_used(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.template_name)


class TestWebViewsAbout(TemplateUsedMixin, TestCase):
    template_name = 'about.html'
    url = reverse_lazy('webviews:about')


class TestWebViewsMethod(TemplateUsedMixin, TestCase):
    template_name = 'method.html'
    url = reverse_lazy('webviews:method')


class TestWebViewsKj(TemplateUsedMixin, TestCase):
    template_name = 'kj.html'
    url = reverse_lazy('webviews:kj')


class TestWebViewsTeam(TemplateUsedMixin, TestCase):
    template_name = 'team.html'
    url = reverse_lazy('webviews:team')


class TestWebViewsPartners(TemplateUsedMixin, TestCase):
    template_name = 'partners.html'
    url = reverse_lazy('webviews:partners')


class TestWebViewsFriends(TemplateUsedMixin, TestCase):
    template_name = 'm_friends.html'
    url = reverse_lazy('webviews:friends')
