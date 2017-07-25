import requests

def get_url(url):
    print 'get_url started'
    resp = requests.get(url)
    print 'get_url_finished'
    print resp

