from unittest import TestCase

from django.urls import reverse


class TestWebViewsUrls(TestCase):
    def test_should_render_url(self):
        self.assertEqual("/m/about", reverse('webviews:about'))
        self.assertEqual("/m/method", reverse('webviews:method'))
        self.assertEqual("/m/kj", reverse('webviews:kj'))
        self.assertEqual("/m/team", reverse('webviews:team'))
        self.assertEqual("/m/partners", reverse('webviews:partners'))
        self.assertEqual("/m/friends", reverse('webviews:friends'))
