import serial
import requests
import psutil
import time

PUERTO = "COM4"
BAUDRATE = 115200
INTERVALO = 2

def get_hardware_data():
    try:
        r = requests.get("http://localhost:8085/data.json", timeout=2)
        data = r.json()

        def buscar_por_sensorid(node, sensor_id):
            if node.get("SensorId") == sensor_id:
                return node.get("Value", "")
            for child in node.get("Children", []):
                result = buscar_por_sensorid(child, sensor_id)
                if result is not None:
                    return result
            return None

        cpu_raw = buscar_por_sensorid(data, "/amdcpu/0/temperature/2")
        gpu_raw = buscar_por_sensorid(data, "/gpu-nvidia/0/temperature/0")
        ram_raw = buscar_por_sensorid(data, "/ram/data/0")

        def limpiar(valor):
            if valor:
                return valor.split(" ")[0]
            return "N/A"

        return {
            "cpu": limpiar(cpu_raw),
            "gpu": limpiar(gpu_raw),
            "ram": limpiar(ram_raw)
        }

    except Exception as e:
        print(f"Error leyendo sensores: {e}")
        return None

print(f"Conectando a {PUERTO}...")
try:
    ser = serial.Serial(PUERTO, BAUDRATE, timeout=1)
    print("Conectado!")
except Exception as e:
    print(f"Error puerto: {e}")
    exit()

while True:
    data = get_hardware_data()
    if data:
        mensaje = f"{data['cpu']}|{data['gpu']}|{data['ram']}\n"
        ser.write(mensaje.encode())
        print(f"CPU:{data['cpu']}  GPU:{data['gpu']}  RAM:{data['ram']}GB")
    time.sleep(INTERVALO)