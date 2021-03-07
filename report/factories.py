import factory.fuzzy
from django.utils import timezone

from pola.users.factories import UserFactory
from product.factories import ProductFactory


class ReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.Report'

    product = factory.SubFactory(ProductFactory)
    client = factory.sequence(lambda n: f"client{n}")
    description = factory.fuzzy.FuzzyText()


class ResolvedReportFactory(ReportFactory):
    resolved_at = factory.lazy_attribute(lambda o: timezone.now())
    resolved_by = factory.SubFactory(UserFactory)


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.Attachment'

    report = factory.SubFactory(ReportFactory)
    attachment = factory.django.ImageField(
        width=200, height=200, filename=factory.sequence(lambda n: f"report-{n}.png")
    )
