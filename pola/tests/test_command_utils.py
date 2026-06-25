from unittest import mock

from django.test import TestCase

from pola.management.command_utils import load_s3_files_list


class TestLoadS3FilesList(TestCase):
    @mock.patch('pola.management.command_utils.create_s3_connection')
    @mock.patch('pola.management.command_utils.Bucket')
    def test_load_s3_files_list_returns_set_of_file_keys(self, mock_bucket_class, mock_create_s3_connection):
        """load_s3_files_list should return a set of all file keys from S3 bucket"""
        # Mock the S3 connection and bucket
        mock_conn = mock.Mock()
        mock_create_s3_connection.return_value = mock_conn

        # Mock S3 keys
        mock_key1 = mock.Mock()
        mock_key1.name = 'file1.txt'
        mock_key2 = mock.Mock()
        mock_key2.name = 'file2.txt'
        mock_key3 = mock.Mock()
        mock_key3.name = 'folder/file3.txt'

        mock_bucket = mock.Mock()
        mock_bucket.list.return_value = [mock_key1, mock_key2, mock_key3]
        mock_bucket_class.return_value = mock_bucket

        bucket_name = 'test-bucket'
        result = load_s3_files_list(bucket_name)

        # Verify the result
        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 3)
        self.assertIn('file1.txt', result)
        self.assertIn('file2.txt', result)
        self.assertIn('folder/file3.txt', result)

        # Verify the mocks were called correctly
        mock_create_s3_connection.assert_called_once()
        mock_bucket_class.assert_called_once_with(mock_conn, name=bucket_name)
        mock_bucket.list.assert_called_once()

    @mock.patch('pola.management.command_utils.create_s3_connection')
    @mock.patch('pola.management.command_utils.Bucket')
    def test_load_s3_files_list_returns_empty_set_for_empty_bucket(
        self, mock_bucket_class, mock_create_s3_connection
    ):
        """load_s3_files_list should return empty set when bucket is empty"""
        mock_conn = mock.Mock()
        mock_create_s3_connection.return_value = mock_conn

        mock_bucket = mock.Mock()
        mock_bucket.list.return_value = []
        mock_bucket_class.return_value = mock_bucket

        bucket_name = 'empty-bucket'
        result = load_s3_files_list(bucket_name)

        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 0)
