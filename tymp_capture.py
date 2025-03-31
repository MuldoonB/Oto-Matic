from gpiozero import Button
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import os
import time

button = Button(5)
picam2 =Picamera2()
video_config=picam2.create_video_configuration()
picam2.configure(video_config)

path_var= os.environ.get("GLOBAL_SES_PATH", /home/pi/videos)

encoder - H264Encoder(bitrate=10000000)

def record():
    if path_variable:
        print(f"Path variable: {path_variable}")
    else:
        print("Path variable not set."    
    
    output=f"{path_var}/video_{datetime.now():%Y-%m-%d-%H-%M-%S}}.h264")
    picam2.start_recording(encoder,output)
    time.sleep(10)
    picam2.stop_recording()
    
button.when_pressed = record

pause()`