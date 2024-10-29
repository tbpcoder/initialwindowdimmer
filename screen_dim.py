import cv2
import numpy as np
from PIL import ImageGrab
import screen_brightness_control as sbc
import tkinter as tk

# Function to capture the screen and calculate the average brightness
# Function to capture the screen and calculate the average brightness
def get_average_brightness():
    try:
        # Capture the screen
        screen = ImageGrab.grab()  # Capture the entire screen
        screen_np = np.array(screen)  # Convert to a numpy array

        # Convert the image from RGB to BGR (OpenCV format)
        frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # Calculate the average brightness (in grayscale)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = gray_frame.mean()
        
        return avg_brightness
    except KeyboardInterrupt:
        print("Screen capture interrupted by user.")
        raise  # Re-raise the exception if you want to handle it further up the call stack
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None  # Return None if an error occurs

# Function to calculate the target brightness
def calctargetbrightness(avg_brightness, sensitivity):
    try:
        res = 1 - (avg_brightness * sensitivity / 2550)
        return res * 100
    except Exception as e:
        print(f"Error calculating target brightness: {e}")
        return None

# Function to adjust screen brightness based on average brightness (inverse logic)
def adjust_brightness():
    try:
        if not paused:  # Only adjust brightness if not paused
            avg_brightness = get_average_brightness()
            if avg_brightness is None:  # Check for errors in getting average brightness
                return None, None
            
            print(f"Average Brightness: {avg_brightness}")

            target_brightness = calctargetbrightness(avg_brightness, sensitivity.get())

            # Cap the target brightness at the maximum brightness allowed
            max_brightness = max_brightness_slider.get() * 10  # Scale from 0-10 to 0-100
            target_brightness = min(target_brightness, max_brightness)

            # Set screen brightness
            sbc.set_brightness(target_brightness)
            print(f"Adjusted screen brightness to: {target_brightness}%")
            
            return avg_brightness, target_brightness  # Return both values for display
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
    
    # Ensure we return a tuple, even if an error occurs
    return None, None

# Function to update the display with current brightness values
def update_display():
    avg_brightness, target_brightness = adjust_brightness()
    if avg_brightness is not None and target_brightness is not None:
        brightness_text.set(f"Avg Brightness: {avg_brightness:.2f}\nAdjusted Brightness: {target_brightness:.2f}%")
    root.after(1000, update_display)  # Update every second

# Function to toggle pause state
def toggle_pause():
    global paused
    paused = not paused  # Toggle the pause state
    pause_button.config(text="Play" if paused else "Pause")  # Change button text

# Setting up the Tkinter GUI
root = tk.Tk()
root.title("Screen Brightness Monitor")
root.geometry("400x400")  # Adjusted Height for better layout
root.configure(bg="#2E2E2E")  # Dark background color

# Default values
default_sensitivity = 7
default_max_brightness = 8  # Corresponds to 80%

# Sensitivity slider
sensitivity = tk.IntVar(value=default_sensitivity)
sensitivity_label = tk.Label(root, text="Sensitivity (1-10):", bg="#2E2E2E", fg="white", font=("Helvetica", 12))
sensitivity_label.pack(pady=(20, 5))
sensitivity_slider = tk.Scale(root, from_=1, to=10, orient='horizontal', variable=sensitivity, bg="#4A4A4A", fg="white", sliderlength=20, length=300)
sensitivity_slider.pack(pady=(0, 20))

# Max brightness slider
max_brightness_slider = tk.IntVar(value=default_max_brightness)
max_brightness_label = tk.Label(root, text="Max Brightness (0-10):", bg="#2E2E2E", fg="white", font=("Helvetica", 12))
max_brightness_label.pack(pady=(10, 5))
max_brightness_slider = tk.Scale(root, from_=0, to=10, orient='horizontal', variable=max_brightness_slider, bg="#4A4A4A", fg="white", sliderlength=20, length=300)
max_brightness_slider.pack(pady=(0, 20))

# Display for brightness values
brightness_text = tk.StringVar()
label = tk.Label(root, textvariable=brightness_text, font=("Helvetica", 14), bg="#2E2E2E", fg="cyan")
label.pack(expand=True, fill='both', padx=20, pady=(10, 20))

# Pause/Play button
paused = False  # Initialize the paused state
pause_button = tk.Button(root, text="Pause", command=toggle_pause, bg="#FF5733", fg="white", font=("Helvetica", 12), relief="raised", bd=3)
pause_button.pack(pady=(10, 20))

if __name__ == "__main__":
    print("Running screen dimmer in the background...")
    try:
        update_display()  # Start the display update
        root.mainloop()  # Start the Tkinter event loop
    except KeyboardInterrupt:
        print("Application stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting the application.")
