from django.core.paginator import Paginator

from constants import constants_teamfinder as constant


def paginate(request, queryset, items_per_page=constant.ITEMS_ON_PAGE):
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj
