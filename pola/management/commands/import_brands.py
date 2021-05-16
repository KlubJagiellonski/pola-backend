import argparse
import csv
import re

from django.core.management import BaseCommand

from company.models import Brand, Company
from product.models import Product


def update_product(self, brand, ean_code, company, product_name):
    product = Product.objects.filter(code=ean_code).first()
    if product:
        product.brand = brand
        product.name = product_name
        product.company = company
        product.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully updated product {product_name}"))
    else:
        Product(company=company, brand=brand, code=ean_code, name=product_name).save()
        self.stdout.write(self.style.SUCCESS(f"Successfully created product {product_name}"))


def nip_number(value):
    if len(value) == 10 and value.isdigit():
        return value
    raise argparse.ArgumentTypeError(f"Invalid NIP number: '{value}'")


def ask_yes_no(question):
    confirm = input(question)
    while True:
        if confirm not in ('Y', 'n', 'yes', 'no'):
            confirm = input('Please enter either "yes" or "no": ')
            continue
        if confirm in ('Y', 'yes'):
            return True
        else:
            return False


class Command(BaseCommand):
    help = 'Import lidl companies from .tsv file'

    def add_arguments(self, parser):
        parser.add_argument('tsv_filepath', type=argparse.FileType('r'))
        parser.add_argument('company_nip', type=nip_number)
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_false',
            dest='interactive',
            help=('Tells Django to NOT prompt the user for input of any kind. '),
        )

    def handle(self, *args, **options):
        brand_owner = Company.objects.filter(nip__exact=options['company_nip']).first()
        if not brand_owner:
            self.stdout.write(self.style.ERROR(f'Company with nip {options["company_nip"]} does not exist.'))
            return

        if options['interactive'] and not ask_yes_no(
            f'You seleceted company: {brand_owner.official_name} with nip: {brand_owner.nip}. Proceed? (Y/n)'
        ):
            self.stdout.write(self.style.ERROR('Operation cancelled.'))
            return

        with options['tsv_filepath'] as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            index_successful = 0
            line_no = 0
            for line_no, row in enumerate(csv_reader):
                # skip column names
                if line_no == 0:
                    continue
                # find polish nip
                nip = row[8].split(",")[0][2::]
                brand_name = row[2]
                ean_codes = re.findall(r'[0-9]+', row[0])
                product_name = row[5]

                # check if brand exist in db
                brand = Brand.objects.filter(company=brand_owner, common_name=brand_name).first()
                if not brand:
                    brand = Brand(company=brand_owner, common_name=brand_name)
                    brand.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully created brand {brand.common_name} "))
                # check if company from tsv file exist in db
                company = Company.objects.filter(nip__exact=nip).first()
                if not company:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Company with nip {nip} does not exist. '
                            f'Script will create a new company with name: {row[7]} nip: {nip}'
                        )
                    )
                    company = Company(nip=nip, name=row[7])
                    company.save()

                if len(ean_codes) > 1:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Product with name {product_name} has multiple ean codes: "
                            f"{', '.join(str(x) for x in ean_codes)}. "
                            f"Script will create/update multiple products, one for each code."
                        )
                    )
                for code in ean_codes:
                    # check if product exist in db
                    update_product(self, brand, code, company, product_name)
                    index_successful += 1
            if line_no == 0:
                self.stdout.write(self.style.SUCCESS('Empty file. Nothing to do'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Processed {line_no} products successful.'))
