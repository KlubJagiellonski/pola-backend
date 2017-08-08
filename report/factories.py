import datetime
from django.utils import timezone

import factory
import factory.fuzzy

from pola.users.factories import UserFactory
from product.factories import ProductFactory


class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.Report'
    product = factory.SubFactory(ProductFactory)
    client = factory.sequence(lambda n: "client%s" % n)
    description = factory.fuzzy.FuzzyText()


class ResolvedReportFactory(ReportFactory):
    resolved_at = factory.lazy_attribute(lambda o: timezone.now())
    resolved_by = factory.SubFactory(UserFactory)
