<div align="center">

# ESP32-S3 Pump Controller (planning draft)

**Single-phase submersible pump controller board: ESP32-S3, 2 relays with NO + NC terminals, PZEM-004T energy sensing, HLK 5 V supply, USB-C, and a choice of 16x2 LCD / OLED / 128x64 LCD.**

</div>

> **Status (2026-10-28): plan only.** There is no schematic, PCB or firmware yet. Part numbers were looked up on LCSC today; datasheets for most parts are not read yet. The board involves 230 V AC: read [docs/safety.md](docs/safety.md) and the safety section of [PLAN.md](PLAN.md) first.

## Planned features
- ESP32-S3-WROOM-1-N8, Wi-Fi, ESPHome firmware with Home Assistant (same entities as [Smart-Submersible-Pump-Controller-ESPHome](https://github.com/ElectroIoT/Smart-Submersible-Pump-Controller-ESPHome)).
- PZEM-004T v3 header: voltage, current, power, energy, frequency; dry-run and over-current protection.
- 2 SPDT relays (Songle SRD-05VDC-SL-C), COM / NO / NC on 5.08 mm screw terminals for each.
- Hi-Link HLK-5M05 5 V / 1 A module, 3.3 V LDO, fuse and varistor on the mains input.
- USB-C (LCSC C165948) for flashing and logging via native USB; no USB-UART chip.
- Display options on one board: 16x2 I2C LCD, I2C OLED or 128x64 ST7920 LCD; START / STOP / MENU buttons, buzzer, status LEDs, 2 float-switch inputs.
- Target PCB: 100 x 80 mm, 2 layers, mains/low-voltage isolation slot.

## Repository map
```
.
|-- PLAN.md              full project plan (start here)
|-- hardware/            bom/ (LCSC CSV), board-v1/ (later), datasheets/
|-- firmware/esphome/    ESPHome package (later)
|-- docs/                safety.md, more to come
`-- test/                hardware test plan (later)
```

## Documents
| What | Where |
|---|---|
| Plan: GPIO table, display design, isolation notes, power budget, BOM, phases, open questions | [PLAN.md](PLAN.md) |
| LCSC bill of materials (draft) | [hardware/bom/pump-controller-bom-v0.csv](hardware/bom/pump-controller-bom-v0.csv) |
| Safety | [docs/safety.md](docs/safety.md) |

## License
[MIT](LICENSE).
