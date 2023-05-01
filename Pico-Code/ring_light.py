from hit_strength import hit_strength
import machine, neopixel, time

pixel_count = 16
lights_pin = machine.Pin(4, machine.Pin.OUT)
pixels = neopixel.NeoPixel(lights_pin, pixel_count)


def waiting_for_impact():
    for j in range(255):
        for i in range(pixel_count):
            rc_index = (i * 256 // pixel_count) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()


def model_hit(force):
    pixels.fill(__get_hit_color(force))
    pixels.write()


def __get_hit_color(force):
    if force < hit_strength.LOW:
        return (128, 0, 0)
    elif force < hit_strength.MEDIUM:
        return (255, 0, 0)
    elif force < hit_strength.HIGH:
        return (75, 0, 130)
    else:
        return (138, 43, 226)


def waiting_for_connection():
    color_chase((0, 255, 0), 25)
    color_chase((0, 0, 0), 25)


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
