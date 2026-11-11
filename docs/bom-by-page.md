# BorePilot - BOM by schematic page

Planned refs and nets (no schematic yet). Page 6 = cover and notes, no parts.

## SCHEMATIC PAGE 1 - Power and USB
Mains in, HLK-5M05, 5 V OR-ing, 3.3 V LDO, USB-C and ESD. Mains parts J2, J3, U2 stay in the upper-left of the page, away from low-voltage sheets.

| Done | Ref | Part | LCSC | Qty |
|---|---|---|---|---|
| [ ] | J2 | AC in screw terminal 2P 5.08 mm | C474952 | 1 |
| [ ] | J3 | AC tap to PZEM voltage input, 2P | C474952 | 1 |
| [ ] | U2 | HLK-5M05 AC-DC 5 V 1 A module | C209907 | 1 |
| [ ] | D4 | Schottky OR-ing: HLK to +5V | C2758511 | 1 |
| [ ] | D5 | Schottky OR-ing: USB VBUS to +5V | C2758511 | 1 |
| [ ] | C1 | 470 uF 16 V bulk on +5V | C47344174 | 1 |
| [ ] | U3 | SGM2212-3.3 LDO, SOT-223 | C3294699 | 1 |
| [ ] | C2 | 10 uF 1206, LDO input | C9807 | 1 |
| [ ] | C3 | 10 uF 1206, LDO output | C9807 | 1 |
| [ ] | C5 | 10 uF 1206, +5V near relays | C9807 | 1 |
| [ ] | C6 | 10 uF 1206, +5V after OR-ing | C9807 | 1 |
| [ ] | C15 | 100 nF 1206, HLK output | C24497 | 1 |
| [ ] | J1 | USB-C 16-pin receptacle (user part C165948) | C165948 | 1 |
| [ ] | U4 | USBLC6-2SC6 ESD protection | C7519 | 1 |
| [ ] | R1 | 5.1 k, CC1 pull-down | C26033 | 1 |
| [ ] | R2 | 5.1 k, CC2 pull-down | C26033 | 1 |
| [ ] | C7 | 10 uF 1206, VBUS | C9807 | 1 |
| [ ] | C11 | 100 nF 1206, VBUS | C24497 | 1 |

Parts on this page: 18

## SCHEMATIC PAGE 2 - ESP32-S3 core
Module, antenna pigtail, EN/BOOT buttons, decoupling.

| Done | Ref | Part | LCSC | Qty |
|---|---|---|---|---|
| [ ] | U1 | ESP32-S3-WROOM-1U-N16R8 module | C3013946 | 1 |
| [ ] | ANT1 | U.FL to SMA pigtail 200 mm | C2683345 | 1 |
| [ ] | ANT2 | 2.4 GHz SMA antenna (NOT CHOSEN YET) | TBD | 1 |
| [ ] | J13 | UART / BOOT header 1x6 (not fitted by default) | C492405 | 1 |
| [ ] | SW1 | Reset button (EN) | C318884 | 1 |
| [ ] | SW2 | BOOT button (GPIO0) | C318884 | 1 |
| [ ] | R3 | 10 k, EN pull-up | C17902 | 1 |
| [ ] | C4 | 10 uF 1206, 3V3 at module | C9807 | 1 |
| [ ] | C8 | 100 nF 1206, EN to GND | C24497 | 1 |
| [ ] | C9 | 100 nF 1206, module 3V3 | C24497 | 1 |
| [ ] | C10 | 100 nF 1206, module 3V3 | C24497 | 1 |

Parts on this page: 11

## SCHEMATIC PAGE 3 - Relays and mains contacts
K1, K2 with drivers, flyback diodes, LEDs and COM/NO/NC terminals.

| Done | Ref | Part | LCSC | Qty |
|---|---|---|---|---|
| [ ] | K1 | Relay 1, SRD-05VDC-SL-C | C35449 | 1 |
| [ ] | K2 | Relay 2, SRD-05VDC-SL-C | C35449 | 1 |
| [ ] | Q1 | AO3400A driver, relay 1 | C20917 | 1 |
| [ ] | Q2 | AO3400A driver, relay 2 | C20917 | 1 |
| [ ] | D1 | Schottky flyback, K1 coil | C2758511 | 1 |
| [ ] | D2 | Schottky flyback, K2 coil | C2758511 | 1 |
| [ ] | R18 | 100 k gate pull-down Q1 | C17900 | 1 |
| [ ] | R19 | 100 k gate pull-down Q2 | C17900 | 1 |
| [ ] | R10 | 1 k, LED3 series | C4410 | 1 |
| [ ] | R11 | 1 k, LED4 series | C4410 | 1 |
| [ ] | LED3 | Green LED: relay 1 energised | C2986059 | 1 |
| [ ] | LED4 | Green LED: relay 2 energised | C2986059 | 1 |
| [ ] | J4 | Relay 1 terminal 2P: NO / NC | C474952 | 1 |
| [ ] | J14 | Relay 1 terminal 2P: COM (both pins on COM) | C474952 | 1 |
| [ ] | J5 | Relay 2 terminal 2P: NO / NC | C474952 | 1 |
| [ ] | J15 | Relay 2 terminal 2P: COM (both pins on COM) | C474952 | 1 |
| [ ] | C17 | 100 nF 1206, +5V relay 1 | C24497 | 1 |
| [ ] | C18 | 100 nF 1206, +5V relay 2 | C24497 | 1 |

Parts on this page: 18

## SCHEMATIC PAGE 4 - PZEM link and I/O
PZEM header with divider, buttons, LEDs, optional buzzer, float inputs, spare header.

| Done | Ref | Part | LCSC | Qty |
|---|---|---|---|---|
| [ ] | J6 | JST XH 4P header for PZEM-004T | C594232 | 1 |
| [ ] | R16 | 4.7 k, PZEM_TX divider top | C17936 | 1 |
| [ ] | R4 | 10 k, PZEM_TX divider bottom | C17902 | 1 |
| [ ] | C16 | 100 nF 1206, header 5 V | C24497 | 1 |
| [ ] | SW3 | START button | C318884 | 1 |
| [ ] | SW4 | STOP button | C318884 | 1 |
| [ ] | SW5 | MENU button | C318884 | 1 |
| [ ] | LED1 | Red LED: power | C965798 | 1 |
| [ ] | LED2 | Red LED: Wi-Fi / status | C965798 | 1 |
| [ ] | R8 | 1 k, LED1 series | C4410 | 1 |
| [ ] | R9 | 1 k, LED2 series | C4410 | 1 |
| [ ] | BZ1 | OPTIONAL passive buzzer MLT-8530 | C94599 | 1 |
| [ ] | R22 | OPTIONAL 10 ohm series resistor for BZ1 (limits buzzer voltage) | C17903 | 1 |
| [ ] | Q4 | AO3400A buzzer driver (optional) | C20917 | 1 |
| [ ] | D3 | Schottky flyback across buzzer (optional) | C2758511 | 1 |
| [ ] | R21 | 100 k gate pull-down Q4 (optional) | C17900 | 1 |
| [ ] | J10 | Float input 1 screw terminal 2P | C474952 | 1 |
| [ ] | J11 | Float input 2 screw terminal 2P | C474952 | 1 |
| [ ] | J12 | 1x6 spare header | C492405 | 1 |
| [ ] | R6 | 10 k optional pull-up IN1 (DNP) | C17902 | 1 |
| [ ] | R7 | 10 k optional pull-up IN2 (DNP) | C17902 | 1 |

Parts on this page: 21

## SCHEMATIC PAGE 5 - Display options
16x2 I2C LCD, I2C OLED, 12864 ST7920 with level shifters.

| Done | Ref | Part | LCSC | Qty |
|---|---|---|---|---|
| [ ] | J7 | 1x4 header: 16x2 I2C LCD | C2691448 | 1 |
| [ ] | J8 | 1x4 header: I2C OLED | C2691448 | 1 |
| [ ] | J9 | 1x20 female header: 12864 ST7920 | C41413628 | 1 |
| [ ] | U5 | PCA9306 I2C level shifter (16x2 only) | C33196 | 1 |
| [ ] | U6 | SN74AHCT125 3.3 V to 5 V buffer (12864 only) | C155176 | 1 |
| [ ] | Q3 | AO3400A backlight switch | C20917 | 1 |
| [ ] | RV2 | 10 k trimmer, 12864 contrast | C58159 | 1 |
| [ ] | R12 | 4.7 k, SDA pull-up 3V3 | C17936 | 1 |
| [ ] | R13 | 4.7 k, SCL pull-up 3V3 | C17936 | 1 |
| [ ] | R14 | 4.7 k, SDA_5V pull-up (DNP with backpack) | C17936 | 1 |
| [ ] | R15 | 4.7 k, SCL_5V pull-up (DNP with backpack) | C17936 | 1 |
| [ ] | R5 | 10 k, PCA9306 EN pull-up | C17902 | 1 |
| [ ] | R20 | 100 k gate pull-down Q3 | C17900 | 1 |
| [ ] | C12 | 100 nF 1206, U5 VREF1 | C24497 | 1 |
| [ ] | C13 | 100 nF 1206, U5 VREF2 | C24497 | 1 |
| [ ] | C14 | 100 nF 1206, U6 VCC | C24497 | 1 |
| [ ] | C19 | 100 nF 1206, display 5 V | C24497 | 1 |

Parts on this page: 17
