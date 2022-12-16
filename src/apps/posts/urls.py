from django.urls import path
from .views import CompilationListView, CompilationTableView

urlpatterns = [
    path('', CompilationListView.as_view(), name='compilation_list'),
    path('table/', CompilationTableView.as_view(), name='table_compilations')
]
