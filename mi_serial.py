import serial

def read_serial(port, baud_rate=9600):
    ser = serial.Serial(port, baud_rate)
    while True:
        if ser.in_waiting:
            data = ser.readline().decode('utf-8').strip()
            print(f"Data received: {data}")
            # Aquí podrías actualizar la interfaz con los datos recibidos
