import datetime

from django.shortcuts import render
from django.views.generic import ListView, View, DetailView, CreateView

from django.http import JsonResponse
from django.template.loader import render_to_string

from apps.posts.services.compilation import get_search_compilations_queryset, get_all_compilation_queryset, \
    get_content_compilation_queryset, get_date_range_compilation_filter, create_compilation, update_compilation, \
    create_final_compilation, update_or_create_final_compilation
from apps.posts.models import Compilation, Content, FinalCompilation

from django.core.paginator import Paginator

from apps.posts.services.content import update_or_create_content, create_content
from apps.posts.services.post import get_formatted_posts_by_compilation_id
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['compilation'].datetime_send = datetime.date.strftime(context['compilation'].datetime_send,
                                                                      '%Y-%m-%dT%H:%M')
        context['posts'] = get_formatted_posts_by_compilation_id(context['compilation'].pk)
        return context

    def post(self, request, pk):
        if request.FILES.get('media'):
            format_file = str(request.FILES.get('media')).split('.')[-1]
            if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                type_content = 0
            else:
                type_content = 1
            update_or_create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='compilation',
                to_id=pk
            )
        update_compilation(
            compilation_id=pk,
            name=request.POST.get('name'),
            text=request.POST.get('text').replace('<p>', '').replace('</p>', ''),
            date=datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
            datetime_send=datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M'),
            done=True if request.POST.get('complete') == 'true' else False
        )
        return JsonResponse({'success': True})


class FinalCompilationSaveView(View):
    def post(self, request, pk):
        final_compilation = update_or_create_final_compilation(
            compilation_id=pk,
            text=request.POST.get('text').replace('<p>', '').replace('</p>', '')
        )[0]
        if request.FILES.get('media'):
            format_file = str(request.FILES.get('media')).split('.')[-1]
            if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                type_content = 0
            else:
                type_content = 1
            update_or_create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='final_compilation',
                to_id=final_compilation.pk
            )
        return JsonResponse({'success': True})


class CompilationCreateView(View):
    def get(self, requet):
        return render(requet, 'posts/form_create.html')

    def post(self, request):
        compilation_id = request.POST.get('compilation_id')
        if compilation_id != 'undefined':
            compilation = update_compilation(
                compilation_id=int(compilation_id),
                name=request.POST.get('name'),
                text=request.POST.get('text').replace('<p>', '').replace('</p>', ''),
                date=datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
                datetime_send=datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M'),
                done=True if request.POST.get('complete') == 'true' else False
            )
            if request.FILES.get('media'):
                format_file = str(request.FILES.get('media')).split('.')[-1]
                if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                    type_content = 0
                else:
                    type_content = 1
                update_or_create_content(
                    file_name=str(request.FILES.get('media')),
                    file=request.FILES.get('media'),
                    type_content=type_content,
                    to='compilation',
                    to_id=compilation.id
                )
        else:
            compilation = create_compilation(
                name=request.POST.get('name'),
                text=request.POST.get('text').replace('<p>', '').replace('</p>', ''),
                date=datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
                datetime_send=datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M'),
                done=True if request.POST.get('complete') == 'true' else False
            )
            format_file = str(request.FILES.get('media')).split('.')[-1]
            if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                type_content = 0
            else:
                type_content = 1
            create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='compilation',
                to_id=compilation.id
            )

        gid = render_to_string('posts/form_gid.html', {'compilation_id': compilation.pk}, request=request)
        return JsonResponse({'success': True, 'gid': gid})


class FinalCompilationCreateView(View):
    def post(self, request):
        compilation_id = request.POST.get('compilation')
        final_compilation = create_final_compilation(
            compilation_id=int(compilation_id),
            text=request.POST.get('text').replace('<p>', '').replace('</p>', '')
        )
        format_file = str(request.FILES.get('media')).split('.')[-1]
        if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
            type_content = 0
        else:
            type_content = 1
        print(final_compilation)
        create_content(
            file_name=str(request.FILES.get('media')),
            file=request.FILES.get('media'),
            type_content=type_content,
            to='final_compilation',
            to_id=final_compilation.pk
        )
        return JsonResponse({'success': True})


class PostUpdateView(View):
    def post(self, request):
        list_values_edit = []
        list_values_add = []
        for key in request.POST.keys():
            if 'name_product' in key:
                if 'add' in key:
                    list_values_add.append(key.split('_')[-1])
                else:
                    list_values_edit.append(key.split('_')[-1])

        for index in list_values_edit:
            name = request.POST['name_product_' + index]
            sizes = request.POST['sizes_' + index]
            link = request.POST['link_' + index]
            description = request.POST['description_' + index]
            price_old = request.POST['price_old_' + index]
            price_new = request.POST['price_new_' + index]

        for index in list_values_add:
            name = request.POST['name_product_add_' + index]
            sizes = request.POST['sizes_add_' + index]
            link = request.POST['link_add_' + index]
            description = request.POST['description_add_' + index]
            price_old = request.POST['price_old_add_' + index]
            price_new = request.POST['price_new_add_' + index]

        print(list_values_edit, list_values_add)
        return JsonResponse({'data': True})
