from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from product.models import Product
from company.models import Company
from report.models import Report


class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        c = super(FrontPageView, self).get_context_data(**kwargs)
        c['oldest_reports'] = (Report.objects.only_open()
                                     .order_by('-created_at')[:10])
        c['newest_reports'] = (Report.objects.only_open()
                                     .order_by('created_at')[:10])
        c['most_popular_products'] = (Product.objects
                                             .with_query_count()
                                             .filter(company__isnull=True)
                                             .order_by('-query_count')[:10])
        c['most_popular_companies'] = (Company.objects
                                              .with_query_count()
                                              .filter(plCapital__isnull=True)
                                              .order_by('-query_count')[:10])
        return c
