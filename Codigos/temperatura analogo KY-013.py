import network
import time
import ubinascii
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# 📌 Configuración WiFi
WIFI_SSID = "LEO"
WIFI_PASSWORD = "94941890"

# 📌 Configuración MQTT
MQTT_BROKER = "192.168.137.242"  # Cambia por la IP de tu broker Mosquitto
MQTT_PORT = 1883
MQTT_TOPIC = "jajj/temperatura"
CLIENT_ID = ubinascii.hexlify(network.WLAN().config('mac')).decode()

# 📌 Pines
SENSOR_PIN = 34  # ⚡ PIN ANALÓGICO para el sensor KY-013
LED_PIN = 2      # LED integrado del ESP32

# 🛠️ Configurar Sensor y LED
sensor = ADC(Pin(SENSOR_PIN))  
sensor.atten(ADC.ATTN_11DB)  # Rango completo de 0 a 3.3V
led = Pin(LED_PIN, Pin.OUT)

# 🔹 Conectar a WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Conectando a WiFi...", end=" ")

    intentos = 10
    while not wlan.isconnected() and intentos > 0:
        time.sleep(1)
        print(".", end="")
        intentos -= 1

    if wlan.isconnected():
        print("Conectado:", wlan.ifconfig())
    else:
        print("Error de conexión WiFi. Reiniciando...")
        time.sleep(2)
        machine.reset()  # Reinicia el ESP32 si no se conecta

# 🔹 Conectar a MQTT con reintento
def conectar_mqtt():
    while True:
        try:
            client = MQTTClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT)
            client.connect()
            print(" Conectado al broker MQTT")
            return client
        except Exception as e:
            print(f" Error MQTT: {e}, reintentando en 5 segundos...")
            time.sleep(5)

# 🔹 Función para obtener la temperatura en °C
def leer_temperatura():
    valor = sensor.read()  # Valor analógico (0-4095)
    voltaje = (valor / 4095.0) * 3.3  # Convertir a voltaje
    temperatura = voltaje * 100  # LM35: 10mV por grado
    return round(temperatura, 2)  # Redondear a 2 decimales

# 🔹 Programa principal
conectar_wifi()
mqtt_client = conectar_mqtt()

estado_anterior = None

while True:
    try:
        temperatura = leer_temperatura()
        print(f" Temperatura: {temperatura} °C")

        # Enviar datos a MQTT si cambia el valor
        if estado_anterior is None or abs(temperatura - estado_anterior) > 0.5:
            mqtt_client.publish(MQTT_TOPIC, str(temperatura))
            print(f" Enviado a MQTT: {temperatura}")
            estado_anterior = temperatura  # Actualiza el estado

        # Enciende LED si la temperatura es alta
        led.value(1 if temperatura > 30 else 0)

        # Verifica conexión WiFi y MQTT
        if not network.WLAN(network.STA_IF).isconnected():
            print("WiFi desconectado, reconectando...")
            conectar_wifi()

        time.sleep(2)  # Espera 2s antes de la siguiente lectura

    except Exception as e:
        print(f"Error en loop: {e}, intentando reconectar...")
        time.sleep(2)
        mqtt_client = conectar_mqtt()  # Reconectar MQTT
