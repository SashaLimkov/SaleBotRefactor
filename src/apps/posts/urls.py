from django.urls import path
from .views import CompilationListView, CompilationTableView, CompilationDetailView, FinalCompilationSaveView,\
                    CompilationCreateView, FinalCompilationCreateView, PostUpdateView, PostCreateView,\
                    CompilationDeleteView, PostDeleteView

urlpatterns = [
    path('', CompilationListView.as_view(), name='compilation_list'),
    path('<int:pk>', CompilationDetailView.as_view(), name='compilation_detail'),
    path('create/', CompilationCreateView.as_view(), name='compilation_create'),
    path('final/', FinalCompilationCreateView.as_view(), name='compilation_final_create'),
    path('final/<int:pk>', FinalCompilationSaveView.as_view(), name='compilation_final_detail'),
    path('table/', CompilationTableView.as_view(), name='table_compilations'),
    path('post/', PostUpdateView.as_view(), name='update_post'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('delete_compilatiom/', CompilationDeleteView.as_view(), name='delete_compilation'),
    path('delete_post/', PostDeleteView.as_view(), name='delete_post')
]
