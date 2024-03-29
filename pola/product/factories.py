import factory.fuzzy

from pola.company.factories import BrandFactory, CompanyFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    name = factory.Sequence(lambda n: f'product{n}')
    code = factory.sequence(lambda n: f"{n:013}")
    company = factory.SubFactory(CompanyFactory)
    brand = factory.SubFactory(BrandFactory)
