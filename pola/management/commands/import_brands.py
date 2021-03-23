import argparse
import csv
import os
import re

from django.core.management import BaseCommand

from company.models import Brand, Company
from product.models import Product


def update_product(self, brand, ean_code, company, product_name):
    product = Product.objects.filter(code=ean_code).first()
    if product:
        product = Product.objects.get(code=ean_code)
        product.brand = brand
        product.name = product_name
        product.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully updated product {product_name}"))
    else:
        Product(company=company, brand=brand, code=ean_code, name=product_name).save()
        self.stdout.write(self.style.SUCCESS(f"Successfully created product {product_name}"))


class Command(BaseCommand):
    help = 'Import lidl companies from .tsv file'

    def add_arguments(self, parser):
        parser.add_argument('tsv_filepath', type=argparse.FileType('r'))
        parser.add_argument('company_nip')

    def handle(self, *args, **options):
        if not options['tsv_filepath'] or not os.path.exists(options['tsv_filepath'].name):
            raise SystemExit("Invalid path")
        if not options['company_nip'] or len(options['company_nip']) != 10 and options['company_nip'].isdigit():
            raise SystemExit("Company nip not valid")
        brand_owner = Company.objects.filter(nip__exact=options['company_nip']).first()
        if not brand_owner:
            self.stdout.write(self.style.ERROR(f'Company with nip {options["company_nip"]} does not exist.'))
            return
        confirm = input(
            f'You seleceted company: {brand_owner.official_name} with nip: {brand_owner.nip}. Proceed? (Y/n)'
        )
        while True:
            if confirm not in ('Y', 'n', 'yes', 'no'):
                confirm = input('Please enter either "yes" or "no": ')
                continue
            if confirm in ('Y', 'yes'):
                break
            else:
                return

        with options['tsv_filepath'] as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            index_successful = 0
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
                if Brand.objects.filter(company=brand_owner, common_name=brand_name).count():
                    brand = Brand.objects.filter(company=brand_owner, common_name=brand_name).first()
                else:
                    brand = Brand(company=brand_owner, common_name=brand_name)
                    brand.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully created brand {brand.common_name} "))
                # check if company from tsv file exist in db
                if Company.objects.filter(nip__exact=nip).count():
                    company = Company.objects.get(nip__exact=nip)
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Company with nip {nip} does not exist. '
                            f'Script will create a new company with name: {row[7]} nip: {nip}'
                        )
                    )
                    company = Company(nip=nip, name=row[7])
                    company.save()

                if len(ean_codes) == 1:
                    # check if product exist in db
                    update_product(self, brand, ean_codes[0], company, product_name)
                    index_successful += 1
                else:
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
            self.stdout.write(self.style.SUCCESS(f'Processed {line_no} products successful.'))
