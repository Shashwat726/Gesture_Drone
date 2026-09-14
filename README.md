# Gesture-Controlled Drone

A drone that responds to hand gestures, built from scratch.

## What it does
- Detects hand gestures in real time using the phone camera
- Maps gestures to discrete drone commands (ascend, descend, hover, land, record)
- Commands sent from phone → ESP32 → Flight Controller
- Custom 3D-printed frame built on a self-built 3D printer

## Hardware
- **Vision brain:** Samsung Galaxy M32 (runs gesture detection)
- **Comms bridge:** ESP32 microcontroller
- **Frame:** Custom designed, 3D printed in PETG
- **Flight controller:** Betaflight F4/F7

## Tech Stack
- Python, OpenCV, MediaPipe (gesture detection)
- Arduino C++ (ESP32 firmware)
- Betaflight + MSP protocol (flight controller comms)

## Current Status
Phase A — Software & Vision (Day 30/160)
- [x] Phone camera feed streaming to Python over WiFi
- [x] Live annotations — FPS counter, crosshair, border
- [x] Snapshot and timestamped video recording
- [x] **MediaPipe hand tracking & Custom Gesture Engine (Completed!)**

## Build Log
Started: May 2025
Target: First flight in 160 days

## Progress

### Section 1 (Days 1-11) — Complete
- Phone camera streaming via DroidCam
- Frame annotation, snapshot/recording
- Clean function-based structure

### Section 2 (Days 12-19) — Complete
- HSV color masking, thresholding (simple/Otsu/adaptive)
- Morphological ops (erosion, dilation, opening, closing)
- Contour detection, bounding boxes, centroids
- ROI cropping, Canny edge detection, background subtraction
- Performance profiling — confirmed WiFi capture is the bottleneck, not CV processing
- Milestone: working end-to-end color-blob tracker (object_tracker.py)

### Section 3 (Days 20-30) — Complete
- Integrated MediaPipe Hand Tracking (Modern Tasks API)
- Extracted 21 3D hand landmarks for real-time finger state analysis
- **Jedi Interface Built:** HOVER (Open), FIST LOCK (Position Track), ARISE/LAND (Dynamic Velocity), PHOTO/VIDEO (Pinch), 360 ORBIT (Circle Path)
- Engineered a universal proportional "palm length" baseline to solve 3D perspective distortion (the grabbing angle)
- Built Exponential Moving Average (EMA) filters for buttery smooth altitude/velocity tracking
- Designed Temporal Smoothing (Mode filtering/Debouncing) to completely eliminate false positives and camera noise