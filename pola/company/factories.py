import factory
import factory.fuzzy


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Company'

    name = factory.Sequence(lambda n: 'company%d' % n)
    official_name = factory.Sequence(lambda n: 'company_official_%d' % n)
    common_name = factory.Sequence(lambda n: 'company_official_%d' % n)
    description = factory.fuzzy.FuzzyText()


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Brand'

    company = factory.SubFactory(CompanyFactory)
    name = factory.Sequence(lambda n: 'brand%d' % n)
    common_name = factory.Sequence(lambda n: 'common_brand_name%d' % n)
