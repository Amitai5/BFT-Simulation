import ring_light, select, time, sys
from machine import Pin, UART

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


def __connected():
    if __has_data():
        return DEVICE_ID in str(serial.readline())
    return False


def connect():
    while __connected() == False:
        ring_light.waiting_for_connection()
        print(DEVICE_ID + ", time: " + str(time.time()))
    led.toggle()
