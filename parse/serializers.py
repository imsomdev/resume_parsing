from rest_framework import serializers
from .models import Upload

# class FileSerializer(serializers.Serializer):
#     file = serializers.FileField(max_length=None, allow_empty_file=False)

class UploadSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'