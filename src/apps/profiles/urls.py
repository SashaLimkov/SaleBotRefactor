from django.urls import path
from .views import ProfileListView, ProfileTableView

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile_list'),
    path('table/', ProfileTableView.as_view(), name='table_profiels')
]
