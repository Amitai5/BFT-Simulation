import ring_light, time, math
from machine import Pin, I2C
from imu import MPU6050


# create a function to get the average over time
def read_average(time_ms):
    sum = 0
    counter = 0
    end_time = time.ticks_ms() + time_ms
    while time.ticks_ms() < end_time:
        sum += imu.accel.y
        counter += 1
    print(counter)
    return sum / counter


i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

# store the noise value it is usually at so we can negate it later
gravity_default = abs(read_average(100))
HIT_THRESHOLD = 0.4


def read_force(callback_func, none):
    ring_light.waiting_for_impact()
    while True:
        value = abs(gravity_default - read_average(20))
        if is_significant(value):
            callback_func(value)


def is_significant(value):
    diff = gravity_default * HIT_THRESHOLD
    return value > diff or value < -diff
