from django.core.management import BaseCommand

from pola.product.models import Product
from product.models import sentence_transformer


class Command(BaseCommand):
    help = 'Populates the products with sample vector embedding'

    def handle(self, *args, **options):
        for product in Product.objects.filter(embedding=None):
            product.embedding = sentence_transformer.encode(product.name)
            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated products embeddings'))
