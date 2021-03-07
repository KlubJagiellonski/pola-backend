import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings
from rq import Queue

from pola.rq_tasks import get_url_at_time
from pola.rq_worker import conn

q = Queue(connection=conn)


def send_ai_pics(
    product,
    device_name,
    original_width,
    original_height,
    width,
    height,
    files_count,
    file_ext,
    mime_type,
    filenames,
):

    files = []
    i = 1
    for filename in filenames:
        files.append({'title': f'{i}', 'image_url': filename.split('?')[0].encode('utf-8')})
        i += 1

    url = 'https://slack.com/api/chat.postMessage?' + urlencode(
        {
            'token': settings.SLACK_TOKEN,
            'channel': settings.SLACK_CHANNEL_AI_PICS,
            'username': 'New AI pics',
            'text': 'Product: *{}*\n'
            'Device: *{}*\n'
            'Dimensions: *{}x{}* (Original: {}x{})\n'
            '*{} {}* files ({})'.format(
                product,
                device_name,
                width,
                height,
                original_width,
                original_height,
                files_count,
                file_ext,
                mime_type,
            ),
            'attachments': json.dumps(files),
        }
    )

    # requests.get(url)
    q.enqueue(get_url_at_time, url, datetime.utcnow() + timedelta(seconds=15))


def send_ai_pics_request(product, preview_text):

    url = 'https://slack.com/api/chat.postMessage?' + urlencode(
        {
            'token': settings.SLACK_TOKEN,
            'channel': settings.SLACK_CHANNEL_AI_PICS,
            'username': 'AI pics Requested',
            'text': f"Product: *{product.encode('utf-8')}*\nPreview text: *{preview_text.encode('utf-8')}*",
        }
    )

    # requests.get(url)
    q.enqueue(get_url_at_time, url, datetime.utcnow() + timedelta(seconds=0))


def send_ai_pics_stats(msg):

    url = 'https://slack.com/api/chat.postMessage?' + urlencode(
        {
            'token': settings.SLACK_TOKEN,
            'channel': settings.SLACK_CHANNEL_AI_STATS,
            'username': 'AI Stats',
            'text': msg.encode('utf-8'),
        }
    )

    requests.get(url)
    # q.enqueue(get_url_at_time, url, datetime.utcnow()+timedelta(seconds=0))
