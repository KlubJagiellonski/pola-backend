import csv
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.views.generic import View


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class ExportView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        rows, columns = self.get_rows_and_columns()
        writer = csv.DictWriter(response, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
        return response

    def get_rows_and_columns(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
SELECT company_company.common_name,
       company_company.official_name,
       company_company.name,
       company_company.nip,
       company_company.query_count,
       COUNT(product_product.id)        as count_product_id,
       SUM(product_product.query_count) as sum_product_product_query_count,
       CASE
            WHEN company_company."plCapital" IS NOT NULL
                AND company_company."plWorkers" IS NOT NULL
                AND company_company."plRnD" IS NOT NULL
                AND company_company."plRegistered" IS NOT NULL
                AND company_company."plNotGlobEnt" IS NOT NULL
            THEN
            (
                  0.35 * company_company."plCapital"
                + 0.30 * company_company."plWorkers"
                + 0.15 * company_company."plRnD"
                + 0.10 * company_company."plRegistered"
                + 0.10 * company_company."plNotGlobEnt"
            )
            ELSE -1 END AS pola_score
FROM company_company
         LEFT JOIN
     product_product
     ON
         product_product.company_id = company_company.id
GROUP BY company_company.common_name, company_company.official_name, company_company.name,
         company_company.nip, company_company.query_count, pola_score
ORDER BY company_company.query_count DESC
LIMIT 100;
            """
            )
            rows = dictfetchall(cursor)
            columns = [col[0] for col in cursor.description]
        return rows, columns

    def get_filename(self):
        date_suffix = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        return f'bi_export-{date_suffix}.csv'
