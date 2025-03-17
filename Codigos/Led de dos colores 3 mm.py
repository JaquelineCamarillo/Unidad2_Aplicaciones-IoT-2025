import machine
import time

# 🔹 Configuración del pin de control del LED de dos colores (KY-029)
PIN_LED_CONTROL = 33  # Conectar el pin de control del KY-029 a este GPIO
led_control = machine.Pin(PIN_LED_CONTROL, machine.Pin.OUT)

# 🔹 Función para encender el LED en color rojo
def encender_rojo():
    led_control.value(1)  # HIGH en el pin de control para encender rojo
    print("🔴 LED Rojo Encendido")

# 🔹 Función para encender el LED en color verde
def encender_verde():
    led_control.value(0)  # LOW en el pin de control para encender verde
    print("🟢 LED Verde Encendido")

# 🔹 Bucle principal
while True:
    encender_rojo()  # Enciende el LED en rojo
    time.sleep(2)  # Espera 2 segundos
    encender_verde()  # Enciende el LED en verde
    time.sleep(2)  # Espera 2 segundos
