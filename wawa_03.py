import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## Hardware ##
# data = 2 #  26 DIOA on HV507
# NBL = 3 #   29 !BL on HV507
# NPol = 4 #  30 !POL on HV507
# CLK  = 17 # 37 CLK on HV507
# NLE = 27 #  38 !LE on HV507

# EXTEND = 3
# RETRACT = 2
# PULSE = 27
# SINGLE = 17

EXTEND = 17
PULSE = 27

polarity = 1

# Global variable to track the last polarity change
last_polarity_change = time.time()

GPIO.setup(EXTEND, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PULSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#RC_time_constant = 1 # delay for capcitor RC time constant
#sleep = 0.01
bounce = 200
single_width = 5
pulse_width = 10
timeout = 30

def EXTEND_callback(channel):
    print("EXTEND")
    status()
 
def PULSE_callback(channel):
    print("PULSE")
    status()



GPIO.add_event_detect(EXTEND, GPIO.RISING,
                      callback = EXTEND_callback,
                      bouncetime=bounce)

GPIO.add_event_detect(PULSE, GPIO.RISING,
                      callback = PULSE_callback,
                      bouncetime=bounce)


 

def status():
    print("")
    print("##### Status #####")
    print("EXTEND = ", GPIO.input(EXTEND))
    print("PULSE = ", GPIO.input(PULSE))
    print("##################")
    print("")
    return



def polarity_swap(polarity):
    global last_polarity_change
    last_polarity_change = time.time()
    return (1 - polarity)


status()



def main():
    global last_polarity_change
    global polarity  # Declare polarity as global

    try:
        while True:
            current_time = time.time()
            
            # Check if 30 seconds have passed since the last polarity change
            if 
                current_time - last_polarity_change >= 30:
                polarity = polarity_swap(polarity)
                last_polarity_change = current_time
                print("Polarity swapped due to 30 seconds inactivity.")
                print("Polarity is now ", polarity)

      
         
    except KeyboardInterrupt:

        status()
        GPIO.cleanup()
        
main()

 
