from django.shortcuts import render, redirect
from django.http import request, JsonResponse, HttpResponse
from django.shortcuts import render
from parse.json_script import parse
from .forms import UploadForm
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import FileSerializer


# Create your views here.
def createJson(request):
    context = parse('/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/upload_and_parse/parse_api/parse_api/media/documents/')
    
    return JsonResponse(context)


# views.py

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


class FileUploadViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer_class = FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            handle_uploaded_file(request.FILES['file'])

            return Response(status=status.HTTP_201_CREATED)

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
