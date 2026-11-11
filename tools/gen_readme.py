"""Generate README.md for BorePilot from tools/gen_pages.py data and hardware/bom CSV.
Run from the repo root:  python -X utf8 -I tools/gen_readme.py"""
import os, sys, io, contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import gen_pages as G

ROOT = G.ROOT


def bom_section(sid):
    groups, order = {}, []
    for sec, ref, name, c, q, note in G.P:
        if sec != sid:
            continue
        if c not in groups:
            groups[c] = {"refs": [], "q": 0, "names": []}
            order.append(c)
        g = groups[c]
        g["refs"].append(ref)
        g["q"] += q
        short = name.split(",")[0].replace("OPTIONAL ", "").replace(" (optional)", "").replace(" (DNP)", "")
        if short not in g["names"]:
            g["names"].append(short)
    rows = []
    for c in order:
        g = groups[c]
        mpn = G.info(c)[0]
        opt = " *(optional)*" if any("OPTIONAL" in p[2] or "optional" in p[2] or "DNP" in p[2] for p in G.P if p[3] == c and p[0] == sid and p[1] in g["refs"]) else ""
        fn = " / ".join(g["names"][:2]) if len(g["names"]) > 1 else g["names"][0]
        link = f"[{c}](https://www.lcsc.com/product-detail/{c}.html)" if c.startswith("C") and c != "TBD" else c
        rows.append(f"| {', '.join(g['refs'])} | {g['q']} | {fn}{opt} | `{mpn}` | {link} |")
    return "| Ref | Qty | Function | Part | LCSC |\n|---|---:|---|---|---|\n" + "\n".join(rows) + "\n"


def bom_all():
    out = []
    for sid, title, col, desc in G.S:
        out.append(f"**{title}**  \n<sub>{desc}</sub>\n\n{bom_section(sid)}")
    return "\n".join(out)


def cost():
    tot, n = 0.0, 0
    for r in G.rows:
        try:
            tot += float(r["Unit price USD"]) * int(r["Qty"])
            n += int(r["Qty"])
        except ValueError:
            pass
    return tot, n


tot, nparts = cost()

README = f'''<div align="center">

<img src="docs/images/borepilot-hero-animated.svg" alt="BorePilot, ESP32-S3 smart borewell pump controller" width="100%">

# BorePilot

**ESP32-S3 smart borewell pump controller: start, stop and protect a single-phase submersible pump from Home Assistant.**

![status](https://img.shields.io/badge/status-board%20routed%2C%20untested-orange) ![board](https://img.shields.io/badge/PCB-100%20x%2090%20mm%2C%202%20layers-blue) ![mcu](https://img.shields.io/badge/MCU-ESP32--S3--WROOM--1U-informational) ![license](https://img.shields.io/badge/license-MIT-green) ![eda](https://img.shields.io/badge/EDA-EasyEDA%20Pro-lightgrey)

</div>

> **Status (2026-11-11).** Schematic finished (ERC clean), PCB routed and DRC clean in EasyEDA, labels on every connector pin and button. **The board has not been built or tested, and the firmware is not written yet.** The board involves 230 V AC: read [docs/safety.md](docs/safety.md) first and have a qualified person review the mains section before you power it.

## Features

| | | |
|---|---|---|
| **Pump control** | 2 SPDT relays (Songle SRD-05VDC-SL-C), NO / COM / NC on 5.08 mm screw terminals | START / STOP for a contactor or a small pump |
| **Energy and protection** | PZEM-004T v3 header: voltage, current, power, energy, frequency | dry-run and over-current stop (in firmware) |
| **Home Assistant** | ESP32-S3-WROOM-1U-N16R8, Wi-Fi, external antenna through U.FL | ESPHome, same entities as Smart-Submersible-Pump-Controller-ESPHome |
| **Display options** | 16x2 I2C LCD, I2C OLED or 128x64 ST7920 on one board | START / STOP / MENU buttons, buzzer, status LEDs |
| **Level inputs** | 2 float-switch inputs, spare GPIO header | optional wireless tank node (ESP-NOW), see [TankPilot](https://github.com/ElectroIoT/ESP32-S3-TankPilot) |
| **Power** | Hi-Link HLK-5M05 (5 V / 1 A), 470 uF bulk, SGM2212 3.3 V LDO | USB-C for flashing and logs (native USB, no UART chip) |
| **Mains aware layout** | slots between relay contacts and coils, 6.4 mm clearance goal | no on-board fuse or varistor: protect upstream |

<img src="docs/images/borepilot-flow-animated.svg" alt="How BorePilot works" width="100%">

## The board

<div align="center">
<img src="docs/images/board-top.png" alt="BorePilot PCB, top view, routed in EasyEDA" width="640">

*Top view of PCB1 (screenshot of the routed design in EasyEDA). Red = top copper, blue = bottom copper. Every connector pin and button carries a silkscreen name.*
</div>

<div align="center">
<img src="docs/images/social/02_square_1080x1080.png" width="300"> <img src="docs/images/social/01_hero_og_1200x630.png" width="470">
</div>

| | |
|---|---|
| Size | 100 x 90 mm, 2 layers, 1.6 mm, four M3 mounting holes |
| Mains side | J2 (AC in), J3 (AC tap for the PZEM), HLK-5M05, relay contacts J4 / J5 |
| Isolation | two 8 x 1 mm slots per relay between COM and the coil pins, HLK-area slot |
| Tracks | mains and relay contacts 1.5 mm, +5 V 0.8 mm, +3V3 0.6 mm, coil 0.5 mm, signals 0.25 mm, GND pour on both layers |
| DRC | 0 errors (JLCPCB capability rules plus the BorePilot rule set) |
| Parts | {nparts} pieces from LCSC, about {tot:.2f} USD with the listing prices of 2026-10-28 |

## Connectors

| Ref | What | Pins (left to right as printed on the board) |
|---|---|---|
| J1 | USB-C | programming, logs, 5 V |
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

## Bill of materials

{nparts} pieces, about {tot:.2f} USD. Listing prices and LCSC numbers are from 2026-10-28; datasheets of several parts are not read yet (see [PLAN.md](PLAN.md)). Full CSV: [hardware/bom/pump-controller-bom-v0.csv](hardware/bom/pump-controller-bom-v0.csv). Parts marked *optional* are fitted only if you want that feature.

{bom_all()}
Not on the board: ANT1 (U.FL to SMA pigtail, KH-IPEX-SMA-W-200, C2683345) and ANT2 (2.4 GHz SMA antenna, not chosen yet); the PZEM-004T v3 module; fuse clips.

## Design documents

| What | Where |
|---|---|
| Project plan, power budget, safety notes, open questions | [PLAN.md](PLAN.md) |
| BOM by section and by schematic page (tick lists with LCSC links) | [docs/bom-by-section.html](docs/bom-by-section.html), [docs/bom-by-page.html](docs/bom-by-page.html) |
| Schematic build guide for EasyEDA Pro (page by page, net names) | [docs/schematic-guide.html](docs/schematic-guide.html) |
| Wiring by section, connection diagram | [docs/wiring-by-section.html](docs/wiring-by-section.html), [docs/connection-diagram.html](docs/connection-diagram.html) |
| Footprint check against datasheets (K1, U2, J1, KF128, BZ1) | [docs/footprints.html](docs/footprints.html) |
| Footprint fixes, relay slots and placement table (tick list) | [docs/footprint-placement.html](docs/footprint-placement.html) |
| PCB floor plan by block (planning floor plan: the final board in EasyEDA differs in detail) | [docs/pcb-section-guide.html](docs/pcb-section-guide.html) |
| Schematic review (8 errors found and fixed) | [docs/schematic-review-2026-10-28.md](docs/schematic-review-2026-10-28.md) |
| Safety | [docs/safety.md](docs/safety.md) |

## Open items

- Firmware: not written. Plan: reuse the ESPHome package, add a latched pump state, start-up grace time, hysteresis and minimum off-time (PLAN.md section 2).
- Gerber and assembly files are not in the repository yet: export them from the EasyEDA project once you are happy with the board.
- Datasheets not read for SGM2212, PCA9306, SS34B, MLT-8530, KF128 ratings, ST7920 and PZEM-004T v3; the footprints of U1, U3 to U6 and J9 are not compared with drawings.
- Mains section needs a qualified engineer review: no fuse or varistor on board, no protective earth through the PCB, HLK-5M05 EMC parts (X2 capacitor, choke) not fitted.
- Relay coil tracks run within about 4 to 6 mm of the COM track; the slots lengthen the surface path, the measured distances are in [docs/footprint-placement.html](docs/footprint-placement.html).
- Nothing has been tested on hardware.

## Safety

This board switches mains. Build and test it only if you know how to work safely with 230 V AC. Use low-voltage loads on the bench until the mains section has been reviewed, and keep the board in an enclosure with the terminals covered. See [docs/safety.md](docs/safety.md).

## Repository map

```
.
|-- PLAN.md              full project plan
|-- hardware/            bom/ (LCSC CSV), datasheets/
|-- docs/                guides, wiring, BOM pages, footprint and placement sheets, images/
|-- firmware/esphome/    ESPHome package (not written yet)
|-- test/                hardware test plan (later)
`-- tools/               generators for the docs pages, README and images
```

## License

[MIT](LICENSE).
'''

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n").write(README)
print("README.md", len(README))
