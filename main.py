import time
import cv2
import mss
import numpy as np
import easyocr
import torch
import ctypes
import win32api
from config import WISH_ITEM_POS, SUMMON_SCREEN_PATH, SUMMON_SCREEN, X1_WARP, X10_WARP , VALID_DICT

ctypes.windll.user32.SetProcessDPIAware()

prev_state = 0
press_inside = None

# A class for state management
class AppState():    
    def __init__(self):
        self.on_summon_screen = False
        self.waiting_for_next = False


def normalize_text(text):
    cleaned = " ".join(text.lower().split())
    
    if cleaned in VALID_DICT:
        return VALID_DICT[cleaned]

    if cleaned.endswith(" new"):
        cleaned_short = cleaned[:-4].strip()
        if cleaned_short in VALID_DICT:
            return VALID_DICT[cleaned_short]
    return None

if __name__ == "__main__":
    state = AppState()
    
    reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
    print(reader.lang_char)
    summon_screen = cv2.imread(SUMMON_SCREEN_PATH, cv2.IMREAD_GRAYSCALE)
    
    with mss.mss() as sct:
        count = 1
        while True:
            exchange_crop = sct.grab(SUMMON_SCREEN)
            
            # Check if we are on summon screen by matching a template unique to the summon screen
            img = np.array(exchange_crop)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            
            result = cv2.matchTemplate(img_gray, summon_screen, cv2.TM_CCOEFF_NORMED)
            
            threshold = 0.8
            loc = np.where(result >= threshold)
                
            state.on_summon_screen = len(loc[0]) > 0
            
            if state.on_summon_screen:
                print("We are on the summon screen", count)
                count += 1
            
            x, y = win32api.GetCursorPos()
            state_mouse_active = state.on_summon_screen
            
            def in_banner(x, y, box):
                top, left, w, h = box
                right, bottom = left + w, top + h
                return left <= x <= right and top <= y <= bottom
            
            state_mouse = win32api.GetKeyState(0x01)  # Left button
            # Press detection
            if state_mouse < 0 and prev_state >= 0:
                if in_banner(x, y, X1_WARP):
                    press_inside = "x1"
                elif in_banner(x, y, X10_WARP):
                    press_inside = "x10"
                else:
                    press_inside = None
            
            elif state_mouse >= 0 and prev_state < 0:
                if press_inside and state_mouse_active:
                    # Confirm release is inside same banner
                    if (press_inside == "x1" and in_banner(x, y, X1_WARP)) or (press_inside == "x10" and in_banner(x, y, X10_WARP)):
                        item_list = []
                        
                        while len(item_list) != 10:
                            
                            wish_img = sct.grab(WISH_ITEM_POS)
                            img_num = np.array(wish_img)
                            wish_item = reader.readtext(img_num, detail=0, decoder="greedy", paragraph=True, blocklist="123456890")
                            
                            print(wish_item)
                            
                            if not wish_item:
                                if not item_list:
                                    continue
                                else:
                                    state.waiting_for_next = False
                                    
                            else:          
                                if not state.waiting_for_next:
                                    text = wish_item[0]
                                    
                                    valid_item = normalize_text(text)
                                    
                                    if valid_item:
                                        item_list.append(valid_item)
                                        state.waiting_for_next = True

                            print(item_list)
                            
                        state.waiting_for_next = False
                        print(item_list)
                        
                press_inside = None
            
            prev_state = state_mouse
            
            time.sleep(0.01)