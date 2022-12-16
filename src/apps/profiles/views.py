import datetime

from django.views.generic import ListView, View

from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.profiles.models import Profile

from django.core.paginator import Paginator

from apps.profiles.services.profile import get_search_profiles_queryset, get_all_profiles_queryset, \
    get_subscribe_profile_queryset, get_date_range_profiles_filter
from apps.utils.services.paginator import get_paginator_context


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/list.html'
    context_object_name = 'profiles'


class ProfileTableView(View):
    def post(self, request):
        queryset = None
        search = request.POST.get('search', '')
        page = int(request.POST.get('page', 1))
        daterange = request.POST.get('date-range', '').split(' to ')
        filter_date = None

        if len(daterange) == 2:
            date_start = datetime.datetime.strptime(daterange[0], '%Y-%m-%d')
            date_end = datetime.datetime.strptime(daterange[1], '%Y-%m-%d')
            filter_date = get_date_range_profiles_filter(date_start, date_end)
        if len(search) >= 3:
            queryset = get_search_profiles_queryset(search, filter_date)
        if not queryset and not search:
            queryset = get_all_profiles_queryset(filter_date)

        paginator = Paginator(queryset, 50)
        queryset = get_subscribe_profile_queryset(paginator.page(page))
        context_paginator = get_paginator_context(page, paginator.num_pages)

        context = {'rows': queryset}
        data = {
            'rows': render_to_string('profiles/row.html', context, request=request),
            'paginator': render_to_string('partials/paginator.html', context_paginator, request=request)
        }
        return JsonResponse(data)
