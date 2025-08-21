import cv2
import mss
import mss.tools
import numpy as np
import pytesseract
from PIL import Image

class Helper:
    def capturePart(pos):
        with mss.mss() as sct: 
            while True:
                monitor = {
                    "top": pos[0],
                    "left": pos[1],
                    "width": pos[2],
                    "height": pos[3]
                }
                sct_img = sct.grab(monitor)

                img = np.array(sct_img)  # BGRA
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
                pil_img = Image.fromarray(img_rgb)

                extracted_text = pytesseract.image_to_string(pil_img).strip()
                print(extracted_text)

    def getPartPos(file_name):
        icon_template = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
        template_height, template_width = icon_template.shape[:2]
        with mss.mss() as sct:
            while True:
                monitor = sct.monitors[1]
                
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                
                result = cv2.matchTemplate(img_gray, icon_template, cv2.TM_CCOEFF_NORMED)
                
                threshold = 0.8
                
                loc = np.where(result >= threshold)

                if len(loc[0]) > 0:
                    top_left = (loc[1][0], loc[0][0])
                    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                    
                    print(f"Icon detected at:")
                    print(f"Top: {top_left[1]}, Left: {top_left[0]}")
                    print(f"Width: {template_width}, Height: {template_height}")
                    
                    # Optional: draw rectangle for visualization
                    cv2.rectangle(img, top_left, bottom_right, 255, 2)
                    cv2.imshow("Detected", img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break

    def captureFull():
        x = 1
        with mss.mss() as sct:
            while True:
                monitor = sct.monitors[1] 
                output = f"img_{x}.png"
                x += 1

                sct_img = sct.grab(monitor)
                
                
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

                print(f"Saved {output}")

    def matchTemplate(template_name):
        icon_template = cv2.imread(template_name, cv2.IMREAD_GRAYSCALE)
        with mss.mss() as sct:
            while True:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                
                result = cv2.matchTemplate(img_gray, icon_template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                
                loc = np.where(result >= threshold)

                if len(loc[0]) > 0:
                    print('DETECTED!!!!!!')
                    break