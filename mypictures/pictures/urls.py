from django.urls import path

from . import views


app_name = 'pictures'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('file_search', views.FileSearch.as_view(), name='file_search'),
    path('upload', views.upload, name='file_upload'),
]
