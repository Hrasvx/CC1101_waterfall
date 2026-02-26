import serial
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from collections import deque

PORT = "COM5" # change this
BAUD = 115200

TARGET_WIDTH = 200
HISTORY_DEPTH = 80
ser = serial.Serial(PORT, BAUD, timeout=1)

spectrum_history = deque(maxlen=HISTORY_DEPTH)

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(10, 6))
plt.show(block=False)

while True:
    try:
        if ser.in_waiting == 0:
            plt.pause(0.02)
            continue

        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        sweep = []

        points = line.split(",")

        for p in points:
            if ":" in p:
                try:
                    _, rssi = p.split(":")
                    sweep.append(float(rssi))
                except:
                    pass

        if len(sweep) > 0:
            sweep = sweep[:TARGET_WIDTH]

            if len(sweep) < TARGET_WIDTH:
                sweep.extend([sweep[-1]] * (TARGET_WIDTH - len(sweep)))
            spectrum_history.append(sweep)
            if len(spectrum_history) > HISTORY_DEPTH:
                spectrum_history.popleft()
            matrix = np.array(list(spectrum_history), dtype=float)
            ax.clear()
            matrix = np.clip(matrix, -95, -60)
            ax.imshow(
                matrix,
                aspect='auto',
                cmap='magma',
                interpolation='bicubic'
            )

            ax.set_title("Spectrum")
            ax.set_xlabel("Frequency Bin")
            ax.set_ylabel("Time")

            plt.pause(0.001)

    except KeyboardInterrupt:
        break

ser.close()