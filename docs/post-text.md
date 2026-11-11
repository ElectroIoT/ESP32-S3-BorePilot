# Text for the OSHWLab and PCBWay project pages

Copy-ready text for posting BorePilot. Files and images are in this repository.

## Name
BorePilot - ESP32-S3 Smart Borewell Pump Controller

## One-line summary (OSHWLab, 150 characters at most)
ESP32-S3 pump controller: 2 relays, PZEM-004T energy metering, 3 display options, Home Assistant over Wi-Fi (ESPHome), 230 V aware layout.

## Short description
BorePilot is an open-source controller board for a single-phase submersible (borewell) pump. An ESP32-S3 switches two relays, reads voltage, current, power and energy from a PZEM-004T module, watches two float switches and reports everything to Home Assistant over Wi-Fi. One board supports three displays (16x2 I2C LCD, I2C OLED or 128x64 ST7920) and has START / STOP / MENU buttons, a status LED and an optional buzzer. A Hi-Link HLK-5M05 makes the 5 V from the mains and USB-C is used for flashing and logs.

## Details
**What it does**
- Start and stop a pump or a contactor with two SPDT relays (NO / COM / NC screw terminals).
- Measures voltage, current, power, energy and frequency through a PZEM-004T v3 (header on the board).
- Dry-run and over-current protection (firmware, to be written).
- Home Assistant through ESPHome over Wi-Fi, external antenna on the ESP32-S3-WROOM-1U.
- Three display options on one board, START / STOP / MENU buttons, two float-switch inputs, spare GPIO header.
- Optional wireless tank-level node (ESP-NOW), see TankPilot.

**Board**
- 100 x 90 mm, 2 layers, 1.6 mm, four M3 mounting holes, 81 parts.
- Mains and relay contact tracks 1.5 mm, +5 V 0.8 mm, +3V3 0.6 mm, signals 0.25 mm, GND pour.
- Two 8 x 1 mm slots around the coil pins of each relay, mains clearance goal 6.4 mm.
- Every connector pin and button is labelled on the silkscreen.
- DRC: 0 errors.

**Status**
Schematic ERC clean, PCB routed and DRC clean, files exported. Not built and not tested yet, firmware not written yet. The board switches 230 V AC: build only if you know how to work with mains, use low-voltage loads on the bench first and have the mains section reviewed.

**Files**
GitHub: https://github.com/ElectroIoT/ESP32-S3-BorePilot (private until published)
- hardware/gerber/BorePilot_Gerber_2026-11-11.zip
- hardware/assembly/BorePilot_BOM.csv and BorePilot_PickAndPlace.csv
- hardware/schematic/BorePilot_Schematic.pdf

**Cost**
Parts about 16 USD (listing prices 2026-10-28) without the PCB and the PZEM module.

## Tags
ESP32, ESP32-S3, Home Assistant, ESPHome, pump controller, borewell, energy monitor, PZEM-004T, relay, IoT

## License
MIT

## Images to upload
- Cover / product image: docs/images/social/01_hero_og_1200x630.png (or 02_square_1080x1080.png)
- PCB 3D image: docs/images/renders/blue_iso.png
- Details images: renders/blue_top.png, renders/blue_bottom.png, social/03_features_1080x1640.png, schematic pages in docs/schematic/

## PCBWay project form
- Title: BorePilot - ESP32-S3 Smart Borewell Pump Controller
- Category: IoT / Home automation
- Tags: ESP32-S3, Home Assistant, ESPHome, pump controller, PZEM-004T, relay
- Upload: Gerber zip, BOM CSV, pick-and-place CSV, schematic PDF
- Board: 2 layers, 100 x 90 mm, 1.6 mm. Mention the milled relay slots.
