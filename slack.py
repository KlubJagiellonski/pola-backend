from django.conf import settings
from rq import Queue
from pola.rq_worker import conn
from pola.rq_tasks import get_url
import requests
from urllib import urlencode
import json

q = Queue(connection=conn)

def send_ai_pics(product, device_name, original_width, original_height,
                 width, height,
                 files_count, file_ext, mime_type,
                 filenames):

    files = []
    i = 1
    for filename in filenames:
        files.append({'title':'{}'.format(i), 'image_url':filename.split('?')[0]})
        i += 1

    url = 'https://slack.com/api/chat.postMessage?'+\
        urlencode({
            'token':settings.SLACK_TOKEN,
            'channel':settings.SLACK_CHANNEL_AI_PICS,
            'username':'New AI pics',
            'text':'Product: *{}*\n'
                   'Device: *{}*\n'
                   'Dimensions: *{}x{}* (Original: {}x{})\n'
                   '*{} {}* files ({})\n'
                   '{}'
                .format(product, device_name,
                        width, height,
                        original_width, original_height,
                        files_count, file_ext, mime_type,
                        files
                        ),
            'attachments': json.dumps(files)
        })

    #requests.get(url)
    q.enqueue(get_url, url)
