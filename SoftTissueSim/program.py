from web_server import web_server
from machine import Pin, I2C
import _thread
import machine
import time

WIFI_PASSWORD = "8189169000"
SSID = "Amitai's Hotspot"


def main():
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    server = web_server(SSID, WIFI_PASSWORD)

    file = open("web/Home.html", "r")
    server.set_html(file.read())

    while True:
        server.serve()
        print("_____________________________________________________________")


try:
    main()
except KeyboardInterrupt:
    print("Crippling Error")
    # machine.reset()
