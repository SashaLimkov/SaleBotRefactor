from django.urls import path
from .views import CompilationListView, CompilationTableView, CompilationDetailView

urlpatterns = [
    path('', CompilationListView.as_view(), name='compilation_list'),
    path('<int:pk>', CompilationDetailView.as_view(), name='compilation_detail'),
    path('table/', CompilationTableView.as_view(), name='table_compilations')
]
