from django.urls import path
from .views import UserListView, UserTableView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('table/', UserTableView.as_view(), name='table_users')
]
