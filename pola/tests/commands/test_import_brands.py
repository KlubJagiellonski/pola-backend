import os
import re
from io import StringIO

from django.core.files.temp import NamedTemporaryFile
from django.core.management import call_command
from django.test import TestCase

from company.factories import CompanyFactory
from company.models import Brand, Company
from product.models import Product

EXAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_import_brands_fixture.tsv")

ANSI_ESCAPE_SEQUENCE_REGEXP = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")


def strip_ansi_escape_sequence(text: str) -> str:
    """Remove 7-bit C1 ANSI escape sequences"""
    return ANSI_ESCAPE_SEQUENCE_REGEXP.sub("", text)


class ImportBrandsTestCase(TestCase):
    def test_missing_company(self):
        out = StringIO()
        with NamedTemporaryFile() as tmp_file:
            call_command('import_brands', tmp_file.name, "1234566789", interactive=False, stdout=out)
        self.assertIn("Company with nip 1234566789 does not exist.", strip_ansi_escape_sequence(out.getvalue()))

    def test_empty_file(self):
        CompanyFactory(nip="1234566789")
        out = StringIO()
        with NamedTemporaryFile() as tmp_file:
            call_command('import_brands', tmp_file.name, "1234566789", interactive=False, stdout=out)
        self.assertIn("Empty file. Nothing to do", strip_ansi_escape_sequence(out.getvalue()))

    def test_example_file(self):
        CompanyFactory(nip="1234566789")
        out = StringIO()
        call_command('import_brands', EXAMPLE_FILE, "1234566789", interactive=False, stdout=out)
        self.assertIn(
            'Successfully created brand Pilos \n'
            'Company with nip 7010399415 does not exist. Script will create a new company with name: '
            'Mazowiecka Sp.Mlecz. nip: 7010399415\n'
            'Successfully created product Jogurt pitny 1,5%, czerwona pomarańcza\n'
            'Successfully created product Jogurt pitny 1,5%, żurawina\n'
            'Company with nip 7220002329 does not exist. Script will create a new company with name: '
            'Mlekovita nip: 7220002329\n'
            'Product with name Serek twarogowy plastry, z ziołami has multiple ean codes: '
            '20387754, 20980368. Script will create/update multiple products, one for each code.\n'
            'Successfully created product Serek twarogowy plastry, z ziołami\n'
            'Successfully created product Serek twarogowy plastry, z ziołami\n'
            'Processed 3 products successful.',
            strip_ansi_escape_sequence(out.getvalue()).strip(),
        )
        self.assertTrue(Company.objects.filter(nip="7010399415", name="Mazowiecka Sp.Mlecz.").exists())
        self.assertTrue(Company.objects.filter(nip="7220002329", name="Mlekovita").exists())
        self.assertEqual(4, Product.objects.filter(code__in=["20268190", "20268176", "20387754", "20980368"]).count())
        self.assertTrue(Brand.objects.filter(common_name="Pilos").exists())
