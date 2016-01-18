from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Requeries all codes for data from ILiM'

    def handle(self, *args, **options):
        raise ZeroDivisionError
