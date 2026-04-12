from xmlrpc import client

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .h5_loading import load_h5_file
from .LLM_API import llm_response



# Create your views here.
def home(request):
    return render(request,"home.html")


def file_upload(request):
    if request.method == 'POST':

        file = request.FILES.get('file')




        # Check if a file was uploaded
        if not file:
             
             return render(request, 'home.html')
        


        # check if file is h5
        if not file.name.endswith('.h5'):
             
             return render(request, 'home.html', {
                    'error': 'Invalid file type. Please upload a .h5 file.'
                })




        

        #check if the file is empty or not
        if file.size == 0:

            return render(request, 'home.html', {
                'error': 'The uploaded file is empty.'
            })
        

        
        
        

        
        #limit file size to 1MB 
        if file.size > 1 * 1024 * 1024:
             
             return render(request, 'home.html', {
                 
                 'error': 'The Filesize exceeds the limit of 1MB.'

             })






        #file check

            
        file_name, error = load_h5_file(file, 'media')

        if error:
            return render(request, 'home.html', {'error': error})
        




        #LLM RESPONSE 

        image_path = f"media/{file_name}"

        llm_output = llm_response(image_path)

        if not llm_output:
            llm_output = "Sorry service is currently unavailable"



        
        

        return render(request, 'home.html', {
            'image_url': f'/media/{file_name}' ,
              'llm_output': llm_output  })
            

           
               
  
        

    
