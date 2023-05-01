import fsr, time


TIME_MS = 2500

print("Test Started...")
start_time = time.ticks_ms()
end_time = start_time + TIME_MS

acc_values = []
force_file = open("force_values.csv", "a")
while time.ticks_ms() < end_time:
    force_file.write(str(fsr.get_avg_strain(fsr.AVG_COUNT)) + ",")

force_file.close()
print("Test Finished...")
