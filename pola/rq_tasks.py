import time
from datetime import datetime

import requests


def get_url(url):
    requests.get(url)


def get_url_at_time(url, at_time):
    while at_time > datetime.utcnow():
        time.sleep(1)

    requests.get(url)
