import strain_gauge as sa
import time

TIME_MS = 1250

print("Test Started...")
start_time = time.ticks_ms()
end_time = start_time + TIME_MS

force_values = []
while time.ticks_ms() < end_time:
    force_values.append(sa.get_avg_strain(sa.AVG_COUNT))

file = open("force_values.csv", "a")
for force in force_values:
    file.write(str(force) + ",")
file.close()
print("Test Finished...")
