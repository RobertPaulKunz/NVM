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

switch_extend = 17
switch_pulse = 27

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

GPIO.setup(switch_extend, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_pulse, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(HB1L, GPIO.OUT, initial = 0)
GPIO.setup(HB1H, GPIO.OUT, initial = 0)
GPIO.setup(HB2L, GPIO.OUT, initial = 0)
GPIO.setup(HB2H, GPIO.OUT, initial = 0)
GPIO.setup(HB3L, GPIO.OUT, initial = 0)
GPIO.setup(HB3H, GPIO.OUT, initial = 0)
GPIO.setup(HV100_ON, GPIO.OUT, initial = 0)

pulse_width = 10
timeout = 30
polarity = 1
 
######################################################################################
################################# H-Bridge Functions #################################
######################################################################################

def picos_on():
    print("entering picos_on function")
    GPIO.output(HV100_ON, 1)
    print("exiting picos_on function")
    return
    
def picos_off():
    print("entering picos_off function")
    GPIO.output(HV100_ON, 0)
    print("exiting picos_off function")
    return

def status():
    print("##### Status #####")
    print("extend = ", GPIO.input(switch_extend))
    print("pulse = ", GPIO.input(switch_pulse))
    print("HB1L = ", GPIO.input(HB1L), " HB1H = ", GPIO.input(HB1H))
    print("HB2L = ", GPIO.input(HB2L), " HB2H = ", GPIO.input(HB2H))
    print("HB3L = ", GPIO.input(HB3L), " HB3H = ", GPIO.input(HB3H))
    print("HV100_ON = ", GPIO.input(HV100_ON))
    print("##################")
    return

def POS_HV_200v():
    print("entering POS_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3L, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2L, 1)    
    GPIO.output(HB3H, 1)
    print("exiting POS_HV_200v function")
    return

def NEG_HV_200v():
    print("entering NEG_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2H, 1)    
    GPIO.output(HB3L, 1)
    print("exiting NEG_HV_200v function")
    return

def ZERO_HV_200v():
    print("entering ZERO_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)    
    GPIO.output(HB2L, 1)
    GPIO.output(HB3L, 1)
    print("exiting ZERO_HV_200v function")
    return

def H_Bridge_float():
    print("entering H_Bridge_float function")
    GPIO.output(HB1H, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3L, 0)
    print("exiting H_Bridge_float function")
    return

def single_mode():
    pass

def pulse_mode():
    pass

def polarity_swap():
    global polarity
    polarity = 1 - polarity

H_Bridge_float()
picos_on()
ZERO_HV_200v()
status()

def main():    
    try:
        while True:
            extend_state = GPIO.input(switch_extend)
            pulse_state = GPIO.input(switch_pulse)

            if not extend_state and not pulse_state:
                ZERO_HV_200v()
            elif not extend_state and pulse_state:
                ZERO_HV_200v()
            elif extend_state and not pulse_state:
                NEG_HV_200v()
            elif extend_state and pulse_state:
                POS_HV_200v()
           
    except KeyboardInterrupt:
        ZERO_HV_200v()
        picos_off()
        status()
        GPIO.cleanup()
        
main()
        