import RPi.GPIO as GPIO
import time
import argparse

# Define default GPIO pin numbers
DEFAULT_SWITCH_A_PIN = 27
DEFAULT_SWITCH_B_PIN = 17
DEFAULT_HB1L_PIN = 19
DEFAULT_HB1H_PIN = 26
DEFAULT_HB2L_PIN = 6
DEFAULT_HB2H_PIN = 13
DEFAULT_HB3L_PIN = 9
DEFAULT_HB3H_PIN = 11
DEFAULT_HV100_ON_PIN = 20

# Define default delay values
DEFAULT_SINGLE_WIDTH = 5
DEFAULT_PULSE_WIDTH = 10

def setup_gpio_pins(switch_A, switch_B, HB1L, HB1H, HB2L, HB2H, HB3L, HB3H, HV100_ON):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switch_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(HB1L, GPIO.OUT, initial=0)
    GPIO.setup(HB1H, GPIO.OUT, initial=0)
    GPIO.setup(HB2L, GPIO.OUT, initial=0)
    GPIO.setup(HB2H, GPIO.OUT, initial=0)
    GPIO.setup(HB3L, GPIO.OUT, initial=0)
    GPIO.setup(HB3H, GPIO.OUT, initial=0)
    GPIO.setup(HV100_ON, GPIO.OUT, initial=0)

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
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B))
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
    return

def single_mode(single_width):
    print("entering single_mode function")    
    print("switch_A = ", GPIO.input(switch_A))
    print("switch_B = ", GPIO.input(switch_B)) 
    POS_HV_200v()
    time.sleep(single_width)
    NEG_HV_200v()
    time.sleep(single_width)
    return

def pulse_mode(pulse_width):
    print("entering pulse_mode function")    
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
    return

def polarity_swap(polarity):
    return (1 - polarity)

def extend(polarity):
    NEG_HV_200v()

def main():
    parser = argparse.ArgumentParser(description="H-Bridge Control Program")
    parser.add_argument("--switch_A", type=int, default=DEFAULT_SWITCH_A_PIN, help="GPIO pin for switch A")
    parser.add_argument("--switch_B", type=int, default=DEFAULT_SWITCH_B_PIN, help="GPIO pin for switch B")
    parser.add_argument("--HB1L", type=int, default=DEFAULT_HB1L_PIN, help="GPIO pin for HB1L")
    parser.add_argument("--HB1H", type=int, default=DEFAULT_HB1H_PIN, help="GPIO pin for HB1H")
    parser.add_argument("--HB2L", type=int, default=DEFAULT_HB2L_PIN, help="GPIO pin for HB2L")
    parser.add_argument("--HB2H", type=int, default=DEFAULT_HB2H_PIN, help="GPIO pin for HB2H")
    parser.add_argument("--HB3L", type=int, default=DEFAULT_HB3L_PIN, help="GPIO pin for HB3L")
    parser.add_argument("--HB3H", type=int, default=DEFAULT_HB3H_PIN, help="GPIO pin for HB3H")
    parser.add_argument("--HV100_ON", type=int, default=DEFAULT_HV100_ON_PIN, help="GPIO pin for HV100_ON")
    parser.add_argument("--single_width", type=int, default=DEFAULT_SINGLE_WIDTH, help="Single width delay")
    parser.add_argument("--pulse_width", type=int, default=DEFAULT_PULSE_WIDTH, help="Pulse width delay")
    args = parser.parse_args()

    try:
        setup_gpio_pins(args.switch_A, args.switch_B, args.HB1L, args.HB1H, args.HB2L, args.HB2H, args.HB3L, args.HB3H, args.HV100_ON)

        while True:
            if (GPIO.input(args.switch_A) == 0) and (GPIO.input(args.switch_B) == 0):
                ZERO_HV_200v()
            elif (GPIO.input(args.switch_A) == 0) and (GPIO.input(args.switch_B) == 1):
                ZERO_HV_200v()
            elif (GPIO.input(args.switch_A) == 1) and (GPIO.input(args.switch_B) == 0):
                single_mode(args.single_width)
            elif (GPIO.input(args.switch_A) == 1) and (GPIO.input(args.switch_B) == 1):
                pulse_mode(args.pulse_width)
    except KeyboardInterrupt:
        ZERO_HV_200v()
        picos_off()
        status()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
