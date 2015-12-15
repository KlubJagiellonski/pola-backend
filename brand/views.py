from django.http import Http404
from django.shortcuts import render_to_response
from company.models import Company


def search(request):
    keyword = request.GET.get('q')
    if keyword:
        try:
            companies = Company.objects.filter(
                brand__name__icontains=keyword)
        except Company.DoesNotExist:
            raise Http404("Poll does not exist")
        return render_to_response(
            'brand/search_result.html', {'companies': companies})
    return render_to_response('brand/search_form.html')
