from django.urls import path

from . import views


app_name = 'pictures'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('file_search', views.search, name='file_search'),
    path('search_result/<str:keyword>', views.FileSearch.as_view(), name='search_result'),
    path('upload', views.upload, name='file_upload'),
    path('delete/<int:pk>', views.remove, name='file_remove'),
    path('file/<str:filename>', views.get_file, name='get_file'),
]
