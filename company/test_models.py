from django.test import TestCase

from .models import Company
from brand.models import Brand


class GetSetBrandTestCase(TestCase):
    def setUp(self):
        c1 = Company.objects.create(name="lion")
        Brand.objects.bulk_create([
            Brand(name="brand_1", company=c1),
            Brand(name="brand_2", company=c1),
            Brand(name="brand_3", company=c1)
        ])

    def test_get_brand_result_all_brands(self):
        c1 = Company.objects.first()
        brands = c1.get_brands()
        self.assertSetEqual(
            set(["brand_1", "brand_2", "brand_3"]),
            set(brands)
        )

    def test_set_identical_brands_dont_make_changes(self):
        c1 = Company.objects.first()
        prev_brands = [x.id for x in c1.brand_set.all()]
        c1.set_brands("brand_1,brand_2, brand_3")
        next_brands = [x.id for x in c1.brand_set.all()]
        self.assertListEqual(prev_brands, next_brands)

    def test_append_brand_dont_edit_prev_brands(self):
        c1 = Company.objects.first()
        prev_ids = [x.id for x in c1.brand_set.all()]
        c1.set_brands("brand_1,brand_2,brand_3,brand_4")
        next_ids = [x.id for x in c1.brand_set.all()]
        new_ids = set(next_ids) - set(prev_ids)
        self.assertEqual(len(new_ids), 1)
