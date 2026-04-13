from .UNet_loader import model
import numpy as np



def  run_Unet(mri_image_4C):

    # convert to float32

    mri_image_4C = mri_image_4C.astype('float32')


    # normalize per channel

    for i in range(4):

        channel = mri_image_4C[:,:,i]

        min_val = np.min(channel)
    
        max_val = np.max(channel)
    
        if max_val > min_val:

            mri_image_4C[:,:,i] = (channel - min_val) / (max_val - min_val)


    # add batch size

    mri_input = np.expand_dims(mri_image_4C, axis=0)


    # prediction

    pred = model.predict(mri_input)


    # remove batch from dimensions

    pred =pred[0]


    # create the mask

    mask = np.argmax(pred, axis=-1)

    return mask