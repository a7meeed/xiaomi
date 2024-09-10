import pyautogui
import time
import threading
import tkinter as tk
import numpy as np
from PIL import ImageGrab, Image, ImageTk
import cv2

# Global flag to control the loop and selected region
running = False
selected_region = None

# Screen selection helper class
class ScreenSelector(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect_id = None
        self.preview_id = None
        self.canvas = tk.Canvas(self, cursor="cross", bg='grey', relief='raised')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.title("Select Region")
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)
        self.grab_set()
        self.update_preview()  # Show initial screen preview
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
        self.update_preview()

    def on_button_release(self, event):
        self.end_x, self.end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.destroy()

    def get_coordinates(self):
        x1, y1, x2, y2 = self.start_x, self.start_y, self.end_x, self.end_y
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        return (int(x1), int(y1), int(x2), int(y2))

    def update_preview(self):
        try:
            # Capture the screen
            screen = ImageGrab.grab()
            img_np = np.array(screen)
            preview_img = Image.fromarray(img_np)

            # Update preview image on canvas
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            preview_photo = ImageTk.PhotoImage(preview_img)
            self.preview_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=preview_photo)
            self.canvas.image = preview_photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            print(f"Error updating preview: {e}")

# Function to check for the red color in the selected region
def check_for_red_color():
    global running, selected_region
    while running:
        if selected_region:
            x1, y1, x2, y2 = selected_region
            try:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                img_np = np.array(screenshot)

                hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
                lower_red1 = np.array([0, 50, 50])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([160, 50, 50])
                upper_red2 = np.array([180, 255, 255])
                mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                red_mask = mask1 | mask2

                # Debugging: Show the mask
                cv2.imshow("Red Mask", red_mask)
                cv2.waitKey(1)

                red_pixels = np.any(red_mask)

                if red_pixels:
                    print("Red color detected. Waiting for removal...")
                    start_time = time.time()
                    while red_pixels and running:
                        time.sleep(0.1)
                        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                        img_np = np.array(screenshot)
                        hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
                        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                        red_mask = mask1 | mask2
                        red_pixels = np.any(red_mask)
                    if running and time.time() - start_time >= 1:
                        pyautogui.press('enter')
                        update_status_async("Enter pressed")
                        print("Enter key pressed.")
                else:
                    print("No red color detected. Checking for 1 second...")
                    start_time = time.time()
                    while not red_pixels and running:
                        time.sleep(0.1)
                        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                        img_np = np.array(screenshot)
                        hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
                        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                        red_mask = mask1 | mask2
                        red_pixels = np.any(red_mask)
                        if time.time() - start_time >= 1:
                            pyautogui.press('enter')
                            update_status_async("Enter pressed")
                            print("Enter key pressed.")
                            break

            except Exception as e:
                print(f"Error: {e}")

        time.sleep(0.1)

# Function to let the user select the screen region
def select_screen_region():
    global selected_region
    update_status_async("Select a region for monitoring...")
    selector = ScreenSelector(window)
    selected_region = selector.get_coordinates()
    update_status_async(f"Selected region: {selected_region}")

# Function to start the process
def start_text_detection():
    global running
    if not running and selected_region:
        running = True
        threading.Thread(target=check_for_red_color, daemon=True).start()
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
    window.title("Red Color Detection and Enter Key Press")
    window.attributes('-topmost', True)

    select_button = tk.Button(window, text="Select Region", command=select_screen_region, width=15, height=2)
    select_button.pack(pady=10)

    start_button = tk.Button(window, text="Start", command=start_text_detection, width=10, height=2)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop", command=stop_text_detection, width=10, height=2)
    stop_button.pack(pady=10)

    clear_button = tk.Button(window, text="Clear", command=clear_status, width=10, height=2)
    clear_button.pack(pady=10)

    global status_label
    status_label = tk.Label(window, text="Press 'Select Region' to define area")
    status_label.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
