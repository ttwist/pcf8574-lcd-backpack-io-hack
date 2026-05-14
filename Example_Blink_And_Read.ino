/**
 * @file Example_Blink_And_Read.ino
 * @brief Demonstration sketch using the modified PCF8574 LCD backpack.
 * @version 1.0.0
 */

#include <Arduino.h>
#include "PCF8574_IO.h"

// Instantiate the expander object with default I2C address 0x27
PCF8574_IO expander(0x27);

const uint8_t BUTTON_PIN = 0;   // Tactile switch connected between P0 and GND
const uint8_t LED_PIN = 3;      // Modified P3 pin (LCD pin 7) connected to LED via resistor
const int POT_ANALOG_PIN = A0;   // Wire from LCD pin 3 (V0) to Arduino's Analog A0

void setup() {
    Serial.begin(115200);
    
    // Initialize the I2C bus and PCF8574
    expander.begin();
    
    // Configure P0 as input (writes logic 1 to the pin)
    expander.setupInput(BUTTON_PIN);
    
    Serial.println("Modified PCF8574 I/O Expansion board ready!");
}

void loop() {
    // --- 1. Handle Expander I/O ---
    // The switch pulls the pin to GND, so it is pressed when getPin returns false
    bool buttonPressed = !expander.getPin(BUTTON_PIN);
    
    if (buttonPressed) {
        expander.setPin(LED_PIN, true);  // Turn ON LED on P3
    } else {
        expander.setPin(LED_PIN, false); // Turn OFF LED on P3
    }
    
    // --- 2. Handle the Onboard Bonus Potentiometer ---
    int potValue = analogRead(POT_ANALOG_PIN);
    
    // Print potentiometer telemetry to Serial Monitor every 500ms
    static unsigned long lastPrint = 0;
    if (millis() - lastPrint > 500) {
        Serial.print("Bonus Potentiometer Value on ADC: ");
        Serial.println(potValue);
        lastPrint = millis();
    }
    
    delay(20); // Short delay for debouncing stability
}
