from django.conf import settings
from rq import Queue
from pola.rq_worker import conn
from pola.rq_tasks import get_url
import requests
from urllib import urlencode

q = Queue(connection=conn)

def send_ai_pics(product, device_name, original_width, original_height,
                 width, height,
                 files_count, file_ext, mime_type,
                 filenames):

    files = ''
    for filename in filenames:
        files += filename.split('?')[0]+'\n'

    url = 'https://slack.com/api/chat.postMessage?'+\
        urlencode({
            'token':settings.SLACK_TOKEN,
            'channel':settings.SLACK_CHANNEL_AI_PICS,
            'username':'New AI pics',
            'text':'Product: *{}*\n'
                   'Device: *{}*\n'
                   'Dimensions: *{}x{}* ({}x{})\n'
                   '*{} {}* files ({})\n'
                   '{}'
                .format(product, device_name,
                        original_width, original_height,
                        width, height,
                        files_count, file_ext, mime_type,
                        files
                        )
        })


    #requests.get(url)
    q.enqueue(get_url, url)
