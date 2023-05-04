import fsr, time


TIME_MS = 1250

print("Test Started...")
start_time = time.ticks_ms()
end_time = start_time + TIME_MS

acc_values = []
force_file = open("force_values.csv", "a")
while time.ticks_ms() < end_time:
    force_file.write(str(3.3 * fsr.get_strain() / 65535.0) + ",")

force_file.close()
print("Test Finished...")
