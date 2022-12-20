from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DetailView

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.core.paginator import Paginator

from apps.users.services.users import get_search_users_queryset, get_all_users_queryset
from apps.utils.services.paginator import get_paginator_context
from django.contrib.auth import authenticate, login, logout


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserTableView(LoginRequiredMixin, View):
    def post(self, request):
        queryset = None

        search = request.POST.get('search', '')
        page = int(request.POST.get('page', 1))

        if len(search) >= 3:
            queryset = get_search_users_queryset(search)
        if not queryset and not search:
            queryset = get_all_users_queryset()

        paginator = Paginator(queryset, 50)
        queryset = paginator.page(page)
        context_paginator = get_paginator_context(page, paginator.num_pages)

        context = {'rows': queryset}
        data = {
            'rows': render_to_string('users/row.html', context, request=request),
            'paginator': render_to_string('partials/paginator.html', context_paginator, request=request)
        }
        return JsonResponse(data)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/form.html'


class UserAuthView(View):
    def get(self, request):
        return render(request, 'auth/auth-login.html')

    def post(self, request):
        username = request.POST['input-username']
        password = request.POST['password-input']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/auth-login.html', context={'error': True})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
