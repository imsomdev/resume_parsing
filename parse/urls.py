from . import views
from django.urls import path

urlpatterns = [
    path('',views.createJson, name='create-json'),
    path('upload', views.uploadFile, name='uploadFile')
]
