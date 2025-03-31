from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os

button = Button(26)
camera =Picamera2()
path_var= os.environ.get("GLOBAL_SES_PATH", /home/pi/photos)


def capture():
    if path_variable:
        print(f"Path variable: {path_variable}")
    else:
        print("Path variable not set."    
    
    filename=f"{path_var}/photo_{datetime.now():%Y-%m-%d-%H-%M-%S}}.png")
    camera.capture_file(filename,format="png")
    
    
button.when_pressed = capture

pause()