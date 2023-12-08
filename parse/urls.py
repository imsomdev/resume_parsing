from . import views
from django.urls import path

urlpatterns = [
    path('create-json',views.createJson, name='createJson'),
    path('upload', views.uploadFile, name='uploadFile')
]
