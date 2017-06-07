import random

def add_ask_for_pics(result):
    if random.choice([True, False]):
        result['ask_for_pics']=True
        result['ask_for_pics_text']='Text'

    return result
