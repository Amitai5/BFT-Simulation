import machine, time, math
from machine import Pin, ADC

str_gauge = ADC(Pin(26, Pin.IN, Pin.PULL_UP))  # Connected to pin GP_26
machine.freq(260000000)

DEFAULT_STRAIN = 1123
HIT_THRESHOLD = 360
HIT_CONSTANT = 0.1
AVG_COUNT = 5


def start(callback_func, discard):
    while True:
        read_force(callback_func, None)
    # _thread.start_new_thread(read_force, (callback_func, None))


def get_strain():
    return abs(DEFAULT_STRAIN - int(round(str_gauge.read_u16() >> 4)))


# create a function to get the average over a number of readings (in terms of powers of two)
def get_avg_strain(pow):
    avg_force = int(0)
    count = 2**pow
    counter = 0

    while counter < count:
        avg_force += get_strain()
        counter += 1
    return avg_force >> pow


def read_force(callback_func, none):
    avg_strain = get_avg_strain(AVG_COUNT)
    print(avg_strain)
    if avg_strain > HIT_THRESHOLD:
        callback_func(avg_strain)
