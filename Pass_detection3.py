import pyautogui
import time
import threading
import tkinter as tk
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab

# Set the path to tesseract executable if needed (Windows)
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
            update_status("Enter pressed")
        else:
            update_status("Waiting for 'Pass'...")

        # Delay to avoid overwhelming the CPU
        time.sleep(1)

# Function to start the process
def start_text_detection():
    global running
    if not running:  # Only start if it's not already running
        running = True
        # Start a new thread to prevent blocking the GUI
        threading.Thread(target=check_for_pass_text).start()
        update_status("Monitoring started...")

# Function to stop the process
def stop_text_detection():
    global running
    running = False
    update_status("Monitoring stopped.")

# Function to update the status label
def update_status(message):
    status_label.config(text=message)

# Function to clear the status
def clear_status():
    status_label.config(text="")

# Create the GUI window
def create_gui():
    global status_label
    
    window = tk.Tk()
    window.title("Auto Enter Key Presser on 'Pass' Detection")

    # Create Start button
    start_button = tk.Button(window, text="Start", command=start_text_detection, width=10, height=2)
    start_button.pack(pady=10)






    # Create Stop button
    stop_button = tk.Button(window, text="Stop", command=stop_text_detection, width=10, height=2)
    stop_button.pack(pady=10)

    # Create Clear button
    clear_button = tk.Button(window, text="Clear", command=clear_status, width=10, height=2)
    clear_button.pack(pady=10)

    # Add a label to display the status
    status_label = tk.Label(window, text="Press 'Start' to begin monitoring")
    status_label.pack(pady=10)

    # Start the GUI loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()

