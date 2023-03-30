import ring_light, select, time, sys

DEVICE_ID = "BT-1826"


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
        return input() == DEVICE_ID
    return False


def connect():
    while __connected() == False:
        ring_light.waiting_for_connection()
        print(DEVICE_ID + ", time: " + str(time.time()))

    print("Connection Established!")
