from gpiozero import Button
from picamera2 import Picamera2
from datetime import datetime
from signal import pause

button = Button(26)
camera = Picamera2()

def capture():
    camera.capture(f'/home/pi/{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg')

button.when_pressed = capture

pause()