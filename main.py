# TODO geef de afstand weer op een lcd scherm of het aantal vrienden.
#  verstuur de afstand via serial. Geef dit ook weer online
import utime
import neopixel
import machine
import sys
import time
from machine import Pin

# Define pins
trigger = machine.Pin(14, machine.Pin.OUT)
echo = machine.Pin(15, machine.Pin.IN)
sensor = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
np = neopixel.NeoPixel(machine.Pin(16), 8)
url = "http://localhost:8000/raspberry/set-online-status/"
uart = sys.stdout



def neopixel():
    red = [255, 0, 0]
    green = [0, 255, 0]
    orange = [255, 120, 0]
    minimal_distance = 50
    optimal_distance = 80

    # roep de functie measure_distance aan om de afstand op te halen
    distance = measure_distance()
    if distance < minimal_distance:
        # berekening voor de hoeveelheid lampen die aangezet moeten worden
        number_off_lit_leds = int((distance // (minimal_distance / 8)))
        set_neopixel_color(red, number_off_lit_leds)
        print("True")
    elif minimal_distance <= distance < optimal_distance:
        # berekening voor de hoeveelheid lampen die aangezet moeten worden
        number_of_lit_leds = int(8 - ((distance - minimal_distance) // ((optimal_distance - minimal_distance) / 8)))
        set_neopixel_color(orange, number_of_lit_leds)
        print("True")
    else:
        set_neopixel_color(green, 0)
        print("False")


def set_neopixel_color(color, number_of_leds):
    for i in range(0, 8 - number_of_leds):
        np[i] = color
        np.write()

    for j in range(8 - number_of_leds, 8):
        np[j] = [0, 0, 0]
        np.write()


def send_signal(message):
    #sends True or false to the computer
    try:
        serial_port = "COM3"  #Port where the pico is connected to

        time.sleep(2)
        # Allow the serial connection to initialize

        # Send the message
        uart.write(message.encode())
        uart.close()
    except Exception as e:
        print(f"Error sending signal: {e}")


def measure_distance():
    # Send a 10us pulse to trigger the sensor
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()

    # Measure the duration of the echo pulse
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    while echo.value() == 1:
        signal_on = utime.ticks_us()

    time_passed = utime.ticks_diff(signal_on, signal_off)

    # Calculate distance (time_passed / 2) * speed of sound (34300 cm/s)
    distance = (time_passed * 0.0343) / 2
    return distance



while True:

    # test_uart_over_usb()
    neopixel()
    utime.sleep(1)
