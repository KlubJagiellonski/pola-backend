from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context['oldest_reports'] = set()
        context['newest_reports'] = set()
        context['most_popular_products'] = set()
        context['most_popular_companies'] = set()
        return context
