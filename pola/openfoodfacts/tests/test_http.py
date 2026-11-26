import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pola.openfoodfacts.http import RemoteFile, fetch_bytes


class FetchBytesTests(unittest.TestCase):
    def test_complete_file_is_not_downloaded_again(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'abc')
            remote = RemoteFile(size=3, etag='same')
            with (
                mock.patch('pola.openfoodfacts.http.remote_file', return_value=remote),
                mock.patch('pola.openfoodfacts.http._fetch_once', side_effect=AssertionError('downloaded')),
            ):
                fetch_bytes('https://example.test/file.gz', dest)

            self.assertEqual(dest.read_bytes(), b'abc')
            self.assertEqual((Path(directory) / 'file.gz.etag').read_text(encoding='utf-8').strip(), 'same')

    def test_partial_file_resumes(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'ab')
            remote = RemoteFile(size=3, etag='same')
            with (
                mock.patch('pola.openfoodfacts.http.remote_file', return_value=remote),
                mock.patch('pola.openfoodfacts.http._fetch_once', return_value=None) as fetch_once,
            ):
                fetch_bytes('https://example.test/file.gz', dest)

            fetch_once.assert_called_once_with('https://example.test/file.gz', dest)
            self.assertEqual(dest.read_bytes(), b'ab')
