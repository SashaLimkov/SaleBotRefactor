import asyncio
import datetime
import traceback
import unicodedata
from html import unescape

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, View, DetailView, CreateView

from django.http import JsonResponse
from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from apps.posts.services.compilation import get_search_compilations_queryset, get_all_compilation_queryset, \
    get_content_compilation_queryset, get_date_range_compilation_filter, create_compilation, update_compilation, \
    create_final_compilation, update_or_create_final_compilation, delete_final_compilation
from apps.posts.models import Compilation, Content, FinalCompilation, Post, Item

from django.core.paginator import Paginator

from apps.posts.services.content import update_or_create_content, create_content
from apps.posts.services.item import update_item, create_item
from apps.posts.services.post import get_formatted_posts_by_compilation_id, update_post, create_post, get_post_text
from apps.settings.services.currency import get_list_currency
from apps.users.services.logs import create_log
from apps.utils.services.paginator import get_paginator_context
from bot.utils.deleter import try_delete_message
from bot.utils.message_worker import try_edit_message_caption, try_send_post_to_user


class CompilationListView(LoginRequiredMixin, ListView):
    model = Compilation
    template_name = 'posts/list.html'
    context_object_name = 'compilations'


class CompilationTableView(LoginRequiredMixin, View):
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


class CompilationDetailView(LoginRequiredMixin, DetailView):
    model = Compilation
    template_name = 'posts/form.html'
    context_object_name = 'compilation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['compilation'].datetime_send = datetime.date.strftime(context['compilation'].datetime_send,
                                                                      '%Y-%m-%dT%H:%M')
        context['posts'] = get_formatted_posts_by_compilation_id(context['compilation'].pk)
        context['currency'] = get_list_currency()
        return context

    def post(self, request, pk):
        content = (None, None)
        if request.FILES.get('media'):
            format_file = str(request.FILES.get('media')).split('.')[-1]
            if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                type_content = 0
            else:
                type_content = 1
            content = update_or_create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='compilation',
                to_id=pk
            )
        datetime_send = datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M')
        compilation = update_compilation(
            compilation_id=pk,
            name=request.POST.get('name'),
            text=request.POST.get('text').replace('<p>', '').replace('</p>', '<br>'),
            date=datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
            datetime_send=datetime_send,
            done=True if request.POST.get('complete') == 'true' else False
        )
        create_log(request.user, 5, compilation)
        if compilation.message_id:
            # compilation.contents.first()
            text = unicodedata.normalize('NFKC', unescape(compilation.text.replace('<br>', '\n')))
            if content[0]:
                asyncio.run(try_send_post_to_user(
                    file_path=content[0].file.path,
                    file_type=content[0].type,
                    text=text,
                    chat_id=settings.CHANNEL,
                    message_id=compilation.message_id,
                ))
            else:
                asyncio.run(try_edit_message_caption(settings.CHANNEL, text, compilation.message_id, None))
        if content[0]:
            media = render_to_string('posts/media.html', context={'form': 'gid', 'content': content[0]})
        else:
            media = False
        return JsonResponse({'success': True, 'media': media})


class FinalCompilationSaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        content = (None, None)
        if request.POST.get('visible') == 'true':
            final_compilation = update_or_create_final_compilation(
                compilation_id=pk,
                text=request.POST.get('text').replace('<p>', '').replace('</p>', '')
            )[0]
            create_log(request.user, 8, final_compilation)

            if request.FILES.get('media'):
                format_file = str(request.FILES.get('media')).split('.')[-1]
                if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                    type_content = 0
                else:
                    type_content = 1
                content = update_or_create_content(
                    file_name=str(request.FILES.get('media')),
                    file=request.FILES.get('media'),
                    type_content=type_content,
                    to='final_compilation',
                    to_id=final_compilation.pk
                )
            if final_compilation.message_id:
                text = unicodedata.normalize('NFKC', unescape(final_compilation.text.replace('<br>', '\n')))
                if content[0]:
                    asyncio.run(try_send_post_to_user(
                        file_path=content[0].file.path,
                        file_type=content[0].type,
                        text=text,
                        chat_id=settings.CHANNEL,
                        message_id=final_compilation.message_id,
                    ))
                asyncio.run(try_edit_message_caption(settings.CHANNEL, text, final_compilation.message_id, None))
        else:
            try:
                final_compilation = FinalCompilation.objects.get(pk=pk)
                asyncio.run(try_delete_message(settings.CHANNEL, final_compilation.message_id))
                delete_final_compilation(pk)
            except:
                pass

        if content[0]:
            media = render_to_string('posts/media.html', context={'form': 'gid', 'content': content[0]})
        else:
            media = False

        return JsonResponse({'success': True, 'media': media})


class CompilationCreateView(LoginRequiredMixin, View):
    def get(self, requet):
        return render(requet, 'posts/form_create.html')

    def post(self, request):
        print(request.POST)
        print("____________________________________________________")
        print(datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M'))
        compilation = create_compilation(
            name=request.POST.get('name'),
            text=request.POST.get('text').replace('<p>', '').replace('</p>', ''),
            date=datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d'),
            datetime_send=datetime.datetime.strptime(request.POST.get('date_send'), '%Y-%m-%dT%H:%M'),
            done=True if request.POST.get('complete') == 'true' else False
        )
        create_log(request.user, 3, compilation)
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

        # gid = render_to_string('posts/form_gid.html', {'compilation_id': compilation.pk}, request=request)
        return redirect('compilation_detail', compilation.id)


class FinalCompilationCreateView(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST)
        if request.POST.get('visible') == 'true':
            compilation_id = request.POST.get('compilation')
            final_compilation = create_final_compilation(
                compilation_id=int(compilation_id),
                text=request.POST.get('text').replace('<p>', '').replace('</p>', '')
            )
            create_log(request.user, 3, final_compilation)
            format_file = str(request.FILES.get('media')).split('.')[-1]
            if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
                type_content = 0
            else:
                type_content = 1
            create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='final_compilation',
                to_id=final_compilation.pk
            )
        return JsonResponse({'success': True})


class PostUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        print(request.POST)
        compilation = int(request.POST.get('compilation'))
        post = int(request.POST.get('post'))

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
            price_new = request.POST['price_new_' + index] if request.POST['price_new_' + index] else None
            update_item(index, name, link, sizes, description, price_old, price_new)

        for index in list_values_add:
            name = request.POST['name_product_add_' + index]
            sizes = request.POST['sizes_add_' + index]
            link = request.POST['link_add_' + index]
            description = request.POST['description_add_' + index]
            price_old = request.POST['price_old_add_' + index]
            price_new = request.POST['price_new_add_' + index] if request.POST['price_new_add_' + index] else None
            create_item(post, name, link, sizes, description, price_old, price_new)

        format_file = str(request.FILES.get('media')).split('.')[-1]
        if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
            type_content = 0
        else:
            type_content = 1
        content = (None, None)
        if 'media' in request.FILES.keys():
            content = update_or_create_content(
                file_name=str(request.FILES.get('media')),
                file=request.FILES.get('media'),
                type_content=type_content,
                to='post',
                to_id=post
            )

        shop = request.POST.get('shop')
        currency = request.POST.get('currency')
        post = update_post(post, shop, currency)

        create_log(request.user, 1, post)

        if post.message_id:
            if content[0]:
                asyncio.run(try_send_post_to_user(
                    file_path=content[0].file.path,
                    file_type=content[0].type,
                    text=get_post_text(post),
                    chat_id=settings.CHANNEL,
                    message_id=post.message_id,
                ))
            else:
                asyncio.run(try_edit_message_caption(settings.CHANNEL, get_post_text(post), post.message_id, None))

        return redirect('compilation_detail', pk=compilation)


class PostCreateView(LoginRequiredMixin, View):
    def post(self, request):
        compilation = int(request.POST.get('compilation'))
        shop = request.POST.get('shop')
        currency = request.POST.get('currency')
        post = create_post(compilation, shop, currency)

        create_log(request.user, 0, post)

        post = post.pk

        list_values_add = []
        for key in request.POST.keys():
            if 'name_product' in key:
                if 'add' in key:
                    list_values_add.append(key.split('_')[-1])

        for index in list_values_add:
            name = request.POST['name_product_add_' + index]
            sizes = request.POST['sizes_add_' + index]
            link = request.POST['link_add_' + index]
            description = request.POST['description_add_' + index]
            price_old = request.POST['price_old_add_' + index]
            price_new = request.POST['price_new_add_' + index] if request.POST['price_new_add_' + index] else None
            create_item(post, name, link, sizes, description, price_old, price_new)

        format_file = str(request.FILES.get('media')).split('.')[-1]
        if format_file.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
            type_content = 0
        else:
            type_content = 1
        update_or_create_content(
            file_name=str(request.FILES.get('media')),
            file=request.FILES.get('media'),
            type_content=type_content,
            to='post',
            to_id=post
        )

        return redirect('compilation_detail', pk=compilation)


class CompilationDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        compilation_id = pk
        try:
            x = Compilation.objects.get(pk=compilation_id)
            posts = x.post_set.all()
            for post in posts:
                asyncio.run(try_delete_message(settings.CHANNEL, post.message_id))
            try:
                asyncio.run(try_delete_message(settings.CHANNEL, x.message_id))
            except:
                pass
            try:
                asyncio.run(try_delete_message(settings.CHANNEL, x.finalcompilation_set.first().message_id))
            except:
                pass
            create_log(request.user, 4, x)
            x.delete()

        except:
            traceback.format_exc()
        return redirect('compilation_list')


class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        post = int(request.POST.get('post'))
        try:
            x = Post.objects.get(pk=post)
            asyncio.run(try_delete_message(settings.CHANNEL, x.message_id))
            create_log(request.user, 2, x)
            x.delete()
        except:
            pass
        return JsonResponse({'status': True})


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        item = int(request.POST.get('item'))
        try:
            Item.objects.get(pk=item).delete()
        except:
            print(traceback.format_exc())
        return JsonResponse({'status': True})
