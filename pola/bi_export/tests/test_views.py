import csv
import io

from django.urls import reverse_lazy
from test_plus.test import TestCase

from pola.company.factories import CompanyFactory
from pola.product.factories import ProductFactory
from pola.tests.test_views import PermissionMixin


class TestHome(PermissionMixin, TestCase):
    url = reverse_lazy('bi_export:top_companies')
    template_name = 'index.html'

    def test_generate_report(self):
        c1 = CompanyFactory(plCapital=100, plWorkers=100, plRnD=100, plRegistered=100, plNotGlobEnt=100, query_count=50)
        c2 = CompanyFactory(
            plCapital=100, plWorkers=100, plRnD=100, plRegistered=100, plNotGlobEnt=100, query_count=100
        )
        ProductFactory(company=c1, brand__company=c1, query_count=33)

        self.login()
        resp = self.client.get(self.url)
        csv_content = list(csv.DictReader(io.StringIO(resp.content.decode())))

        self.assertEqual(
            [
                {
                    'common_name': c2.common_name,
                    'count_product_id': '0',
                    'name': c2.name,
                    'nip': '',
                    'official_name': c2.common_name,
                    'pola_score': '100.00',
                    'query_count': '100',
                    'sum_product_product_query_count': '',
                },
                {
                    'common_name': c1.common_name,
                    'count_product_id': '1',
                    'name': c1.name,
                    'nip': '',
                    'official_name': c1.common_name,
                    'pola_score': '100.00',
                    'query_count': '50',
                    'sum_product_product_query_count': '33',
                },
            ],
            csv_content,
        )
