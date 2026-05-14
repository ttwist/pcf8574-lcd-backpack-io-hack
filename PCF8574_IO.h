/**
 * @file PCF8574_IO.h
 * @author Your Name / GitHub Username
 * @brief Lightweight I/O expander library for modified LCD backpacks.
 * @version 1.0.0
 * @date 2026-05-14
 * 
 * @copyright Copyright (c) 2026 / MIT License
 */

#ifndef PCF8574_IO_H
#define PCF8574_IO_H

#include <Arduino.h>
#include <Wire.h>

class PCF8574_IO {
public:
    // Constructor: Takes I2C address (default 0x27) and optional custom TwoWire bus
    PCF8574_IO(uint8_t address = 0x27, TwoWire *wireBus = &Wire);

    void begin();
    void writeByte(uint8_t value);
    uint8_t readByte();
    
    void setupInput(uint8_t pin);
    void setPin(uint8_t pin, bool level);
    bool getPin(uint8_t pin);

private:
    uint8_t _address;
    TwoWire *_wire;
    uint8_t _portState; // Keeps track of the current state of all output pins
};

#endif
