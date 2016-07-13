from django.core.management.base import BaseCommand, CommandError
from company.models import Company
from reversion.models import Version


class Command(BaseCommand):
    help = 'Deletes empty revisions'

    def add_arguments(self, parser):
        parser.add_argument('last_company_id')

    def handle(self, *args, **options):
        companies = Company.objects.filter(pk__gte=options["last_company_id"])\
            .order_by('id')
        for company in companies:
            if company.name:
                print "{} (id:{})".format(company.name.encode('UTF-8'), company.id)
            versions = Version.objects.\
                filter(object_id_int=company.pk,
                       content_type_id=16,
                       revision__comment='Firma utworzona automatycznie na '
                                         'podstawie API ILiM',
                       revision__user__isnull=True)\
                .values('id','revision_id')\
                .order_by('revision__date_created')
            first_record = True
            with connection.cursor() as cursor:
                for version in versions:
                    if first_record:
                        first_record=False
                    else:
                        cursor.execute(
                            'delete from reversion_version where id=%s',
                            [version['id']])
                        cursor.execute(
                            'delete from reversion_revision where id=%s',
                            [version['revision_id']])
                        print '.',
