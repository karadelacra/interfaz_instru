import serial
import tkinter as tk
from threading import Thread
import time

# Parámetros del ADC
volt_ref = 3.3
res = 4096

# Variable global para almacenar datos
sensor_values = {"Temperatura": 0.0, "Luz": 0.0, "Humedad": 0.0}
sensor_names = ["Temperatura", "Luz", "Humedad"]


# Límites de los intervalos
TEMP_ALTA = 25
TEMP_BAJA = 18
HUM_ALTA = 80
HUM_BAJA = 60
LUX_ALTO = 156 #40,000 lux
LUX_BAJO = 120 #15,000 lux


# Función para leer datos desde el puerto serial
def read_serial(port, baud_rate):
    global sensor_values
    try:
        ser = serial.Serial(port, baud_rate, timeout=5)
    except Exception as e:
        print(f"Error al intentar abrir el puerto serial: {e}")
        return

    last_data_time = time.time()
    try:
        while True:
            current_time = time.time()
            if ser.in_waiting:
                try:
                    data = ser.readline()

                    try:
                        data = data.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        data = data.decode('latin-1').strip()

                    def separar_y_convertir_a_float(cadena):
                        flotantes = []
                        i = 0
                        while i < len(cadena):
                            if cadena[i] == '.':
                                if i + 2 < len(cadena):
                                    numero = cadena[:i + 3]
                                    try:
                                        flotantes.append(float(numero))
                                    except ValueError:
                                        print(f"No se pudo convertir '{numero}' a float, ignorando.")
                                    cadena = cadena[i + 3:]
                                    i = -1
                            i += 1
                        return flotantes

                    sensor_data = separar_y_convertir_a_float(data)
                    if len(sensor_data) == 3:
                        sensor_values["Temperatura"] = sensor_data[0]
                        sensor_values["Luz"] = sensor_data[2] + 10.9
                        sensor_values["Humedad"] = sensor_data[1]

                        last_data_time = time.time()
                except ValueError as ve:
                    print(f"Error al convertir datos: {ve}")
            if current_time - last_data_time > 5:
                sensor_values["Temperatura"] = "⚠ Sin datos"
                sensor_values["Luz"] = "⚠ Sin datos"
                sensor_values["Humedad"] = "⚠ Sin datos"
    except KeyboardInterrupt:
        print("Lectura serial interrumpida.")
    finally:
        if ser.is_open:
            ser.close()
            print("Puerto serial cerrado correctamente.")

# Actualizar la interfaz gráfica
def update_ui():
    # Evaluar las acciones necesarias
    temp = sensor_values["Temperatura"]
    hum = sensor_values["Humedad"]
    lux = sensor_values["Luz"]


    # Actualizar etiquetas de sensores
    for i, sensor_name in enumerate(sensor_names):
        value = sensor_values[sensor_name]
        if isinstance(value, (int, float)):
            value = round(value, 2)  # Redondear a 2 decimales
        if sensor_name == "Temperatura":
            if value == "⚠ Sin datos":
                sensor_data_labels[i].config(text=value, fg="gray")
                canvas.itemconfig(bar_rects[i], fill="gray")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value > TEMP_ALTA:
                sensor_data_labels[i].config(text=f"🔥 Alta: {value} °C", fg="red")
                bar_height = calculate_bar_height(value, TEMP_BAJA, TEMP_ALTA)
                canvas.itemconfig(bar_rects[i], fill="red")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value < TEMP_BAJA:
                sensor_data_labels[i].config(text=f"❄️ Baja: {value} °C", fg="blue")
                bar_height = calculate_bar_height(value, TEMP_BAJA, TEMP_ALTA)
                canvas.itemconfig(bar_rects[i], fill="blue")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            else:
                sensor_data_labels[i].config(text=f"✅ {value} °C", fg="green")
                bar_height = calculate_bar_height(value, TEMP_BAJA, TEMP_ALTA)
                canvas.itemconfig(bar_rects[i], fill="green")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
        elif sensor_name == "Humedad":
            if value == "⚠ Sin datos":
                sensor_data_labels[i].config(text=value, fg="gray")
                canvas.itemconfig(bar_rects[i], fill="gray")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value > HUM_ALTA:
                sensor_data_labels[i].config(text=f"💧 Alta: {value} %", fg="red")
                bar_height = calculate_bar_height(value, HUM_BAJA, HUM_ALTA)
                canvas.itemconfig(bar_rects[i], fill="red")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value < HUM_BAJA:
                sensor_data_labels[i].config(text=f"💧 Baja: {value} %", fg="blue")
                bar_height = calculate_bar_height(value, HUM_BAJA, HUM_ALTA)
                canvas.itemconfig(bar_rects[i], fill="blue")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            else:
                sensor_data_labels[i].config(text=f"✅ {value} %", fg="green")
                bar_height = calculate_bar_height(value, HUM_BAJA, HUM_ALTA)
                canvas.itemconfig(bar_rects[i], fill="green")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
        elif sensor_name == "Luz":
            if value == "⚠ Sin datos":
                sensor_data_labels[i].config(text=value, fg="gray")
                canvas.itemconfig(bar_rects[i], fill="gray")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value > LUX_ALTO:
                sensor_data_labels[i].config(text=f"☀️ Alta:  {round(value*value*1.5, 2)} Lux", fg="red")
                bar_height = calculate_bar_height(value, LUX_BAJO, LUX_ALTO)
                canvas.itemconfig(bar_rects[i], fill="red")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            elif value < LUX_BAJO:
                sensor_data_labels[i].config(text=f"☀️ Baja: {round(value*value*1.3, 2)} Lux", fg="blue")
                bar_height = calculate_bar_height(value, LUX_BAJO, LUX_ALTO)
                canvas.itemconfig(bar_rects[i], fill="blue")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)
            else:
                sensor_data_labels[i].config(text=f"✅ {round(value*value*1.4, 2)} Lux", fg="green")
                bar_height = calculate_bar_height(value, LUX_BAJO, LUX_ALTO)
                canvas.itemconfig(bar_rects[i], fill="green")
                canvas.coords(bar_rects[i], i * 100 + 50, BAR_MAX_HEIGHT - bar_height, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT)


    root.after(500, update_ui)  # Actualizar cada 500 ms

# Calcular altura de la barra basada en el valor actual y los límites
def calculate_bar_height(value, min_val, max_val):
    if value == "⚠ Sin datos":
        return 0
    if value < min_val:
        return 0
    if value > max_val:
        return BAR_MAX_HEIGHT
    return int((value - min_val) / (max_val - min_val) * BAR_MAX_HEIGHT)

# Iniciar la lectura serial en un hilo
def start_reading():
    port = "COM5"  # Cambia esto por el puerto donde está conectada tu ESP32
    baud_rate = 9600
    thread = Thread(target=read_serial, args=(port, baud_rate))
    thread.daemon = True
    thread.start()

# Crear la ventana principal
root = tk.Tk()
root.title("Sensor Data Viewer")
root.geometry("500x500")
root.resizable(False, False)

# Crear un canvas para las barras
BAR_WIDTH = 50
BAR_MAX_HEIGHT = 200
canvas = tk.Canvas(root, width=400, height=BAR_MAX_HEIGHT + 50, bg="white")
canvas.pack(pady=10)

# Crear barras para cada sensor
bar_rects = []
for i in range(len(sensor_names)):
    bar = canvas.create_rectangle(i * 100 + 50, BAR_MAX_HEIGHT, i * 100 + 50 + BAR_WIDTH, BAR_MAX_HEIGHT, fill="gray")
    bar_rects.append(bar)

# Crear un marco para organizar los datos
frame = tk.Frame(root, bg="white")
frame.pack(pady=20, padx=20)

# Crear las columnas para los sensores
sensor_labels = []
sensor_frames = []
sensor_data_labels = []

for i, sensor_name in enumerate(sensor_names):
    column_frame = tk.Frame(frame, borderwidth=2, relief="ridge", bg="white", width=200, height=100)
    column_frame.grid_propagate(False)

    sensor_label = tk.Label(column_frame, text=sensor_name, font=("Helvetica", 14), bg="white", fg="gray")
    sensor_label.pack()

    sensor_data_label = tk.Label(column_frame, text="", font=("Helvetica", 12), bg="white", fg="gray")
    sensor_data_label.pack()

    sensor_frames.append(column_frame)
    sensor_labels.append(sensor_label)
    sensor_data_labels.append(sensor_data_label)

# Mostrar las columnas en la interfaz
for i, frame in enumerate(sensor_frames):
    frame.grid(row=0, column=i, padx=5, pady=5)

# Botón para iniciar la lectura
start_button = tk.Button(root, text="Iniciar Lectura", font=("Helvetica", 14), command=start_reading, bg="orange", fg="black")
start_button.pack(pady=10)

# Actualizar la interfaz periódicamente
root.after(500, update_ui)

# Iniciar la interfaz gráfica
root.mainloop()
