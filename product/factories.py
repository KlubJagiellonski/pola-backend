import math

import factory
import factory.fuzzy

from company.factories import CompanyFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    name = factory.Sequence(lambda n: 'product%s' % n)
    code = factory.fuzzy.FuzzyInteger(math.pow(10, 13), math.pow(10, 14) - 1)
    company = factory.SubFactory(CompanyFactory)
