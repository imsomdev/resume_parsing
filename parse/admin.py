from django.contrib import admin
from .models import Upload

# Register your models here.
class UploadAdmin(admin.ModelAdmin):
    list_display = ('file',)

admin.site.register(Upload, UploadAdmin)