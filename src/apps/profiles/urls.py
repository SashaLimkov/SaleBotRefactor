from django.urls import path
from .views import ProfileListView, ProfileTableView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile_list'),
    path('<int:pk>', ProfileDetailView.as_view(), name='profile_detail'),
    path('table/', ProfileTableView.as_view(), name='table_profiels'),

]
