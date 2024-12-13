import matplotlib.pyplot as plt
import serial
from matplotlib.animation import FuncAnimation

def update(frame):
    if ser.in_waiting:
        data = ser.readline().decode('utf-8').strip()
        y_data.append(float(data))
        x_data.append(len(y_data))
        ax.clear()
        ax.plot(x_data, y_data)

ser = serial.Serial("COM3", 9600)
x_data, y_data = [], []

fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, interval=100)

plt.show()
