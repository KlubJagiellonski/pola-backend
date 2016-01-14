from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import TemplateView
from django.views.generic.detail import (
    BaseDetailView, SingleObjectTemplateResponseMixin)
from braces.views import LoginRequiredMixin
from company.models import Company
from product.models import Product
from report.models import Report
from pola.models import Stats
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import get_default_timezone
from django.db import connection

class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        c = super(FrontPageView, self).get_context_data(**kwargs)

        c['most_popular_companies'] = (Company.objects
                                          .with_query_count()
                                          .filter(verified=False)
                                          .order_by('-query_count')[:10])

        c['no_of_companies'] = Company.objects.count()
        c['no_of_not_verified_companies'] = Company.objects\
            .filter(verified=False).count()
        c['no_of_verified_companies'] = Company.objects.\
            filter(verified=True).count()

        c['newest_reports'] = (Report.objects.only_open()
                                     .order_by('-created_at')[:10])
        c['no_of_open_reports'] = Report.objects.only_open().count()
        c['no_of_resolved_reports'] = Report.objects.only_resolved().count()
        c['no_of_reports'] = Report.objects.count()

        c['most_popular_590_products'] =  (Product.objects.with_query_count()
                                          .filter(company__isnull=True,
                                                  code__startswith='590')
                                          .order_by('-query_count')[:10])
        c['no_of_most_popular_590_products'] = (Product.objects
                                                .filter(company__isnull=True,
                                                        code__startswith='590')
                                                .count())

        c['most_popular_not_590_products'] =\
            (Product.objects.with_query_count().filter(company__isnull=True)
                .exclude(code__startswith='590').order_by('-query_count')[:10])
        c['no_of_most_popular_not_590_products'] = \
            (Product.objects.filter(company__isnull=True).
             exclude(code__startswith='590').count())

        return c


class ActionMixin(object):
    success_url = None

    def action(self):
        raise ImproperlyConfigured("No action to do. Provide a action body.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.action()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            self.success_url = force_text(self.success_url)
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseActionView(ActionMixin, BaseDetailView):
    """
    Base view for action on an object.
    Using this base class requires subclassing to provide a response mixin.
    """


class ActionView(SingleObjectTemplateResponseMixin, BaseActionView):
    template_name_suffix = '_action'


class StatsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-stats.html'

    def get_context_data(self, *args, **kwargs):
        c = super(StatsPageView, self).get_context_data(**kwargs)

        stats = []

        date = timezone.now()
        for i in range(0, 30):
            midnight = datetime(
                date.year, date.month, date.day,
                tzinfo=get_default_timezone()) + \
                timedelta(days=1)
            try:
                stat = Stats.objects.get(
                    year=date.year, month=date.month, day=date.day)
            except ObjectDoesNotExist:
                stat = Stats()
            if stat.year is None or stat.calculated_at < midnight:
                stat.calculate(date.year, date.month, date.day)
                Stats.save(stat)
            date = date - timedelta(days=1)
            setattr(stat, 'index', i)

            stats.append(stat)

        c['stats'] = list(reversed(stats))
        c['stats5'] = [stats[i] for i in range(0, 5)]
        return c


class EditorsStatsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-editors-stats.html'

    def execute_query(self, sql, params):
        cursor = connection.cursor()

        cursor.execute(sql, params)

        columns = [col[0] for col in cursor.description]

        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def query_log(self, id):
        return self.execute_query(
            "select to_char(reversion_revision.date_created, \'YYYY-MM\'),"
                "username, count(*) "
            "from users_user "
            "join reversion_revision on users_user.id=user_id "
            "join reversion_version on reversion_revision.id = "
                "reversion_version.revision_id "
            "where reversion_version.content_type_id=%s "
            "group by to_char(reversion_revision.date_created, \'YYYY-MM\'), "
                "username "
            "order by 1 desc, 3 desc;", [id])

    def get_context_data(self, *args, **kwargs):
        c = super(EditorsStatsPageView, self).get_context_data(**kwargs)

        c['company_log'] = self.query_log(16)
        c['product_log'] = self.query_log(15)
        c['report_log'] = self.execute_query(
            "select to_char(report_report.resolved_at, 'YYYY-MM'), username, "
                "count(*) "
            "from users_user "
            "join report_report on users_user.id=report_report.resolved_by_id "
            "group by to_char(report_report.resolved_at, 'YYYY-MM'), username "
            "order by 1 desc, 3 desc;", None)

        return c
