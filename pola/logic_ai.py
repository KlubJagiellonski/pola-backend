# -*- coding: utf-8 -*-
import random

QUERY_COUNT_THRESHOLD = 1000
DESIRED_AI_PICS_COUNT = 2000

def add_ask_for_pics(product, result):
    if product and product.name \
        and 'plScore' in result and result['plScore']\
        and product.query_count > QUERY_COUNT_THRESHOLD\
        and random.randint(0, DESIRED_AI_PICS_COUNT) > product.ai_pics_count:

        ai = result['ai'] = {}
        ai['ask_for_pics'] = True
        ai['ask_for_pics_preview'] = 'Naucz Polę tego produktu'
        ai['ask_for_pics_title'] = 'Naucz Polę tego produktu'
        ai['ask_for_pics_text'] = \
            'Pomóż nauczyć Polę rozpoznawania produktów po wyglądzie. ' \
            'Nakręć film obracając produkt tak jak na ' \
            'przykładzie poniżej. Postaraj się nie zasłaniać produktu.'
        ai['ask_for_pics_product'] = u'Uczysz Polę produktu: {}'.format(product.name)
        ai['ask_for_pics_button_start'] = 'Nakręć film'
        ai['max_pic_size'] = 800

    return result
