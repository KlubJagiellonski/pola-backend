from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^method$', TemplateView.as_view(template_name="method.html"), name="method"),
    url(r'^kj$', TemplateView.as_view(template_name="kj.html"), name="kj"),
    url(r'^team$', TemplateView.as_view(template_name="team.html"), name="team"),
    url(r'^partners$', TemplateView.as_view(template_name="partners.html"), name="partners"),
    url(r'^friends$', TemplateView.as_view(template_name="m_friends.html"), name="friends"),
]
