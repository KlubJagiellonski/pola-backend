import csv
from datetime import datetime

from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.views.generic import View


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class ExportView(View):
    def get(self, request: HttpRequest):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.get_filename()}"'
        rows = self.get_rows()
        if rows:
            fieldnames = ['No data']
        else:
            fieldnames = rows[0].keys()
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        return response

    def get_rows(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
SELECT company_company.common_name,
       company_company.official_name,
       company_company.name,
       company_company.nip,
       company_company.query_count,
       COUNT(product_product.id)        as count_product_id,
       SUM(product_product.query_count) as sum_product_product_query_count
FROM company_company
         LEFT JOIN
     product_product
     ON
         product_product.company_id = company_company.id
GROUP BY company_company.common_name, company_company.official_name, company_company.name,
         company_company.nip, company_company.query_count
ORDER BY company_company.query_count DESC
LIMIT 100;
            """
            )
            rows = dictfetchall(cursor)
        return rows

    def get_filename(self):
        date_suffix = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
        return f'bi_export-{date_suffix}.csv'
