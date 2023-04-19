import ring_light, _thread, time
from machine import Pin, I2C
from imu import MPU6050

HIT_WINDOW_MASS = 0.105  # the weight of the hit window in KG
LEG_MASS = 0.709  # the weight of the hit window in KG

ACCEL_THRESHOLD = 4.00
CAPTURE_TIME = 500
GRAVITY = 9.80665

# Create the Hit Window IMU on pins 0 and 1
window_i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
window_mpu = MPU6050(window_i2c)
DEFAULT_WINDOW_ACCEL = -1.0

# Create the Model Leg IMU on pins 0 and 1
leg_i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
leg_mpu = MPU6050(leg_i2c)
DEFAULT_LEG_ACCEL = -1.0

# Force Calculation
# Two accelerometers, one on the leg and one on the hit window
# First, take the hit window acceleration and subtract the leg acceleration from it (remove the force absorbed by the leg)
# Second,


def start(callback_func, discard):
    ring_light.waiting_for_impact()
    while True:
        read_force(callback_func, None)
    # _thread.start_new_thread(read_force, (callback_func, None))


def read_force(callback_func, none):
    curr_accel = get_window_accel()
    if curr_accel > ACCEL_THRESHOLD:
        window_max_accel, leg_max_accel = read_max_accel(CAPTURE_TIME)
        avg_force = max_accel_to_force(window_max_accel, leg_max_accel)
        callback_func(avg_force, window_max_accel, leg_max_accel)


def max_accel_to_force(window_max_accel, leg_max_accel):
    return window_max_accel * HIT_WINDOW_MASS  # - (leg_max_accel * LEG_MASS)


# create a function to get the maximum over time
def read_max_accel(time_ms):
    window_max_accel = 0.0
    leg_max_accel = 0.0

    start_time = time.ticks_ms()
    end_time = start_time + time_ms

    while time.ticks_ms() < end_time:
        accel1 = get_window_accel()
        if accel1 > window_max_accel:
            window_max_accel = accel1

        accel2 = get_leg_accel()
        if accel2 > leg_max_accel:
            leg_max_accel = accel2

        # If we zero out then break the loop
        if (accel1 - accel2) <= ACCEL_THRESHOLD:
            break

    return window_max_accel, leg_max_accel


def get_window_accel():
    return round(abs(window_mpu.accel.z + DEFAULT_WINDOW_ACCEL) * GRAVITY, 3)


def get_leg_accel():
    return round(abs(leg_mpu.accel.z + DEFAULT_LEG_ACCEL) * GRAVITY, 3)
