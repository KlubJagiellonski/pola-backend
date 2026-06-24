import factory
import factory.fuzzy


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Company'

    name = factory.Sequence(lambda n: f'company{n}')
    official_name = factory.Sequence(lambda n: f'company_official_{n}')
    common_name = factory.Sequence(lambda n: f'company_official_{n}')
    description = factory.fuzzy.FuzzyText()


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Brand'

    company = factory.SubFactory(CompanyFactory)
    name = factory.Sequence(lambda n: f'brand{n}')
    common_name = factory.Sequence(lambda n: f'common_brand_name{n}')
