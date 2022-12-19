from django.urls import path
from .views import SettingsView, RatesView

urlpatterns = [
    path('rates/', RatesView.as_view(), name='rates'),
    path('', SettingsView.as_view(), name='settings'),
]
