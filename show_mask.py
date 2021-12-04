from matplotlib import pyplot as plt
from skimage import io
import os

image = io.imread('masks/mask_01.png')
io.imshow(image) 
io.show()