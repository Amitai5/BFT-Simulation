from web_server import web_server
from machine import Pin, I2C
import ring_light
import sensors
import _thread

WIFI_PASSWORD = "bENdOVER525"
SSID = "29DOVER-3"


_thread.start_new_thread(sensors.read_force, ())


def main():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    server = web_server(SSID, WIFI_PASSWORD)

    file = open("web/Home.html", "r")
    server.set_html(file.read())

    while True:
        server.serve()
        # print("____________________________________________________________")


try:
    main()
except KeyboardInterrupt:
    print("Crippling Error")
    # machine.reset()
