import factory
import factory.fuzzy

from company.factories import CompanyFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'
    name = factory.Sequence(lambda n: 'product%s' % n)
    code = factory.sequence(lambda n: '00000000%s' % n)
    company = factory.SubFactory(CompanyFactory)
