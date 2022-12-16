from django.views.generic import ListView, View

from django.http import JsonResponse
from django.template.loader import render_to_string

from apps.posts.services.compilation import get_search_compilations_queryset, get_all_compilation_queryset, \
    get_content_compilation_queryset
from apps.profiles.models import Profile

from django.core.paginator import Paginator

from apps.utils.services.paginator import get_paginator_context


class CompilationListView(ListView):
    model = Profile
    template_name = 'posts/list.html'
    context_object_name = 'compilations'


class CompilationTableView(View):
    def post(self, request):
        queryset = None

        search = request.POST.get('search', '')
        page = int(request.POST.get('page', 1))

        if len(search) >= 3:
            queryset = get_search_compilations_queryset(search)
        if not queryset:
            queryset = get_all_compilation_queryset()

        paginator = Paginator(queryset, 50)
        queryset = get_content_compilation_queryset(paginator.page(page))
        context_paginator = get_paginator_context(page, paginator.num_pages)

        context = {'rows': queryset}
        data = {
            'rows': render_to_string('posts/row.html', context, request=request),
            'paginator': render_to_string('partials/paginator.html', context_paginator, request=request)
        }
        return JsonResponse(data)
