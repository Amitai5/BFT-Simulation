import machine, ring_light, _thread, math, time
from machine import Pin, ADC

str_gauge = ADC(Pin(26, Pin.IN, Pin.PULL_UP))  # Connected to pin GP_26
machine.freq(260000000)

# values from Desmos function: https://www.desmos.com/calculator/fxz5psayfz
CALIBRATION_SCALE_A = -2666.78
CALIBRATION_SCALE_B = 6972.36

HIT_THRESHOLD = 0.5  # this is a reading of approximately zero
MAX_VOLTAGE = 3.33
AVG_COUNT = 3


def start(callback_func, discard):
    _thread.start_new_thread(ring_light.waiting_for_impact, ())
    while True:
        read_force(callback_func, None)


def get_strain():
    return int(round(str_gauge.read_u16()))


# create a function to get the average over a number of readings (in terms of powers of two)
def get_avg_strain(pow):
    avg_force = int(0)
    count = 2**pow
    counter = 0

    while counter < count:
        avg_force += get_strain()
        counter += 1
    return avg_force >> pow


def strain_to_force(voltage):
    resistance = (MAX_VOLTAGE / voltage) * 1000 - 1000
    return math.pow(10, resistance - CALIBRATION_SCALE_B) / CALIBRATION_SCALE_A


def read_force(callback_func, none):
    avg_strain = get_avg_strain(AVG_COUNT)
    voltage = MAX_VOLTAGE * (avg_strain / 65535.0)

    if voltage > HIT_THRESHOLD:
        force = strain_to_force(voltage)
        callback_func(force)
        _thread.start_new_thread(ring_light.waiting_for_impact, ())
