import random
import string
import sys

from django.core.cache import cache
from django.test import override_settings
from django.urls import clear_url_caches
from test_plus.test import TestCase

from pola.s3 import create_s3_client, create_s3_resource


class TestPolaWebView(TestCase):
    def setUp(self) -> None:
        random_prefix = "".join(random.choices(list(string.ascii_lowercase), k=10))
        self.bucket_name = f"test-bucket-{random_prefix}"
        self.s3_client = create_s3_client()
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        self.customization_settings = override_settings(ENABLE_POLA_WEB_CUSTOMIZATION=True)
        self.customization_settings.enable()
        self._clear_url_caches()

    def _clear_url_caches(self):
        if 'pola.config.urls' in sys.modules:
            del sys.modules['pola.config.urls']
        clear_url_caches()

    def tearDown(self) -> None:
        bucket = create_s3_resource().Bucket(self.bucket_name)
        bucket.objects.all().delete()
        self.s3_client.delete_bucket(Bucket=self.bucket_name)
        self.customization_settings.disable()
        self._clear_url_caches()

    def test_should_return_404_for_invalid_cms_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/cms/invalid')
            self.assertEqual(response.status_code, 404)
            self.assertIn("<title>Nie ma takiej strony</title>", response.content.decode())
            self.assertIn("<h1>Nie ma takiej strony</h1>", response.content.decode())

    def test_should_return_404_for_invalid_normal_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
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

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
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

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/article/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

    def test_should_return_200_for_home_page(self):
        content = "index.html"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="index.html",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

    def test_should_return_200_when_file_exists(self):
        content = "test.js"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="test.js",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/test.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

    def test_should_support_caching_based_on_etag(self):
        content = "test.js"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="test.js",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/test.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

            valid_etag = response.headers['ETag']
            invalid_etag = response.headers['ETag'] + "2"
            for method, header_name, etag, expected_code, expected_content in (
                ('get', 'HTTP_IF_NONE_MATCH', valid_etag, 304, ''),
                ('head', 'HTTP_IF_NONE_MATCH', valid_etag, 304, ''),
                ('get', 'HTTP_IF_MATCH', valid_etag, 200, content),
                ('head', 'HTTP_IF_MATCH', valid_etag, 200, ''),
                ('get', 'HTTP_IF_NONE_MATCH', invalid_etag, 200, content),
                ('head', 'HTTP_IF_NONE_MATCH', invalid_etag, 200, ''),
                ('get', 'HTTP_IF_MATCH', invalid_etag, 200, content),
                ('head', 'HTTP_IF_MATCH', invalid_etag, 200, ''),
            ):
                cache.clear()
                if method == 'get':
                    response = self.client.get('/test.js', **{header_name: etag})
                elif method == 'head':
                    response = self.client.head('/test.js', **{header_name: etag})
                self.assertEqual(response.status_code, expected_code)
                self.assertEqual(expected_content, response.content.decode())

    def test_should_support_conditional_requests(self):
        content = "test.js"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="test.js",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/test.js')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(content, response.content.decode())

            response = self.client.get('/test.js', **{'HTTP_IF_MODIFIED_SINCE': response.headers['Last-Modified']})
            self.assertEqual(response.status_code, 304)
            self.assertEqual('', response.content.decode())

            response = self.client.head('/test.js', **{'HTTP_IF_MODIFIED_SINCE': response.headers['Last-Modified']})
            self.assertEqual(response.status_code, 304)
            self.assertEqual('', response.content.decode())
