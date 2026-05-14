# 🛠️ The 9-NOK I2C I/O Expander Hack
### Transforming a flawed LCD Backpack into a Clean 8-bit GPIO Breakout

Standard PCF8574 I2C LCD backpacks (often labeled HW-061) cost less than 1 USD / 9 NOK, making them significantly cheaper than buying a bare PCF8574 chip on a breakout board. However, a major hardware design flaw prevents them from being used for general I/O out of the box: **the backlight transistor lacks a base resistor**. 

When Pin 3 (P3) is pulled HIGH, the transistor's Base-Emitter junction clamps the entire logic line to ~0.7V. This destroys regular 3.3V/5V logic levels and overloads the PCF8574 chip by drawing maximum current.

This modification strips away unneeded components, fixes the voltage clamp flaw, routes the isolated P3 pin safely out to an unused terminal on the LCD header, and uncovers a bonus 10k potentiometer for analog sensing.

---

## 🪛 Hardware Modification Guide

### 1. What to Remove
To convert the backpack into a dedicated, safe 8-bit I/O module, desolder or clip the following parts:
*   **Transistor (Q1):** Remove the SOT-23 transistor completely to disconnect the P3 clamp from GND.
*   **Resistor (R7):** Remove the 4.7kΩ base resistor.
*   **LED Jumper & Headers:** Pull off the black jumper and desolder the two jumper pins.
*   **Unused LCD Header Pins:** Desolder or clip pins **8, 9, 10** (D1, D2, D3) and pins **15, 16** (LED+, LED-).

### 2. The P3 Bypass Wire
Solder a short jumper wire from the vacant PCF8574-side pad of **R7** directly to **LCD Pin 7 (D0)**. Because character LCDs use 4-bit mode, pins 7–10 are entirely unused, providing a clean routing path.

### 3. Bonus 10k Potentiometer
The onboard trimmer (originally for LCD contrast) is wired directly between VCC and GND. **LCD Pin 3 (V0)** is connected to the wiper. You can now use Pin 3 as a standalone analog dial connected directly to your microcontroller's ADC.

---

## 📸 Component Modification Diagrams

Below are visual guides indicating exactly which parts to remove and how the final trace bypass looks:


| Components to Remove | Final Modification Result |
| :---: | :---: |
| ![Components to Remove Placeholder](https://placeholder.com) | ![Final Result Placeholder](https://placeholder.com) |
| *Locate and remove Q1, R7, Jumper, and unused headers.* | *Bridge the R7 pad to LCD Pin 7 (D0).* |

> 💡 **Tip for adding your photos:** Upload your pictures to the repository, then change the image paths above to `./your-photo-before.jpg` and `./your-photo-after.jpg`.

---

## 🗺️ Modified Pinout Mapping


| Header Pin | New Breakout Function | PCF8574 Bit Map | Description |
| :--- | :--- | :--- | :--- |
| **Pin 3 (V0)** | **10k Potentiometer Wiper** | *None (Analog)* | Variable voltage. Connect to MCU Analog Input (ADC). |
| **Pin 4 (RS)** | Digital I/O | **P0** | General Digital Input/Output |
| **Pin 5 (RW)** | Digital I/O | **P1** | General Digital Input/Output |
| **Pin 6 (E)** | Digital I/O | **P2** | General Digital Input/Output |
| **Pin 7 (D0)** | **Digital I/O (Bypassed)** | **P3** | Safe 3.3V/5V logic (Formerly blocked by transistor) |
| **Pin 11 (D4)**| Digital I/O | **P4** | General Digital Input/Output |
| **Pin 12 (D5)**| Digital I/O | **P5** | General Digital Input/Output |
| **Pin 13 (D6)**| Digital I/O | **P6** | General Digital Input/Output |
| **Pin 14 (D7)**| Digital I/O | **P7** | General Digital Input/Output |

---

## 💻 Software Usage

Because the PCF8574 utilizes a **quasi-bidirectional** architecture, pins do not have direction registers. To read a pin as an input, it must be driven HIGH to activate its weak internal pull-up. The provided libraries handle this automatically via `setupInput()`.

### Arduino (C++) Quick Start
1. Include `PCF8574_IO.h` and `PCF8574_IO.cpp` in your sketch folder.
2. Initialize the library and toggle individual pins:
```cpp
#include "PCF8574_IO.h"
PCF8574_IO expander(0x27);

void setup() {
    expander.begin();
    expander.setupInput(0); // Set P0 as Input (Button to GND)
}

void loop() {
    bool pressed = !expander.getPin(0);
    expander.setPin(3, pressed); // Mirror state to P3 (LCD Pin 7)
}
```

### MicroPython Quick Start
1. Upload `pcf8574_io.py` to your microcontroller.
2. Run your control loop inside `main.py`:
```python
from machine import Pin, I2C
from pcf8574_io import PCF8574_IO

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
expander = PCF8574_IO(i2c, 0x27)

expander.setup_input(0) # Prepare P0 for button reading

while True:
    pressed = not expander.get_pin(0)
    expander.set_pin(3, pressed) # Control P3
```

---

## 🔗 License
This project is open-source and available under the **MIT License**. Feel free to use, modify, and distribute it for your own projects!
