import serial
import tkinter as tk
from threading import Thread

def read_serial(port, baud_rate, labels):
    ser = serial.Serial(port, baud_rate)
    while True:
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').strip()
            # Suponiendo que los datos llegan como "sensor1,sensor2,sensor3"
            sensor_data = data.split(',')
            if len(sensor_data) == 3:
                labels[0].config(text=f"Sensor 1: {sensor_data[0]}")
                labels[1].config(text=f"Sensor 2: {sensor_data[1]}")
                labels[2].config(text=f"Sensor 3: {sensor_data[2]}")

def start_reading():
    port = "COM3"  # Cambia esto por el puerto donde está conectada tu ESP32
    baud_rate = 9600
    thread = Thread(target=read_serial, args=(port, baud_rate, sensor_labels))
    thread.daemon = True
    thread.start()

# Crear la ventana principal
root = tk.Tk()
root.title("Sensor Data Viewer")

# Crear un marco para organizar los logs
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# Crear las columnas para los sensores
sensor_labels = []
for i in range(3):
    column_frame = tk.Frame(frame, borderwidth=2, relief="groove")
    column_frame.grid(row=0, column=i, padx=10, pady=10)

    column_label = tk.Label(column_frame, text=f"Sensor {i + 1}", font=("Helvetica", 16, "bold"))
    column_label.pack(pady=5)

    sensor_label = tk.Label(column_frame, text="Waiting for data...", font=("Helvetica", 12))
    sensor_label.pack(pady=5)

    sensor_labels.append(sensor_label)

# Botón para iniciar la lectura
start_button = tk.Button(root, text="Start Reading", font=("Helvetica", 14), command=start_reading)
start_button.pack(pady=10)

root.mainloop()
