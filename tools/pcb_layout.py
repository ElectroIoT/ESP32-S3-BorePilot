"""BorePilot PCB placement (planning data). Board 100 x 90 mm, origin lower-left, y up, mm.
Each entry: ref -> (x_center, y_center, width, height, rotation). Sizes are footprint estimates,
NOT taken from EasyEDA footprints: compare with the real footprints before routing.
BLOCKS group the parts into functional blocks; each block gets one top-silkscreen box."""

BOARD_W, BOARD_H = 100.0, 90.0
SLOT = dict(x=28.1, w=1.3, y0=51.0, y1=77.0)         # isolation slot, HLK area only (mains | low voltage), shortened 2026-11-11
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, 86.0), (96.0, 86.0)]   # M3, 3.2 mm, no pad
R1206 = (4.6, 2.6)
S603 = (2.6, 1.6)
BOX_MARGIN = 1.0

L = {}


def put(ref, x, y, w, h, rot=0):
    L[ref] = (x, y, w, h, rot)


def small(ref, x, y, size=R1206, rot=0):
    put(ref, x, y, size[0], size[1], rot)


# ---- MAINS IN
put("J2", 15, 84, 10.2, 8)
put("J3", 26, 84, 10.2, 8)
# ---- POWER (HLK + 5 V + 3.3 V)
put("U2", 27, 64, 38, 23)
small("C15", 49, 58)
put("D4", 50, 72.5, 5.4, 4.4)
put("D5", 50, 67, 5.4, 4.4)
put("C1", 57.5, 70.5, 9, 9)
put("U3", 65.5, 70, 7, 7)
small("C2", 60, 63.5)
small("C3", 66, 63.5)
small("C5", 50.5, 61.5)
small("C6", 55.5, 61.5)
# ---- RELAYS (split terminals, relay turned 270 degrees, decision 2026-11-11)
# Relay origin at rotation 270: COM and the two coil pins face up, NO / NC face down.
# COM runs down between the two slots under the relay body to J14 / J15, NO / NC go to J4 / J5 below the relay.
# Low-voltage parts (driver, diode, LED) sit in a strip above the relay, at least 7.8 mm from the COM pad.
def relay(n, x0, y0):
    k, j_no = f"K{n}", ("J4", "J5")[n - 1]
    q, d, r_g, r_l, led, cap = (("Q1", "D1", "R18", "R10", "LED3", "C17"), ("Q2", "D2", "R19", "R11", "LED4", "C18"))[n - 1]
    put(k, x0, y0, 19.2, 15.6, 270)
    put(j_no, x0, y0 - 16, 15.5, 8)
    put(d, x0 - 2.4, y0 + 17.2, 5.4, 4.4)
    put(q, x0 + 2.6, y0 + 17.2, 3.4, 3)
    small(r_g, x0 + 7.4, y0 + 17.2)
    small(r_l, x0 - 3, y0 + 21)
    put(led, x0 + 1.5, y0 + 21, *S603)
    small(cap, x0 + 6, y0 + 21)


relay(1, 17.5, 27)
relay(2, 39.5, 27)
# ---- ESP32-S3
put("U1", 81.5, 76.5, 19.2, 18)
put("J13", 83, 87.5, 15.3, 2.8)
small("C4", 75.5, 64.5)
small("C9", 80.5, 64.5)
small("C10", 85.5, 64.5)
small("R3", 75.5, 61)
small("C8", 75.5, 57.5)
put("SW1", 81.5, 58.5, 5.5, 5.5)
put("SW2", 88.5, 58.5, 5.5, 5.5)
# ---- DISPLAY HEADERS (OLED / 16x2) + level shifter
put("J8", 43, 87.5, 10.2, 2.8)
put("J7", 54.5, 87.5, 10.2, 2.8)
put("U5", 46, 83.7, 4, 3.4)
small("R12", 51.5, 83.7)
small("R13", 56.5, 83.7)
small("R14", 61.5, 83.7)
small("R15", 66.5, 83.7)
small("R5", 51.5, 80.8)
small("C12", 56.5, 80.8)
small("C13", 61.5, 80.8)
# ---- 12864 LCD connector and driver
put("J9", 97, 34, 2.8, 51)
put("U6", 86, 47, 9, 6.5)
put("Q3", 89, 40, 3.4, 3)
small("R20", 80, 40)
put("RV2", 76, 45, 7.5, 7)
small("C14", 89.7, 52)
small("C19", 85, 40.5)
# ---- SPARE I/O
put("J12", 97, 71, 2.8, 15.3)
# ---- USER INTERFACE (buttons, LEDs, buzzer)
put("SW3", 59, 29.2, 5.5, 5.5)
put("SW4", 66, 29.2, 5.5, 5.5)
put("SW5", 73, 29.2, 5.5, 5.5)
put("LED1", 59, 34.7, *S603)
small("R8", 63.5, 34.7)
put("LED2", 68, 34.7, *S603)
small("R9", 73, 34.7)
put("BZ1", 62, 21, 8.5, 8.5)
put("Q4", 69.5, 21, 3.4, 3)
put("D3", 74.5, 21, 5.4, 4.4)
small("R22", 69.5, 16.5)
small("R21", 74.5, 16.5)
# ---- USB-C
put("J1", 84.5, 4.2, 9, 7.5)
put("U4", 84.5, 13, 3.2, 3)
small("R1", 88, 16.5)
small("R2", 88, 19.5)
small("C7", 88.5, 10)
small("C11", 88.5, 13)
# ---- PZEM link
put("J6", 86.5, 27, 10.2, 6)
small("R16", 86.4, 33)
small("R4", 81.9, 33)
small("C16", 90.9, 33)
# ---- FLOAT INPUTS
put("J10", 61, 4, 10.2, 8)
put("J11", 72, 4, 10.2, 8)
small("R6", 61, 10.5)
small("R7", 72, 10.5)

BLOCKS = [
    ("mains_in", "MAINS IN 230 V", "#ff4d4d", ["J2", "J3"]),
    ("power", "POWER 5V / 3V3", "#ff9f43", ["U2", "C15", "D4", "D5", "C1", "U3", "C2", "C3", "C5", "C6"]),
    ("relay1", "RELAY 1", "#2fbf71", ["K1", "J4", "Q1", "D1", "R18", "R10", "LED3", "C17"]),
    ("relay2", "RELAY 2", "#1b9e5b", ["K2", "J5", "Q2", "D2", "R19", "R11", "LED4", "C18"]),
    ("esp32", "ESP32-S3", "#a66cff", ["U1", "J13", "C4", "C9", "C10", "R3", "C8", "SW1", "SW2"]),
    ("disp_hdr", "DISPLAY OLED / 16x2", "#ff4d94", ["J8", "J7", "U5", "R12", "R13", "R14", "R15", "R5", "C12", "C13"]),
    ("lcd_drv", "12864 LCD DRIVER", "#e91e63", ["U6", "Q3", "R20", "RV2", "C14", "C19"]),
    ("lcd_con", "12864 LCD", "#c2185b", ["J9"]),
    ("spare", "SPARE", "#9aa5b5", ["J12"]),
    ("ui", "BUTTONS LEDs BUZZER", "#f4c20d", ["SW3", "SW4", "SW5", "LED1", "R8", "LED2", "R9", "BZ1", "Q4", "D3", "R22", "R21"]),
    ("usb", "USB-C", "#4895ef", ["J1", "U4", "R1", "R2", "C7", "C11"]),
    ("pzem", "PZEM", "#00bcd4", ["J6", "R16", "R4", "C16"]),
    ("inputs", "FLOAT INPUTS", "#c0a000", ["J10", "J11", "R6", "R7"]),
]
REF_BLOCK = {r: b[0] for b in BLOCKS for r in b[3]}

OFFBOARD = {"ANT1": "U.FL pigtail to the module's U.FL connector, SMA bulkhead on the enclosure",
            "ANT2": "2.4 GHz SMA antenna on the outside of the enclosure"}


def rect(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def box_of(block_id):
    refs = [b for b in BLOCKS if b[0] == block_id][0][3]
    rs = [rect(L[r]) for r in refs]
    x0 = min(r[0] for r in rs) - BOX_MARGIN
    y0 = min(r[1] for r in rs) - BOX_MARGIN
    x1 = max(r[2] for r in rs) + BOX_MARGIN
    y1 = max(r[3] for r in rs) + BOX_MARGIN
    return (max(x0, 0.6), max(y0, 0.6), min(x1, BOARD_W - 0.6), min(y1, BOARD_H - 0.6))


def check():
    """Return a list of problems: overlaps, board edge, holes, slot band, mains creepage, silkscreen boxes."""
    prob = []
    rs = {k: rect(v) for k, v in L.items()}
    keys = list(rs)
    edge = {"J1", "J10", "J11", "J6", "J2", "J3", "J7", "J8", "J12", "J13", "J4", "J5", "J9"}
    for i in range(len(keys)):
        a = rs[keys[i]]
        inside = a[0] >= 0.5 and a[1] >= 0.5 and a[2] <= BOARD_W - 0.5 and a[3] <= BOARD_H - 0.5
        on_board = a[0] >= -0.01 and a[1] >= -0.01 and a[2] <= BOARD_W + 0.01 and a[3] <= BOARD_H + 0.01
        if not inside and not (keys[i] in edge and on_board):
            prob.append(f"{keys[i]} outside board {tuple(round(t, 1) for t in a)}")
        for j in range(i + 1, len(keys)):
            b = rs[keys[j]]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.2 and oy > 0.2:
                prob.append(f"overlap {keys[i]} / {keys[j]} ({ox:.1f} x {oy:.1f})")
        for (hx, hy) in HOLES:
            cx = min(max(hx, a[0]), a[2])
            cy = min(max(hy, a[1]), a[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"{keys[i]} touches mounting hole at ({hx},{hy})")
    sx0, sx1 = SLOT["x"] - 3.2, SLOT["x"] + SLOT["w"] + 3.2
    mains = {"J2", "J3", "J4", "J5", "U2", "K1", "K2"}
    for k, a in rs.items():
        if k in mains:
            continue
        if SLOT["y0"] - 3 < (a[1] + a[3]) / 2 < SLOT["y1"] + 3 and a[0] < sx1 and a[2] > sx0:
            prob.append(f"{k} inside the 3.2 mm band around the slot")
        for m in ("J2", "J3"):
            b = rs[m]
            dx = max(b[0] - a[2], a[0] - b[2], 0)
            dy = max(b[1] - a[3], a[1] - b[3], 0)
            if (dx * dx + dy * dy) ** 0.5 < 6.4:
                prob.append(f"{k} is closer than 6.4 mm to mains terminal {m}")
    missing = [r for r in L if r not in REF_BLOCK]
    if missing:
        prob.append(f"parts without a block: {missing}")
    # silkscreen boxes: no foreign part inside, no box-box overlap, clear of the mounting holes
    boxes = {b[0]: box_of(b[0]) for b in BLOCKS}
    for bid, bx in boxes.items():
        for ref, a in rs.items():
            if REF_BLOCK[ref] == bid:
                continue
            ox = min(a[2], bx[2]) - max(a[0], bx[0])
            oy = min(a[3], bx[3]) - max(a[1], bx[1])
            if ox > 0.05 and oy > 0.05:
                prob.append(f"part {ref} lies inside the silkscreen box of {bid}")
        for (hx, hy) in HOLES:
            cx = min(max(hx, bx[0]), bx[2])
            cy = min(max(hy, bx[1]), bx[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"silkscreen box {bid} touches a mounting hole")
    ids = list(boxes)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = boxes[ids[i]], boxes[ids[j]]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > -0.3 and oy > -0.3:
                prob.append(f"silkscreen boxes {ids[i]} / {ids[j]} overlap or are closer than 0.3 mm")
    return prob


if __name__ == "__main__":
    pr = check()
    print(len(L), "parts,", len(BLOCKS), "blocks,", len(pr), "problems")
    for p in pr:
        print(" ", p)
