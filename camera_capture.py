from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os

button = Button(26)
camera =Picamera2()
path_var= os.environ.get("GLOBAL_SES_PATH")


def capture():
    if path_var:
        print(f"Path variable: {path_var}")
    else:
        print("Path variable not set."  )  
        path_var='/home/pi/photos'
    
    filename=f"{path_var}/photo_{datetime.now():%Y-%m-%d-%H-%M-%S}.png"
    camera.capture_file(filename,format="png")
    
while True:
    button.wait_for_press()  # Blocks until the button is pressed
    capture()
    print("Ready for the next press...")
    # Optional: Add a small delay to avoid rapid triggers if the button bounces
    time.sleep(1)