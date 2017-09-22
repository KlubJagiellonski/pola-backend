# -*- coding: utf-8 -*-
import random
import slack

QUERY_COUNT_THRESHOLD = 1000
DESIRED_AI_PICS_COUNT = 2000

preview_texts = [
    'Naucz Polę tego produktu',
    'Pomóż Poli stać się lepszą',
    'Pola potrzebuje Twojej pomocy',
    'Pola pomaga. Pomóż Poli',
    'Poświęć Poli 10 sekund',
    'Naciśnij aby pomóc Poli',
    'Polą Cię potrzebuję',
    'Co Ty możesz zrobić dla Poli?',
    'A teraz zeskanuj całą lodówkę',
    'A teraz zeskanuj całą łazienkę',
]

def add_ask_for_pics(product, result):
    if product and product.name \
        and 'plScore' in result and result['plScore']\
        and product.query_count > QUERY_COUNT_THRESHOLD\
        and random.randint(0, DESIRED_AI_PICS_COUNT) > product.ai_pics_count:

        ai = result['ai'] = {}
        ai['ask_for_pics'] = True
        ai['ask_for_pics_preview'] = random.choice(preview_texts)
        ai['ask_for_pics_title'] = 'Naucz Polę tego produktu'
        ai['ask_for_pics_text'] = \
            'Pomóż nauczyć Polę rozpoznawania produktów po wyglądzie. ' \
            'Nakręć film obracając produkt tak jak na ' \
            'przykładzie poniżej. Postaraj się nie zasłaniać produktu.'
        ai['ask_for_pics_product'] = u'Uczysz Polę produktu: {}'.format(product.name)
        ai['ask_for_pics_button_start'] = 'Nakręć film'
        ai['max_pic_size'] = 800

        slack.send_ai_pics_request(u'{} ({})'.format(str(product), product.code),
                                   ai['ask_for_pics_preview'])

    return result
