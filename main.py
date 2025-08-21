import cv2
import mss
import numpy as np
import pytesseract
from utils import sct_to_image
from config import BANNER_POS, WISH_POS, VALID_BANNERS, WISH_TEMPLATE_PATH

#A class for tracking the last seen banner type
class AppState():    
    def __init__(self):
        self.banner_type = None
        
if __name__ == "__main__":
    state = AppState()
    wish_template = cv2.imread(WISH_TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    
    if wish_template is None:
        raise FileNotFoundError(f"Wish template not found at {WISH_TEMPLATE_PATH}")
    
    with mss.mss() as sct:
        banner_position = {
                    "top": BANNER_POS[0],
                    "left": BANNER_POS[1],
                    "width": BANNER_POS[2],
                    "height": BANNER_POS[3]
                }
        
        wish_position = {
                    "top": WISH_POS[0],
                    "left": WISH_POS[1],
                    "width": WISH_POS[2],
                    "height": WISH_POS[3]
                }
        
        while True:
            sct_img = sct.grab(banner_position)
            
            pil_img = sct_to_image(sct_img)
            
            custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
            
            banner_type = pytesseract.image_to_string(pil_img, lang='eng', config=custom_config).strip()

            #if the banner type is one of the following, save it in the global state
            if banner_type in VALID_BANNERS:
                
                state.banner_type = banner_type
            
            if state.banner_type != None:
                sct_img = sct.grab(wish_position)
                
                img_gray = sct_to_image(sct_img, True)
                
                result = cv2.matchTemplate(img_gray, wish_template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                
                loc = np.where(result >= threshold)

                #if we detect a wish template, then last seen banner type *must* be the correct banner
                if len(loc[0]) > 0:
                    print(f'The user just wished on a {state.banner_type} banner!')
                    state.banner_type = None