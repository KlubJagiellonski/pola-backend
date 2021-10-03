import random
import string

from test_plus.test import TestCase

from pola.s3 import create_s3_client, create_s3_resource


class TestPolaWebView(TestCase):
    def setUp(self) -> None:
        random_prefix = "".join(random.choices(list(string.ascii_lowercase), k=10))
        self.bucket_name = f"test-bucket-{random_prefix}"
        self.s3_client = create_s3_client()
        self.s3_client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self) -> None:
        bucket = create_s3_resource().Bucket(self.bucket_name)
        bucket.objects.all().delete()
        self.s3_client.delete_bucket(Bucket=self.bucket_name)

    def test_should_return_404_for_invalid_cms_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name, ENABLE_POLA_WEB_CUSTOMIZATION=True):
            response = self.client.get('/cms/invalid')
            self.assertEqual(response.status_code, 404)
            self.assertIn("<title>Nie ma takiej strony</title>", response.content.decode())
            self.assertIn("<h1>Nie ma takiej strony</h1>", response.content.decode())

    def test_should_return_404_for_invalid_normal_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name, ENABLE_POLA_WEB_CUSTOMIZATION=True):
            response = self.client.get('/invalid')
            self.assertEqual(response.status_code, 404)
            self.assertIn("<title>Nie ma takiej strony</title>", response.content.decode())
            self.assertIn("<h1>Nie ma takiej strony</h1>", response.content.decode())

    def test_should_return_404_when_404_html_exists(self):
        content = "test-404.html"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="404.html",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name, ENABLE_POLA_WEB_CUSTOMIZATION=True):
            response = self.client.get('/invalid')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(content, response.content.decode())

    def test_should_return_200_when_index_exists(self):
        content = "index.html"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="article/index.html",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name, ENABLE_POLA_WEB_CUSTOMIZATION=True):
            response = self.client.get('/article/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

    def test_should_return_200_when_file_exists(self):
        content = "test.js"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="test.js",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name, ENABLE_POLA_WEB_CUSTOMIZATION=True):
            response = self.client.get('/test.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())
