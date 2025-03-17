import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configurar WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configurar MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT (Raspberry Pi)
MQTT_TOPIC = "sensor/gas"

# 🔹 Configuración del sensor MQ-5
PIN_ANALOGICO = 34  # Salida AO (Cambiar si usas otro GPIO)
sensor_analogico = machine.ADC(machine.Pin(PIN_ANALOGICO))
sensor_analogico.width(machine.ADC.WIDTH_10BIT)  # Rango de 0 a 1023

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
    client = MQTTClient("ESP32_Gas", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para leer el sensor MQ-5
def leer_sensor():
    return sensor_analogico.read()  # Lectura de 0 a 1023

# 🔹 Función para enviar datos por MQTT
def enviar_datos():
    valor = leer_sensor()
    client.publish(MQTT_TOPIC, str(valor))  # Enviar solo el número
    print("📤 Dato enviado:", valor)

# 🔹 Bucle principal
while True:
    try:
        enviar_datos()  # Leer y enviar el valor del sensor
        time.sleep(10)   # Enviar cada 10 segundos

    except Exception as e:
        print("❌ Error en el bucle:", e)