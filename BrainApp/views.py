from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .h5_loading import load_h5_file



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



            
        file_name, error = load_h5_file(file, 'media')

        if error:
            return render(request, 'home.html', {'error': error})
        

        return render(request, 'home.html', {
            'image_url': f'/media/{file_name}'   })
            

           
               
        
    else: 
                
                return render (request, 'home.html',{
                    'error':'No file selected'
                })
        
    return render(request, 'home.html')
        

    
