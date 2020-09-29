import factory
import factory.fuzzy


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'company.Company'

    name = factory.fuzzy.FuzzyText(prefix='company_')
    official_name = factory.fuzzy.FuzzyText(prefix='company_official_')
    common_name = factory.fuzzy.FuzzyText(prefix='company_official_')
    description = factory.fuzzy.FuzzyText()
