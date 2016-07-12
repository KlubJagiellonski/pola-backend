from django.core.management.base import BaseCommand, CommandError
from company.models import Company
from reversion.models import Version


class Command(BaseCommand):
    help = 'Deletes empty revisions'

    def handle(self, *args, **options):
        companies = Company.objects.all()
        for company in companies:
            if company.name:
                print company.name.encode('UTF-8')
            versions = Version.objects.\
                filter(object_id_int=company.pk,
                       content_type_id=16,
                       revision__comment='Firma utworzona automatycznie na '
                                         'podstawie API ILiM',
                       revision__user__isnull=True)\
                .order_by('revision__date_created')
            first_record = True
            for version in versions:
                if first_record:
                    first_record=False
                else:
                    version.revision.delete()
                    version.delete()
                    print '.',
