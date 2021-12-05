from skimage.util.dtype import img_as_ubyte
from skimage import transform as tf
from face_change.preprocess import preprocess
import numpy as np


def trans(face, img, mask, mask_indices):
    dest, src, mask_image = preprocess(face, mask, mask_indices)

    # get the perspective transformation matrix
    # h, mask = cv2.findHomography(src[0:5], dest[0:5], cv2.RANSAC,5.0)
    transformer = tf.AffineTransform()
    transformer.estimate(dest[:5], src[:5])
    
    # transformed masked image
    # maskReg  = cv2.warpPerspective(mask_image, h, (img.shape[1], img.shape[0]))
    maskReg = tf.warp(mask_image, transformer, output_shape=img.shape)
    maskReg = img_as_ubyte(maskReg)
    

    flag_channel = maskReg[..., -1]
    flag_channel = np.expand_dims(flag_channel, -1)
    flag_channel = np.concatenate([flag_channel]*3, -1)
    img = np.where(flag_channel, maskReg[..., :-1], img)

    return img

