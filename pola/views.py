from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from product.models import Product
from company.models import Company


class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context['oldest_reports'] = set()
        context['newest_reports'] = set()
        context['most_popular_products'] = (Product.objects.with_query_count()
                                            .order_by('query_count')[:10])
        context['most_popular_companies'] = (Company.objects.with_query_count()
                                             .order_by('query_count')[:10])
        return context
