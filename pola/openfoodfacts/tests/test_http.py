import tempfile
import unittest
import urllib.error
import urllib.request
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path
from unittest import mock

from pola.openfoodfacts.http import (
    RemoteFile,
    _fetch_once,
    _local_file_is_complete,
    _remote_file_changed,
    _store_etag,
    fetch_bytes,
    fetch_text,
    remote_file,
)

URL = 'https://example.test/file.gz'


class _Body:
    def __init__(self, payload: bytes, status: int = 200, headers: dict[str, str] | None = None) -> None:
        self._payload = payload
        self._status = status
        self.headers = headers or {}

    def getcode(self) -> int:
        return self._status

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            size = len(self._payload)
        chunk = self._payload[:size]
        self._payload = self._payload[size:]
        return chunk

    def __enter__(self) -> '_Body':
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class _Script:
    def __init__(self, events: list[object]) -> None:
        self.events = list(events)
        self.requests: list[urllib.request.Request] = []

    def __call__(self, request: urllib.request.Request, timeout: int = 60) -> _Body:
        self.requests.append(request)
        event = self.events.pop(0)
        if isinstance(event, Exception):
            raise event
        return event


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(URL, code, 'error', EmailMessage(), BytesIO(b''))


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
                fetch_bytes(URL, dest)

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
                fetch_bytes(URL, dest)

            fetch_once.assert_called_once_with(URL, dest)
            self.assertEqual(dest.read_bytes(), b'ab')

    def test_complete_remote_file_is_kept(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'abc')
            (dest.parent / 'file.gz.etag').write_text('same\n', encoding='utf-8')
            probe = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/3', 'ETag': '"same"'})
            script, _sleep = self._fetch(dest, [probe])

            self.assertEqual(len(script.requests), 1)
            self.assertEqual(dest.read_bytes(), b'abc')

    def test_resume_false_replaces_an_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'old')
            script, _sleep = self._fetch(dest, [_Body(b'new')], resume=False)

            self.assertEqual(dest.read_bytes(), b'new')
            self.assertIsNone(script.requests[0].get_header('Range'))

    def test_partial_response_appends_the_remainder(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'ab')
            probe = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/5', 'ETag': '"abc"'})
            chunk = _Body(b'cde', 206)
            script, _sleep = self._fetch(dest, [probe, chunk])

            self.assertEqual(script.requests[1].get_header('Range'), 'bytes=2-')
            self.assertEqual(dest.read_bytes(), b'abcde')
            self.assertEqual((dest.parent / 'file.gz.etag').read_text(encoding='utf-8').strip(), 'abc')

    def test_full_response_replaces_a_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'ab')
            probe = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/4', 'ETag': '"tag"'})
            body = _Body(b'wxyz', 200)
            self._fetch(dest, [probe, body])

            self.assertEqual(dest.read_bytes(), b'wxyz')

    def test_changed_remote_replaces_the_local_file(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'abcd')
            (dest.parent / 'file.gz.etag').write_text('old\n', encoding='utf-8')
            probe = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/3', 'ETag': '"new"'})
            script, _sleep = self._fetch(dest, [probe, _Body(b'xyz', 200)])

            self.assertIsNone(script.requests[1].get_header('Range'))
            self.assertEqual(dest.read_bytes(), b'xyz')
            self.assertEqual((dest.parent / 'file.gz.etag').read_text(encoding='utf-8').strip(), 'new')

    def test_probe_failure_still_downloads_the_body(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            self._fetch(dest, [urllib.error.URLError('down'), _Body(b'abc')])

            self.assertEqual(dest.read_bytes(), b'abc')

    def test_download_retries_then_succeeds(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            _script, sleep = self._fetch(dest, [urllib.error.URLError('down'), _Body(b'ok')], resume=False)

            sleep.assert_called_once()
            self.assertEqual(dest.read_bytes(), b'ok')

    def test_download_stops_after_the_last_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            script = _Script([urllib.error.URLError('down')] * 8)
            sleep = mock.Mock()
            with (
                mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script),
                mock.patch('pola.openfoodfacts.http.time.sleep', sleep),
            ):
                with self.assertRaises(urllib.error.URLError):
                    fetch_bytes(URL, dest, resume=False)

            self.assertEqual(sleep.call_count, 7)

    def _fetch(self, dest: Path, events: list[object], *, resume: bool = True) -> tuple[_Script, mock.Mock]:
        script = _Script(events)
        sleep = mock.Mock()
        with (
            mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script),
            mock.patch('pola.openfoodfacts.http.time.sleep', sleep),
        ):
            fetch_bytes(URL, dest, resume=resume)
        return script, sleep


class FetchOnceTests(unittest.TestCase):
    def test_416_on_a_partial_file_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'abc')
            script = _Script([_http_error(416)])
            with mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script):
                _fetch_once(URL, dest)

            self.assertEqual(script.requests[0].get_header('Range'), 'bytes=3-')
            self.assertEqual(dest.read_bytes(), b'abc')

    def test_416_on_an_empty_file_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            script = _Script([_http_error(416)])
            with mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script):
                with self.assertRaises(urllib.error.HTTPError):
                    _fetch_once(URL, dest)

    def test_other_http_error_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            dest.write_bytes(b'abc')
            script = _Script([_http_error(500)])
            with mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script):
                with self.assertRaises(urllib.error.HTTPError):
                    _fetch_once(URL, dest)


class RemoteFileTests(unittest.TestCase):
    def test_content_range_and_etag(self):
        body = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/9', 'ETag': '"abc"'})
        self.assertEqual(self._remote([body]), RemoteFile(size=9, etag='abc'))

    def test_content_length_when_range_is_ignored(self):
        body = _Body(b'abcd', 200, {'Content-Length': '4', 'ETag': ' "tag" '})
        self.assertEqual(self._remote([body]), RemoteFile(size=4, etag='tag'))

    def test_unusable_lengths_leave_the_size_empty(self):
        starred = _Body(b'x', 206, {'Content-Range': 'bytes 0-0/*', 'ETag': '""'})
        self.assertEqual(self._remote([starred]), RemoteFile(size=None, etag=None))
        missing = _Body(b'abcd', 200, {'Content-Range': 'bytes 0-0', 'Content-Length': 'nope'})
        self.assertEqual(self._remote([missing]), RemoteFile(size=None, etag=None))

    def test_probe_failure_returns_an_empty_description(self):
        self.assertEqual(self._remote([urllib.error.URLError('down')]), RemoteFile(size=None, etag=None))

    def _remote(self, events: list[object]) -> RemoteFile:
        script = _Script(events)
        with mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script):
            return remote_file(URL)


class LocalFileTests(unittest.TestCase):
    def test_completion_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            self.assertFalse(_local_file_is_complete(dest, RemoteFile(3, 'e')))
            dest.write_bytes(b'')
            self.assertFalse(_local_file_is_complete(dest, RemoteFile(0, 'e')))
            self.assertFalse(_local_file_is_complete(dest, RemoteFile(None, 'e')))
            dest.write_bytes(b'abc')
            self.assertFalse(_local_file_is_complete(dest, RemoteFile(2, 'e')))
            self.assertTrue(_local_file_is_complete(dest, RemoteFile(3, None)))
            self.assertTrue(_local_file_is_complete(dest, RemoteFile(3, 'e')))
            _store_etag(dest, 'e')
            self.assertTrue(_local_file_is_complete(dest, RemoteFile(3, 'e')))
            self.assertFalse(_local_file_is_complete(dest, RemoteFile(3, 'other')))
            (dest.parent / 'file.gz.etag').write_text('\n', encoding='utf-8')
            self.assertTrue(_local_file_is_complete(dest, RemoteFile(3, 'e')))

    def test_change_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            self.assertFalse(_remote_file_changed(dest, RemoteFile(3, 'e')))
            dest.write_bytes(b'abcd')
            self.assertTrue(_remote_file_changed(dest, RemoteFile(3, None)))
            dest.write_bytes(b'ab')
            self.assertFalse(_remote_file_changed(dest, RemoteFile(3, None)))
            self.assertFalse(_remote_file_changed(dest, RemoteFile(3, 'e')))
            _store_etag(dest, 'e')
            self.assertFalse(_remote_file_changed(dest, RemoteFile(3, 'e')))
            self.assertTrue(_remote_file_changed(dest, RemoteFile(3, 'other')))

    def test_store_etag_skips_a_missing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'file.gz'
            _store_etag(dest, None)
            self.assertFalse((dest.parent / 'file.gz.etag').exists())
            _store_etag(dest, 'abc')
            self.assertEqual((dest.parent / 'file.gz.etag').read_text(encoding='utf-8'), 'abc\n')


class FetchTextTests(unittest.TestCase):
    def test_fetch_text_decodes_utf8(self):
        script = _Script([_Body('mleko'.encode())])
        with mock.patch('pola.openfoodfacts.http.urllib.request.urlopen', side_effect=script):
            self.assertEqual(fetch_text(URL), 'mleko')
