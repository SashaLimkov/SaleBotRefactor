import datetime

from django.views.generic import ListView, View, DetailView

from django.http import JsonResponse
from django.template.loader import render_to_string

from apps.posts.services.compilation import get_search_compilations_queryset, get_all_compilation_queryset, \
    get_content_compilation_queryset, get_date_range_compilation_filter
from apps.posts.models import Compilation

from django.core.paginator import Paginator

from apps.utils.services.paginator import get_paginator_context


class CompilationListView(ListView):
    model = Compilation
    template_name = 'posts/list.html'
    context_object_name = 'compilations'


class CompilationTableView(View):
    def post(self, request):
        queryset = None

        search = request.POST.get('search', '')
        page = int(request.POST.get('page', 1))
        daterange = request.POST.get('date-range', '').split(' to ')
        filter_date = None

        if len(daterange) == 2:
            date_start = datetime.datetime.strptime(daterange[0], '%Y-%m-%d')
            date_end = datetime.datetime.strptime(daterange[1], '%Y-%m-%d')
            filter_date = get_date_range_compilation_filter(date_start, date_end)
        if len(search) >= 3:
            queryset = get_search_compilations_queryset(search, filter_date)
        print(queryset)
        if not queryset and not search:
            queryset = get_all_compilation_queryset(filter_date)

        paginator = Paginator(queryset, 50)
        queryset = get_content_compilation_queryset(paginator.page(page))
        context_paginator = get_paginator_context(page, paginator.num_pages)

        context = {'rows': queryset}
        data = {
            'rows': render_to_string('posts/row.html', context, request=request),
            'paginator': render_to_string('partials/paginator.html', context_paginator, request=request)
        }
        return JsonResponse(data)


class CompilationDetailView(DetailView):
    model = Compilation
    template_name = 'posts/form.html'
    context_object_name = 'compilation'

