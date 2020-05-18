from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginator(request, queryset, per_page=25):
    per_page = request.GET.get('per_page', per_page)

    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.page(paginator.num_pages)
