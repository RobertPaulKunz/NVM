import RPi.GPIO as GPIO
import time

# Use the BCM GPIO numbering scheme
GPIO.setmode(GPIO.BCM)

# GPIO pins for the toggle switches
toggle_switch1 = 17  # Replace with your GPIO pin number
toggle_switch2 = 27  # Replace with your GPIO pin number

# GPIO pins for the LEDs
led1 = 18  # Replace with your GPIO pin number
led2 = 23  # Replace with your GPIO pin number
led3 = 24  # Replace with your GPIO pin number

# Set up the GPIO pins for switches and LEDs
GPIO.setup(toggle_switch1, GPIO.IN)
GPIO.setup(toggle_switch2, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

def update_leds():
    switch1_state = GPIO.input(toggle_switch1)
    switch2_state = GPIO.input(toggle_switch2)

    if not switch1_state and not switch2_state:
        # Switch 1 LOW and Switch 2 LOW
        GPIO.output(led1, False)
        GPIO.output(led2, True)
        GPIO.output(led3, False)
    elif not switch1_state and switch2_state:
        # Switch 1 LOW and Switch 2 HIGH
        GPIO.output(led1, False)
        GPIO.output(led2, True)
        GPIO.output(led3, False)
    elif switch1_state and not switch2_state:
        # Switch 1 HIGH and Switch 2 LOW
        GPIO.output(led1, False)
        GPIO.output(led2, False)
        GPIO.output(led3, True)
    else:
        # Switch 1 HIGH and Switch 2 HIGH
        GPIO.output(led1, True)
        GPIO.output(led2, False)
        GPIO.output(led3, False)

try:
    while True:
        update_leds()
        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    GPIO.cleanup()
