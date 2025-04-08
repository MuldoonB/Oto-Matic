from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os
import time

button = Button(26)
path_var = '/home/pi/photos'
camera = None  # Initialize camera as None

def initialize_camera():
    """Initializes the Picamera2 object."""
    global camera
    if camera is None:
        try:
            camera = Picamera2()
            # Create a still configuration with the desired maximum resolution
            # The 'main' stream is typically used for full-resolution captures
            config = camera.create_still_configuration(main={"size": (2592, 1944)})
            # Configure the camera with the created configuration
            camera.configure(config)
            camera.start()
            print("Camera initialized.")
        except Exception as e:
            print(f"Error initializing camera: {e}")
            camera = None

def release_camera():
    """Releases the Picamera2 object."""
    global camera
    if camera:
        camera.stop()
        camera.close()
        camera = None
        print("Camera released.")

def capture():
    """Captures a photo and releases the camera."""
    global camera
    if not camera:
        print("Camera not initialized. Press button again.")
        return

    if path_var:
        print(f"Path variable: {path_var}")
    else:
        print("Path variable not set.")
        return

    time.sleep(2)
    filename = f"{path_var}/photo_{datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    try:
        camera.capture_file(filename, format="png")
        print(f"Photo saved as: {filename}")
    except Exception as e:
        print(f"Error capturing photo: {e}")
    finally:
        release_camera()

def button_pressed():
    """Handles the button press event."""
    print("Button pressed. Initializing camera...")
    initialize_camera()
    if camera:
        capture()
        print("Ready for the next press...")
    time.sleep(0.2)  # Debounce delay (adjust as needed)

button.when_pressed = button_pressed

print("Waiting for button press...")
pause()  # Efficiently wait for button presses