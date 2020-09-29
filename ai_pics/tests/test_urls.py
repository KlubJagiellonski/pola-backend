from django.urls import reverse
from test_plus import TestCase


class TestAiPicsUrls(TestCase):
    def test_should_render_urls(self):
        self.assertEqual("/cms/ai_pics/", reverse("ai_pics:list"))
        self.assertEqual("/cms/ai_pics/42", reverse("ai_pics:detail", args=[42]))
        self.assertEqual("/cms/ai_pics/api/set-api-pic-state", reverse("ai_pics:set-api-pic-state"))
        self.assertEqual("/cms/ai_pics/api/delete-api-pic", reverse("ai_pics:delete-api-pic"))
        self.assertEqual("/cms/ai_pics/api/delete-attachment", reverse("ai_pics:delete-attachment"))
