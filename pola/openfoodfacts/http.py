import shutil
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

USER_AGENT = 'pola-backend-openfoodfacts/1.0'
DOWNLOAD_ATTEMPTS = 8


@dataclass(frozen=True)
class RemoteFile:
    size: int | None
    etag: str | None


def fetch_bytes(url: str, dest: Path, *, resume: bool = True) -> None:
    if not resume and dest.exists():
        dest.unlink()
    remote = remote_file(url) if resume else RemoteFile(size=None, etag=None)
    if resume and _local_file_is_complete(dest, remote):
        _store_etag(dest, remote.etag)
        print(f'Keeping downloaded file {dest} ({dest.stat().st_size} bytes)', flush=True)
        return
    if resume and _remote_file_changed(dest, remote):
        dest.unlink(missing_ok=True)
        _etag_path(dest).unlink(missing_ok=True)
    for attempt in range(1, DOWNLOAD_ATTEMPTS + 1):
        try:
            _fetch_once(url, dest)
            _store_etag(dest, remote.etag)
            return
        except (TimeoutError, urllib.error.URLError, OSError):
            if attempt == DOWNLOAD_ATTEMPTS:
                raise
            time.sleep(min(5 * attempt, 30))


def _fetch_once(url: str, dest: Path) -> None:
    existing = dest.stat().st_size if dest.exists() else 0
    headers = {'User-Agent': USER_AGENT}
    if existing:
        headers['Range'] = f'bytes={existing}-'
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as exc:
        if exc.code == 416 and existing:
            return
        raise
    with response:
        status = response.getcode()
        mode = 'ab' if status == 206 else 'wb'
        with dest.open(mode) as handle:
            shutil.copyfileobj(response, handle)


def remote_file(url: str) -> RemoteFile:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Range': 'bytes=0-0'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            size = _total_size(response.headers)
            if size is None and response.getcode() == 200:
                length = response.headers.get('Content-Length')
                if length and length.isdigit():
                    size = int(length)
            if response.getcode() == 206:
                response.read(1)
            return RemoteFile(size=size, etag=_etag(response.headers))
    except (TimeoutError, urllib.error.URLError, OSError):
        return RemoteFile(size=None, etag=None)


def _local_file_is_complete(path: Path, remote: RemoteFile) -> bool:
    if remote.size is None or remote.size == 0 or not path.is_file():
        return False
    if path.stat().st_size != remote.size:
        return False
    saved = _stored_etag(path)
    return remote.etag is None or saved is None or saved == remote.etag


def _remote_file_changed(path: Path, remote: RemoteFile) -> bool:
    if not path.is_file():
        return False
    local_size = path.stat().st_size
    if remote.size is not None and local_size > remote.size:
        return True
    if remote.etag is None:
        return False
    saved = _stored_etag(path)
    return saved is not None and saved != remote.etag


def _etag_path(path: Path) -> Path:
    return path.with_name(path.name + '.etag')


def _stored_etag(path: Path) -> str | None:
    etag_path = _etag_path(path)
    if not etag_path.is_file():
        return None
    text = etag_path.read_text(encoding='utf-8').strip()
    return text or None


def _store_etag(path: Path, etag: str | None) -> None:
    if etag is None:
        return
    _etag_path(path).write_text(etag + '\n', encoding='utf-8')


def _total_size(headers) -> int | None:
    content_range = headers.get('Content-Range')
    if not content_range or '/' not in content_range:
        return None
    total = content_range.rsplit('/', 1)[-1].strip()
    if total.isdigit():
        return int(total)
    return None


def _etag(headers) -> str | None:
    etag = headers.get('ETag')
    if not etag:
        return None
    return etag.strip().strip('"') or None


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode('utf-8')
