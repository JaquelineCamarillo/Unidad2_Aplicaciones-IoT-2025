import network
import time
from machine import Pin, time_pulse_us
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.42.100"
MQTT_PORT = 1883  # 📌 Agregado
MQTT_TOPIC = "cecr/distancia"

# 🔗 Conectar a WiFi con reintentos
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    
    intentos = 0
    while not wifi.isconnected() and intentos < 10:
        print("Conectando a WiFi...")
        time.sleep(1)
        intentos += 1

    if wifi.isconnected():
        print("Conectado a WiFi! IP:", wifi.ifconfig()[0])
    else:
        print("Error: No se pudo conectar a WiFi")

# 📡 Conectar a MQTT con manejo de errores
def conectar_mqtt():
    try:
        client = MQTTClient("ESP32", MQTT_BROKER, MQTT_PORT)
        client.connect()
        print("Conectado a MQTT!")
        return client
    except Exception as e:
        print("Error al conectar a MQTT:", e)
        return None

# 📏 Configuración de pines del HC-SR04
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

# 📏 Medir distancia con el HC-SR04
def medir_distancia():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()

    duracion = time_pulse_us(ECHO, 1, 30000)  # Máx. 30ms (5m)

    if duracion < 0:
        print("Error: No se detectó señal")
        return None

    distancia = (duracion * 0.0343) / 2  # Convertir a cm
    return distancia

# 🏁 Código principal
conectar_wifi()
client = conectar_mqtt()

if client:
    while True:
        distancia = medir_distancia()
        if distancia is not None:
            mensaje = f"{distancia:.2f}"  # Formato numérico
            client.publish(MQTT_TOPIC, mensaje)
            print(f"Enviado: {mensaje} cm")
        time.sleep(1)
else:
    print("No se pudo conectar a MQTT, revisa la configuración.")