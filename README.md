# \# Gesture-Controlled Drone

# 

# A drone that responds to hand gestures, built from scratch.

# 

# \## What it does

# \- Detects hand gestures in real time using the phone camera

# \- Maps gestures to discrete drone commands (ascend, descend, hover, land, record)

# \- Commands sent from phone → ESP32 → Flight Controller

# \- Custom 3D-printed frame built on a self-built 3D printer

# 

# \## Hardware

# \- \*\*Vision brain:\*\* Samsung Galaxy M32 (runs gesture detection)

# \- \*\*Comms bridge:\*\* ESP32 microcontroller

# \- \*\*Frame:\*\* Custom designed, 3D printed in PETG

# \- \*\*Flight controller:\*\* Betaflight F4/F7

# 

# \## Tech Stack

# \- Python, OpenCV, MediaPipe (gesture detection)

# \- Arduino C++ (ESP32 firmware)

# \- Betaflight + MSP protocol (flight controller comms)

# 

# \## Current Status

# Phase A — Software \& Vision (Day 9/160)

# \- \[x] Phone camera feed streaming to Python over WiFi

# \- \[x] Live annotations — FPS counter, crosshair, border

# \- \[x] Snapshot and timestamped video recording

# \- \[ ] MediaPipe hand tracking (next)

# 

# \## Build Log

# Started: May 2025

# Target: First flight in 160 days

