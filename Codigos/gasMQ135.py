import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT
MQTT_TOPIC = "sensor/gas135"

# 🔹 Configuración del sensor MQ-135
PIN_ANALOGICO = 34  # Conectar la salida AO del MQ-135 a este GPIO
sensor_mq135 = machine.ADC(machine.Pin(PIN_ANALOGICO))

# Ajuste de resolución (0 - 4095 para ESP32)
sensor_mq135.width(machine.ADC.WIDTH_12BIT)

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
    client = MQTTClient("ESP32_MQ135", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para leer el sensor MQ-135
def leer_sensor():
    return sensor_mq135.read()  # Valor analógico entre 0 y 4095

# 🔹 Función para enviar datos por MQTT
def enviar_datos():
    valor = leer_sensor()
    client.publish(MQTT_TOPIC, str(valor))
    print(f"📤 Enviado - MQ-135: {valor}")

# 🔹 Bucle principal
while True:
    try:
        enviar_datos()  # Leer y enviar el valor del sensor
        time.sleep(4)  # Ajusta el tiempo de muestreo según lo necesites
    except Exception as e:
        print("❌ Error en el bucle:", e)
