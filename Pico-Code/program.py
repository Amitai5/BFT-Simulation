import ring_light, com_serial, machine, time, fsr


def model_hit(force):
    ring_light.model_hit(force)
    print(">>" + str(force) + ";")
    time.sleep(10)


def main():
    # com_serial.connect()
    fsr.start(model_hit, None)


try:
    main()
except KeyboardInterrupt:
    print("Crippling Error")
    # machine.reset()
