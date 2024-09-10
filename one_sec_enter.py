import pyautogui
import time
import keyboard  # to detect key presses

def press_enter_every_second():
    while True:
        # Check if the 'Esc' key is pressed to exit
        if keyboard.is_pressed('esc'):
            print("Esc pressed, exiting the program.")
            break
        
        # Press the Enter key
        pyautogui.press('enter')
        print("Enter pressed")
        
        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":
    print("Pressing 'Enter' every 1 second... (Press Esc to stop)")
    press_enter_every_second()
