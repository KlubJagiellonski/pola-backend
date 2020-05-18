# from company.models import Company
# from mojepanstwo_api import KrsClient
# from pola import logic

# usage:
# export PYTHONIOENCODING=UTF-8
# python manage.py shell
# execfile('utils/test_mojepanstwo_api_v3.py')

# companies = Company.objects.filter(name__isnull=False)
#
# krs = KrsClient()
#
# for company in companies:
#     print company.name.encode('utf-8')
#
#     companies = krs.get_companies_by_name(company.name)
#     print companies
#     if companies.__len__() == 1:
#         print logic.shareholders_to_str(krs, companies[0]["id"], "---")
#
#     print
#     print
