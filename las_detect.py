import mss
import cv2
import numpy as np
import pytesseract
import pyautogui
import tkinter as tk
import threading
import time

# Set the path to tesseract executable if needed (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global flag to control the loop
running = False

# Function to capture the screen and check for "Pass" text
def check_for_pass_text():
    global running
    with mss.mss() as sct:
        while running:
            # Capture the screen
            screenshot = sct.shot(output='screenshot.png')

            # Convert the screenshot to an OpenCV image
            img_np = cv2.imread('screenshot.png')

            # Use Pytesseract to extract text from the image
            text = pytesseract.image_to_string(img_np, lang='eng')

            # Print the detected text for debugging
            print(f"Detected text: {text}")

            # Check if the word "Pass" is in the detected text
            if "Pass" in text:
                print("Detected 'Pass' on the screen!")
                # Press Enter if "Pass" is detected
                pyautogui.press('enter')
                update_status_async("Enter pressed")
            else:
                update_status_async("Waiting for 'Pass'...")

            # Delay to avoid overwhelming the CPU
            time.sleep(0.1)

# Function to start the process
def start_text_detection():
    global running
    if not running:  # Only start if it's not already running
        running = True
        # Start a new thread to prevent blocking the GUI
        threading.Thread(target=check_for_pass_text).start()
        update_status_async("Monitoring started...")

# Function to stop the process
def stop_text_detection():
    global running
    running = False
    update_status_async("Monitoring stopped.")

# Function to update the status label asynchronously
def update_status_async(message):
    status_label.after(0, update_status, message)

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

    # Make the window always on top
    window.attributes('-topmost', True)

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
    global status_label
    status_label = tk.Label(window, text="Press 'Start' to begin monitoring")
    status_label.pack(pady=10)

    # Start the GUI loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
