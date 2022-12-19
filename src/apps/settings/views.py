from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'


class RatesView(LoginRequiredMixin, TemplateView):
    template_name = 'rates.html'
