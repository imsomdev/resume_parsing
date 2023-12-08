from django.shortcuts import render, redirect
from django.http import request, JsonResponse, HttpResponse
from django.shortcuts import render
from parse.json_script import parse
from .forms import UploadForm


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
        # return redirect ('createJson')
    else:
        form = UploadForm()
    context = {
        'form':form,
    }
    return render(request, 'upload.html', context)
