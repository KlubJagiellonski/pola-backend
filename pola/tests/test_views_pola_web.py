import random
import string
from contextlib import ExitStack
from http import HTTPStatus as st

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from django.utils import translation
from test_plus.test import TestCase

from pola.s3 import create_s3_client, create_s3_resource


class TestPolaWebView(TestCase):
    def setUp(self) -> None:
        random_prefix = "".join(random.choices(list(string.ascii_lowercase), k=10))
        self.bucket_name = f"test-bucket-{random_prefix}"
        self.s3_client = create_s3_client()
        self.s3_client.create_bucket(Bucket=self.bucket_name)

        self.customization_settings = ExitStack()
        self.customization_settings.enter_context(translation.override('pl'))
        self.customization_settings.__enter__()

    def tearDown(self) -> None:
        bucket = create_s3_resource().Bucket(self.bucket_name)
        bucket.objects.all().delete()
        self.s3_client.delete_bucket(Bucket=self.bucket_name)
        self.customization_settings.close()

    def test_should_return_404_for_invalid_cms_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/cms/invalid')
            self.assertEqual(response.status_code, st.NOT_FOUND)
            self.assertIn("<title>Nie ma takiej strony</title>", response.content.decode())
            self.assertIn("<h1>Nie ma takiej strony</h1>", response.content.decode())

    def test_should_return_404_for_invalid_normal_view(self):
        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/invalid')
            self.assertEqual(response.status_code, st.NOT_FOUND)
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
            self.assertEqual(response.status_code, st.NOT_FOUND)
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
            self.assertEqual(response.status_code, st.OK)
            self.assertEqual(content, response.content.decode())

    def test_should_redirect_to_home_cms_when_app_starts(self):
        user = get_user_model().objects.create_user(username="pola", password="pass123")
        self.client.force_login(user)
        response = self.client.get(reverse('index'), follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('home-cms'),
            status_code=st.MOVED_PERMANENTLY,
            target_status_code=st.OK,
        )

    def test_should_return_200_when_file_exists(self):
        content = "test.js"
        self.s3_client.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key="test.js",
        )

        with self.settings(AWS_STORAGE_WEB_BUCKET_NAME=self.bucket_name):
            response = self.client.get('/test.js')
            self.assertEqual(response.status_code, st.OK)
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
            self.assertEqual(response.status_code, st.OK)
            self.assertEqual(content, response.content.decode())

            valid_etag = response.headers['ETag']
            invalid_etag = response.headers['ETag'] + "2"
            for method, header_name, etag, expected_code, expected_content in (
                ('get', 'HTTP_IF_NONE_MATCH', valid_etag, st.NOT_MODIFIED, ''),
                ('head', 'HTTP_IF_NONE_MATCH', valid_etag, st.NOT_MODIFIED, ''),
                ('get', 'HTTP_IF_MATCH', valid_etag, st.OK, content),
                ('head', 'HTTP_IF_MATCH', valid_etag, st.OK, ''),
                ('get', 'HTTP_IF_NONE_MATCH', invalid_etag, st.OK, content),
                ('head', 'HTTP_IF_NONE_MATCH', invalid_etag, st.OK, ''),
                ('get', 'HTTP_IF_MATCH', invalid_etag, st.OK, content),
                ('head', 'HTTP_IF_MATCH', invalid_etag, st.OK, ''),
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
            self.assertEqual(response.status_code, st.OK)
            self.assertEqual(content, response.content.decode())

            response = self.client.get('/test.js', **{'HTTP_IF_MODIFIED_SINCE': response.headers['Last-Modified']})
            self.assertEqual(response.status_code, st.NOT_MODIFIED)
            self.assertEqual('', response.content.decode())

            response = self.client.head('/test.js', **{'HTTP_IF_MODIFIED_SINCE': response.headers['Last-Modified']})
            self.assertEqual(response.status_code, st.NOT_MODIFIED)
            self.assertEqual('', response.content.decode())
