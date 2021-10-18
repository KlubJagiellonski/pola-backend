import csv
import io

from django.urls import reverse_lazy
from test_plus.test import TestCase

from company.factories import CompanyFactory
from pola.tests.test_views import PermissionMixin
from product.factories import ProductFactory


class TestHome(PermissionMixin, TestCase):
    url = reverse_lazy('bi_export:top_companies')
    template_name = 'index.html'

    def test_generate_report(self):
        c1 = CompanyFactory(plCapital=100, plWorkers=100, plRnD=100, plRegistered=100, plNotGlobEnt=100, query_count=50)
        c2 = CompanyFactory(
            plCapital=100, plWorkers=100, plRnD=100, plRegistered=100, plNotGlobEnt=100, query_count=100
        )
        ProductFactory(company=c1, query_count=33)

        self.login()
        resp = self.client.get(self.url)
        csv_content = list(csv.DictReader(io.StringIO(resp.content.decode())))
        from pprint import pprint

        pprint(csv_content)
        self.assertEqual(
            [
                {
                    'common_name': c2.common_name,
                    'official_name': c2.official_name,
                    'name': 'company1',
                    'nip': '',
                    'query_count': '100',
                    'count_product_id': '0',
                    'sum_product_product_query_count': '',
                    'pola_score': '100.00',
                },
                {
                    'common_name': 'company_official_0',
                    'official_name': 'company_official_0',
                    'name': 'company0',
                    'nip': '',
                    'query_count': '50',
                    'count_product_id': '1',
                    'sum_product_product_query_count': '33',
                    'pola_score': '100.00',
                },
                {
                    'common_name': 'company_official_2',
                    'official_name': 'company_official_2',
                    'name': 'company2',
                    'nip': '',
                    'query_count': '0',
                    'count_product_id': '0',
                    'sum_product_product_query_count': '',
                    'pola_score': '-1',
                },
            ],
            csv_content,
        )
