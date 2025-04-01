import network
import time
import machine
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.42.100"
MQTT_PORT = 1883  
MQTT_TOPIC = "cecr/potenciometro"

# 📌 Configuración del pin analógico
POT_PIN = 34  # GPIO34 (entrada ADC)
adc = machine.ADC(machine.Pin(POT_PIN))
adc.atten(machine.ADC.ATTN_11DB)  # Rango de 0V a 3.3V
adc.width(machine.ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)

# 🔗 Conectar a WiFi
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

# 📡 Conectar a MQTT
def conectar_mqtt():
    try:
        client = MQTTClient("ESP32_POT", MQTT_BROKER, MQTT_PORT)
        client.connect()
        print("Conectado a MQTT!")
        return client
    except Exception as e:
        print("Error al conectar a MQTT:", e)
        return None

# 🏁 Código principal
conectar_wifi()
client = conectar_mqtt()

if client:
    while True:
        valor = adc.read()  # Leer el valor del potenciómetro (0-4095)
        mensaje = str(valor)  # Convertir a string para MQTT
        client.publish(MQTT_TOPIC, mensaje)
        print(f"Enviado: {mensaje}")
        time.sleep(1)  # Enviar cada segundo
else:
    print("No se pudo conectar a MQTT, revisa la configuración.")