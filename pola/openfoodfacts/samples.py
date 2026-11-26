from decimal import Decimal

from pola.openfoodfacts.models import Product

_NAMES = (
    'Jogurt naturalny',
    'Masło extra',
    'Makaron pełnoziarnisty',
    'Ryż basmati',
    'Płatki owsiane',
    'Sok jabłkowy',
    'Ketchup',
    'Musztarda',
    'Czekolada mleczna',
    'Herbatniki',
    'Tuńczyk w oleju',
    'Fasola czerwona',
    'Pomidory krojone',
    'Oliwa z oliwek',
    'Miód wielokwiatowy',
    'Kefir',
    'Twaróg chudy',
    'Szynka konserwowa',
    'Kiełbasa śląska',
    'Jabłka suszone',
)
_BRANDS = (
    ('Mlekovita', 'en:mlekovita'),
    ('Piekarnia', 'en:piekarnia'),
    ('Oatly', 'en:oatly'),
    ('Krakus', 'en:krakus'),
    ('Łowicz', 'en:lowicz'),
)
_GRADES = ('a', 'b', 'c', 'd', 'e')
_ALLERGENS = (None, 'en:milk', 'en:gluten', 'en:soybeans', 'en:nuts')


def _sample(number: int) -> dict[str, object]:
    name = _NAMES[(number - 1) % len(_NAMES)]
    brand, brand_tag = _BRANDS[(number - 1) % len(_BRANDS)]
    row: dict[str, object] = {
        'code': f'590{number:010d}',
        'product_name': f'{name} {number}',
        'brands': brand,
        'brands_tags': brand_tag,
        'quantity': f'{(number % 5) + 1}00 g',
        'countries_tags': 'en:poland',
        'nutriscore_grade': _GRADES[(number - 1) % len(_GRADES)],
        'nova_group': (number % 4) + 1,
    }
    allergen = _ALLERGENS[number % len(_ALLERGENS)]
    if allergen is not None:
        row['allergens_tags'] = allergen
    if number % 7 != 0:
        row['energy_kcal'] = Decimal(40 + (number % 50) * 7)
        row['proteins'] = Decimal(number % 20)
        row['salt'] = Decimal('0.1') * (number % 10)
    return row


SAMPLES = (
    {
        'code': '5900000000001',
        'product_name': 'Mleko owsiane',
        'brands': 'Oatly',
        'brands_tags': 'en:oatly',
        'quantity': '1 l',
        'allergens_tags': 'en:gluten',
        'countries_tags': 'en:poland',
        'nutriscore_grade': 'b',
        'nova_group': 3,
        'energy_kcal': Decimal('45.0000'),
        'carbohydrates': Decimal('6.5000'),
        'sugars': Decimal('4.1000'),
        'proteins': Decimal('1.0000'),
        'salt': Decimal('0.1000'),
    },
    {
        'code': '5900000000002',
        'product_name': 'Chleb żytni',
        'brands': 'Piekarnia',
        'brands_tags': 'en:piekarnia',
        'quantity': '500 g',
        'countries_tags': 'en:poland',
        'nutriscore_grade': 'a',
        'nova_group': 1,
        'energy_kcal': Decimal('250.0000'),
        'fiber': Decimal('8.0000'),
        'proteins': Decimal('8.5000'),
        'salt': Decimal('1.2000'),
    },
    {
        'code': '5900000000003',
        'product_name': 'Woda źródlana',
        'brands': 'Żywiec Zdrój',
        'brands_tags': 'en:zywiec-zdroj',
        'quantity': '1.5 l',
        'countries_tags': 'en:poland',
        'nova_group': 1,
    },
    {
        'code': '5900000000004',
        'product_name': 'Ser gouda',
        'brands': 'Mlekovita',
        'brands_tags': 'en:mlekovita',
        'quantity': '150 g',
        'allergens_tags': 'en:milk',
        'countries_tags': 'en:poland',
        'nutriscore_grade': 'd',
        'nova_group': 4,
        'energy_kcal': Decimal('350.0000'),
        'fat': Decimal('28.0000'),
        'saturated_fat': Decimal('18.0000'),
        'proteins': Decimal('24.0000'),
        'salt': Decimal('1.8000'),
    },
    *tuple(_sample(number) for number in range(5, 101)),
)


def load_samples() -> int:
    for row in SAMPLES:
        values = dict(row)
        code = values.pop('code')
        Product.objects.update_or_create(code=code, defaults=values)
    return len(SAMPLES)


def delete_samples() -> None:
    Product.objects.filter(code__in=[row['code'] for row in SAMPLES]).delete()
