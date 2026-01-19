# BLE-Based Fire and Gas Monitoring System

A real-time fire and gas monitoring system built using **Arduino UNO R4**, environmental sensors, Bluetooth Low Energy (BLE), and cloud integration via **ThingSpeak**.
The Arduino works as a BLE peripheral, while a Python application receives data and uploads it to the cloud.

---

## Project Overview

This project continuously monitors:
- Gas concentration
- Flame presence
- Temperature
- Humidity

When a dangerous condition is detected, the system:
- Activates a buzzer
- Shows alerts on an RGB LCD
- Sends data over BLE
- Uploads readings to ThingSpeak

---

## Features

- Real-time gas and flame detection
- Temperature and humidity monitoring
- RGB LCD display
- Audible alert system
- BLE notification-based communication
- Python BLE client
- Cloud data logging

---

## System Architecture

Sensors → Arduino UNO R4 → BLE → Python Client → ThingSpeak Cloud

---

## Hardware Requirements

- Arduino UNO R4 (WiFi or Minima)
- DHT11 Temperature & Humidity Sensor
- MQ Gas Sensor (Analog)
- Flame Sensor (Digital)
- RGB 16x2 LCD (I2C)
- Buzzer
- Breadboard and jumper wires
- USB cable

---

## Pin Configuration

| Component | Arduino Pin |
|---------|-------------|
| DHT11 | D2 |
| Flame Sensor | D3 |
| Gas Sensor | A0 |
| Buzzer | D8 |
| RGB LCD | I2C |

---

## Arduino Software Setup

### Required Libraries

Install from Arduino Library Manager:
- ArduinoBLE
- DHT sensor library (Adafruit)
- Adafruit Unified Sensor
- rgb_lcd (Seeed Studio / Grove)
- Wire (built-in)

### Arduino Includes

```cpp
#include <ArduinoBLE.h>
#include <DHT.h>
#include <Wire.h>
#include "rgb_lcd.h"
```

---

## BLE Configuration

- Device Name: UNO_R4_FIRE
- Service UUID: 19B10000-E8F2-537E-4F6C-D104768A1216
- Characteristic UUID: 19B10001-E8F2-537E-4F6C-D104768A1216
- Mode: Read + Notify

### Data Format

STATUS|TEMP|GAS|HUMIDITY|FLAME

Example:
ALERT|32.5|180|58|1

---

## Alert Logic

- Gas alert when value ≥ 150
- Flame alert when flame detected
- Buzzer ON during alert
- LCD color:
  - Green = Safe
  - Red = Alert

---

## Python Client Setup

### Requirements
- Python 3.8+
- Bluetooth-enabled system

### Install Dependencies

```bash
pip install bleak requests
```

### Used Libraries

```python
import asyncio
import requests
from bleak import BleakScanner, BleakClient
```

---

## ThingSpeak Setup

Configure a ThingSpeak channel with these fields:

| Field | Data |
|------|------|
| 1 | Status |
| 2 | Temperature |
| 3 | Gas |
| 4 | Humidity |
| 5 | Flame |

Update credentials in Python code:
```python
THINGSPEAK_WRITE_KEY = "YOUR_API_KEY"
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
```

---

## How to Run

### Arduino
1. Connect hardware
2. Upload sketch
3. Close Serial Monitor
4. Power the board

### Python
```bash
python ble_thingspeak_client.py
```

---

## Common Issues

- BLE not found: Close Serial Monitor and restart Arduino
- LCD not working: Check I2C wiring and library
- ThingSpeak error: Verify API key and network

---

## Author

Arun Chaudhary

---

## License

Educational and academic use only.
