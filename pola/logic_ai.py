import random

QUERY_COUNT_THRESHOLD = 1000
DESIRED_AI_PICS_COUNT = 2000

preview_texts = [
    'Naucz Polę tego produktu',
    'Pomóż Poli stać się lepszą',
    'Pola potrzebuje Twojej pomocy',
    'Pola pomaga. Pomóż Poli',
    'Poświęć Poli 10 sekund',
    'Naciśnij aby pomóc Poli',
    'Pola Cię potrzebuje',
    'Co Ty możesz zrobić dla Poli?',
    'Rozwijaj z nami Polę!',
]

ENABLE_AI_PICS_REQUEST = False


def add_ask_for_pics(product, result):
    if not ENABLE_AI_PICS_REQUEST:
        return result

    if (
        product
        and product.name
        and product.company
        and 'plScore' in result
        and result['plScore']
        and product.company.query_count > QUERY_COUNT_THRESHOLD
        and random.randint(0, DESIRED_AI_PICS_COUNT) > product.ai_pics_count
    ):

        ai = result['ai'] = {}
        ai['ask_for_pics'] = True
        ai['ask_for_pics_preview'] = random.choice(preview_texts)
        ai['ask_for_pics_title'] = 'Naucz Polę tego produktu'
        ai['ask_for_pics_text'] = (
            'Pomóż nauczyć Polę rozpoznawania produktów po wyglądzie. '
            'Nakręć film obracając produkt tak jak na '
            'przykładzie poniżej. Postaraj się nie zasłaniać produktu.'
        )
        ai['ask_for_pics_product'] = f'Uczysz Polę produktu: {product.name}'
        ai['ask_for_pics_button_start'] = 'Nakręć film'
        ai['max_pic_size'] = 800

    return result
