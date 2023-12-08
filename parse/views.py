# from django.shortcuts import render
from django.http import request, JsonResponse, HttpResponse
from django.shortcuts import render
from parse.json_script import parse
from .forms import UploadForm
from parse.json_script import parse



# Create your views here.
def createJson(request):
    context = parse('/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/test2')
    return JsonResponse(context)


# views.py

def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponse('The file is saved')
    else:
        form = UploadForm()
    context = {
        'form':form,
    }
    return render(request, 'upload.html', context)
