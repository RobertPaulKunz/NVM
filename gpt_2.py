import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers
HB1L = 19  # opto-isolator U4
HB1H = 26  # opto-isolator U5
HB2L = 6   # opto-isolator U7
HB2H = 13  # opto-isolator U6
HB3L = 9   # opto-isolator U8
HB3H = 11  # opto-isolator U9
HV100_ON = 20        # U3
HV300_ON = 21        # U2
DISCHARGE100V = 23   # MOSFET U10
DISCHARGE300V = 24   # MOSFET U11
switch_A = 27
switch_B = 17
output_pin = 22  # Adjust this to your desired output pin

# Define timing variables
single_width = 5
pulse_width = 10
timeout = 30

# Initial polarity
polarity = 1

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([HB1L, HB1H, HB2L, HB2H, HB3L, HB3H, HV100_ON, HV300_ON, DISCHARGE100V, DISCHARGE300V], GPIO.OUT, initial=0)
GPIO.setup([switch_A, switch_B, output_pin], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to turn on HV100_ON (H-Bridge)
def picos_on():
    print("Entering picos_on function")
    GPIO.output(HV100_ON, GPIO.HIGH)
    print("Exiting picos_on function")

# Function to turn off HV100_ON (H-Bridge)
def picos_off():
    print("Entering picos_off function")
    GPIO.output(HV100_ON, GPIO.LOW)
    print("Exiting picos_off function")

# Function to set GPIO pin states for POS_HV_200v
def POS_HV_200v():
    print("Entering POS_HV_200v function")
    GPIO.output(HB1L, GPIO.LOW)
    GPIO.output(HB2H, GPIO.LOW)
    GPIO.output(HB3L, GPIO.LOW)
    GPIO.output(HB1H, GPIO.HIGH)
    GPIO.output(HB2L, GPIO.HIGH)    
    GPIO.output(HB3H, GPIO.HIGH)
    print("Exiting POS_HV_200v function")

# Function to set GPIO pin states for NEG_HV_200v
def NEG_HV_200v():
    print("Entering NEG_HV_200v function")
    GPIO.output(HB1L, GPIO.LOW)
    GPIO.output(HB2L, GPIO.LOW)
    GPIO.output(HB3H, GPIO.LOW)
    GPIO.output(HB1H, GPIO.HIGH)
    GPIO.output(HB2H, GPIO.HIGH)    
    GPIO.output(HB3L, GPIO.HIGH)
    print("Exiting NEG_HV_200v function")

# Function to set GPIO pin states for ZERO_HV_200v (Assuming you have a function for this)
def ZERO_HV_200v():
    print("Entering ZERO_HV_200v function")
    # Define the actions for setting HV to zero
    # Adjust the code based on your requirements
    print("Exiting ZERO_HV_200v function")

# Function to set GPIO pin states for floating the H-Bridge
def H_Bridge_float():
    print("Entering H_Bridge_float function")
    GPIO.output(HB1H, GPIO.LOW)
    GPIO.output(HB2H, GPIO.LOW)
    GPIO.output(HB3H, GPIO.LOW)
    GPIO.output(HB1L, GPIO.LOW)
    GPIO.output(HB2L, GPIO.LOW)
    GPIO.output(HB3L, GPIO.LOW)
    print("Exiting H_Bridge_float function")

# Function to print the status of GPIO pins
def status():
    print("##### Status #####")
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B))
    print("HB1L = ", GPIO.input(HB1L), " HB1H = ", GPIO.input(HB1H))
    print("HB2L = ", GPIO.input(HB2L), " HB2H = ", GPIO.input(HB2H))
    print("HB3L = ", GPIO.input(HB3L), " HB3H = ", GPIO.input(HB3H))
    print("HV100_ON = ", GPIO.input(HV100_ON))
    print("##################")

# Function for single mode operation
def single_mode():
    print("Entering single_mode function")    
    start_time = time.time()

    while time.time() - start_time < single_width:
        print("switch_A = ", GPIO.input(switch_A))
        print("switch_B = ", GPIO.input(switch_B)) 
        POS_HV_200v()

        # Check if the time limit is reached
        if time.time() - start_time > 30:
            print("Swapping polarity due to time limit")
            return polarity_swap(polarity)

    NEG_HV_200v()
    time.sleep(single_width)

# Function for pulse mode operation
def pulse_mode():
    print("Entering pulse_mode function")    
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B)) 
    POS_HV_200v()
    time.sleep(pulse_width)
    ZERO_HV_200v()
    time.sleep(pulse_width)
    NEG_HV_200v()
    time.sleep(pulse_width)
    ZERO_HV_200v()
    time.sleep(pulse_width)

# Function to swap polarity
def polarity_swap(polarity):
    return 1 - polarity

# Function to extend based on polarity
def extend(polarity):
    if polarity == 1:
        NEG_HV_200v()

# Main control loop
def main():
    try:
        while True:        
            if (GPIO.input(switch_A) == 0) and (GPIO.input(switch_B) == 0):
                ZERO_HV_200v()
            elif (GPIO.input(switch_A) == 0) and (GPIO.input(switch_B) == 1):
                ZERO_HV_200v()
            elif (GPIO.input(switch_A) == 1) and (GPIO.input(switch_B) == 0):
                single_mode()
            elif (GPIO.input(switch_A) == 1) and (GPIO.input(switch_B) == 1):
                pulse_mode()            
    except KeyboardInterrupt:
        ZERO_HV_200v()
        picos_off()
        status()
        GPIO.cleanup()

# Call the main function to start the control loop
if __name__ == "__main__":
    main()
