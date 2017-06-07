# -*- coding: utf-8 -*-
import random

def add_ask_for_pics(result):
    if random.choice([True, False]):
        result['ask_for_pics'] = True
        result['ask_for_pics_card_text'] = 'Naucz Polę jak wygląda ten produkt!'
        result['ask_for_pics_text'] = \
            'Pomóż nauczyć Polę rozpoznawania produktów po wyglądzie. ' \
            'Nakręć film obracając produkt w dłoni tak jak na ' \
            'przykładzie poniżej. Postaraj się nie zasłaniać produktu.'
        result['ask_for_pics_button_yes_text'] = 'Chętnię pomogę!'
        result['ask_for_pics_button_no_text'] = 'Może innym razem...'

    return result
