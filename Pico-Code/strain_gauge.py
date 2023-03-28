from hx711 import HX711
from machine import Pin
import ring_light, math

pin_OUT = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(13, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT)
hx711.set_gain(64)
hx711.tare()

# store the noise value it is usually at so we can negate it later
default_weight = abs(hx711.read_average(20))
HIT_THRESHOLD = 0.02


def read_force(callback_func, none):
    ring_light.waiting_for_impact()
    while True:
        value = hx711.read_average() + default_weight
        if is_significant(value):
            callback_func(math.fabs(value))


def is_significant(value):
    diff = default_weight * HIT_THRESHOLD
    return value > diff or value < -diff
