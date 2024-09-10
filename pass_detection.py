import pyautogui
import time
import threading
import tkinter as tk
import cv2
import pytesseract
import numpy as np  # Import numpy for array manipulation
from PIL import ImageGrab  # For capturing screenshots

# Set the path to tesseract executable if needed (Windows)
# Replace with your Tesseract-OCR installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global flag to control the loop
running = False

# Function to capture the screen and check for "Pass" text
def check_for_pass_text():
    global running
    while running:
        # Capture the screen
        screenshot = ImageGrab.grab()
        
        # Convert the screenshot to an OpenCV image
        img_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Use Pytesseract to extract text from the image
        text = pytesseract.image_to_string(img_np)
        
        # Check if the word "Pass" is in the detected text
        if "Pass" in text:
            print("Detected 'Pass' on the screen!")
            # Press Enter if "Pass" is detected
            pyautogui.press('enter')
            print("Enter pressed")

        # Delay to avoid overwhelming the CPU
        time.sleep(1)

# Function to start the process
def start_text_detection():
    global running
    if not running:  # Only start if it's not already running
        running = True
        # Start a new thread to prevent blocking the GUI
        threading.Thread(target=check_for_pass_text).start()

# Function to stop the process
def stop_text_detection():
    global running
    running = False
    print("Stopped checking for text.")

# Create the GUI window
def create_gui():
    window = tk.Tk()
    window.title("Auto Enter Key Presser on 'Pass' Detection")

    # Create Start button
    start_button = tk.Button(window, text="Start", command=start_text_detection, width=10, height=2)
    start_button.pack(pady=10)

    # Create Stop button
    stop_button = tk.Button(window, text="Stop", command=stop_text_detection, width=10, height=2)
    stop_button.pack(pady=10)

    # Add a label to guide the user
    instruction_label = tk.Label(window, text="Detect 'Pass' on screen and press Enter")
    instruction_label.pack(pady=10)

    # Start the GUI loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
