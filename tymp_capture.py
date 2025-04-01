import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import os

# Stepper Motor GPIO Pins (Adjust if needed)
IN1 = 11
IN2 = 12
IN3 = 13
IN4 = 15

# Button GPIO Pin
BUTTON_PIN = 5

# Stepper Motor Parameters
STEPS_PER_REVOLUTION = 200  # Adjust based on your motor
STEP_DELAY = 0.005        # Adjust for speed
FORWARD_STEPS = 100       # Number of steps to move forward
BACKWARD_STEPS = 100      # Number of steps to move backward

# Camera Settings
RECORDING_TIME = 5        # Duration of the video recording in seconds
OUTPUT_FILENAME = "video.h264"
VIDEO_RESOLUTION = (1920, 1080) # 1080p resolution
VIDEO_FRAMERATE = 30          # 30 frames per second

# Global flag to track recording state
is_recording = False
camera = None

def setStep(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

def stop_stepper():
    setStep(0, 0, 0, 0)

def forward_stepper(delay, steps):
    for _ in range(steps):
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)

def backward_stepper(delay, steps):
    for _ in range(steps):
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        time.sleep(delay)

def button_callback(channel):
    global is_recording
    global camera

    if not is_recording:
        print("Button pressed - Starting recording and motor movement...")
        is_recording = True

        # Initialize camera if not already done
        if camera is None:
            try:
                camera = Picamera2(resolution=VIDEO_RESOLUTION, framerate=VIDEO_FRAMERATE)
            except Exception as e:
                print(f"Error initializing camera: {e}")
                is_recording = False
                return

        try:
            # Start recording
            camera.start_recording(OUTPUT_FILENAME)
            print(f"Recording started at {VIDEO_RESOLUTION} {VIDEO_FRAMERATE}fps...")

            # Move stepper motor forward
            print("Moving stepper forward...")
            forward_stepper(STEP_DELAY, FORWARD_STEPS)
            stop_stepper()
            time.sleep(0.5)

            # Move stepper motor backward
            print("Moving stepper backward...")
            backward_stepper(STEP_DELAY, BACKWARD_STEPS)
            stop_stepper()
            time.sleep(0.5)

            # Move stepper motor back to starting position
            print("Moving stepper to starting position...")
            forward_stepper(STEP_DELAY, BACKWARD_STEPS) # Move forward by the same number of backward steps
            stop_stepper()
            time.sleep(0.5)

            # Stop recording
            camera.stop_recording()
            print("Recording stopped.")

        except Exception as e:
            print(f"An error occurred during recording or motor movement: {e}")
            if camera is not None and camera.recording:
                camera.stop_recording()
        finally:
            is_recording = False
            print("Ready for next button press.")
    else:
        print("Recording is already in progress. Ignoring button press.")

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location

    # Stepper motor pins setup
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    stop_stepper() # Initialize with all coils off

    # Button pin setup
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300) # Debounce

def destroy():
    global camera
    GPIO.cleanup()
    if camera is not None:
        camera.close()
    print("GPIO and camera resources cleaned up.")

if __name__ == '__main__':
    setup()
    print("Ready. Press the button on GPIO 5 to start recording at 1080p 30fps and motor movement.")
    try:
        while True:
            time.sleep(1) # Keep the main thread running to detect button presses
    except KeyboardInterrupt:
        destroy()