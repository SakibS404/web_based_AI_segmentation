import tensorflow as tf




#dice loss

def dice_loss(y_true, y_pred, smooth=1e-6):

  #remove background
    y_true = y_true[..., 1:]
    y_pred = y_pred[..., 1:]



    # per batch

    intersection = tf.reduce_sum(y_true * y_pred, axis=[1,2])
    denominator = tf.reduce_sum(y_true + y_pred, axis=[1,2])

    dice_loss = (2. * intersection + smooth) / (denominator + smooth)

    return 1 - tf.reduce_mean(dice_loss)





#custom weighted crossentropy

def weighted_cce(y_true, y_pred):




    # weights for each label
    weights = tf.constant([0.1, 1.3, 1.0, 1.0], dtype=tf.float32)

    cce = tf.keras.losses.categorical_crossentropy(y_true,y_pred)

    #adding weights to the pixles
    pixle_weights = tf.reduce_sum(y_true * weights, axis=-1)






    return tf.reduce_mean(cce * pixle_weights)




#custom loss

def custom_loss(y_true, y_pred):


  cce = weighted_cce(y_true, y_pred)

  dice = dice_loss(y_true, y_pred)

  return  cce * 0.75 +  dice * 0.25


