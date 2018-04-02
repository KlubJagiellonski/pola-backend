# -*- coding: utf-8 -*-
import random

QUERY_COUNT_THRESHOLD = 1000
DESIRED_AI_PICS_COUNT = 2000

preview_texts = [
    u'Naucz Polę tego produktu',
    u'Pomóż Poli stać się lepszą',
    u'Pola potrzebuje Twojej pomocy',
    u'Pola pomaga. Pomóż Poli',
    u'Poświęć Poli 10 sekund',
    u'Naciśnij aby pomóc Poli',
    u'Pola Cię potrzebuje',
    u'Co Ty możesz zrobić dla Poli?',
    u'Rozwijaj z nami Polę!',
]


def add_ask_for_pics(product, result):
    if product and product.name and product.company \
            and 'plScore' in result and result['plScore']\
            and product.company.query_count > QUERY_COUNT_THRESHOLD\
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

    return result
