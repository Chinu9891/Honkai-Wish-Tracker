import cv2
import numpy as np
from PIL import Image

#Converts an MSS screenshot into either a PIL image or a NumPy array (grayscale)
def sct_to_image(sct_img, gray=False):
    img = np.array(sct_img)
    if gray:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    return Image.fromarray(img_rgb)