"""BorePilot PCB placement (planning data). Board 100 x 80 mm, origin lower-left, y up, mm.
Each entry: ref -> (x_center, y_center, width, height, rotation). Sizes are footprint estimates,
NOT taken from EasyEDA footprints: compare with the real footprints before routing."""

BOARD_W, BOARD_H = 100.0, 80.0
SLOT = dict(x=28.1, w=1.3, y0=7.0, y1=69.0)          # isolation slot (mains | low voltage)
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, 76.0), (96.0, 76.0)]   # M3, 6.4 mm pads
R1206 = (4.6, 2.6)
S603 = (2.6, 1.6)

L = {}


def put(ref, x, y, w, h, rot=0):
    L[ref] = (x, y, w, h, rot)


def small(ref, x, y, size=R1206, rot=0):
    put(ref, x, y, size[0], size[1], rot)


# ---- mains side (left, x < 28)
put("J2", 13, 74, 10.2, 8)
put("J3", 24, 74, 10.2, 8)
put("U2", 27, 55, 38, 23)
# ---- relays straddle the slot, contact terminals on the left edge
put("K1", 28.75, 33, 19.2, 15.6)
put("K2", 28.75, 14.5, 19.2, 15.6)
put("J4", 5.5, 33, 15.5, 8, 90)
put("J5", 5.5, 15.5, 15.5, 8, 90)
# ---- relay drivers (low-voltage side, right of the relays)
put("Q1", 42, 38.5, 3.4, 3)
put("D1", 42, 34, 5.4, 4.4)
small("R18", 47, 38.5)
small("R10", 47, 34.5)
put("LED3", 51.5, 34.5, *S603)
small("C17", 46.5, 30.5)
put("Q2", 42, 19.5, 3.4, 3)
put("D2", 42, 15, 5.4, 4.4)
small("R19", 47, 19.5)
small("R11", 47, 15.5)
put("LED4", 51.5, 15.5, *S603)
small("C18", 47.5, 10.2)
# ---- power
put("C15", 49, 49, *R1206)
put("D4", 52, 68, 5.4, 4.4)
put("D5", 52, 62.5, 5.4, 4.4)
put("C1", 59.3, 66, 9, 9)
put("U3", 67.3, 65.5, 7, 7)
small("C2", 61.5, 59.5)
small("C3", 69, 59)
small("C5", 50.5, 57)
small("C6", 55.5, 57)
# ---- ESP32 core (top right)
put("U1", 81.5, 66.5, 19.2, 18)
small("C4", 73.5, 54.5)
small("C9", 78.5, 54.5)
small("C10", 83.5, 54.5)
put("SW1", 77, 48, 5.5, 5.5)
put("SW2", 85, 48, 5.5, 5.5)
small("R3", 70.5, 51)
small("C8", 70.5, 47.5)
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
# ---- display connectors
put("J9", 96.5, 34, 2.8, 51)
put("J8", 38, 76, 10.2, 2.8)
put("J7", 50, 76, 10.2, 2.8)
put("J12", 64, 77, 15.3, 2.8)
put("U6", 87, 40, 9, 6.5)
put("Q3", 90, 29, 3.4, 3)
put("RV2", 89, 22.5, 7.5, 7)
put("SJ1", 91, 46.5, 3, 1.6)
put("U5", 77.5, 31, 4, 3.4)
small("R12", 62.5, 44)
small("R13", 62.5, 41)
small("R14", 62.5, 38)
small("R15", 62.5, 35)
small("R5", 68.5, 44)
small("R20", 68.5, 41)
small("C12", 68.5, 38)
small("C13", 68.5, 35)
small("C14", 83, 35)
small("C19", 91, 52)
# ---- buttons, LEDs, buzzer
put("SW3", 56, 26, 5.5, 5.5)
put("SW4", 63, 26, 5.5, 5.5)
put("SW5", 70, 26, 5.5, 5.5)
put("LED1", 57, 31.5, *S603)
small("R8", 61.5, 31.5)
put("LED2", 66, 31.5, *S603)
small("R9", 71, 31.5)
put("BZ1", 71, 13, 9, 9)
put("Q4", 71, 20.5, 3.4, 3)
put("D3", 76.5, 21.5, 5.4, 4.4)
small("R21", 66, 19.5)
small("R6", 56, 17)
small("R7", 56, 14)

# off board (listed in the tables, not drawn)
OFFBOARD = {"ANT1": "U.FL pigtail to the module's U.FL connector, SMA bulkhead on the enclosure",
            "ANT2": "2.4 GHz SMA antenna on the outside of the enclosure"}


def check():
    """Return a list of problems: overlaps (>0.2 mm), off-board parts, hole clashes."""
    prob = []
    items = list(L.items())
    def rect(v):
        x, y, w, h, r = v
        if r in (90, 270):
            w, h = h, w
        return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    rs = {k: rect(v) for k, v in items}
    keys = list(rs)
    for i in range(len(keys)):
        a = rs[keys[i]]
        if a[0] < 0.5 or a[1] < -0.01 or a[2] > BOARD_W - 0.5 or a[3] > BOARD_H - 0.5:
            if not (keys[i] in ("J1", "J10", "J11", "J6", "J2", "J3", "J7", "J8", "J12", "J4", "J5", "J9") and a[0] > -0.01 and a[1] > -0.01 and a[2] < BOARD_W + 0.01 and a[3] < BOARD_H + 0.01):
                prob.append(f"{keys[i]} outside board {tuple(round(t,1) for t in a)}")
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
    # isolation: low-voltage parts must not touch the slot band, mains parts stay left
    sx0, sx1 = SLOT["x"] - 3.2, SLOT["x"] + SLOT["w"] + 3.2
    mains = {"J2", "J3", "J4", "J5", "U2", "K1", "K2"}
    for k, a in rs.items():
        if k in mains:
            continue
        if SLOT["y0"] - 3 < (a[1] + a[3]) / 2 < SLOT["y1"] + 3 and a[0] < sx1 and a[2] > sx0:
            prob.append(f"{k} inside the 3.2 mm band around the slot")
    return prob


if __name__ == "__main__":
    pr = check()
    print(len(L), "parts,", len(pr), "problems")
    for p in pr:
        print(" ", p)
