import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT
MQTT_TOPIC = "sensor/impacto"

# 🔹 Configuración del sensor KY-031 (salida analógica)
PIN_KY031 = 34  # Conectar la salida analógica del KY-031 a este GPIO
adc = machine.ADC(machine.Pin(PIN_KY031))
adc.atten(machine.ADC.ATTN_0DB)  # Configuración de rango de 0-3.3V
adc.width(machine.ADC.WIDTH_12BIT)  # Configura la resolución a 12 bits (0-4095)

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
    client = MQTTClient("ESP32_KY031", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para leer el sensor KY-031
def leer_sensor():
    # Leer el valor analógico del sensor KY-031 (valor entre 0 y 4095)
    return adc.read()

# 🔹 Función para enviar datos por MQTT
def enviar_datos():
    valor = leer_sensor()
    client.publish(MQTT_TOPIC, str(valor))
    print(f"📤 Enviado - KY-031 Valor: {valor}")

# 🔹 Bucle principal
while True:
    try:
        enviar_datos()  # Leer y enviar el valor del sensor
        time.sleep(5)  # Ajusta el tiempo de muestreo
    except Exception as e:
        print("❌ Error en el bucle:", e)
