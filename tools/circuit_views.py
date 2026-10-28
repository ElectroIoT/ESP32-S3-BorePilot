"""Easy 'circuit view' pictures for every section (same style as the relay view).
Used by gen_wiring.py. Planned nets only; check pin names against the EasyEDA symbols."""
import html
from relay_view import pill, flag, ln, dot, gnd, res_v, C5, CS, CR, CG

e = html.escape
C3 = "#f4b400"
CL, CN, CU, CI, CP = "#e53935", "#1e88e5", "#8e24aa", "#ec407a", "#00bcd4"
W = 760
RAILS = ("+5V", "+5V_HLK", "VBUS", "+3V3")


def net_col(n):
    if n in ("+5V", "+5V_HLK", "VBUS"): return C5
    if n == "+3V3": return C3
    if n == "GND": return CG
    if n == "L": return CL
    if n == "N": return CN
    if n.startswith(("USB_", "CC")): return CU
    if n in ("SDA", "SCL", "SDA_5V", "SCL_5V", "V0", "VOUT", "PSB", "BL_K", "PCA_EN") or n.startswith("LCD_"): return CI
    if n.startswith("PZEM"): return CP
    if n.startswith(("COM", "NO", "NC")): return CR
    return CS


def gndL(x, y):
    """Ground symbol reached from the right, label on the left."""
    return (ln([(x, y), (x - 12, y)], CG)
            + f'<line x1="{x-12}" y1="{y-7}" x2="{x-12}" y2="{y+7}" stroke="{CG}" stroke-width="2"/>'
            + f'<line x1="{x-16}" y1="{y-4}" x2="{x-16}" y2="{y+4}" stroke="{CG}" stroke-width="2"/>'
            + f'<line x1="{x-20}" y1="{y-2}" x2="{x-20}" y2="{y+2}" stroke="{CG}" stroke-width="2"/>'
            + f'<text x="{x-26}" y="{y+4}" text-anchor="end" class="net" fill="{CG}">GND</text>')


def net_end(x, y, name, side):
    """Flag at the end of a wire. side 'l': flag sits left of x; 'r': right of x."""
    c = net_col(name)
    if name in RAILS:
        pw = 7 * len(name) + 12
        cx = x - pw / 2 if side == "l" else x + pw / 2
        return flag(cx, y, name, c)
    return pill(x, y, name, c, "r" if side == "l" else "l")


def part(x, y, w, ref, name, code, L, R, minrows=0):
    rows = max(len(L), len(R), minrows)
    h = 46 + 20 * rows
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>',
         f'<text x="{x+8}" y="{y+16}" class="ref">{e(ref)}</text><text x="{x+8+8*len(ref)+8}" y="{y+16}" class="role">{e(name)}</text>',
         f'<text x="{x+8}" y="{y+29}" class="lab">[{e(code)}]</text>']
    ys = {}
    for side, pins in (("L", L), ("R", R)):
        for i, (lab, net) in enumerate(pins):
            py = y + 46 + 20 * i
            if side == "L":
                o.append(f'<text x="{x+8}" y="{py+4}" class="pin">{e(lab)}</text>')
                ex, ox = x, -1
            else:
                o.append(f'<text x="{x+w-8}" y="{py+4}" text-anchor="end" class="pin">{e(lab)}</text>')
                ex, ox = x + w, 1
            if net == "NC":
                o.append(f'<line x1="{ex+ox*4}" y1="{py-4}" x2="{ex+ox*10}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><line x1="{ex+ox*10}" y1="{py-4}" x2="{ex+ox*4}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/>')
            elif net == "GND":
                o.append(gndL(ex, py) if side == "L" else ln([(ex, py), (ex + 14, py)], CG) + gnd(ex + 14, py))
            elif net:
                c = net_col(net)
                o.append(ln([(ex, py), (ex + ox * 40, py)], c) + dot(ex, py, c) + net_end(ex + ox * 40, py, net, "l" if side == "L" else "r"))
            ys[(side, lab)] = py
    return "".join(o), ys, h


def cap_v(x, y1, y2, c, label):
    m = (y1 + y2) / 2
    return (ln([(x, y1), (x, m - 4)], c) + ln([(x, m + 4), (x, y2)], c)
            + f'<line x1="{x-9}" y1="{m-4}" x2="{x+9}" y2="{m-4}" stroke="var(--fg)" stroke-width="2.5"/>'
            + f'<line x1="{x-9}" y1="{m+4}" x2="{x+9}" y2="{m+4}" stroke="var(--fg)" stroke-width="2.5"/>'
            + f'<text x="{x+13}" y="{m+4}" class="pin">{e(label)}</text>')


def res_h(x1, x2, y, c, label, below=False):
    m = (x1 + x2) / 2
    ty = y + 24 if below else y - 10
    return (ln([(x1, y), (m - 14, y)], c) + ln([(m + 14, y), (x2, y)], c)
            + f'<rect x="{m-14}" y="{y-6}" width="28" height="12" fill="var(--card)" stroke="{c}" stroke-width="2"/>'
            + f'<text x="{m}" y="{ty}" text-anchor="middle" class="pin">{e(label)}</text>')


def diode_h(x1, x2, y, c, label, cathode="right"):
    m = (x1 + x2) / 2
    if cathode == "right":
        tri = f'<polygon points="{m-10},{y-10} {m-10},{y+10} {m+10},{y}" fill="var(--card)" stroke="var(--fg)" stroke-width="2"/><line x1="{m+11}" y1="{y-11}" x2="{m+11}" y2="{y+11}" stroke="var(--fg)" stroke-width="3"/>'
    else:
        tri = f'<polygon points="{m+10},{y-10} {m+10},{y+10} {m-10},{y}" fill="var(--card)" stroke="var(--fg)" stroke-width="2"/><line x1="{m-11}" y1="{y-11}" x2="{m-11}" y2="{y+11}" stroke="var(--fg)" stroke-width="3"/>'
    return (ln([(x1, y), (m - 12, y)], c) + ln([(m + 12, y), (x2, y)], c) + tri
            + f'<text x="{m}" y="{y-16}" text-anchor="middle" class="pin">{e(label)}</text>')


def sw_v(x, y1, y2, label):
    m = (y1 + y2) / 2
    return (ln([(x, y1), (x, m - 14)], CS) + ln([(x, m + 14), (x, y2)], CG)
            + f'<circle cx="{x}" cy="{m-14}" r="3" fill="var(--fg)"/><circle cx="{x}" cy="{m+14}" r="3" fill="var(--fg)"/><line x1="{x}" y1="{m-14}" x2="{x+12}" y2="{m+8}" stroke="var(--fg)" stroke-width="2"/>'
            + f'<text x="{x+18}" y="{m+4}" class="pin">{e(label)}</text>')


def sw_h(x1, x2, y, label):
    m = (x1 + x2) / 2
    return (ln([(x1, y), (m - 14, y)], CS) + ln([(m + 14, y), (x2, y)], CG)
            + f'<circle cx="{m-14}" cy="{y}" r="3" fill="var(--fg)"/><circle cx="{m+14}" cy="{y}" r="3" fill="var(--fg)"/><line x1="{m-14}" y1="{y}" x2="{m+10}" y2="{y-12}" stroke="var(--fg)" stroke-width="2"/>'
            + f'<text x="{m}" y="{y-18}" text-anchor="middle" class="pin">{e(label)}</text>')


def mosfet(x, y, ref, code="AO3400A"):
    """60x70 box: D top (x+30,y), G left (x,y+45), S bottom (x+30,y+70)."""
    return (f'<rect x="{x}" y="{y}" width="60" height="70" rx="6" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>'
            f'<text x="{x+6}" y="{y+16}" class="ref">{ref}</text><text x="{x+6}" y="{y+31}" class="lab">{code}</text>'
            f'<text x="{x+48}" y="{y+14}" class="pin">D</text><text x="{x+4}" y="{y+49}" class="pin">G</text><text x="{x+48}" y="{y+66}" class="pin">S</text>')


def svg(h, body, title):
    return (f'<svg viewBox="0 0 {W} {h}" width="{W}" height="{h}" class="cdia">'
            f'<text x="14" y="24" class="ref" style="font-size:15px">{e(title)}</text>{body}</svg>')


def txt(x, y, s, cls="lab"):
    return f'<text x="{x}" y="{y}" class="{cls}">{e(s)}</text>'


# ------------------------------------------------------------------ views
def v_mains():
    b = ['<rect x="40" y="52" width="610" height="244" rx="8" fill="#e53935" fill-opacity=".05" stroke="#e53935" stroke-dasharray="6 4"/>',
         '<text x="48" y="68" class="lab" style="fill:#e53935!important;font-weight:700">MAINS SIDE (230 V): the red slot on the PCB keeps 6.4 mm from the low-voltage side</text>']
    s, ys, h = part(110, 82, 120, "J2", "AC in, 2P screw", "C474952", [], [("1  L", "L"), ("2  N", "N")])
    b.append(s)
    s, ys2, h = part(110, 200, 120, "J3", "AC tap to PZEM", "C474952", [], [("1  L", "L"), ("2  N", "N")])
    b.append(s)
    s, ys3, h = part(440, 82, 150, "U2", "HLK-5M05 5V 1A", "C209907", [("AC(L)", "L"), ("AC(N)", "N")], [("+Vo", "+5V_HLK"), ("-Vo", "GND")])
    b.append(s)
    yvo = ys3[("R", "+Vo")]
    b.append(dot(620, yvo, C5) + cap_v(620, yvo, yvo + 70, C5, "C15 100nF") + gnd(620, yvo + 70))
    b.append(txt(14, 318, "J2 pin 1 is L, pin 2 is N. J3 repeats L and N for the PZEM voltage input. U2 makes the isolated 5 V rail (3000 VAC isolation per datasheet)."))
    b.append(txt(14, 336, "No fuse or varistor on the board (owner decision): the panel breaker / fuse must protect J2."))
    return svg(350, "".join(b), "MAINS INPUT: breaker to J2, J3 tap and the HLK-5M05 module")


def v_power():
    b = []
    b.append(net_end(60, 70, "+5V_HLK", "l") + ln([(60, 70), (130, 70)], C5) + diode_h(130, 260, 70, C5, "D4 SS34B", "right") + ln([(260, 70), (330, 70)], C5))
    b.append(net_end(60, 150, "VBUS", "l") + ln([(60, 150), (130, 150)], C5) + diode_h(130, 260, 150, C5, "D5 SS34B", "right") + ln([(260, 150), (300, 150), (300, 70)], C5) + dot(300, 70, C5))
    b.append(txt(70, 112, "bar = cathode toward +5V: neither source can push power into the other"))
    b.append(ln([(330, 70), (700, 70)], C5, 3) + flag(350, 50, "+5V", C5))
    for x, ref, val in [(400, "C1", "470uF"), (490, "C6", "10uF"), (580, "C5", "10uF")]:
        b.append(dot(x, 70, C5) + cap_v(x, 70, 170, C5, f"{ref} {val}") + gnd(x, 170))
    b.append(dot(660, 70, C5) + ln([(660, 70), (660, 240)], C5))
    s, ys, h = part(420, 215, 150, "U3", "SGM2212-3.3 LDO", "C3294699", [("VIN", None), ("GND", None)], [("VOUT", None)])
    b.append(s)
    b.append(ln([(660, 261), (360, 261), (360, 261)], C5) if False else "")
    yin, ygn, yout = ys[("L", "VIN")], ys[("L", "GND")], ys[("R", "VOUT")]
    b.append(ln([(420, yin), (350, yin)], C5) + dot(350, yin, C5) + ln([(350, yin), (350, 190), (660, 190), (660, 70)], C5) if False else "")
    b.append(ln([(420, yin), (380, yin), (380, 200), (660, 200)], C5) + dot(660, 200, C5))
    b.append(ln([(420, ygn), (390, ygn)], CG) + gndL(390, ygn))
    b.append(cap_v(340, yin, yin + 70, C5, "C2 10uF") + ln([(340, yin), (380, yin)], C5) + dot(380, yin, C5) + gnd(340, yin + 70))
    b.append(ln([(570, yout), (630, yout)], C3) + dot(570, yout, C3) + flag(660, yout, "+3V3", C3))
    b.append(dot(600, yout, C3) + cap_v(600, yout, yout + 60, C3, "C3 10uF") + gnd(600, yout + 60))
    b.append(txt(14, 380, "Either source can power the board: USB alone runs the logic, the HLK runs everything. +3V3 goes to the ESP32 and pages 2 to 5 by net flag."))
    return svg(400, "".join(b), "5 V / 3.3 V POWER: OR-ing diodes, bulk caps and the LDO")


def v_usb():
    b = []
    s, ys, h = part(150, 50, 190, "J1", "USB-C (symbol pins)", "C165948",
                    [("A4B9 VBUS", "VBUS"), ("B4A9 VBUS", "VBUS"), ("A1B12 GND", "GND"), ("B1A12 GND", "GND"), ("EH1-4 shell", "GND")],
                    [("A5 CC1", "CC1"), ("B5 CC2", "CC2"), ("A6 DP1", "USB_DP_J1"), ("B6 DP2", "USB_DP_J1"), ("A7 DN1", "USB_DN_J1"), ("B7 DN2", "USB_DN_J1"), ("A8 SBU1", "NC"), ("B8 SBU2", "NC")])
    b.append(s)
    # CC resistors (right column)
    b.append(txt(520, 80, "CC pull-downs (USB-C needs them)", "ref"))
    b.append(pill(500, 110, "CC1", CU, "r") + res_h(500, 600, 110, CU, "R1 5.1k", True) + ln([(600, 110), (640, 110)], CU) + gndL(660, 110).replace("", "") if False else "")
    b.append(pill(470, 110, "CC1", CU, "l") + ln([(520, 110), (540, 110)], CU) + res_h(540, 620, 110, CU, "R1 5.1k", True) + ln([(620, 110), (640, 110)], CU) + gnd(640, 110))
    b.append(pill(470, 170, "CC2", CU, "l") + ln([(520, 170), (540, 170)], CU) + res_h(540, 620, 170, CU, "R2 5.1k", True) + ln([(620, 170), (640, 170)], CU) + gnd(640, 170))
    # U4
    s, ys2, h2 = part(150, 300, 200, "U4", "USBLC6-2SC6 ESD", "C7519",
                      [("1 I/O1 (J1 side)", "USB_DP_J1"), ("3 I/O2 (J1 side)", "USB_DN_J1"), ("5 VBUS", "VBUS"), ("2 GND", "GND")],
                      [("6 I/O1 (MCU side)", "USB_DP"), ("4 I/O2 (MCU side)", "USB_DN")])
    b.append(s)
    b.append(txt(470, 340, "to GPIO20 (D+)", "pin") + txt(470, 360, "to GPIO19 (D-)", "pin"))
    # VBUS decoupling
    b.append(txt(470, 410, "VBUS decoupling", "ref"))
    b.append(flag(490, 438, "VBUS", C5) + ln([(520, 438), (660, 438)], C5))
    b.append(dot(550, 438, C5) + cap_v(550, 438, 498, C5, "C7 10uF") + gnd(550, 498) + dot(650, 438, C5) + cap_v(650, 438, 498, C5, "C11 100nF") + gnd(650, 498))
    b.append(txt(14, 540, "Same-name flags join: both D+ pins (A6, B6) become USB_DP_J1, both D- pins USB_DN_J1. After U4 they continue as USB_DP / USB_DN to GPIO20 / GPIO19. SBU pins are not used."))
    return svg(560, "".join(b), "USB-C: connector, CC resistors, ESD part, data to the ESP32")


def v_mcu():
    b = []
    left = [("3V3", "+3V3"), ("GND", "GND"), ("EN", "EN"), ("IO0", "IO0_BOOT"), ("IO19", "USB_DN"), ("IO20", "USB_DP")]
    right = [("IO4", "RLY1"), ("IO5", "RLY2"), ("IO8", "SDA"), ("IO9", "SCL"), ("IO10", "LCD_CS"), ("IO11", "LCD_MOSI"), ("IO12", "LCD_CLK"),
             ("IO13", "LCD_BL"), ("IO14", "LCD_RST"), ("IO15", "BUZZ"), ("IO16", "LED_ST"), ("IO17", "PZEM_TXD"), ("IO18", "PZEM_RXD"),
             ("IO1", "BTN_START"), ("IO2", "BTN_STOP"), ("IO6", "BTN_MENU"), ("IO39", "IN1"), ("IO40", "IN2"), ("IO41", "SP1"), ("IO42", "SP2"),
             ("IO47", "SP3"), ("IO48", "SP4"), ("TXD0", "TXD0"), ("RXD0", "RXD0")]
    s, ys, h = part(300, 50, 190, "U1", "ESP32-S3-WROOM-1U-N16R8", "C3013946", left, right)
    b.append(s)
    # reset / boot circuits (left, below the power pins)
    y0 = 50 + 46 + 20 * 6 + 70
    b.append(txt(14, y0 - 96, "Reset (EN) circuit", "ref"))
    b.append(pill(60, y0, "EN", CS, "r") + ln([(60, y0), (250, y0)], CS))
    b.append(dot(110, y0, CS) + res_v(110, y0 - 56, y0, C3, "R3 10k") + flag(110, y0 - 64, "+3V3", C3))
    b.append(dot(170, y0, CS) + cap_v(170, y0, y0 + 56, CG, "C8 100nF") + gnd(170, y0 + 56))
    b.append(dot(230, y0, CS) + sw_v(230, y0, y0 + 56, "SW1 reset") + gnd(230, y0 + 56))
    y1 = y0 + 140
    b.append(txt(14, y1 - 40, "BOOT circuit (hold while powering up to flash)", "ref"))
    b.append(pill(130, y1, "IO0_BOOT", CS, "r") + ln([(130, y1), (150, y1)], CS) + sw_v(150, y1, y1 + 56, "SW2 BOOT") + gnd(150, y1 + 56))
    # decoupling (below U1)
    yd = 50 + 46 + 20 * len(right) + 50
    b.append(txt(300, yd - 30, "3.3 V decoupling next to the module", "ref"))
    b.append(flag(330, yd, "+3V3", C3) + ln([(360, yd), (620, yd)], C3))
    for i, (ref, val) in enumerate([("C4", "10uF"), ("C9", "100nF"), ("C10", "100nF")]):
        x = 400 + 100 * i
        b.append(dot(x, yd, C3) + cap_v(x, yd, yd + 56, C3, f"{ref} {val}") + gnd(x, yd + 56))
    b.append(txt(14, yd + 100, "Nothing except SW2 on IO0. IO3, IO45, IO46, IO7, IO21, IO35 to IO38: no-connect. Antenna = U.FL pigtail ANT1 to ANT2 (not drawn as wires)."))
    return svg(yd + 120, "".join(b), "ESP32-S3 CORE: reset, boot, decoupling and the signals leaving the page")


def v_pzem():
    b = []
    s, ys, h = part(300, 60, 190, "J6", "JST XH 4-pin to PZEM", "C594232",
                    [("1  +5V", "+5V"), ("4  GND", "GND")], [("2  to PZEM RX", "PZEM_TXD"), ("3  from PZEM TX", None)])
    b.append(s)
    y3 = ys[("R", "3  from PZEM TX")]
    b.append(ln([(490, y3), (540, y3)], CP) + dot(490, y3, CP) + res_h(540, 620, y3, CP, "R16 4.7k", True) + ln([(620, y3), (660, y3)], CP) + dot(650, y3, CP) + pill(660, y3, "PZEM_RXD", CP, "l"))
    b.append(ln([(650, y3), (650, y3 + 10)], CP) + res_v(650, y3 + 10, y3 + 60, CG, "R4 10k") + gnd(650, y3 + 60))
    b.append(dot(110, 100, C5) + cap_v(110, 100, 160, C5, "C16 100nF") + ln([(60, 100), (110, 100)], C5) + flag(40, 100, "+5V", C5) + gnd(110, 160))
    b.append(txt(14, 250, "R16 + R4 divide the module's 5 V TX down for GPIO18 (RX). GPIO17 (TX) drives the PZEM RX pin directly."))
    b.append(txt(14, 268, "Match J6 to the pin order printed on your PZEM module before soldering."))
    return svg(290, "".join(b), "PZEM-004T LINK: header, divider on the module's TX line")


def v_ui():
    b = [txt(14, 54, "Buttons (internal pull-ups, press = low)", "ref")]
    for i, (ref, net) in enumerate([("SW3 START", "BTN_START"), ("SW4 STOP", "BTN_STOP"), ("SW5 MENU", "BTN_MENU")]):
        y = 90 + 40 * i
        b.append(pill(70, y, net, CS, "r") + ln([(70, y), (110, y)], CS) + sw_h(110, 230, y, ref) + gnd(230, y))
    b.append(txt(14, 230, "Status LEDs", "ref"))
    b.append(flag(60, 266, "+3V3", C3) + res_h(90, 190, 266, C3, "R8 1k") + ln([(190, 266), (200, 266)], C3) + diode_h(200, 290, 266, C3, "LED1 red power", "right") + gnd(290, 266))
    b.append(pill(90, 316, "LED_ST", CS, "r") + res_h(90, 190, 316, CS, "R9 1k") + ln([(190, 316), (200, 316)], CS) + diode_h(200, 290, 316, CS, "LED2 red status", "right") + gnd(290, 316))
    b.append(txt(400, 54, "Float / level inputs (dry contact to GND)", "ref"))
    s, ys, h = part(500, 70, 140, "J10", "2P screw terminal", "C474952", [("1", "IN1"), ("2", "GND")], [])
    b.append(s)
    s, ys, h = part(500, 170, 140, "J11", "2P screw terminal", "C474952", [("1", "IN2"), ("2", "GND")], [])
    b.append(s)
    b.append(txt(400, 276, "R6 / R7: 10k pull-ups to +3V3, not fitted (DNP).", "lab"))
    b.append(txt(14, 380, "OPTIONAL buzzer: BZ1 + Q4 + D3 + R21 (leave all four off if not wanted)", "ref"))
    b.append(flag(70, 410, "+5V", C5) + ln([(100, 410), (300, 410)], C5))
    b.append(dot(160, 410, C5) + ln([(160, 410), (160, 440)], C5) + f'<rect x="130" y="440" width="60" height="30" rx="5" fill="var(--card)" stroke="var(--fg)" stroke-width="2"/><text x="160" y="459" text-anchor="middle" class="pin">BZ1</text>' + ln([(160, 470), (160, 500)], CS) + dot(160, 500, CS))
    b.append(dot(260, 410, C5) + ln([(260, 410), (260, 500)], C5) + diode_h(160, 260, 500, CS, "D3", "left"))
    b.append(txt(110, 490, "", "pin"))
    b.append(ln([(160, 500), (160, 520)], CS) + mosfet(130, 520, "Q4"))
    b.append(ln([(130, 565), (80, 565)], CS) + dot(100, 565, CS) + pill(80, 565, "BUZZ", CS, "r") + res_v(100, 575, 615, CG, "R21 100k") + gnd(100, 615) + ln([(160, 590), (160, 615)], CG) + gnd(160, 615))
    return svg(660, "".join(b), "BUTTONS, LEDs, FLOAT INPUTS and OPTIONAL BUZZER")


def v_oled():
    b = [txt(14, 46, "Check your OLED's pin order (some modules have VCC and GND swapped).")]
    s, ys, h = part(300, 70, 190, "J8", "1x4 header: I2C OLED", "C2691448",
                    [("1  GND", "GND"), ("2  VCC", "+3V3"), ("3  SCL", "SCL"), ("4  SDA", "SDA")], [])
    b.append(s)
    b.append(txt(14, 230, "Pull-ups R12 (SDA) and R13 (SCL), 4.7 k to +3V3, serve the OLED and the I2C side of the 16x2 level shifter."))
    b.append(pill(60, 280, "SDA", CI, "r") + ln([(60, 280), (110, 280)], CI) + dot(150, 280, CI) + ln([(110, 280), (250, 280)], CI) + res_v(150, 230 + 0, 280, C3, "") if False else "")
    b.append(pill(60, 300, "SDA", CI, "r") + ln([(60, 300), (260, 300)], CI) + dot(140, 300, CI) + res_v(140, 250, 300, C3, "R12 4.7k") + flag(140, 242, "+3V3", C3))
    b.append(pill(300, 300, "SCL", CI, "r") + ln([(300, 300), (500, 300)], CI) + dot(380, 300, CI) + res_v(380, 250, 300, C3, "R13 4.7k") + flag(380, 242, "+3V3", C3))
    return svg(330, "".join(b), "OPTION B: I2C OLED, 3.3 V direct")


def v_lcd16():
    b = []
    s, ys, h = part(130, 60, 160, "U5", "PCA9306 level shifter", "C33196",
                    [("1 GND", "GND"), ("2 VREF1", "+3V3"), ("3 SCL1", "SCL"), ("4 SDA1", "SDA")],
                    [("8 EN", None), ("7 VREF2", "+5V"), ("6 SCL2", None), ("5 SDA2", None)])
    b.append(s)
    yen = ys[("R", "8 EN")]
    b.append(ln([(290, yen), (330, yen)], C5) + dot(290, yen, C5) + res_h(330, 400, yen, C5, "R5 10k", False) + ln([(400, yen), (420, yen)], C5) + flag(450, yen, "+5V", C5))
    ysc, ysd = ys[("R", "6 SCL2")], ys[("R", "5 SDA2")]
    s2, ys2, h2 = part(520, 200, 190, "J7", "1x4 header: 16x2 I2C LCD", "C2691448",
                       [("1  GND", "GND"), ("2  VCC", "+5V"), ("3  SDA", None), ("4  SCL", None)], [])
    b.append(s2)
    ysda, yscl = ys2[("L", "3  SDA")], ys2[("L", "4  SCL")]
    b.append(ln([(290, ysd), (350, ysd), (350, ysda), (520, ysda)], CI) + dot(290, ysd, CI) + dot(520, ysda, CI))
    b.append(ln([(290, ysc), (370, ysc), (370, yscl), (520, yscl)], CI) + dot(290, ysc, CI) + dot(520, yscl, CI))
    b.append(txt(300, ysd + 16, "SDA_5V", "net") + txt(380, ysc - 6, "SCL_5V", "net"))
    b.append(txt(14, 340, "R14 / R15 (4.7k from SDA_5V / SCL_5V to +5V): fit ONLY if the LCD backpack has no pull-ups. C12 100nF on VREF1, C13 100nF on VREF2."))
    b.append(txt(14, 358, "The 5 V I2C of the backpack never reaches the ESP32: the PCA9306 separates the two sides."))
    return svg(380, "".join(b), "OPTION A: 16x2 I2C LCD through the PCA9306 level shifter")


def v_lcd12864():
    b = []
    s, ys, h = part(130, 60, 200, "U6", "SN74AHCT125 buffer", "C155176",
                    [("2 1A", "LCD_CS"), ("5 2A", "LCD_MOSI"), ("9 3A", "LCD_CLK"), ("12 4A", "LCD_RST"), ("14 VCC", "+5V"), ("7 GND", "GND"), ("1 1OE", "GND"), ("4 2OE", "GND"), ("10 3OE", "GND"), ("13 4OE", "GND")],
                    [("3 1Y", None), ("6 2Y", None), ("8 3Y", None), ("11 4Y", None)])
    b.append(s)
    s2, ys2, h2 = part(560, 60, 160, "J9", "12864 ST7920 header", "C41413628",
                       [("4 RS", None), ("5 R/W", None), ("6 E", None), ("17 RST", None), ("1 VSS", "GND"), ("2 VDD", "+5V"), ("19 BLA", "+5V"), ("20 BLK", "BL_K"), ("15 PSB", "PSB"), ("3 V0", "V0"), ("18 VOUT", "VOUT")], [])
    b.append(s2)
    for (a, bb) in [("3 1Y", "4 RS"), ("6 2Y", "5 R/W"), ("8 3Y", "6 E"), ("11 4Y", "17 RST")]:
        y1, y2 = ys[("R", a)], ys2[("L", bb)]
        b.append(ln([(330, y1), (560, y2)], CI) if y1 == y2 else "")
    # rows are aligned by order: 1Y..4Y rows 0..3 and RS..RST rows 0..3
    b.append(txt(350, 86, "RS / R/W / E / RST at 5 V", "pin"))
    yb = 60 + h2 + 40
    b.append(txt(14, yb - 14, "Backlight switch, contrast trimmer and serial-mode jumper", "ref"))
    b.append(mosfet(130, yb, "Q3") + ln([(160, yb), (160, yb - 8)], CI) + pill(166, yb - 8, "BL_K", CI, "l"))
    b.append(ln([(130, yb + 45), (90, yb + 45)], CS) + dot(100, yb + 45, CS) + pill(90, yb + 45, "LCD_BL", CS, "r") + res_v(100, yb + 55, yb + 95, CG, "R20 100k") + gnd(100, yb + 95) + ln([(160, yb + 70), (160, yb + 95)], CG) + gnd(160, yb + 95))
    b.append(txt(330, yb + 14, "RV2 10k trimmer (contrast)", "pin"))
    b.append(f'<rect x="352" y="{yb+30}" width="24" height="60" fill="var(--card)" stroke="{CI}" stroke-width="2"/>')
    b.append(ln([(364, yb + 30), (364, yb + 14)], C5) + flag(364, yb + 6, "+5V", C5) + ln([(364, yb + 90), (364, yb + 106)], CI) + pill(374, yb + 106, "VOUT", CI, "l") + ln([(376, yb + 60), (410, yb + 60)], CI) + pill(414, yb + 60, "V0", CI, "l"))
    b.append(txt(560, yb + 14, "SJ1 solder jumper (default bridged)", "pin") + pill(540, yb + 50, "PSB", CI, "r") + ln([(540, yb + 50), (600, yb + 50)], CI) + f'<rect x="600" y="{yb+40}" width="30" height="20" rx="3" fill="none" stroke="var(--fg)" stroke-width="2"/>' + ln([(630, yb + 50), (660, yb + 50)], CG) + gnd(660, yb + 50))
    b.append(txt(14, yb + 140, "C14 100nF on U6 VCC, C19 100nF on the J9 +5V. PSB to GND = serial mode. Check contrast wiring and the backlight resistor on your own module's datasheet."))
    return svg(yb + 160, "".join(b), "OPTION C: 12864 ST7920 through the 74AHCT125, backlight and contrast")


VIEWS = {
    "mains": [("mains", v_mains, "How the mains reaches the HLK module. The red dashed area is the 230 V side.", ["J2 pin 1 is L, pin 2 is N. J3 repeats L and N for the PZEM voltage input.", "U2 turns it into isolated 5 V (+5V_HLK) on the low-voltage side.", "There is no fuse or varistor on the board: your panel breaker must protect it."])],
    "power": [("power", v_power, "How 5 V and 3.3 V are made.", ["The HLK output and USB VBUS each go through a Schottky diode into the common +5V rail.", "C1, C5, C6 smooth the rail; C2 sits on the LDO input.", "U3 makes +3V3, with C3 at its output."])],
    "usb": [("usb", v_usb, "How USB-C is wired.", ["CC1 and CC2 each have a 5.1 k resistor to GND so a USB-C cable gives 5 V.", "D+ pins A6/B6 and D- pins A7/B7 are tied together, go through U4, then on to GPIO20 / GPIO19.", "VBUS feeds D5 (page 1) and U4."])],
    "mcu": [("mcu", v_mcu, "What the ESP32 needs around it.", ["3V3 and GND power the module; C4, C9, C10 decouple it.", "EN: 10 k pull-up to +3V3, 100 nF to GND and the reset button.", "IO0: the BOOT button to GND only. All other GPIOs leave the page as net flags."])],
    "pzem": [("pzem", v_pzem, "How the PZEM module is connected.", ["+5V and GND power the module from the J6 header.", "GPIO17 (TX) drives the PZEM RX pin directly (3.3 V is enough).", "PZEM TX returns through R16 and R4 which divide it down for GPIO18 (RX)."])],
    "ui": [("ui", v_ui, "Buttons, LEDs, float inputs and the optional buzzer.", ["Each button pulls its GPIO to GND when pressed.", "LED1 is the power LED (from +3V3); LED2 follows GPIO16.", "Floats connect between IN1 / IN2 and GND. The buzzer parts are optional."])],
    "disp": [("disp_b", v_oled, "Simplest: only four wires.", ["Fit this one first if you use an OLED."]),
             ("disp_a", v_lcd16, "5 V LCD backpack, separated from the 3.3 V I2C by the PCA9306.", ["Do not connect the backpack straight to the ESP32 pins."]),
             ("disp_c", v_lcd12864, "12864 graphic LCD: level buffer, contrast trimmer and backlight switch.", ["Fit the PSB jumper (SJ1) for serial mode."])],
}


def cards_for(sid):
    out = []
    for key, fn, desc, pts in VIEWS.get(sid, []):
        li = "".join(f"<li>{e(p)}</li>" for p in pts)
        out.append(f'<section class="card" id="cv-{key}" style="--c:#2fbf71"><h3>Circuit view</h3><p class="mut">{e(desc)} Colours: orange = 5 V, yellow = 3.3 V, grey = GND, green = GPIO, pink = display / I2C, purple = USB, cyan = UART, red / blue = mains.</p><div class="scroll">{fn()}</div><ol class="how">{li}</ol></section>')
    return "".join(out)
