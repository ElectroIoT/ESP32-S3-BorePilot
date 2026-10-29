"""BorePilot PCB placement (planning data). Board 100 x 90 mm, origin lower-left, y up, mm.
Each entry: ref -> (x_center, y_center, width, height, rotation). Sizes are footprint estimates,
NOT taken from EasyEDA footprints: compare with the real footprints before routing."""

BOARD_W, BOARD_H = 100.0, 90.0
SLOT = dict(x=28.1, w=1.3, y0=7.0, y1=77.0)          # isolation slot (mains | low voltage)
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, 86.0), (96.0, 86.0)]   # M3, 6.4 mm pads
R1206 = (4.6, 2.6)
S603 = (2.6, 1.6)

L = {}


def put(ref, x, y, w, h, rot=0):
    L[ref] = (x, y, w, h, rot)


def small(ref, x, y, size=R1206, rot=0):
    put(ref, x, y, size[0], size[1], rot)


# ---- mains side (left, x < 28), cables enter from the top and left edges
put("J2", 13, 84, 10.2, 8)
put("J3", 24, 84, 10.2, 8)
put("U2", 27, 63, 38, 23)
# relays straddle the slot, contact terminals on the left edge
put("K1", 28.75, 40, 19.2, 15.6)
put("K2", 28.75, 19.5, 19.2, 15.6)
put("J4", 5.5, 40, 15.5, 8, 90)
put("J5", 5.5, 19.5, 15.5, 8, 90)
# ---- relay drivers (low-voltage side, right of the relays)
put("Q1", 42, 44.5, 3.4, 3)
put("D1", 42, 40, 5.4, 4.4)
small("R18", 47, 44.5)
small("R10", 47, 40.5)
put("LED3", 51.5, 40.5, *S603)
small("C17", 46.5, 36.5)
put("Q2", 42, 24, 3.4, 3)
put("D2", 42, 19.5, 5.4, 4.4)
small("R19", 47, 24)
small("R11", 47, 20)
put("LED4", 51.5, 20, *S603)
small("C18", 47.5, 15)
# ---- power
put("C15", 49, 56, *R1206)
put("D4", 52, 73, 5.4, 4.4)
put("D5", 52, 67.5, 5.4, 4.4)
put("C1", 59.3, 71, 9, 9)
put("U3", 67.3, 70.5, 7, 7)
small("C2", 61.5, 64.5)
small("C3", 69, 64.5)
small("C5", 50.5, 62)
small("C6", 55.5, 62)
# ---- ESP32 core (top right)
put("U1", 81.5, 76.5, 19.2, 18)
small("C4", 73.5, 64.5)
small("C9", 78.5, 64.5)
small("C10", 83.5, 64.5)
put("SW1", 77, 58, 5.5, 5.5)
put("SW2", 85, 58, 5.5, 5.5)
small("R3", 70.5, 61)
small("C8", 70.5, 57.5)
# ---- USB-C (bottom edge, right)
put("J1", 84, 4.2, 9, 7.5)
put("U4", 84, 13, 3.2, 3)
small("R1", 78.5, 11)
small("R2", 78.5, 14.5)
small("C7", 90, 12)
small("C11", 90, 16)
# ---- PZEM link and field inputs (bottom edge)
put("J6", 46, 4.5, 10.2, 6)
small("R16", 55, 9.5)
small("R4", 59.5, 9.5)
small("C16", 63.5, 12.5)
put("J10", 62, 4, 10.2, 8)
put("J11", 73, 4, 10.2, 8)
# ---- display connectors and headers (top edge and right edge)
put("J9", 96.5, 34, 2.8, 51)
put("J8", 43, 87.5, 10.2, 2.8)
put("J7", 54.5, 87.5, 10.2, 2.8)
put("J12", 68, 87.5, 15.3, 2.8)
put("J13", 84, 87.5, 15.3, 2.8)
put("U6", 87, 46, 9, 6.5)
put("Q3", 90, 36, 3.4, 3)
put("RV2", 89, 27, 7.5, 7)
put("U5", 77.5, 38, 4, 3.4)
small("R12", 62.5, 50)
small("R13", 62.5, 47)
small("R14", 62.5, 44)
small("R15", 62.5, 41)
small("R5", 68.5, 50)
small("R20", 68.5, 47)
small("C12", 68.5, 44)
small("C13", 68.5, 41)
small("C14", 81, 41.2)
small("C19", 91.5, 54)
# ---- buttons, LEDs, buzzer
put("SW3", 56, 30, 5.5, 5.5)
put("SW4", 63, 30, 5.5, 5.5)
put("SW5", 70, 30, 5.5, 5.5)
put("LED1", 57, 35.5, *S603)
small("R8", 61.5, 35.5)
put("LED2", 66, 35.5, *S603)
small("R9", 71, 35.5)
put("BZ1", 71, 13, 8.5, 8.5)
put("Q4", 71, 22, 3.4, 3)
put("D3", 76.5, 23, 5.4, 4.4)
small("R21", 66, 21)
small("R22", 62, 17)
small("R6", 56, 17.5)
small("R7", 56, 14.5)

# off board (listed in the tables, not drawn)
OFFBOARD = {"ANT1": "U.FL pigtail to the module's U.FL connector, SMA bulkhead on the enclosure",
            "ANT2": "2.4 GHz SMA antenna on the outside of the enclosure"}


def check():
    """Return a list of problems: overlaps (>0.2 mm), off-board parts, hole clashes, slot band, mains creepage."""
    prob = []
    items = list(L.items())

    def rect(v):
        x, y, w, h, r = v
        if r in (90, 270):
            w, h = h, w
        return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    rs = {k: rect(v) for k, v in items}
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
    return prob


if __name__ == "__main__":
    pr = check()
    print(len(L), "parts,", len(pr), "problems")
    for p in pr:
        print(" ", p)
