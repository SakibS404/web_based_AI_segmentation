import tensorflow as tf
from tensorflow.keras.models import load_model

import os

from .UNet_losses import custom_loss, weighted_cce, dice_loss




#find the absolute path for U-Net model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# create full file path using the  base dir and  file name
Model_path = os.path.join(BASE_DIR, "brain_tumor_UNet_Model.keras")


#load the model and pass the custom loss functions
model = load_model(
    Model_path,
    custom_objects={
        "custom_loss":custom_loss,"weighted_cce":weighted_cce,
        "dice_loss":dice_loss},compile=False)