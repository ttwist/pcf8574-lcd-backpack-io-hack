"""
@file pcf8574_io.py
@author Your Name / GitHub Username
@brief Lightweight MicroPython I/O expander class for modified LCD backpacks.
@version 1.0.0
@date 2026-05-14

@copyright Copyright (c) 2026 / MIT License
"""

from machine import I2C

class PCF8574_IO:
    def __init__(self, i2c: I2C, address: int = 0x27):
        """Initializes the chip with an I2C object and address (e.g., 0x27 or 0x3F)."""
        self.i2c = i2c
        self.address = address
        # Default startup state for PCF8574 is all pins HIGH (0xFF)
        # This makes all pins ready to be used as inputs or weak outputs
        self._port_state = 0xFF 
        self.write_byte(self._port_state)

    def write_byte(self, value: int):
        """Writes a full 8-bit byte (0-255) to the port."""
        self._port_state = value & 0xFF  # Keep within 1-byte boundary
        self.i2c.writeto(self.address, bytearray([self._port_state]))

    def read_byte(self) -> int:
        """Reads the live physical state of all 8 pins directly from the chip."""
        # readfrom returns a bytes object; we extract the first element (int)
        return self.i2c.readfrom(self.address, 1)[0]

    def setup_input(self, pin: int):
        """Prepares a pin (0-7) to be used as an input by writing it HIGH."""
        if not (0 <= pin <= 7):
            raise ValueError("Pin must be between 0 and 7")
        self._port_state |= (1 << pin)  # Input pins must be driven HIGH
        self.write_byte(self._port_state)

    def set_pin(self, pin: int, level: bool):
        """Sets an individual output pin (0-7) to HIGH or LOW."""
        if not (0 <= pin <= 7):
            raise ValueError("Pin must be between 0 and 7")
        
        if level:
            self._port_state |= (1 << pin)
        else:
            self._port_state &= ~(1 << pin)
            
        self.write_byte(self._port_state)

    def get_pin(self, pin: int) -> bool:
        """Reads the real-time logical level of a single pin (0-7)."""
        if not (0 <= pin <= 7):
            raise ValueError("Pin must be between 0 and 7")
        
        current_state = self.read_byte()
        return bool((current_state >> pin) & 1)
