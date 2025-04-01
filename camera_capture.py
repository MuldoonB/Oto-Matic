from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os
import time

button = Button(26)
camera =Picamera2()
path_var= '/home/pi/photos'

# Get the available configurations for still capture
still_config = camera.create_still_configuration()
 
#Find the highest resolution available in the still configurations
max_resolution = (0, 0)
for config in camera.list_camera_configs():
    if config["use_case"] == "still":
        size = config["main"]["size"]
        if size[0] * size[1] > max_resolution[0] * max_resolution[1]:
            max_resolution = size

# Configure the camera with the maximum still resolution
if max_resolution != (0, 0):
    camera.configure(camera.create_still_configuration(main={"size": max_resolution}))
    print(f"Setting camera resolution to maximum: {max_resolution}")
else:
    print("Could not determine maximum still resolution. Using default.")

camera.start()


def capture():
    if path_var:
        print(f"Path variable: {path_var}")
    else:
        print("Path variable not set."  )  
       
            

    time.sleep(2)
    filename=f"{path_var}/photo_{datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    camera.capture_file(filename,format="png")
    
def button_pressed():
    capture()
    print("Ready for the next press...")
    time.sleep(0.2) # Debounce delay (adjust as needed)

button.when_pressed = button_pressed

print("Waiting for button press...")
pause() # Efficiently wait for button presses