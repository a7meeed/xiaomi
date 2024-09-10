import mss
import cv2
import numpy as np
import pytesseract
import time

# Set the path to tesseract executable if needed (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def test_screen_capture():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full-screen capture of the primary monitor
        while True:
            screenshot = sct.grab(monitor)
            img_np = np.array(screenshot)
            text = pytesseract.image_to_string(img_np, lang='eng')
            print(f"Detected text: {text}")
            time.sleep(1)

if __name__ == "__main__":
    test_screen_capture()