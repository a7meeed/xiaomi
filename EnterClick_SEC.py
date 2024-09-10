import pyautogui
import pytesseract
import time
from PIL import ImageGrab

# Set up the path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_message_and_press_enter():
    while True:
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()

        # Use pytesseract to detect text in the screenshot
        text = pytesseract.image_to_string(screenshot)

        # Check if "Pass" or "Fail" is in the text
        if "Pass" in text or "Fail" in text:
            print(f"Message detected: {text.strip()}")
            
            
            # Press Enter key
            pyautogui.press('enter')

        # Wait for 2 seconds before checking again
        time.sleep(2)

if __name__ == "__main__":
    print("Monitoring for 'Pass' or 'Fail' messages...")
    detect_message_and_press_enter()
