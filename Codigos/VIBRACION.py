import network
import machine
import time
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.196"
MQTT_RESPUESTA = "actuador/vibracion"

# Configuración del pin del módulo de vibración
PIN_VIBRACION = 25  
motor = machine.Pin(PIN_VIBRACION, machine.Pin.OUT)

# Función para conectar WiFi
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        wifi.connect(SSID, PASSWORD)
        tiempo_inicio = time.time()
        while not wifi.isconnected():
            if time.time() - tiempo_inicio > 10:
                return False
            time.sleep(1)
    return True

# Conectar WiFi
if not conectar_wifi():
    raise Exception("Error al conectar WiFi")

# Configuración de MQTT
client = MQTTClient("ESP32_VIBRACION", MQTT_BROKER)
client.connect()

# Bucle principal de vibración
while True:
    motor.value(1)  # Encender vibración
    print("1")  # Mostrar en consola
    client.publish(MQTT_RESPUESTA, "1")  # Publicar en MQTT
    time.sleep(2)  # Esperar 2 segundos

    motor.value(0)  # Apagar vibración
    print("0")  # Mostrar en consola
    client.publish(MQTT_RESPUESTA, "0")  # Publicar en MQTT
    time.sleep(2)  # Esperar 2 segundos
