from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about$', TemplateView.as_view(
        template_name="about.html")),
    url(r'^method$', TemplateView.as_view(
        template_name="method.html")),
    url(r'^kj$', TemplateView.as_view(
        template_name="kj.html")),
    url(r'^team$', TemplateView.as_view(
        template_name="team.html")),
    url(r'^partners$', TemplateView.as_view(
        template_name="partners.html")),
        ]

