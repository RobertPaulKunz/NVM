import RPi.GPIO as GPIO
import time

# Set up GPIO pins and initial states
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

switch_A = 27
switch_B = 17
polarity = 1

HB1L = 19
HB1H = 26
HB2L = 6
HB2H = 13
HB3L = 9
HB3H = 11
HV100_ON = 20

GPIO.setup(switch_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(HB1L, GPIO.OUT, initial=0)
GPIO.setup(HB1H, GPIO.OUT, initial=0)
GPIO.setup(HB2L, GPIO.OUT, initial=0)
GPIO.setup(HB2H, GPIO.OUT, initial=0)
GPIO.setup(HB3L, GPIO.OUT, initial=0)
GPIO.setup(HB3H, GPIO.OUT, initial=0)
GPIO.setup(HV100_ON, GPIO.OUT, initial=0)

single_width = 5
pulse_width = 10

def switch_A_callback(channel):
    if GPIO.input(switch_A) == GPIO.HIGH:
        print("Switch A has just been set HIGH")
    else:
        print("Switch A has just been set LOW")

def switch_B_callback(channel):
    if GPIO.input(switch_B) == GPIO.HIGH:
        print("Switch B has just been set HIGH")
    else:
        print("Switch B has just been set LOW")

GPIO.add_event_detect(switch_A, GPIO.BOTH, callback=switch_A_callback, bouncetime=50)
GPIO.add_event_detect(switch_B, GPIO.BOTH, callback=switch_B_callback, bouncetime=50)

def picos_on():
    print("Entering picos_on function")
    GPIO.output(HV100_ON, 1)
    print("Exiting picos_on function")

def picos_off():
    print("Entering picos_off function")
    GPIO.output(HV100_ON, 0)
    print("Exiting picos_off function")

def status():
    print("##### Status #####")
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B))
    print("HB1L = ", GPIO.input(HB1L), " HB1H = ", GPIO.input(HB1H))
    print("HB2L = ", GPIO.input(HB2L), " HB2H = ", GPIO.input(HB2H))
    print("HB3L = ", GPIO.input(HB3L), " HB3H = ", GPIO.input(HB3H))
    print("HV100_ON = ", GPIO.input(HV100_ON))
    print("##################")

def POS_HV_200v():
    print("Entering POS_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3L, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2L, 1)
    GPIO.output(HB3H, 1)
    print("Exiting POS_HV_200v function")

def NEG_HV_200v():
    print("Entering NEG_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2H, 1)
    GPIO.output(HB3L, 1)
    print("Exiting NEG_HV_200v function")

def ZERO_HV_200v():
    print("Entering ZERO_HV_200v function")
    GPIO.output(HB1L, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1H, 1)
    GPIO.output(HB2L, 1)
    GPIO.output(HB3L, 1)
    print("Exiting ZERO_HV_200v function")

def H_Bridge_float():
    print("Entering H_Bridge_float function")
    GPIO.output(HB1H, 0)
    GPIO.output(HB2H, 0)
    GPIO.output(HB3H, 0)
    GPIO.output(HB1L, 0)
    GPIO.output(HB2L, 0)
    GPIO.output(HB3L, 0)
    print("Exiting H_Bridge_float function")

def single_mode():
    print("Entering single_mode function")
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B))
    POS_HV_200v()
    time.sleep(single_width)
    NEG_HV_200v()
    time.sleep(single_width)
    print("Exiting single_mode function")

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
    print("Exiting pulse_mode function")

def polarity_swap(polarity):
    return 1 - polarity

def extend(polarity):
    NEG_HV_200v()

H_Bridge_float()
picos_on()
status()

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
