import ring_light, select, time, sys
from machine import Pin, UART

TIME_MS = 15000

DEVICE_ID = "BT-1826"
serial = UART(0, 9600)
led = Pin("LED", Pin.OUT)
led.toggle()


def __has_data():
    return select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]


def connect():
    start_time = time.ticks_ms()
    end_time = start_time + TIME_MS

    while time.ticks_ms() < end_time:
        # ring_light.waiting_for_connection()
        print(DEVICE_ID + ", time: " + str(time.time()))
    led.toggle()
