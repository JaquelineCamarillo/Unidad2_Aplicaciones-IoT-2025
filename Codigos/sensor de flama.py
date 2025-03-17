import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT
MQTT_TOPIC = "sensor/flama"

# 🔹 Configuración del sensor KY-026
PIN_KY026 = 33  # Conectar la salida del KY-026 a este GPIO
sensor_ky026 = machine.Pin(PIN_KY026, machine.Pin.IN)

# 🔹 Función para conectar WiFi
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("🔄 Conectando a WiFi...")
        wifi.connect(SSID, PASSWORD)
        tiempo_inicio = time.time()
        while not wifi.isconnected():
            if time.time() - tiempo_inicio > 10:
                print("❌ No se pudo conectar a WiFi")
                return False
            time.sleep(1)
    print("✅ Conectado a WiFi:", wifi.ifconfig())
    return True

# 🔹 Conectar WiFi
if not conectar_wifi():
    raise Exception("⚠ Error al conectar WiFi")

# 🔹 Configuración de MQTT
try:
    client = MQTTClient("ESP32_KY026", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para leer el sensor KY-026
def leer_sensor():
    return sensor_ky026.value()  # 0 = Fuego detectado, 1 = No se detecta fuego

# 🔹 Función para enviar datos por MQTT
def enviar_datos():
    estado = leer_sensor()
    client.publish(MQTT_TOPIC, str(estado))
    print(f"📤 Enviado - KY-026 Estado: {estado}")

# 🔹 Bucle principal
while True:
    try:
        enviar_datos()  # Leer y enviar el valor del sensor
        time.sleep(5)  # Ajusta el tiempo de muestreo
    except Exception as e:
        print("❌ Error en el bucle:", e)
