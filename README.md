# 🖥️ WindowsStats Monitor Temp & ram usage → Serial → ESP32 → LCD i2c

Monitor hardware stats from **Windows 10** (CPU°, GPU°, RAM,) displayed in real-time on a **2x16 LCD i2c** connected to an **ESP32**, using **LibreHardwareMonitor** as data source via HTTP + Python serial bridge.

<img width="703" height="834" alt="image" src="https://github.com/user-attachments/assets/4918dd16-4c2d-468c-9046-e3c04294bea2" />
---

## 📐 Architecture

```
[Windows 10]
    LibreHardwareMonitor (Web Server :8085)
            ↓  HTTP GET (JSON)
    monitor.py (Python Script)
            ↓  Serial COM Port
    [ESP32]
            ↓  I2C
    LCD 2x16 (PCF8574 backpack)
```

---

## 🧰 Requirements

### Hardware
- ESP32 (any variant with USB)
- LCD 2x16 with I2C backpack (PCF8574, address `0x27` or `0x3F`)
- USB cable (ESP32 ↔ PC)

### Software
- Windows 10
- [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases)
- Python 3.8+
- Arduino IDE 2.x
- Libraries: `pyserial`, `requests`

---

## 🚀 Setup Guide

### Step 1 — Install & Configure LibreHardwareMonitor

1. Download the latest release from the [LibreHardwareMonitor releases page](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases).
2. Extract the ZIP and run **LibreHardwareMonitor.exe** as **Administrator** (required for full sensor access).
3. In the menu bar go to:
   ```
   Options → Web Server
   ```
4. Enable the web server and set port to **8085**.
5. Click **Start** — the server will expose hardware data at:
   ```
   http://localhost:8085/data.json
   ```

> ✅ Verify it works by opening `http://localhost:8085/data.json` in your browser. You should see a JSON tree of sensors.

---

### Step 2 — Wire the LCD i2c to the ESP32

| LCD I2C Pin | ESP32 Pin |
|-------------|-----------|
| VCC         | 3.3V or 5V |
| GND         | GND       |
| SDA         | GPIO 21   |
| SCL         | GPIO 22   |

> ⚠️ Some LCD backpacks require 5V. Use a level shifter or check your module's datasheet.

---

### Step 3 — Upload Arduino Code to ESP32

1. Open **Arduino IDE 2.x**.
2. Install the ESP32 board package if not already installed:
   - Go to `File → Preferences` and add to "Additional boards manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Then go to `Tools → Board → Boards Manager`, search `esp32` and install.
3. Install the required library:
   - Go to `Sketch → Include Library → Manage Libraries`
   - Search and install **LiquidCrystal_I2C** by Frank de Brabander.
4. Open the file `esp32_lcd_monitor.ino` from this repository.
5. Edit the I2C address if needed (default `0x27`):
   ```cpp
   LiquidCrystal_I2C lcd(0x27, 16, 2);
   ```
6. Select your board:
   ```
   Tools → Board → ESP32 Arduino → ESP32 Dev Module
   ```
7. Select the correct COM port:
   ```
   Tools → Port → COMx  (the one assigned to your ESP32)
   ```
8. Click **Upload** (→).
9. Open `Tools → Serial Monitor` at **115200 baud** and confirm the ESP32 is waiting for data:
   ```
   [ESP32] Ready. Waiting for serial data...
   ```

---

### Step 4 — Install Python Dependencies

Open a terminal (CMD or PowerShell) and run:

```bash
pip install pyserial requests
```

---

### Step 5 — Configure & Run monitor.py

1. Open `monitor.py` in a text editor.
2. Set your ESP32 COM port at the top of the file:
   ```python
   SERIAL_PORT = "COM3"   # ← Change to your ESP32 port (e.g. COM4, COM5)
   BAUD_RATE   = 115200
   LHM_URL     = "http://localhost:8085/data.json"
   ```
3. Run the script:
   ```bash
   python monitor.py
   ```

You should see live output in the terminal and the LCD updating every few seconds:

```
[monitor.py] Connected to COM3
[monitor.py] CPU: 45°C | GPU: 62°C | RAM: 58%
```

---

## 📟 LCD Display Layout

The 2x16 LCD cycles through screens:

```
┌────────────────┐     ┌────────────────┐
│ CPU  45°C  23% │     │ GPU  62°C  48% │
│ RAM  8.1GB 58% │     │ VRAM 4.2GB 52% │
└────────────────┘     └────────────────┘
```

---

## 📁 Repository Structure

```
├── esp32_lcd_monitor.ino   # Arduino sketch for ESP32 + LCD
├── monitor.py              # Python bridge: LHM → Serial
└── README.md
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| `http://localhost:8085/data.json` doesn't respond | Run LibreHardwareMonitor as **Administrator** and check Web Server is enabled |
| LCD shows nothing | Check I2C address (`0x27` vs `0x3F`), run an I2C scanner sketch |
| `Serial port COM3 not found` | Check Device Manager for the correct port, update `SERIAL_PORT` in `monitor.py` |
| `Permission denied` on COM port | Close Arduino IDE Serial Monitor before running `monitor.py` |
| `ModuleNotFoundError` | Run `pip install pyserial requests` |
| ESP32 not detected | Install [CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) or [CH340](https://sparks.gogo.co.nz/ch340.html) USB drivers |

---

## 📜 License

MIT License — free to use, modify, and distribute.
