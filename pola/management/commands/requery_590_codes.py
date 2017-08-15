from django.core.management.base import BaseCommand

from pola.logic_workers import requery_590_codes


class Command(BaseCommand):
    help = 'Requeries all codes for data from ILiM'

    def handle(self, *args, **options):
        requery_590_codes()
