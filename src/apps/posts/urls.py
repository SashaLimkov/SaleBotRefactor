from django.urls import path
from .views import CompilationListView, CompilationTableView, CompilationDetailView, FinalCompilationSaveView,\
                    CompilationCreateView, FinalCompilationCreateView

urlpatterns = [
    path('', CompilationListView.as_view(), name='compilation_list'),
    path('<int:pk>', CompilationDetailView.as_view(), name='compilation_detail'),
    path('create/', CompilationCreateView.as_view(), name='compilation_create'),
    path('final/', FinalCompilationCreateView.as_view(), name='compilation_final_create'),
    path('final/<int:pk>', FinalCompilationSaveView.as_view(), name='compilation_final_detail'),
    path('table/', CompilationTableView.as_view(), name='table_compilations')
]
