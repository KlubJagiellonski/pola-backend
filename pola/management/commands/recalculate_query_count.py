from django.core.management.base import BaseCommand, CommandError
from product import Product


class Command(BaseCommand):
    help = 'Recalculates query counts'

    def handle(self, *args, **options):
        Product.recalculate_query_count()

