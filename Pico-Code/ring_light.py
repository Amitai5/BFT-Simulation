import machine, neopixel, time

pixel_count = 16
lights_pin = machine.Pin(4, machine.Pin.OUT)
pixels = neopixel.NeoPixel(lights_pin, pixel_count)

pixels.fill((0, 16, 0))
pixels.write()


def waiting_for_impact():
    for j in range(255):
        for i in range(pixel_count):
            rc_index = (i * 256 // pixel_count) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()


def waiting_for_WIFI():
    color_chase((0, 255, 0), 50)
    color_chase((0, 0, 0), 50)


def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(pixel_count):
        pixels[i] = color
        time.sleep_ms(wait)
        pixels.write()


def off():
    pixels.fill((0, 0, 0))
    pixels.write()
