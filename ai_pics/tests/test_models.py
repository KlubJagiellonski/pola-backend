from unittest import TestCase

from parameterized import parameterized

from ai_pics.factories import AIAttachmentFactory, AIPicsFactory


class TestAIPics(TestCase):
    def test_getter_state(self):
        self.assertEqual("invalid", AIPicsFactory(is_valid=False).state)
        self.assertEqual("valid", AIPicsFactory(is_valid=True).state)
        self.assertEqual("unknown", AIPicsFactory(is_valid=None).state)

    @parameterized.expand([("invalid", False), ("valid", True), ("AAAAA", None)])
    def test_setter_state(self, current_state, current_is_valid):
        ai_pics = AIPicsFactory()
        ai_pics.state = current_state
        self.assertEqual(current_is_valid, ai_pics.is_valid)

    def test_attachment_count(self):
        ai_pics = AIPicsFactory()
        AIAttachmentFactory.create_batch(10, ai_pics=ai_pics)
        self.assertEqual(ai_pics.attachment_count(), 10)


class TestAIAttachment(TestCase):
    def test_getters(self):
        ai_attachment = AIAttachmentFactory()
        filename = ai_attachment.attachment.url.rsplit("/")[-1]
        self.assertEqual(filename, ai_attachment.filename)
        self.assertEqual(filename, str(ai_attachment))
        url = ai_attachment.get_absolute_url()
        self.assertIn("s3.amazonaws.com", url)
        self.assertIn(filename, url)
