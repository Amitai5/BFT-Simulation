import strain_gauge as force_sensor
import ring_light, com_serial, time


def model_hit(force):
    ring_light.model_hit(force)
    print(str(force) + ";")
    time.sleep(2)
    ring_light.waiting_for_impact()


def main():
    # establish connection to computer
    # com_serial.connect()
    force_sensor.start(model_hit, None)


try:
    main()
except KeyboardInterrupt:
    print("Crippling Error")
    # machine.reset()
