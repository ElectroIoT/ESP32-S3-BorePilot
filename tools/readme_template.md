<div align="center">

<img src="docs/images/borepilot-hero-animated.svg" alt="BorePilot, ESP32-S3 smart borewell pump controller" width="100%">

# BorePilot

**ESP32-S3 smart borewell pump controller: start, stop and protect a single-phase submersible pump from Home Assistant, with live voltage, current and energy.**

![status](https://img.shields.io/badge/status-routed%2C%20DRC%20clean%2C%20untested-orange) ![board](https://img.shields.io/badge/PCB-100%20x%2090%20mm%2C%202%20layers-blue) ![mcu](https://img.shields.io/badge/MCU-ESP32--S3--WROOM--1U-informational) ![parts](https://img.shields.io/badge/parts-81%20on%20board-lightgrey) ![license](https://img.shields.io/badge/license-MIT-green) ![eda](https://img.shields.io/badge/EDA-EasyEDA%20Pro-lightgrey)

</div>

> **Status (2026-11-11).** Schematic finished (ERC clean), PCB routed with **0 DRC errors**, every connector pin and button labelled on the silkscreen, Gerber and assembly files exported. **The board has not been built or tested and the firmware is not written yet.** The board involves 230 V AC: read [docs/safety.md](docs/safety.md) first, use low-voltage loads on the bench and have a qualified person review the mains section before you power it.

## Contents
[Features](#features) | [Board tour](#board-tour-animated) | [3D views](#3d-views) | [How it works](#how-it-works) | [Connectors](#connectors-and-labels) | [GPIO map](#gpio-map) | [Schematic](#schematic) | [Bill of materials](#bill-of-materials) | [Manufacturing files](#manufacturing-files) | [Ordering](#ordering-the-board) | [Documents](#design-documents) | [Open items](#open-items) | [Safety](#safety) | [Repository map](#repository-map)

## Features

| | | |
|---|---|---|
| **Pump control** | 2 SPDT relays (Songle SRD-05VDC-SL-C), NO / COM / NC on 5.08 mm screw terminals | START / STOP for a contactor or a small pump |
| **Energy and protection** | PZEM-004T v3 header: voltage, current, power, energy, frequency | dry-run and over-current stop (in firmware) |
| **Home Assistant** | ESP32-S3-WROOM-1U-N16R8, Wi-Fi, external antenna through U.FL | ESPHome, same entities as the Smart-Submersible-Pump-Controller-ESPHome package |
| **Display options** | 16x2 I2C LCD, I2C OLED or 128x64 ST7920 on one board | START / STOP / MENU buttons, buzzer, status LEDs |
| **Level inputs** | 2 float-switch inputs, spare GPIO header | optional wireless tank node (ESP-NOW), see [TankPilot](https://github.com/ElectroIoT/ESP32-S3-TankPilot) |
| **Power** | Hi-Link HLK-5M05 (5 V / 1 A), 470 uF bulk, SGM2212 3.3 V LDO | USB-C for flashing and logs (native USB, no UART chip) |
| **Mains aware layout** | two 8 x 1 mm slots per relay between COM and the coil, 6.4 mm clearance goal | no on-board fuse or varistor: protect upstream |
| **Labelled** | every connector pin and button has a silkscreen name (top and bottom) | START, STOP, MENU, RESET, BOOT, NO, COM, NC, L, N ... |

## Board tour (animated)

<img src="docs/images/borepilot-anatomy-animated.svg" alt="BorePilot board tour" width="100%">

## 3D views

<div align="center">
<img src="docs/images/renders/blue_iso.png" alt="BorePilot 3D, angled view" width="46%"> <img src="docs/images/renders/blue_top.png" alt="BorePilot 3D, top view" width="46%">
<img src="docs/images/renders/blue_bottom.png" alt="BorePilot 3D, bottom view" width="46%"> <img src="docs/images/board-top.png" alt="BorePilot PCB routed, top copper (EasyEDA)" width="46%">

*3D renders from EasyEDA (blue solder mask). Bottom right: the routed top copper (red = top, blue = bottom). The USB-C socket and its ESD part sit on the bottom side.*
</div>

| | |
|---|---|
| Size | 100 x 90 mm, 2 layers, 1.6 mm, four M3 mounting holes (4, 4), (96, 4), (4, 86), (96, 86) |
| Mains side | J2 (AC in), J3 (AC tap for the PZEM), HLK-5M05, relay contacts J4 / J5 |
| Isolation | two 8 x 1 mm slots per relay between COM and the coil pins, slot in the HLK-5M05 area |
| Tracks | mains and relay contacts 1.5 mm, +5 V 0.8 mm, +3V3 0.6 mm, coil 0.5 mm, USB and signals 0.25 mm, GND pour on both layers |
| DRC | 0 errors (JLCPCB capability rules plus a BorePilot rule set with mains spacing) |
| Parts | 81 on the board, {nparts} pieces in the BOM, about {tot:.2f} USD with the listing prices of 2026-10-28 |

## How it works

<img src="docs/images/borepilot-flow-animated.svg" alt="How BorePilot works" width="100%">

The ESP32-S3 talks to Home Assistant over Wi-Fi (ESPHome). It switches the two relays through low-side MOSFETs, reads the PZEM-004T over UART and the two float inputs, and shows the state on one of three display options. The relay coils run from the 5 V rail; the HLK-5M05 makes 5 V from the mains, and USB-C can power the board for flashing.

## Connectors and labels

Pin names below are printed next to the pins on the board.

| Ref | What | Pins (left to right as printed) |
|---|---|---|
| J1 | USB-C (bottom side) | programming, logs, 5 V |
| J2 | AC in (2P) | L, N |
| J3 | AC tap for the PZEM voltage input (2P) | L, N |
| J4 | Relay 1 contacts (3P) | NO, COM, NC |
| J5 | Relay 2 contacts (3P) | NO, COM, NC |
| J6 | PZEM-004T link (XH 4P) | 5V, RX, TX, GND (module side names) |
| J7 | 16x2 I2C LCD (1x4) | GND, 5V, SDA, SCL |
| J8 | I2C OLED (1x4) | GND, 3V3, SCL, SDA |
| J9 | 128x64 ST7920 (1x20) | GND, VCC, V0, RS, RW, E, D0 to D7, PSB, NC, RST, VOUT, BLA, BLK |
| J10, J11 | float switch 1 and 2 (2P) | IN, GND |
| J12 | spare I/O (1x6) | 3V3, GND, SP1 to SP4 |
| J13 | UART / boot header (1x6, not fitted) | IO0, EN, RX0, TX0, GND, 3V3 |
| SW1 to SW5 | buttons | RESET, BOOT, START, STOP, MENU |

## GPIO map

| GPIO | Net | Use |
|---|---|---|
| EN, 0 | EN, BOOT | SW1 reset, SW2 boot (strapping pin) |
| 19 / 20 | USB D- / D+ | native USB through U4 ESD part |
| 8 / 9 | SDA / SCL | I2C: OLED direct, 16x2 LCD through U5 PCA9306 level shifter |
| 17 / 18 | PZEM_TX / PZEM_RX | UART1 9600 baud to J6, RX through a divider |
| 4, 5 | RLY1, RLY2 | relay drivers (AO3400A, active high) |
| 10 to 14 | LCD_CS, MOSI, CLK, BL, RST | ST7920 through U6 74AHCT125 |
| 1, 2, 6 | START, STOP, MENU | buttons to GND, internal pull-ups |
| 15, 16 | BUZZER, LED_STATUS | optional buzzer, red status LED |
| 39, 40 | IN1, IN2 | float-switch inputs |
| 41, 42 | SPARE1, SPARE2 | J12 |
| 43, 44 | TXD0, RXD0 | J13 |

Details: [PLAN.md](PLAN.md) section 4 and [docs/connection-diagram.html](docs/connection-diagram.html).

## Schematic

Five pages, drawn in EasyEDA Pro, ERC clean. Full PDF: [hardware/schematic/BorePilot_Schematic.pdf](hardware/schematic/BorePilot_Schematic.pdf).

| Page | What |
|---|---|
| 1. Power and USB | mains input J2 / J3, HLK-5M05, Schottky OR-ing, 470 uF, SGM2212 3.3 V LDO, USB-C with ESD part |
| 2. ESP32-S3 core | WROOM-1U module, EN and BOOT buttons, decoupling |
| 3. Relays and mains contacts | two SRD relays, AO3400A drivers, flyback diodes, coil LEDs, J4 / J5 |
| 4. PZEM link and I/O | PZEM header with divider, START / STOP / MENU, LEDs, buzzer, float inputs, spare header |
| 5. Display options | 16x2 LCD through PCA9306, OLED, ST7920 through 74AHCT125, contrast and backlight |

<details><summary>Show the five schematic pages</summary>

<img src="docs/schematic/01_power_usb.png" alt="Schematic page 1: power and USB" width="100%">
<img src="docs/schematic/02_esp32_core.png" alt="Schematic page 2: ESP32-S3 core" width="100%">
<img src="docs/schematic/03_relays_mains.png" alt="Schematic page 3: relays and mains contacts" width="100%">
<img src="docs/schematic/04_pzem_io.png" alt="Schematic page 4: PZEM link and I/O" width="100%">
<img src="docs/schematic/05_display_options.png" alt="Schematic page 5: display options" width="100%">

</details>

Page-by-page build guide, wiring diagrams and the schematic review are listed under [Design documents](#design-documents).

## Bill of materials

{nparts} pieces in the repository BOM, about {tot:.2f} USD (listing prices and LCSC numbers of 2026-10-28; several datasheets are not read yet, see [PLAN.md](PLAN.md)). Files: [hardware/bom/pump-controller-bom-v0.csv](hardware/bom/pump-controller-bom-v0.csv) (with stock and prices) and [hardware/assembly/BorePilot_BOM.csv](hardware/assembly/BorePilot_BOM.csv) (EasyEDA export, 81 pieces, for assembly). Parts marked *optional* are fitted only if you want that feature.

{bom_all()}
Not on the board: ANT1 (U.FL to SMA pigtail, KH-IPEX-SMA-W-200, C2683345) and ANT2 (2.4 GHz SMA antenna, not chosen yet); the PZEM-004T v3 module; fuse clips.

## Manufacturing files

| File | What |
|---|---|
| [hardware/gerber/BorePilot_Gerber_2026-11-11.zip](hardware/gerber/BorePilot_Gerber_2026-11-11.zip) | Gerber and drill files, upload to the PCB maker |
| [hardware/assembly/BorePilot_PickAndPlace.csv](hardware/assembly/BorePilot_PickAndPlace.csv) | pick and place (centroid) file, also as [.xlsx](hardware/assembly/BorePilot_PickAndPlace.xlsx) |
| [hardware/assembly/BorePilot_BOM.csv](hardware/assembly/BorePilot_BOM.csv) | assembly BOM with LCSC part numbers, also as [.xlsx](hardware/assembly/BorePilot_BOM.xlsx) |
| [hardware/schematic/BorePilot_Schematic.pdf](hardware/schematic/BorePilot_Schematic.pdf) | schematic, 5 pages |
| [hardware/pcb/BorePilot_PCB_Layers.pdf](hardware/pcb/BorePilot_PCB_Layers.pdf) | PCB layer drawings |
| [hardware/netlist/BorePilot_Netlist.enet](hardware/netlist/BorePilot_Netlist.enet) | netlist (EasyEDA format) |

The design is made in EasyEDA Pro (project "BorePilot-Smart water pump"). The Gerber, pick-and-place and BOM files were exported from the final routed board on 2026-11-11.

## Ordering the board

1. Upload the Gerber zip to your PCB maker (JLCPCB or PCBWay): 2 layers, 100 x 90 mm, 1.6 mm, 1 oz copper. The board has milled slots (relay slots): tell the maker to keep them.
2. For assembly, upload the BOM and pick-and-place files. Through-hole parts (screw terminals, headers, HLK module, relays, electrolytic capacitor) are hand-soldered. The 230 V part of the board is for qualified builders.
3. Order a small batch first: the board is untested.

## Design documents

| What | Where |
|---|---|
| Project plan, power budget, safety notes, open questions | [PLAN.md](PLAN.md) |
| BOM by section and by schematic page (tick lists with LCSC links) | [docs/bom-by-section.html](docs/bom-by-section.html), [docs/bom-by-page.html](docs/bom-by-page.html) |
| Schematic build guide for EasyEDA Pro (page by page, net names) | [docs/schematic-guide.html](docs/schematic-guide.html) |
| Wiring by section, connection diagram | [docs/wiring-by-section.html](docs/wiring-by-section.html), [docs/connection-diagram.html](docs/connection-diagram.html) |
| Footprint check against datasheets (K1, U2, J1, KF128, BZ1) | [docs/footprints.html](docs/footprints.html) |
| Footprint fixes, relay slots and placement table (tick list) | [docs/footprint-placement.html](docs/footprint-placement.html) |
| PCB floor plan by block (planning floor plan: the final board differs in detail) | [docs/pcb-section-guide.html](docs/pcb-section-guide.html) |
| Schematic review (8 errors found and fixed) | [docs/schematic-review-2026-10-28.md](docs/schematic-review-2026-10-28.md) |
| Safety | [docs/safety.md](docs/safety.md) |

## Open items

- **Firmware:** not written. Plan: reuse the ESPHome package, add a latched pump state, start-up grace time, hysteresis and minimum off-time (PLAN.md section 2).
- **Mains section:** needs a qualified engineer review: no fuse or varistor on board, no protective earth through the PCB, HLK-5M05 EMC parts (X2 capacitor, choke) not fitted.
- **Relay area:** relay coil tracks run within about 4 to 6 mm of the COM track; the slots lengthen the surface path, measured distances are in [docs/footprint-placement.html](docs/footprint-placement.html).
- **Datasheets not read** for SGM2212, PCA9306, SS34B, MLT-8530, KF128 ratings, ST7920 and PZEM-004T v3; footprints of U1, U3 to U6 and J9 are not compared with drawings.
- **Nothing has been tested on hardware.**

## Safety

This board switches mains. Build and test it only if you know how to work safely with 230 V AC. Use low-voltage loads on the bench until the mains section has been reviewed, and keep the board in an enclosure with the terminals covered. See [docs/safety.md](docs/safety.md).

## Repository map

```
.
|-- PLAN.md              full project plan
|-- hardware/
|   |-- gerber/          Gerber + drill zip
|   |-- assembly/        BOM and pick-and-place (csv, xlsx)
|   |-- schematic/       schematic PDF
|   |-- pcb/             PCB layer PDF
|   |-- netlist/         EasyEDA netlist
|   `-- bom/             LCSC BOM with stock and prices
|-- docs/                guides, wiring, BOM pages, footprint and placement sheets
|   |-- images/          renders, board view, animated SVGs, social cards
|   `-- schematic/       schematic pages as PNG
|-- firmware/esphome/    ESPHome package (not written yet)
|-- test/                hardware test plan (later)
`-- tools/               generators for the docs pages, README and images
```

## License

[MIT](LICENSE).
