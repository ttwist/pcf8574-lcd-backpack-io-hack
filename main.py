"""
@file main.py
@brief Demonstration script using the modified PCF8574 LCD backpack in MicroPython.
@version 1.0.0
"""

from machine import Pin, I2C
import time
from pcf8574_io import PCF8574_IO

# 1. Setup I2C (Adjust SCL, SDA pins, and bus ID for your specific microcontroller board)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
expander = PCF8574_IO(i2c, address=0x27)

# 2. Define pin routing mapping
BUTTON_PIN = 0  # Tactile switch connected between P0 and GND
LED_PIN = 3     # Modified P3 pin (LCD pin 7) connected to LED via resistor

# Configure P0 as an input (activates the weak internal pull-up)
expander.setup_input(BUTTON_PIN)

print("Modified PCF8574 I/O Expansion board active!")
print("Press the button on P0 to light up the LED on P3...")

try:
    while True:
        # The switch pulls the pin to GND, so it returns False when pressed
        button_pressed = not expander.get_pin(BUTTON_PIN)
        
        if button_pressed:
            expander.set_pin(LED_PIN, True)   # Turn ON LED on P3
        else:
            expander.set_pin(LED_PIN, False)  # Turn OFF LED on P3
            
        time.sleep(0.02)  # Short delay for debouncing stability

except KeyboardInterrupt:
    # Clear all pins on software exit (Ctrl+C)
    expander.write_byte(0x00)
    print("Program stopped.")
