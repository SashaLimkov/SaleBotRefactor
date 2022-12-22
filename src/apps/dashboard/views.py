from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/main.html'

    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'dashboard/main.html')
        else:
            return redirect('compilation_list')