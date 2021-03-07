from django.core.management.base import BaseCommand
from django.db import connection
from reversion.models import Version

from company.models import Company


class Command(BaseCommand):
    help = 'Deletes empty revisions'

    def add_arguments(self, parser):
        parser.add_argument('last_company_id')

    def handle(self, *args, **options):
        companies = Company.objects.filter(pk__gte=options["last_company_id"]).order_by('id')
        for company in companies:
            if company.name:
                print(f"{company.name.encode('UTF-8')} (id:{company.id})")
            versions = (
                Version.objects.filter(
                    object_id=company.pk,
                    content_type_id=16,
                    revision__comment='Firma utworzona automatycznie na podstawie API ILiM',
                    revision__user__isnull=True,
                )
                .values('id', 'revision_id')
                .order_by('revision__date_created')
            )

            record_no = 0
            with connection.cursor() as cursor:
                for version in versions:
                    if record_no > 0:
                        cursor.execute('delete from reversion_version where id=%s', [version['id']])
                        cursor.execute('delete from reversion_revision where id=%s', [version['revision_id']])
                        if record_no % 50 == 0:
                            print('.', end=' ')
                    record_no += 1
