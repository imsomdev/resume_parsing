from django.shortcuts import render, redirect
from django.http import request, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from parse.json_script import parse
from parse.delete_file import delete
from .forms import UploadForm
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import FileSerializer
import os


def createJson(request):
    path = '/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/upload_and_parse/parse_api/parse_api/media/documents/'
    context = parse(path)
    delete(path)
    return JsonResponse(context)


def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        file_name = request.FILES['file'].name
        # print(file_name)
        if form.is_valid():
            form.save()
        return redirect ('createJson')
    else:
        form = UploadForm()
    context = {
        'form':form,
    }
    return render(request, 'upload.html', context)


#Upload using API

def responseHelper():
    path = '/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/upload_and_parse/parse_api/parse_api/media/documents/'
    context = parse(path)
    delete(path)
    return Response(context)


class FileUploadViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer_class = FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            handle_uploaded_file(request.FILES['file'])
            # res = 
            return responseHelper()


def handle_uploaded_file(f):
    destination_directory = '/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/upload_and_parse/parse_api/parse_api/media/documents/'
    destination_path = os.path.join(destination_directory, f.name)

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    with open(destination_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
