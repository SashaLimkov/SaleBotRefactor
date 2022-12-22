from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.profiles.models import Rate


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'


class RatesView(LoginRequiredMixin, ListView):
    template_name = 'rates.html'
    model = Rate
    context_object_name = 'rates'
