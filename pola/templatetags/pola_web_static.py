import json
import os
from functools import lru_cache

import jsonschema
from django import template
from django.conf import settings

register = template.Library()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
POLA_WEB_DIR = os.path.join(ROOT_DIR, "pola-web")
POLA_WEB_MANIFEST = os.path.join(POLA_WEB_DIR, "asset-manifest.json")

MANIFEST_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "files": {"type": "object", "additionalProperties": {"type": "string"}},
        "entrypoints": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["files", "entrypoints"],
}


@lru_cache(maxsize=None)
def load_manifest():
    with open(POLA_WEB_MANIFEST) as manifest_file:
        content = json.load(manifest_file)
    jsonschema.validate(content, MANIFEST_JSON_SCHEMA)
    return content


@register.simple_tag()
def pola_web_static(path: str):
    if settings.DEBUG:
        load_manifest.cache_clear()
    from django.contrib.staticfiles.storage import staticfiles_storage

    manifest = load_manifest()
    if path not in manifest['files']:
        raise Exception(f"The file cannot be found in the pola-web manifest: {path}")
    path = manifest['files'][path]
    if path.startswith('/static'):
        len_static = len('/static')
        path = path[len_static:]
    return staticfiles_storage.url(path)
