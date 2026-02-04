import functools
import hashlib
import http.server
import os
import threading
from urllib.parse import urlparse
from datetime import datetime, timezone
from datetime import timedelta

from django.conf import settings
from google.api_core import exceptions as gcs_exceptions
from google.cloud import storage

USE_GCS_STORAGE = getattr(settings, "USE_GCS_STORAGE", True)


if USE_GCS_STORAGE:

    @functools.cache
    def get_storage_client():
        return storage.Client()

    @functools.cache
    def get_bucket(bucket_name):
        return get_storage_client().bucket(bucket_name)

else:

    class LocalBlob:
        def __init__(self, bucket, name, data=None, content_type=None, path=None):
            self.bucket = bucket
            self.name = name
            self._data = data
            self._path = path
            self.content_type = content_type
            self.updated = None
            self.etag = None
            self._sync_metadata()

        def _sync_metadata(self):
            if self._path and os.path.exists(self._path):
                stat = os.stat(self._path)
                self.updated = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                with open(self._path, "rb") as handle:
                    data = handle.read()
                self.etag = hashlib.md5(data).hexdigest()
            elif self._data is not None:
                self.updated = datetime.now(tz=timezone.utc)
                self.etag = hashlib.md5(self._data).hexdigest()

        def reload(self):
            if self.bucket._get_blob_record(self.name) is None:
                raise gcs_exceptions.NotFound("Local GCS blob not found")
            self._sync_metadata()

        def delete(self):
            self.bucket._delete_blob(self.name)

        def download_as_bytes(self):
            record = self.bucket._get_blob_record(self.name)
            if record is None:
                raise gcs_exceptions.NotFound("Local GCS blob not found")
            if record["path"]:
                with open(record["path"], "rb") as handle:
                    return handle.read()
            return record["data"]

        def upload_from_string(self, content, content_type=None):
            if isinstance(content, str):
                content = content.encode()
            self.bucket._store_blob(self.name, content, content_type)
            record = self.bucket._get_blob_record(self.name)
            self._data = record["data"]
            self._path = record["path"]
            self.content_type = record["content_type"]
            self._sync_metadata()

        def generate_signed_url(self, *args, **kwargs):
            return f"{settings.GCS_PUBLIC_BASE_URL}/{self.bucket.name}/{self.name}"

    class LocalBucket:
        def __init__(self, name):
            self.name = name
            self._blobs = {}

        def _media_paths(self):
            if self.name not in {
                settings.GCS_AI_PICS_BUCKET_NAME,
                settings.GCS_BACKEND_BUCKET_NAME,
                settings.GCS_COMPANY_LOGOTYPE_BUCKET_NAME,
            }:
                return []
            media_root = settings.MEDIA_ROOT
            file_paths = []
            for root, _, files in os.walk(media_root):
                for filename in files:
                    file_paths.append(os.path.join(root, filename))
            return file_paths

        def _path_to_blob_name(self, path):
            return os.path.relpath(path, settings.MEDIA_ROOT).replace(os.sep, "/")

        def _get_blob_record(self, name):
            if name in self._blobs:
                return self._blobs[name]
            for path in self._media_paths():
                if self._path_to_blob_name(path) == name:
                    return {"data": None, "content_type": None, "path": path}
            return None

        def _store_blob(self, name, data, content_type):
            self._blobs[name] = {"data": data, "content_type": content_type, "path": None}

        def _delete_blob(self, name):
            if name in self._blobs:
                del self._blobs[name]
                return
            record = self._get_blob_record(name)
            if record and record["path"] and os.path.exists(record["path"]):
                os.remove(record["path"])

        def blob(self, name):
            return LocalBlob(self, name)

        def get_blob(self, name):
            record = self._get_blob_record(name)
            if record is None:
                return None
            return LocalBlob(self, name, data=record["data"], content_type=record["content_type"], path=record["path"])

        def list_blobs(self):
            names = set(self._blobs.keys())
            for path in self._media_paths():
                names.add(self._path_to_blob_name(path))
            for name in sorted(names):
                record = self._get_blob_record(name)
                if record:
                    yield LocalBlob(
                        self, name, data=record["data"], content_type=record["content_type"], path=record["path"]
                    )

        def delete(self):
            self._blobs.clear()

    class LocalStorageClient:
        def __init__(self):
            self._buckets = {}

        def bucket(self, name):
            if name not in self._buckets:
                self._buckets[name] = LocalBucket(name)
            return self._buckets[name]

        def create_bucket(self, bucket):
            self._buckets[bucket.name] = bucket
            return bucket

    @functools.cache
    def get_storage_client():
        return LocalStorageClient()

    @functools.cache
    def get_bucket(bucket_name):
        return get_storage_client().bucket(bucket_name)

    _local_server_lock = threading.Lock()
    _local_server = {"thread": None, "server": None}

    def _ensure_local_upload_server():
        parsed = urlparse(settings.GCS_PUBLIC_BASE_URL)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
            return None
        port = parsed.port or 80
        with _local_server_lock:
            if _local_server["server"] and _local_server["server"].server_port == port:
                return port

            class LocalUploadHandler(http.server.BaseHTTPRequestHandler):
                def do_PUT(self):
                    content_length = int(self.headers.get("Content-Length", "0"))
                    if content_length:
                        _ = self.rfile.read(content_length)
                    self.send_response(200)
                    self.end_headers()

                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()

                def do_HEAD(self):
                    self.send_response(200)
                    self.end_headers()

                def log_message(self, format, *args):
                    return

            class ReusableHTTPServer(http.server.HTTPServer):
                allow_reuse_address = True

            try:
                server = ReusableHTTPServer((parsed.hostname, port), LocalUploadHandler)
            except OSError:
                return port

            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            _local_server["server"] = server
            _local_server["thread"] = thread
        return port


def fetch_blob(bucket_name, blob_name):
    blob = get_bucket(bucket_name).blob(blob_name)
    try:
        blob.reload()
    except gcs_exceptions.NotFound:
        return None
    return blob


def generate_signed_upload_url(bucket_name, object_name, content_type, expiration=timedelta(days=1)):
    if not USE_GCS_STORAGE:
        _ensure_local_upload_server()
    blob = get_bucket(bucket_name).blob(object_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT",
        content_type=content_type,
    )
