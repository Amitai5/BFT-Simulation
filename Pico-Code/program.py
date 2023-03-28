from hit_strength import get_hit_strength
import accelerometer as force_sensor
import ring_light, serial, time


def model_hit(force):
    ring_light.model_hit(force)
    print("Hit: " + str(force) + ", Strength: " + str(get_hit_strength(force)))
    time.sleep(2)
    ring_light.waiting_for_impact()


def main():
    # establish connection to computer
    serial.connect()

    # start the sensor readings after we set-up the Pi
    # _thread.start_new_thread(force_sensor.read_force, (model_hit, None))

    while True:
        force_sensor.read_force(model_hit, None)
        # print("____________________________________________________________")


try:
    main()
except KeyboardInterrupt:
    print("Crippling Error")
    # machine.reset()
