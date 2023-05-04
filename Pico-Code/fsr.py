import machine, ring_light, _thread, math, time
from machine import Pin, ADC

str_gauge = ADC(Pin(26, Pin.IN, Pin.PULL_UP))  # Connected to pin GP_26
machine.freq(260000000)

# values from Desmos function: https://www.desmos.com/calculator/t12imu6ria
SCALE_FACTOR = 87.5 / math.pi
CALIB_B = 1.01814
CALIB_A = 0.48597

HIT_THRESHOLD = 0.75  # this is a reading of approximately zero
SCAN_TIME_MS = 500
MAX_VOLTAGE = 3.33
AVG_COUNT = 3


def start(callback_func, discard):
    _thread.start_new_thread(ring_light.waiting_for_impact, ())
    while True:
        read_force(callback_func, None)


def get_strain():
    return int(round(str_gauge.read_u16()))


def get_max_voltage(init_voltage):
    start_time = time.ticks_ms()
    end_time = start_time + SCAN_TIME_MS

    max_voltage = init_voltage
    while time.ticks_ms() < end_time:
        voltage = get_avg_voltage(AVG_COUNT)
        if voltage > max_voltage:
            max_voltage = voltage

    return max_voltage


# create a function to get the average over a number of readings (in terms of powers of two)
def get_avg_voltage(pow):
    avg_force = int(0)
    count = 2**pow
    counter = 0

    while counter < count:
        avg_force += get_strain()
        counter += 1
    return MAX_VOLTAGE * (avg_force >> pow) / 65535.0


def voltage_to_force(voltage):
    return math.pow(10, (voltage - CALIB_B) / CALIB_A) * SCALE_FACTOR


def read_force(callback_func, none):
    voltage = get_avg_voltage(AVG_COUNT)
    if voltage > HIT_THRESHOLD:
        voltage = get_max_voltage(voltage)
        force = voltage_to_force(voltage)
        callback_func(force)
        _thread.start_new_thread(ring_light.waiting_for_impact, ())
