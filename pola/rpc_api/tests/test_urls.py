from django.urls import reverse
from test_plus import TestCase


class TestApiUrls(TestCase):
    def test_should_render(self):
        self.assertEqual("/a/v3/add_ai_pics", reverse("api:add_ai_pics"))
        # API v3
        self.assertEqual("/a/v3/get_by_code", reverse("api:get_by_code_v3"))
        self.assertEqual("/a/v3/create_report", reverse("api:create_report_v3"))
        self.assertEqual("/a/v3/update_report", reverse("api:update_report_v3"))
        # API v2
        self.assertEqual("/a/v2/get_by_code", reverse("api:get_by_code_v2"))
        self.assertEqual("/a/v2/create_report", reverse("api:create_report_v2"))
        self.assertEqual("/a/v2/update_report", reverse("api:update_report_v2"))
        self.assertEqual("/a/v2/attach_file", reverse("api:attach_file_v2"))
