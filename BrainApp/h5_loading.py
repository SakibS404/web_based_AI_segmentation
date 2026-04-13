import h5py
import numpy as np
from PIL import Image
import os


def load_h5_file(file, media_root):


    
    try:

        #loading and reading the h5 file
        with h5py.File(file, 'r') as f:
            if 'image' not in f:
                return None,"Missing MRI image data"
            
            #only  loading the image  not the mask  
            mri_image = f['image'][:]

            #saving a copy of the 4 modality image
            mri_image_4C = mri_image.copy()


    #checking image shape
        if mri_image.shape != (240, 240,4):
            return None, None, "Image shape is invalid please check the file requirements"
    

    # take one of the channels to display
        mri_image = mri_image[:,:,0]


        #applying min max normalization to scale pixles and converting value to unit8
        mri_image = (mri_image - mri_image.min()) / (mri_image.max() - mri_image.min()) 
        mri_image = (mri_image * 255).astype(np.uint8)
       



    #converting single channel into image
        img = Image.fromarray(mri_image)

    #saving the image to media folder
        output_path = os.path.join(media_root, 'uploaded_image.png')
        img.save(output_path)

        return "uploaded_image.png", mri_image_4C,mri_image, None

    except Exception as e:

        return None, None, None, str(e)
            