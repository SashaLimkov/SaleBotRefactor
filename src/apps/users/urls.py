from django.urls import path
from .views import UserListView, UserTableView, UserDetailView, UserAuthView, UserLogoutView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('table/', UserTableView.as_view(), name='table_users'),
    path('auth/', UserAuthView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout')
]
