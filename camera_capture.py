from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os
import time

button = Button(26)
camera =Picamera2()
path_var= os.environ.get("GLOBAL_SES_PATH")
camera.start()

def capture():
    if path_var:
        print(f"Path variable: {path_var}")
    else:
        print("Path variable not set."  )  
        path_var='/home/pi/photos'
            

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