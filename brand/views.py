from django.http import Http404
from django.shortcuts import render_to_response
from company.models import Company
from django.db.models import Q
from django.db.models import Count


def search(request):
    keyword = request.GET.get('q')
    if keyword:
        try:
            where = Q(
                name__icontains=keyword) | Q(brand__name__icontains=keyword)
            companies = Company.objects.filter(
                where).annotate(total=Count('name'))
        except Company.DoesNotExist:
            raise Http404("Poll does not exist")
        return render_to_response(
            'brand/search_result.html', {'companies': companies})
    return render_to_response('brand/search_form.html')
