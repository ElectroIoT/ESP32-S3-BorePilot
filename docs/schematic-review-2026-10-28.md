# Schematic review, 2026-10-28 (EasyEDA project "BorePilot-Smart water pump", 5 pages)

Source: exported PDF (4) plus a live check of the open project (netlist read through the EasyEDA API). Footprints were not compared with datasheets.

## Errors found and fixed in the project
| # | Page | Problem | Fix applied |
|---|---|---|---|
| 1 | 1 Power and USB | LDO output flags were named `+3v3` (lower-case v) but the rest of the design uses `+3V3`: the ESP32 would have had no 3.3 V | renamed the 3 flags to `+3V3` |
| 2 | 2 ESP32 core | R3 (EN pull-up) went to GND: the ESP32 would have been held in reset | R3 now goes to `+3V3` |
| 3 | 4 PZEM and I/O | the switch signal sides had auto names NET82, NET83, NET84: START, STOP and MENU were not connected to the ESP32 | renamed to `BTN_START`, `BTN_STOP`, `BTN_MENU` |
| 4 | 4 PZEM and I/O | buzzer flyback diode D3 was reversed (anode on +5V) | D3 rotated: cathode on +5V, anode on the MOSFET drain |
| 5 | 5 Display options | J7 pins 3 and 4 were SCL / SDA (swapped against the usual backpack order GND, VCC, SDA, SCL) | rewired: pin 3 = SDA_5V, pin 4 = SCL_5V |
| 6 | 5 Display options | Q3 gate had no `LCD_BL` flag: backlight never driven | added `LCD_BL` flag on the gate |
| 7 | 5 Display options | PSB (J9 pin 15) was a floating net: 12864 not in serial mode | PSB flag replaced by `GND` (serial mode permanently) |
| 8 | 5 Display options | R14 / R15 (SDA_5V / SCL_5V pull-ups) were not connected to the I2C lines | added `SDA_5V` / `SCL_5V` flags on U5 pins 5 and 6 |

## Checked and correct
Page 1 mains / HLK / diodes / USB-C / ESD, page 2 all U1 pins vs the GPIO table, page 3 relays (flags RLYn, RLYn_D fixed earlier), page 4 PZEM divider, LEDs, floats, J12, page 5 U5, U6, J9, RV2, option B OLED.
After the fixes the project netlist shows 79 parts all connected, `+3V3` joining U3, U1, R3 and the other 3.3 V pins, and `+5V` joining 31 pins including D3 cathode.

## Still open
- BZ1 (MLT-8530, datasheet read 2026-10-29): 4 corner pads = `+` lead, `-` lead and **two dummy pads** (mechanical only, no electrical function). Symbol pins 3 and 4 are the dummy pads: put No-Connect flags on them, solder them for strength. Pins 1 (+) and 2 (-) are wired correctly.
- BZ1 voltage: datasheet rated 3.6 V, operating 2.5 to 4.5 V (square wave, resonance 2700 Hz), coil 16 ohm, max 95 mA measured at 5 V. The board drives it from +5V, slightly above the 4.5 V operating limit: add about 10 ohm in series (or limit the PWM duty in firmware, or use +3V3).
- J1 SBU pins are floating (DRC warning only, intended).
- TXD0 / RXD0 flags are single-pin nets (no test pad or header). Add a 2-pin header or test pads if you want serial console on those pins.
- J6 pin order must match the printed order on your PZEM module; J8 pin order must match your OLED module.
- No footprint was compared with its datasheet: relay pad numbers, USB-C, HLK pin pitch, KF128 terminals, 1x20 header.
- R6 / R7 (float pull-ups) are on the schematic but meant to be DNP.

## Buzzer fix (2026-10-29)
Add R22 = 10 ohm 1206 (C17903) between +5V and BZ1 pin 1. D3 stays across the branch (cathode +5V, anode on the Q4 drain). BZ1 pins 3 and 4 get No-Connect flags (done by the owner). Circuit view: docs/wiring/ui.html.

## PCB outline (2026-10-29)
PCB1 in EasyEDA now has the 100 x 90 mm board outline (3 mm corners, origin at the lower-left corner, y up), the isolation slot (x 28.1 to 29.4 mm, y 7 to 77 mm) on the Board Outline layer, and four M3 mounting holes (3.2 mm, non-plated, no copper pad) at (4,4), (96,4), (4,86), (96,86) mm. Schematic not yet imported into the PCB.
