import serial
import tkinter as tk
from threading import Thread
import time  # Para manejar tiempos de espera

def read_serial(port, baud_rate, labels, data_labels):
    ser = serial.Serial(port, baud_rate)
    last_data_time = time.time()  # Marca de tiempo para verificar datos
    while True:
        current_time = time.time()
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').strip()
            last_data_time = time.time()  # Actualizar tiempo de última recepción

            # Suponiendo que los datos llegan como "sensor1,sensor2,sensor3"
            sensor_data = data.split(',')
            if len(sensor_data) == 3:
                try:
                    temp = float(sensor_data[0])  # Temperatura (sensor 1)
                    light = sensor_data[1]  # Luz (sensor 2)
                    humidity = sensor_data[2]  # Humedad (sensor 3)

                    # Actualizar textos
                    labels[0].config(text=f"Temperatura")
                    data_labels[0].config(text=f"{temp}°C")

                    labels[1].config(text=f"Luz")
                    data_labels[1].config(text=f"{light} lux")

                    labels[2].config(text=f"Humedad")
                    data_labels[2].config(text=f"{humidity}%")
                except ValueError:
                    pass  # Ignorar datos mal formateados

        # Si no hay datos en 5 segundos, mostrar advertencia
        if current_time - last_data_time > 5:
            for label, data_label in zip(labels, data_labels):
                label.config(text="¡Sin datos!")
                data_label.config(text="⚠️", font=("Helvetica", 14), fg="red")

def animate_loading(data_labels):
    """Animar un reloj de arena en los datos de los sensores mientras cargan."""
    frames = ["⏳", "⌛"]  # Reloj de arena giratorio

    def loop():
        while True:
            for frame in frames:
                for data_label in data_labels:
                    current_text = data_label.cget("text")
                    if current_text != "⚠️":  # Solo animar si no está en estado de error
                        data_label.config(text=frame)
                time.sleep(0.5)  # Cambiar el frame cada 0.5 segundos

    thread = Thread(target=loop, daemon=True)
    thread.start()

def show_loading():
    """Mostrar estado de cargando en todos los sensores"""
    for frame, label, data_label in zip(sensor_frames, sensor_labels, sensor_data_labels):
        frame.config(bg="white")
        label.config(text="Calculando...", font=("Helvetica", 14), fg="black")
        data_label.config(text="⏳", font=("Helvetica", 12), fg="gray")
    animate_loading(sensor_data_labels)

def start_reading():
    show_loading()  # Mostrar estado de cargando
    port = "COM3"  # Cambia esto por el puerto donde está conectada tu ESP32
    baud_rate = 9600
    thread = Thread(target=read_serial, args=(port, baud_rate, sensor_labels, sensor_data_labels))
    thread.daemon = True
    thread.start()

def update_display():
    """Actualizar la interfaz para mostrar el sensor seleccionado y previsualizaciones."""
    for i, frame in enumerate(sensor_frames):
        frame.grid(row=0, column=i, padx=5, pady=5)  # Distribuir de forma fija
        frame.config(bg="white", width=200, height=100)  # Tamaño fijo
        sensor_labels[i].config(font=("Helvetica", 14), fg="black" if i == selected_sensor else "gray")
        sensor_data_labels[i].config(font=("Helvetica", 12), fg="black" if i == selected_sensor else "gray")

def key_pressed(event):
    global selected_sensor
    if event.char in ['1', '2', '3']:
        selected_sensor = int(event.char) - 1
    elif event.keysym == "Left":
        selected_sensor = (selected_sensor - 1) % 3  # Mover a la izquierda (circular)
    elif event.keysym == "Right":
        selected_sensor = (selected_sensor + 1) % 3  # Mover a la derecha (circular)

    update_display()

# Crear la ventana principal
root = tk.Tk()
root.title("Sensor Data Viewer")
root.geometry("500x200")  # Establecer tamaño fijo para la ventana
root.resizable(False, False)

# Crear un marco para organizar los logs
frame = tk.Frame(root, bg="white")
frame.pack(pady=20, padx=20)

# Crear las columnas para los sensores
sensor_labels = []
sensor_frames = []
sensor_data_labels = []
sensor_names = ["Temperatura", "Luz", "Humedad"]

for i, sensor_name in enumerate(sensor_names):
    column_frame = tk.Frame(frame, borderwidth=2, relief="ridge", bg="white", width=200, height=100)
    column_frame.grid_propagate(False)  # Evitar que cambie de tamaño

    sensor_label = tk.Label(column_frame, text=sensor_name, font=("Helvetica", 14), bg="white", fg="gray")
    sensor_label.pack()

    sensor_data_label = tk.Label(column_frame, text="", font=("Helvetica", 12), bg="white", fg="gray")
    sensor_data_label.pack()

    sensor_frames.append(column_frame)  # Guarda el marco para cambiar el color
    sensor_labels.append(sensor_label)
    sensor_data_labels.append(sensor_data_label)

# Inicializar el sensor seleccionado
selected_sensor = 0
update_display()

# Vincular teclas
root.bind("<Key>", key_pressed)

# Botón para iniciar la lectura
start_button = tk.Button(root, text="Start Reading", font=("Helvetica", 14), command=start_reading, bg="orange", fg="black")
start_button.pack(pady=10)

root.mainloop()
