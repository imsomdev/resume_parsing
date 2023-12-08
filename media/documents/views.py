from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import UploadForm


def uploadFile(request):
    if request.method == 'POST' and request.FILES.get('file'):
        # form = UploadForm(request.POST,request.FILES)
        print(request.FILES['file'].read())
        # if form.is_valid():
        #     form.save()
    return HttpResponse(request.FILES['file'].read())
    # else:
    #     form = UploadForm()
    #     context = {
    #         'form':form,
    #     }
    # return render(request, 'upload.html', context)


def sortlistCv(request):
    context = {
        'key':'value'
    }
    return JsonResponse(context)