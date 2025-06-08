# Hand Gesture Controlled Dual Servo System

*Control two servos with hand gestures using Python and Arduino*

## 📌 Overview
This project uses computer vision (MediaPipe) to track hand movements and control two servo motors via an Arduino. The distance between your thumb and index finger determines the servo angle.

**Features:**
- Right hand controls Servo 1
- Left hand controls Servo 2
- Real-time hand tracking with OpenCV
- Arduino communication via Firmata protocol

## 🔧 Hardware Requirements
| Component       | Quantity |
|-----------------|----------|
| Arduino (Uno/Nano) | 1       |
| Servo Motors (SG90) | 2       |
| USB Webcam       | 1        |
| Jumper Wires     | Several  |
| 5V Power Supply  | 1 (recommended) |

## ⚡ Circuit Connections
### Servo Wiring
| Servo Pin | Arduino Pin |
|-----------|------------|
| Servo 1 Signal (Yellow) | D9  |
| Servo 2 Signal (Yellow) | D10 |
| Servo VCC (Red)         | 5V  |
| Servo GND (Brown)       | GND |

> **Important:** For stable operation, power the servos using an external 5V power supply, not Arduino's USB power.

## 💻 Software Setup

### 🔌 Arduino Firmata Setup
1. **Install Arduino IDE**  
   Download from [arduino.cc](https://www.arduino.cc/en/software)

2. **Upload StandardFirmata**  
   - Connect Arduino via USB
   - Open Arduino IDE
   - Go to: `File → Examples → Firmata → StandardFirmata`
   - Select correct board: `Tools → Board → Arduino Uno`
   - Select correct port: `Tools → Port`
   - Click **Upload**

3. **Verify Upload**  
   The RX/TX lights on Arduino should blink briefly after upload.

### 🐍 Python Environment Setup
1. **Install Python** (3.7 or newer)  
   Download from [python.org](https://www.python.org/downloads/)

2. **Install Required Packages**:
```bash
pip install opencv-python mediapipe pyfirmata numpy
```

3. **Run the Application**:
```bash
python hand_servo_control.py
```

## 🚀 How It Works
1. **Hand Detection**: MediaPipe identifies hand landmarks in webcam feed
2. **Distance Calculation**: Measures distance between thumb (Landmark 4) and index finger (Landmark 8)
3. **Angle Mapping**: Converts distance to servo angle (0°-180°)
4. **Arduino Communication**: PyFirmata sends angle data via serial
5. **Servo Movement**: Arduino moves servos to specified positions


## 🔧 Troubleshooting
| Issue | Solution |
|-------|----------|
| Servo jitters | Use external power supply |
| "Port not found" error | Check COM port in code matches Arduino IDE |
| Firmata upload fails | Restart Arduino IDE, re-upload |
| Hand detection unstable | Improve lighting conditions |
| Python package errors | Create fresh virtual environment |
