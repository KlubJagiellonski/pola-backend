import shutil
import urllib.request
from pathlib import Path

USER_AGENT = 'pola-backend-openfoodfacts/1.0'


def fetch_bytes(url: str, dest: Path) -> None:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response, dest.open('wb') as handle:
        shutil.copyfileobj(response, handle)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode('utf-8')
