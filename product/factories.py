import factory.fuzzy

from company.factories import BrandFactory, CompanyFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    name = factory.Sequence(lambda n: f'product{n}')
    code = factory.sequence(lambda n: f'00000000{n}')
    company = factory.SubFactory(CompanyFactory)
    brand = factory.SubFactory(BrandFactory)
