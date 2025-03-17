import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT
MQTT_TOPIC = "sensor/tactil"

# 🔹 Configuración del sensor KY-036
PIN_ANALOGICO = 35   # AO -> GPIO 36 (ADC)
PIN_DIGITAL = 25    # DO -> GPIO 25 (Entrada digital)

# Configurar pines
sensor_analogico = machine.ADC(machine.Pin(PIN_ANALOGICO))
sensor_analogico.atten(machine.ADC.ATTN_11DB)  # Configurar ADC para rango 0-3.3V
sensor_digital = machine.Pin(PIN_DIGITAL, machine.Pin.IN)

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
    client = MQTTClient("ESP32_TACTIL", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Bucle principal
while True:
    try:
        valor_digital = sensor_digital.value()  # Leer salida digital (0 o 1)
        valor_analogico = sensor_analogico.read()  # Leer salida analógica (0-4095)

        # Publicar en MQTT
        client.publish(MQTT_TOPIC, str(valor_digital))

        # Mostrar en consola
        print(f"Digital: {valor_digital}, Analógico: {valor_analogico}")

        time.sleep(0.5)  # Espera medio segundo
    except Exception as e:
        print("❌ Error en el bucle:", e)
