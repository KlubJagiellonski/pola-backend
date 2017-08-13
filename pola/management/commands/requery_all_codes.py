from django.core.management.base import BaseCommand

from pola.logic_workers import requery_all_codes


class Command(BaseCommand):
    help = 'Requeries all codes for data from ILiM'

    def handle(self, *args, **options):
        requery_all_codes()
