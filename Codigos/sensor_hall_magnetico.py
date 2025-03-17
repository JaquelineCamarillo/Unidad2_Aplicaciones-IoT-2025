import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configurar WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configurar MQTT
MQTT_BROKER = "192.168.137.196"  # IP de la Raspberry Pi
MQTT_TOPIC = "sensor/magnetismo"

# 🔹 Configurar el pin para la salida digital del sensor KY-003
PIN_SENSOR = 34  # Asegúrate de usar el pin correcto para tu ESP32
sensor_pin = machine.Pin(PIN_SENSOR, machine.Pin.IN)

# 🔹 Función para conectar WiFi
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

# 🔹 Configuración de MQTT
try:
    client = MQTTClient("ESP32_Magnetismo", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para leer el estado del sensor KY-003
def leer_estado_sensor():
    return sensor_pin.value()  # 1 = No hay campo magnético, 0 = Campo magnético detectado

# 🔹 Función para enviar el estado por MQTT
def enviar_estado():
    estado = leer_estado_sensor()
    data = str(estado)  # Convertir el valor a string
    client.publish(MQTT_TOPIC, data)
    print("📤 Estado del sensor enviado:", data)

# 🔹 Bucle principal
while True:
    try:
        enviar_estado()  # Leer y enviar el estado del sensor
        time.sleep(10)   # Enviar cada 10 segundos

    except Exception as e:
        print("❌ Error en el bucle:", e)