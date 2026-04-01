from unittest import mock

from test_plus import TestCase

from pola.company.factories import CompanyFactory
from pola.logic import serialize_company


class TestSerializeCompany(TestCase):
    @mock.patch("pola.logic.get_pl_score", return_value=0)
    def test_includes_zero_plscore(self, _mock_plscore):
        company = CompanyFactory.create()
        data = serialize_company(company)

        # When plScore is 0, it should be included (not treated as falsy/absent)
        self.assertIn("plScore", data)
        self.assertEqual(0, data["plScore"])
