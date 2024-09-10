import pyautogui
import time
import threading
import tkinter as tk
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab, Image

# Set the path to tesseract executable if needed (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global flag to control the loop and selected region
running = False
selected_region = None

# Screen selection helper class
class ScreenSelector(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect_id = None
        self.canvas = tk.Canvas(self, cursor="cross", bg='grey', relief='raised')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.title("Select Region")
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)
        self.grab_set()
        self.wait_window(self)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        cur_x, cur_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x, self.end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.destroy()

    def get_coordinates(self):
        x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
        # Ensure the coordinates are in correct order
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        return (int(x1), int(y1), int(x2), int(y2))

# Function to capture the selected region of the screen and check for "Pass" text
def check_for_pass_text():
    global running, selected_region
    while running:
        if selected_region:
            x1, y1, x2, y2 = selected_region

            # Capture the specific region of the screen
            try:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                # Convert the screenshot to an OpenCV image
                img_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                # Use Pytesseract to extract text from the image
                text = pytesseract.image_to_string(img_np)

                # Check if the word "Pass" is in the detected text
                if "Pass" in text:
                    print("Detected 'Pass' on the screen!")
                    # Press Enter if "Pass" is detected
                    pyautogui.press('enter')
                    update_status_async("Enter pressed")
                else:
                    update_status_async("Waiting for 'Pass'...")

            except ValueError as e:
                print(f"Error: {e}")

        # Delay for 0.1 seconds to control the screenshot frequency
        time.sleep(0.1)

# Function to let the user select the screen region
def select_screen_region():
    global selected_region
    update_status_async("Select a region for monitoring...")

    # Open the screen selector window
    selector = ScreenSelector(window)
    
    # Get the selected region coordinates
    selected_region = selector.get_coordinates()
    update_status_async(f"Selected region: {selected_region}")

# Function to start the process
def start_text_detection():
    global running
    if not running and selected_region:  # Only start if it's not already running and region is selected
        running = True
        # Start a new thread to prevent blocking the GUI
        threading.Thread(target=check_for_pass_text, daemon=True).start()
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
    global status_label, window
    
    window = tk.Tk()
    window.title("Auto Enter Key Presser on 'Pass' Detection")

    # Make the window always on top
    window.attributes('-topmost', True)

    # Create Select Region button
    select_button = tk.Button(window, text="Select Region", command=select_screen_region, width=15, height=2)
    select_button.pack(pady=10)

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
    status_label = tk.Label(window, text="Press 'Select Region' to define area")
    status_label.pack(pady=10)

    # Start the GUI loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
