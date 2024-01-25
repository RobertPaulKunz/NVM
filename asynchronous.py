import RPi.GPIO as GPIO

def get_gpio_values():
    GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbering
    gpio_pins = range(2, 28)  # GPIO pins available on Raspberry Pi Zero W (excluding 0 and 1)

    values = {}

    try:
        for pin in gpio_pins:
            GPIO.setup(pin, GPIO.IN)
            value = GPIO.input(pin)
            values[f"GPIO{pin}"] = value
    finally:
        GPIO.cleanup()  # Clean up GPIO settings

    return values

if __name__ == "__main__":
    gpio_values = get_gpio_values()
    for pin, value in gpio_values.items():
        print(f"{pin}: {value}")
