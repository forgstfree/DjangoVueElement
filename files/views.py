from django.shortcuts import render, HttpResponse
from .forms import UploadFileForm
# Create your views here.

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print(file.name)
            print(file.size)
            with open('gst01', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return HttpResponse('OK')
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html',{'form':form})

