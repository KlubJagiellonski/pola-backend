from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about$', TemplateView.as_view(template_name="webviews/about.html"), name="about"),
    url(r'^method$', TemplateView.as_view(template_name="webviews/method.html"), name="method"),
    url(r'^kj$', TemplateView.as_view(template_name="webviews/kj.html"), name="kj"),
    url(r'^team$', TemplateView.as_view(template_name="webviews/team.html"), name="team"),
    url(r'^partners$', TemplateView.as_view(template_name="webviews/partners.html"), name="partners"),
    url(r'^friends$', TemplateView.as_view(template_name="webviews/m_friends.html"), name="friends"),
]
