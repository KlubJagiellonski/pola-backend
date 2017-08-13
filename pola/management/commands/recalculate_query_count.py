from django.core.management.base import BaseCommand

from company.models import Company
from product.models import Product


class Command(BaseCommand):
    help = 'Recalculates query counts'

    def handle(self, *args, **options):
        print 'Recalculating product query count'
        Product.recalculate_query_count()
        print 'Recalculating product ai pics count'
        Product.recalculate_ai_pics_count()
        print 'Recalculating company query count'
        Company.recalculate_query_count()
        print 'Finished recalculating query count'

