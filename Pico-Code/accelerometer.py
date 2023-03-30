import ring_light, _thread, time
from machine import Pin, I2C
from imu import MPU6050

MIN_CAPTURE = 18
CAPTURE_TIME = 1500
ACCEL_THRESHOLD = 0.6

GRAVITY = 9.80665
DEFAULT_ACCEL = 1.0  # the default force is 1G
SPRING_CONSTANT = 746000  # spring constant in mm

# Create the IMU on pins 0 and 1
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)


def start(callback_func, discard):
    _thread.start_new_thread(read_force, (callback_func, None))


# create a function to get the average over time
def read_average_accel(time_ms):
    sum = 0
    counter = 0

    start_time = time.ticks_ms()
    end_time = start_time + time_ms

    while time.ticks_ms() < end_time:
        curr_accel = round(abs(DEFAULT_ACCEL - imu.accel.y), 3)
        sum += curr_accel
        counter += 1

        # If we zero out then break the loop
        if curr_accel <= 0.3:
            break

    return (sum / counter, time.ticks_ms() - start_time)


def read_force(callback_func, none):
    ring_light.waiting_for_impact()
    while True:
        curr_accel = abs(DEFAULT_ACCEL - imu.accel.y)
        if is_significant(curr_accel):
            avg_accel, elapsed_time = read_average_accel(CAPTURE_TIME)
            avg_force = accel_to_force(avg_accel, elapsed_time)
            callback_func(avg_force)


def accel_to_force(avg_accel, elapsed_time):
    dist_compressed = (avg_accel * GRAVITY) * pow(elapsed_time / 1000, 2)
    # print(elapsed_time)
    # print(dist_compressed)
    return dist_compressed * SPRING_CONSTANT


def is_significant(value):
    return value > ACCEL_THRESHOLD
