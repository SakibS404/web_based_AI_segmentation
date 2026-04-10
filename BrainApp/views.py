from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage



# Create your views here.
def home(request):
    return render(request,"home.html")


def file_upload(request):
    if request.method == 'POST':

        file = request.FILES.get('file')


        if not file:
             return render(request, 'home.html')
        

        if file.size == 0:
            return render(request, 'home.html', {
                'error': 'The uploaded file is empty.'
            })
        

        
        if file.size > 1 * 1024 * 1024:
             return render(request, 'home.html', {
                 
                 'error': 'The Filesize exceeds the limit of 5MB.'

             })



            
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        image_url = fs.url(filename)

        return render(request, 'home.html', {'image_url': image_url})

           
               
        
    else: 
                
                return render (request, 'home.html',{
                    'error':'No file selected'
                })
        
    return render(request, 'home.html')
        

    
