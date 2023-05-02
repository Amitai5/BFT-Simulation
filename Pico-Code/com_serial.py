import ring_light, select, time, sys
from machine import Pin, UART

DEVICE_ID = "BT-1826"
serial = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
led = Pin("LED", Pin.OUT)
led.on()


def has_data():
    return select.select(
        [
            sys.stdin,
        ],
        [],
        [],
        0.0,
    )[0]


def check_connection():
    if not has_data():
        return False

    activation_code = str(sys.stdin.buffer.read(7).decode("utf-8"))
    if activation_code.startswith(DEVICE_ID):
        return True
    return False


def connect():
    while check_connection() == False:
        ring_light.waiting_for_connection()
        print(DEVICE_ID + ", time: " + str(time.time()))
    led.off()
