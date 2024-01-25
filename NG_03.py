import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins and initial states
switch_A = 27
switch_B = 17
polarity = 1
last_polarity_change = time.time()

# Global variable to track the last polarity change
last_polarity_change = time.time()

# Other hardware pins
HB1L = 19 # opto-isolator U4
HB1H = 26 # opto-isolator U5
HB2L = 6 #  opto-isolator U7
HB2H = 13 # opto-isolator U6
HB3L = 9 #  opto-isolator U8
HB3H = 11 # opto-isolator U9
HV100_ON = 20 # U3
HV300_ON = 21 # U2
DISCHARGE100V = 23 # MOSFET U10
DISCHARGE300V = 24 # MOSFET U11

# Setup GPIO pins
GPIO.setup(switch_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(HB1L, GPIO.OUT, initial = 0)
GPIO.setup(HB1H, GPIO.OUT, initial = 0)
GPIO.setup(HB2L, GPIO.OUT, initial = 0)
GPIO.setup(HB2H, GPIO.OUT, initial = 0)
GPIO.setup(HB3L, GPIO.OUT, initial = 0)
GPIO.setup(HB3H, GPIO.OUT, initial = 0)
GPIO.setup(HV100_ON, GPIO.OUT, initial = 0)


#RC_time_constant = 1 # delay for capcitor RC time constant
#sleep = 0.01

single_width = 5
pulse_width = 10
timeout = 30
debounce = 50

# Switch A callback function
def switch_A_callback(channel):
    global polarity
    # if GPIO.input(switch_A) == GPIO.HIGH:
    #     polarity = polarity_swap(polarity)
    #     print("Switch A went HIGH, polarity swapped.")

    if GPIO.input(switch_A) == GPIO.HIGH and GPIO.input(switch_B) == GPIO.HIGH:
        print("Switch A has just been set HIGH")
        print("Switch B has already been set HIGH")
        print("Pulse Mode")
        polarity = polarity_swap(polarity)
        pulse_mode()
        # main()
    elif GPIO.input(switch_A) == GPIO.LOW and GPIO.input(switch_B) == GPIO.HIGH:
        print("Switch A has just been set LOW")
        print("Switch B has already been set HIGH")
        print("Zero Volts")
        ZERO_HV_200v()
#         main()
    elif GPIO.input(switch_A) == GPIO.HIGH and GPIO.input(switch_B) == GPIO.LOW:
        print("Switch A has just been set HIGH")
        print("Switch B has already been set LOW")
        print("Single Mode")
        polarity = polarity_swap(polarity)
        print("Switch A went HIGH, polarity swapped.")
#         main()
    elif GPIO.input(switch_A) == GPIO.LOW and GPIO.input(switch_B) == GPIO.LOW:
        print("Switch A has just been set LOW")
        print("Switch B has already been set LOW")
        print("Zero Volts")
        ZERO_HV_200v()
#         main()    
    else:
        print("Something has gone wrong")
#         main()

# Switch B callback function      
def switch_B_callback(channel):
    global polarity
    if GPIO.input(switch_B) == GPIO.LOW:
        ZERO_HV_200v()
        polarity = polarity_swap(polarity)
        print("Switch B went LOW, output set to ZERO, polarity swapped.")

    if GPIO.input(switch_A) == GPIO.HIGH and GPIO.input(switch_B) == GPIO.HIGH:
        print("Switch B has just been set HIGH")
        print("Switch A has already been set HIGH")
        print("Pulse Mode")
        NEG_HV_200v()
#         main()
    elif GPIO.input(switch_A) == GPIO.LOW and GPIO.input(switch_B) == GPIO.HIGH:
        print("Switch B has just been set LOW")
        print("Switch A has already been set HIGH")
        print("Zero Volts")
        ZERO_HV_200v()
#         main()
    elif GPIO.input(switch_A) == GPIO.HIGH and GPIO.input(switch_B) == GPIO.LOW:
        print("Switch B has just been set LOW")
        print("Switch A has already been set HIGH")
        print("Single Mode")
        # ZERO_HV_200v()
        polarity = polarity_swap(polarity)
        single_mode(polarity)
        # print("Switch B went LOW, output set to ZERO, polarity swapped.")
        # POS_HV_200v()
#         main()
    elif GPIO.input(switch_A) == GPIO.LOW and GPIO.input(switch_B) == GPIO.LOW:
        print("Switch B has just been set LOW")
        print("Switch A has already been set LOW")
        print("Zero Volts")
        ZERO_HV_200v()
#         main()    
    else:
        print("Something has gone wrong")
#         main()
        
# Add event detection for switches
GPIO.add_event_detect(switch_A, GPIO.BOTH, callback=switch_A_callback, bouncetime=debounce)
GPIO.add_event_detect(switch_B, GPIO.BOTH, callback=switch_B_callback, bouncetime=debounce)

######################################################################################
################################# H-Bridge Functions #################################
######################################################################################

def picos_on():
    # print("entering picos_on function")
    GPIO.output(HV100_ON, 1)
#     GPIO.output(HV300_ON, 1)
    # print("exiting picos_on function")
    return
    
def picos_off():
    # print("entering picos_off function")
    GPIO.output(HV100_ON, 0)
#     GPIO.output(HV300_ON, 0)
    # print("exiting picos_off function")
    return

def status():
    print("##### Status #####")
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B))
    print("HB1L = ", GPIO.input(HB1L), " HB1H = ", GPIO.input(HB1H))
    print("HB2L = ", GPIO.input(HB2L), " HB2H = ", GPIO.input(HB2H))
    print("HB3L = ", GPIO.input(HB3L), " HB3H = ", GPIO.input(HB3H))
    print("HV100_ON = ", GPIO.input(HV100_ON))
    print("##################")
    return

def POS_HV_200v():
    # print("entering POS_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3L, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2L, 1)    
    GPIO.output(HB3H, 1)
    # print("exiting POS_HV_200v function")
    return

def NEG_HV_200v():
    # print("entering NEG_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2H, 1)    
    GPIO.output(HB3L, 1)
    # print("exiting NEG_HV_200v function")
    return

def ZERO_HV_200v():
    # print("entering ZERO_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)    
    GPIO.output(HB2L, 1)
    GPIO.output(HB3L, 1)
    # print("exiting ZERO_HV_200v function")
    return

def H_Bridge_float():
    # print("entering H_Bridge_float function")
    GPIO.output(HB1H, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3L, 0)
#     print("exiting H_Bridge_float function")
    return

def single_mode(polarity):
    # print("entering single_mode function")    
    # print("switch_A = ", GPIO.input(switch_A))
    # print("switch_B = ", GPIO.input(switch_B))
    if polarity == 1:
        POS_HV_200v()
    else:    
        NEG_HV_200v()
    return


def pulse_mode():
    # print("entering pulse_mode function")    
    # print("switch_A = ", GPIO.input(switch_A))
    # print("switch_B = ", GPIO.input(switch_B))
    POS_HV_200v()
    time.sleep(pulse_width)
    ZERO_HV_200v()
    time.sleep(pulse_width)
    NEG_HV_200v()
    time.sleep(pulse_width)
    ZERO_HV_200v()
    time.sleep(pulse_width)
    return

def constant_mode(polarity):
    while True:
        POS_HV_200v()

def polarity_swap(polarity):
    global last_polarity_change
    last_polarity_change = time.time()
    return (1 - polarity)

def extend(polarity):
    NEG_HV_200v()

H_Bridge_float()
picos_on()
status()
POS_HV_200v()


def main():
    global last_polarity_change
    global polarity  # Declare polarity as global

    try:
        while True:
            current_time = time.time()
            
            # Check if 30 seconds have passed since the last polarity change
            if current_time - last_polarity_change >= 30:
                polarity = polarity_swap(polarity)
                last_polarity_change = current_time
                print("Polarity swapped due to 30 seconds inactivity.")

      
            if (GPIO.input(switch_A) == 0) and (GPIO.input(switch_B) == 0):
                ZERO_HV_200v()
            elif (GPIO.input(switch_A) == 0) and (GPIO.input(switch_B) == 1):
                ZERO_HV_200v()
            elif (GPIO.input(switch_A) == 1) and (GPIO.input(switch_B) == 0):
                single_mode(polarity)
            elif (GPIO.input(switch_A) == 1) and (GPIO.input(switch_B) == 1):
                pulse_mode()            
    except KeyboardInterrupt:
        ZERO_HV_200v()
        picos_off()
        status()
        GPIO.cleanup()
        
if __name__ == "__main__":
    main()
 
