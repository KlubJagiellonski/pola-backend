# from company.models import Company
# from mojepanstwo_api import KrsClient
#
# # usage:
# # python manage.py shell
# # execfile('utils/set_sources_to_KRS_if_empty.py')
#
# companies = Company.objects.filter(official_name__isnull=False, sources__isnull=True)
#
# client = KrsClient()
#
# i=1
# for company in companies:
#     print str(i) + '. ' + company.__unicode__().encode('utf-8')
#     i+=1
#
#     json = client.query_podmiot("conditions[nazwa]", company.official_name)
#
#     if json['search']['dataobjects'].__len__() != 1:
#         print 'nie znaleziono'
#         continue
#
#     url = json['search']['dataobjects'][0]['_mpurl']
#     company.sources = u"Dane z KRS|%s" % url
#     company.save(commit_desc='Automatycznie dodane źródło KRS z '
#                              'mojepanstwo.pl')
