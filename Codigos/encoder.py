import network
import machine
import time
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi
SSID = "JAQUELINE"
PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.196"  # IP del servidor MQTT
MQTT_TOPIC = "actuator/encoder"

# 🔹 Configuración de pines para KY-040
PIN_CLK = 32  # CLK -> GPIO 32
PIN_DT = 33   # DT -> GPIO 33
PIN_SW = 25   # SW -> GPIO 25 (botón)

# Configurar los pines en modo entrada
clk = machine.Pin(PIN_CLK, machine.Pin.IN, machine.Pin.PULL_UP)
dt = machine.Pin(PIN_DT, machine.Pin.IN, machine.Pin.PULL_UP)
sw = machine.Pin(PIN_SW, machine.Pin.IN, machine.Pin.PULL_UP)

# Variables para almacenar estado del encoder
contador = 0
ultimo_estado_clk = clk.value()

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
    client = MQTTClient("ESP32_ENCODER", MQTT_BROKER)
    client.connect()
    print("✅ Conectado a MQTT")
except Exception as e:
    print("❌ Error conectando a MQTT:", e)
    raise

# 🔹 Función para detectar rotación
def detectar_rotacion():
    global contador, ultimo_estado_clk
    estado_actual_clk = clk.value()

    if estado_actual_clk != ultimo_estado_clk:  # Detectar cambio de estado
        if dt.value() != estado_actual_clk:  # Giro en sentido horario
            contador += 1
        else:  # Giro en sentido antihorario
            contador -= 1

        # Publicar en MQTT
        client.publish(MQTT_TOPIC, str(contador))
        print(f"📤 Enviado - Contador: {contador}")

    ultimo_estado_clk = estado_actual_clk

# 🔹 Función para detectar pulsaciones del botón
def detectar_boton():
    if sw.value() == 0:  # Botón presionado
        print("🔘 Botón presionado")
        client.publish(MQTT_TOPIC, "boton_presionado")
        time.sleep(0.3)  # Pequeña pausa para evitar rebotes

# 🔹 Bucle principal
while True:
    try:
        detectar_rotacion()
        detectar_boton()
        time.sleep(0.01)  # Pequeña pausa para evitar sobrecarga del CPU
    except Exception as e:
        print("❌ Error en el bucle:", e)
