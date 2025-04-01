from gpiozero import Button, DigitalOutputDevice, Motor
from picamera2 import Picamera2
from time import sleep
from signal import pause

# Stepper Motor GPIO Pins (Adjust if needed)
IN1_PIN = 17  # Example GPIO pin for IN1 (adjust to your wiring)
IN2_PIN = 18  # Example GPIO pin for IN2
IN3_PIN = 27  # Example GPIO pin for IN3
IN4_PIN = 22  # Example GPIO pin for IN4

# Button GPIO Pin
BUTTON_PIN = 5  # Example GPIO pin for the button (adjust to your wiring)

# Stepper Motor Parameters
STEPS_PER_REVOLUTION = 200  # Adjust based on your motor
STEP_DELAY = 0.005        # Adjust for speed
FORWARD_STEPS = 100       # Number of steps to move forward
BACKWARD_STEPS = 100      # Number of steps to move backward

# Camera Settings
RECORDING_TIME = 5        # Duration of the video recording in seconds
OUTPUT_FILENAME = "video_gpiozero.h264"
VIDEO_RESOLUTION = (1920, 1080) # 1080p resolution
VIDEO_FRAMERATE = 30          # 30 frames per second

# Global flag to track recording state
is_recording = False
camera = None

# Define stepper motor control pins as DigitalOutputDevice
in1 = DigitalOutputDevice(IN1_PIN)
in2 = DigitalOutputDevice(IN2_PIN)
in3 = DigitalOutputDevice(IN3_PIN)
in4 = DigitalOutputDevice(IN4_PIN)

# Define the button
button = Button(BUTTON_PIN)

def set_step(w1, w2, w3, w4):
    in1.value = w1
    in2.value = w2
    in3.value = w3
    in4.value = w4

def stop_stepper():
    set_step(0, 0, 0, 0)

def forward_stepper(delay, steps):
    for _ in range(steps):
        set_step(1, 0, 0, 0)
        sleep(delay)
        set_step(0, 1, 0, 0)
        sleep(delay)
        set_step(0, 0, 1, 0)
        sleep(delay)
        set_step(0, 0, 0, 1)
        sleep(delay)

def backward_stepper(delay, steps):
    for _ in range(steps):
        set_step(0, 0, 0, 1)
        sleep(delay)
        set_step(0, 0, 1, 0)
        sleep(delay)
        set_step(0, 1, 0, 0)
        sleep(delay)
        set_step(1, 0, 0, 0)
        sleep(delay)

def button_pressed():
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
            sleep(0.5)

            # Move stepper motor backward
            print("Moving stepper backward...")
            backward_stepper(STEP_DELAY, BACKWARD_STEPS)
            stop_stepper()
            sleep(0.5)

            # Move stepper motor back to starting position
            print("Moving stepper to starting position...")
            forward_stepper(STEP_DELAY, BACKWARD_STEPS) # Move forward by the same number of backward steps
            stop_stepper()
            sleep(0.5)

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

def main():
    global camera
    print("Ready. Press the button to start recording at 1080p 30fps and motor movement (using gpiozero).")
    button.when_pressed = button_pressed

    try:
        pause()  # Keep the script running and listening for button presses
    except KeyboardInterrupt:
        if camera is not None:
            camera.close()
        stop_stepper()
        print("GPIO and camera resources cleaned up.")

if __name__ == '__main__':
    main()