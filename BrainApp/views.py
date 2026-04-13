

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .h5_loading import load_h5_file
from .LLM_API import llm_response
from .U_NET import run_Unet
import numpy as np

from PIL import Image
import os



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

            
        file_name, mri_image_4C, mri_display, error = load_h5_file(file, 'media')

        if error:
            return render(request, 'home.html', {'error': error})
        


        #edge case to 
        llm_output = None
        overlay_path = None
        Unet_success = False


        #settiing error to default none
        unet_error = None
        llm_error = None
        



        try:


            #run unet and get the mask

            mask = run_Unet(mri_image_4C)


        
            #convert mask to rgbp

            mri_color = np.stack([mri_display]  * 3, axis=-1)



            #adding thhe colors to the mask

            color_mask = np.zeros_like(mri_color)

            color_mask[mask == 1] = [255, 0, 0]  #red

            color_mask[mask == 2] = [0, 255, 0] # green

            color_mask[mask == 3] = [0, 0, 255] # blue



            #overlay
            alpha = 0.35

            overlay = ((1- alpha) * mri_color + alpha * color_mask).astype(np.uint8)
        
        
            overlay_mask = Image.fromarray(overlay)
        

            overlay_path = os.path.join('media', 'overlay.png')


            #save overlay as image

            overlay_mask.save(overlay_path)
        


            #error handling for unet
            Unet_success = True

        except Exception as e:
            Unet_success = False
            overlay_path = None
            unet_error = "Sorry but the System was not able to perform tumor detection"
            llm_output = None







        if Unet_success:

             try:
        
                 #LLM RESPONSE 

                llm_output = llm_response(overlay_path)



                if not llm_output:
                     llm_output = "Sorry service is currently unavailable"


             except Exception :
                llm_error = "Sorry but there was an error with the LLM response: "
        
      


        return render(request, 'home.html', {
            'image_url': f'/media/{file_name}' ,
            'overlay_url': f'/{overlay_path}' if overlay_path else None,
              'llm_output': llm_output,
            'unet_error': unet_error,
            'llm_error': llm_error

     })
            

           
               
  
        

    
