# import asyncio
import RPi.GPIO as GPIO
import time
# from machine import Pin

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## Hardware ##
# data = 2 #  26 DIOA on HV507
# NBL = 3 #   29 !BL on HV507
# NPol = 4 #  30 !POL on HV507
# CLK  = 17 # 37 CLK on HV507
# NLE = 27 #  38 !LE on HV507

extend = 17
pulse = 27

# Global variable to track the last polarity change
polarity = 0
last_polarity_change = time.time()

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

GPIO.setup(extend, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(retract, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pulse, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(single, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
bounce = 50

def extend_callback(channel):
    print("extend")
    if GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.LOW:
        print("Disabled")
        ZERO_HV_200v()
        # main()
    elif GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.HIGH:
        print("Disabled")
        ZERO_HV_200v()
        # main()
    elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.LOW:
        print("Single Mode")
        global polarity
        polarity = polarity_swap(polarity)
        single_mode(polarity)
#         main()
    elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.HIGH:
        print("Pulse Mode")
        pulse_mode()
    else:
        print("Something has gone wrong")
#         main()
        
def pulse_callback(channel):
    print("pulse")
    if GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.LOW:
        print("Disabled")
        ZERO_HV_200v()
        # main()
    elif GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.HIGH:
        print("Disabled")
        ZERO_HV_200v()
        # main()
    elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.LOW:
        print("Single Mode")
        global polarity
        polarity = polarity_swap(polarity)
        single_mode(polarity)
#         main()
    elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.HIGH:
        print("Pulse Mode")
        pulse_mode()
    else:
        print("Something has gone wrong")
#         main()
        
GPIO.add_event_detect(extend, GPIO.BOTH,
                      callback = extend_callback,
                      bouncetime=bounce)

GPIO.add_event_detect(pulse, GPIO.BOTH,
                      callback = pulse_callback,
                      bouncetime=bounce)
 
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
    print("extend = ", GPIO.input(extend))
    print("pulse = ", GPIO.input(pulse))
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
    # print("extend = ", GPIO.input(extend))
    # print("retract = ", GPIO.input(retract))
    if polarity == 1:
        POS_HV_200v()
    else:    
        NEG_HV_200v()
    return

def pulse_mode():
    # print("entering pulse_mode function")    
    # print("extend = ", GPIO.input(extend))
    # print("retract = ", GPIO.input(retract))
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
    polarity = (1 - polarity)
    single_mode(polarity)
    return polarity


H_Bridge_float()
picos_on()
ZERO_HV_200v()
status()

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

#             if GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.LOW:
#                 print("Disabled")
#                 ZERO_HV_200v()
#                 # main()
#             elif GPIO.input(extend) == GPIO.LOW and GPIO.input(pulse) == GPIO.HIGH:
#                 print("Disabled")
#                 ZERO_HV_200v()
#                 # main()
#             elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.LOW:
#                 print("Single Mode")                      
#                 single_mode(polarity)
# #                main()
#             elif GPIO.input(extend) == GPIO.HIGH and GPIO.input(pulse) == GPIO.HIGH:
#                 print("Pulse Mode")
#                 pulse_mode()
#             else:
#                 print("Something has gone wrong")
# #         main()

      
           
    except KeyboardInterrupt:
        ZERO_HV_200v()
        picos_off()
        status()
        GPIO.cleanup()
        
main()

 
