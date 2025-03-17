from machine import Pin
import network
import time
import ubinascii
import usocket
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"

# Configuración MQTT
MQTT_BROKER = "192.168.187.101"  # Reemplázalo con la IP de tu Raspberry Pi
MQTT_CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac')).decode()
MQTT_TOPIC = "sensor/botton"

# Conectar al WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)
print("Conectado a WiFi")
print("Dirección IP:", wlan.ifconfig())

# Verificar conexión al broker MQTT
def check_mqtt_connection(host, port, timeout=5):
    try:
        s = usocket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception as e:
        print("Error conectando a MQTT:", e)
        return False

if check_mqtt_connection(MQTT_BROKER, 1883):
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()
    print("Conectado al broker MQTT")
else:
    print("No se pudo conectar a MQTT")
    while True:
        time.sleep(1)  # Evita que el código continúe si no hay conexión MQTT

# Configurar botón
boton = Pin(4, Pin.IN, Pin.PULL_UP)  # Usa el pin GPIO4 o cambia según tu conexión
estado = 0

while True:
    print("Esperando pulsación...")
    if not boton.value():  # Si el botón se presiona (activo bajo)
        estado = not estado  # Alterna entre 0 y 1
        print(f"Publicando: {estado}")  
        try:
            client.publish(MQTT_TOPIC, str(estado))
        except Exception as e:
            print("Error publicando MQTT:", e)
        time.sleep(0.3)  # Pequeña espera para evitar rebotes
    try:
        client.check_msg()  # Mantiene activa la conexión MQTT
    except Exception as e:
        print("Error en la conexión MQTT:", e)
        time.sleep(1)