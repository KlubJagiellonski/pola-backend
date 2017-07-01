# -*- coding: utf-8 -*-
import random

def add_ask_for_pics(result):
    if random.choice([True, False]):
        result['ask_for_pics'] = True
        result['ask_for_pics_preview'] = 'Naucz Polę tego produktu'
        result['ask_for_pics_title'] = 'Naucz Polę tego produktu'
        result['ask_for_pics_text'] = \
            'Pomóż nauczyć Polę rozpoznawania produktów po wyglądzie. ' \
            'Nakręć film obracając produkt tak jak na ' \
            'przykładzie poniżej. Postaraj się nie zasłaniać produktu.'
        result['ask_for_pics_button_start'] = 'Nakręć film'
        result['max_pic_size'] = 800

    return result
