from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.FileUploadViewSet, basename='file')

urlpatterns = [
    path('create-json',views.createJson, name='createJson'),
    path('upload', views.uploadFile, name='uploadFile'),
	path('upload_api', include(router.urls)),

]
