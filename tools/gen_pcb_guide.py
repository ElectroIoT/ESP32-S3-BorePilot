"""Generate docs/pcb-section-guide.html and docs/images/pcb-floorplan.svg (+png) for BorePilot.
Run from the repo root:  python -X utf8 -I tools/gen_pcb_guide.py
Placement data: tools/pcb_layout.py (estimates; footprints must be checked in EasyEDA).
One silkscreen box per functional block (relay 1, relay 2, power, ESP32, ...)."""
import os, sys, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages as G
import pcb_layout as PL

e = html.escape
ROOT = G.ROOT
BW, BH = PL.BOARD_W, PL.BOARD_H
REF_NAME = {p[1]: p[2] for p in G.P}
REF_C = {p[1]: p[3] for p in G.P}
BLK = {b[0]: b for b in PL.BLOCKS}
REF_BLK = PL.REF_BLOCK
FG, BD, LN = "var(--fg)", "var(--board)", "var(--line)"

NOTES = {
 "mains_in": ["AC IN (J2) and AC TAP (J3) sit on the top edge, cables enter from the top. Everything here is 230 V: keep 6.4 mm (8 mm better) to any low-voltage copper and 2 mm to the board edge.",
              "Silkscreen: draw the box with a thick line, add the text MAINS 230 V and L / N next to each terminal pin."],
 "power": ["U2 (HLK-5M05, 38 x 23 mm) lies across the shortened main slot (x 28.1 to 29.4, y 51 to 77 mm): AC pins at the left end, 5 V pins at the right end. Pin pitch checked against the datasheet (6 mm, 18 mm, 33.6 mm).",
           "D4, D5 and C1 go right next to the HLK +5V pin; U3 and its capacitors beside them. C15 across the HLK output pins."],
 "relay1": ["K1 turned 270 degrees at (17.5, 27): COM and the coil pins face up, NO / NC face down. J4 (3-way, pins NO / COM / NC) sits below the relay; two 8 x 1 mm slots between COM and the coil pins (see footprint-placement.html).",
            "Q1, D1, R18, R10, LED3, C17 sit just right of the relay. Contact tracks 1.5 mm, short, never within 6.4 mm of low-voltage copper."],
 "relay2": ["Same as relay 1, one box below it. J5 is on the left edge, cable entry to the left.", "Keep the two relay boxes identical so the second channel can be copied from the first."],
 "esp32": ["U1 at the top right: no PCB antenna, so keep the U.FL connector near the top edge and nothing tall next to it.",
           "C4, C9, C10 directly at the module's 3V3 pin side; SW1 / SW2 within reach of a finger. J13 (UART / boot header) on the top edge, not fitted by default."],
 "disp_hdr": ["J8 (OLED) and J7 (16x2) on the top edge, U5 (PCA9306) and its resistors and capacitors right below them so the I2C lines stay short.",
              "R14 / R15 are fitted only if the LCD backpack has no pull-ups."],
 "lcd_drv": ["U6, Q3, RV2 (contrast trimmer) and the passives between the ESP32 and the J9 header. RV2 stays reachable with a small screwdriver.",
             "C14 right next to U6 pin 14; C19 near the J9 +5V pin."],
 "lcd_con": ["J9 (1x20) runs down the right edge so the 12864 plugs in or cables out at the edge."],
 "spare": ["J12: 3V3, GND and four spare GPIOs, on the right edge."],
 "ui": ["Buttons SW3 to SW5 in a row, LEDs behind them. Buzzer parts BZ1, R22, Q4, D3, R21 are optional: keep the pads, fit them only if you want the buzzer.",
        "R22 (10 ohm) limits the buzzer to about 3.1 V."],
 "usb": ["J1 on the bottom edge, shield tabs to the edge. Route D+ / D- as a pair, short, 90 ohm if the stack allows, straight through U4 to the ESP32.", "R1 / R2 (5.1 k) right at the J1 CC pins."],
 "pzem": ["J6 on the bottom edge; R16 / R4 divider and C16 to its left.", "Mains does not reach this block: the PZEM module has its own mains terminals (fed from J3)."],
 "inputs": ["J10 / J11 screw terminals on the bottom edge, with their optional pull-ups R6 / R7 just above."],
}
NETS = [
 ("L, N (mains)", "1.0 mm min", "Mains conductors: spacing and slot matter more than width. Keep short; 1 oz copper."),
 ("Relay contacts COMn / NOn / NCn", "1.5 mm", "Control-circuit currents only (contactor coil). Run only below the relay (J4 / J5)."),
 ("+5V_HLK, +5V", "0.8 mm", "Peak about 0.75 A in the plan; 0.8 mm on 1 oz is comfortable."),
 ("+3V3", "0.6 mm", "ESP32 bursts to about 0.45 A."),
 ("GND", "pour on both layers", "Low-voltage side only. No pour on the mains side or across the slot."),
 ("Relay coil nodes RLYn_D", "0.5 mm", "About 72 mA each."),
 ("USB_DP / USB_DN", "0.2 mm pair, 90 ohm diff", "Keep short, no stubs; U4 close to J1."),
 ("PZEM_TXD / PZEM_RXD, SDA, SCL, LCD_*, BTN_*, IN1/IN2, BUZZ, LED_ST", "0.25 mm", "Plain signals."),
 ("Isolation slot", "1.3 mm wide", "Routed slot, HLK area only (y 51 to 77 mm); its ends reach 3.2 mm past the nearest mains copper so the creepage path around it stays above 6.4 mm. Relays have their own slots."),
]
STEPS = [
 "In EasyEDA PCB the board outline (100 x 90 mm, 3 mm corners), the isolation slot and the four 3.2 mm mounting holes (4, 4), (96, 4), (4, 86), (96, 86) mm already exist.",
 "Import the schematic (Design > Update/Convert Schematic to PCB). Check every footprint against its datasheet first: J1 USB-C, K1/K2 relays, U2 HLK, KF128 terminals, J9 1x20.",
 "Place block by block with the X / Y tables: mains in, power, relay 1, relay 2, ESP32, displays, USB, PZEM, inputs, buttons. Tick each part here.",
 "Draw one rectangle per block on the Top Silkscreen layer with the block title (dashed boxes in the floor plan). Keep the box edges 1 mm off the pads; the silkscreen is removed from pads anyway.",
 "Draw the net classes from the table above (widths and the USB pair), then pour GND on the low-voltage side only.",
 "Route mains and relay contacts first, then 5 V and 3.3 V, then USB, then the rest by hand.",
 "Run the PCB DRC with a 6.4 mm clearance rule between the mains and low-voltage net classes. Add silkscreen: MAINS WARNING, COM / NO / NC labels, J2 L and N, pin 1 marks.",
 "Export Gerber and have the PCB maker check the slot and the 6.4 mm spacing. No mains power before the engineer review (PLAN.md section 14).",
]


def part_svg(ref, dim=False, fs=None):
    x, y, w, h, r = PL.L[ref]
    if r in (90, 270):
        w, h = h, w
    col = BLK[REF_BLK[ref]][2]
    op = ".22" if dim else "1"
    f = fs or (1.7 if min(w, h) > 3.2 else 1.25)
    rot = f' transform="rotate(-90 {x:.2f} {-y:.2f})"' if h > 1.6 * w and h > 9 else ""
    t = f'<text x="{x:.2f}" y="{-y + f/3:.2f}" text-anchor="middle" font-size="{f}" font-weight="700" fill="{FG}"{rot} style="pointer-events:none">{e(ref)}</text>'
    return (f'<g class="pt" data-ref="{ref}" opacity="{op}"><title>{e(ref)}: {e(REF_NAME[ref])} [{e(REF_C[ref])}]  x={x:.1f} y={y:.1f} mm</title>'
            f'<rect x="{x-w/2:.2f}" y="{-(y+h/2):.2f}" width="{w:.2f}" height="{h:.2f}" rx="0.3" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="0.22"/>{t}</g>')


def board_inner(view_full, active=None, standalone=False):
    fg = "#1c2330" if standalone else FG
    bd = "#e8efe4" if standalone else BD
    ln_ = "#c9d1dc" if standalone else LN
    o = [f'<rect x="0" y="{-BH}" width="{BW}" height="{BH}" rx="3" fill="{bd}" stroke="{fg}" stroke-width="0.35"/>']
    for gx in range(10, int(BW), 10):
        o.append(f'<line x1="{gx}" y1="{-BH}" x2="{gx}" y2="0" stroke="{ln_}" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if view_full:
            o.append(f'<text x="{gx}" y="{-BH-0.8}" text-anchor="middle" font-size="1.4" fill="#5b6677">{gx}</text>')
    for gy in range(10, int(BH), 10):
        o.append(f'<line x1="0" y1="{-gy}" x2="{BW}" y2="{-gy}" stroke="{ln_}" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if view_full:
            o.append(f'<text x="-0.8" y="{-gy+0.5}" text-anchor="end" font-size="1.4" fill="#5b6677">{gy}</text>')
    zx = PL.SLOT["x"]
    o.append(f'<rect x="0.15" y="{-BH+0.15}" width="{zx-0.15:.2f}" height="{BH-0.3}" fill="#e53935" fill-opacity=".07"/>')
    s = PL.SLOT
    o.append(f'<rect x="{s["x"]}" y="{-s["y1"]}" width="{s["w"]}" height="{s["y1"]-s["y0"]}" rx="0.65" fill="#b71c1c"/>')
    for (hx, hy) in PL.HOLES:
        o.append(f'<circle cx="{hx}" cy="{-hy}" r="3.2" fill="none" stroke="#9aa5b5" stroke-width="0.2" stroke-dasharray="0.6 0.4"/><circle cx="{hx}" cy="{-hy}" r="1.6" fill="{bd}" stroke="#9aa5b5" stroke-width="0.2"/>')
    for b in PL.BLOCKS:
        bx = PL.box_of(b[0])
        dim = active is not None and b[0] != active
        narrow = (bx[2] - bx[0]) < 8
        tw = len(b[1]) * 0.95 + 1.2
        if narrow:
            tx, ty = max(min(bx[2] - tw, BW - tw - 0.6), 0.6), -bx[3] - 0.9
            chip = f'<rect x="{tx-0.3:.2f}" y="{ty-1.15:.2f}" width="{tw:.2f}" height="1.6" fill="{bd}"/>'
            txt = f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="1.35" font-weight="700" fill="{b[2]}">{e(b[1])}</text>'
        else:
            tx, ty = bx[0] + 1.6, -bx[3] + 0.5
            chip = f'<rect x="{tx-0.5:.2f}" y="{ty-1.15:.2f}" width="{tw:.2f}" height="1.6" fill="{bd}"/>'
            txt = f'<text x="{tx:.2f}" y="{ty:.2f}" font-size="1.4" font-weight="700" fill="{b[2]}">{e(b[1])}</text>'
        o.append(f'<g opacity="{".35" if dim else "1"}"><rect x="{bx[0]:.2f}" y="{-bx[3]:.2f}" width="{bx[2]-bx[0]:.2f}" height="{bx[3]-bx[1]:.2f}" rx="0.6" fill="none" stroke="{b[2]}" stroke-width="0.28" stroke-dasharray="1.2 0.7"/>{chip}{txt}</g>')
    for ref in PL.L:
        o.append(part_svg(ref, dim=(active is not None and REF_BLK[ref] != active)))
    if view_full:
        o.append(f'<text x="{BW/2}" y="2.8" text-anchor="middle" font-size="1.5" font-weight="700" fill="#2fbf71">MAINS ZONE 230 V is left of the red slot and in the relay terminal strip | LOW VOLTAGE (isolated 5 V / 3.3 V) on the right</text>')
    return "".join(o)


def board_svg(view=None, active=None, width_px=760):
    vx0, vy0, vx1, vy1 = view or (-3, -3, BW + 3, BH + 3)
    w, h = vx1 - vx0, vy1 - vy0
    return (f'<svg viewBox="{vx0:.2f} {-vy1:.2f} {w:.2f} {h:.2f}" width="{width_px:.0f}" height="{width_px*h/w:.0f}" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">'
            + board_inner(view is None, active) + "</svg>")


CSS = """:root{--bg:#f3f1fb;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#c9d1dc;--board:#e8efe4;--acc:#2a6fd6}
@media (prefers-color-scheme:dark){:root{--bg:#0d1017;--fg:#e8ebf2;--mut:#9aa5b5;--card:#171c26;--line:#323b49;--board:#1c2a20;--acc:#6aa3ff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}main{max-width:1320px;margin:0 auto;padding:16px 16px 56px}
.hero{border-radius:16px;padding:18px 22px;color:#fff;background:linear-gradient(120deg,#ff4d4d,#ff9f43 25%,#2fbf71 50%,#4895ef 75%,#a66cff);box-shadow:0 6px 20px rgba(0,0,0,.18)}
.hero h1{margin:0;font-size:1.5rem;text-shadow:0 1px 3px rgba(0,0,0,.35)}.hero p{margin:6px 0 0;font-size:14px;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.warn{background:var(--card);border-left:5px solid #ff4d4d;border-radius:8px;padding:8px 12px;margin:14px 0;font-size:13px}
h2{font-size:1.15rem;margin:0 0 8px}h3{font-size:1rem;margin:14px 0 6px}.mut{color:var(--mut);font-size:13px}.cnt{font-weight:400;font-size:13px;color:var(--mut);margin-left:8px}
.card{background:var(--card);border-radius:14px;padding:14px;margin:14px 0;border-left:8px solid var(--c,#607d8b);box-shadow:0 2px 10px rgba(0,0,0,.08)}.card h2{color:var(--c,var(--fg))}
.scroll{overflow-x:auto}nav{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
nav a{padding:4px 10px;border-radius:14px;color:#fff;text-decoration:none;font-size:12px;font-weight:700}.bar{height:8px;background:var(--line);border-radius:5px;overflow:hidden;min-width:140px}.bar div{height:100%;background:#2fbf71;width:0}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--mut);font-weight:600;white-space:nowrap}
td.num{text-align:right;font-variant-numeric:tabular-nums}tr.ok td{opacity:.42;text-decoration:line-through}input.ck{width:18px;height:18px}
svg.plan{max-width:100%;height:auto}.pt{cursor:pointer}.pt.ok rect{fill-opacity:.1;stroke-dasharray:.6 .6}.pt.ok text{opacity:.4}
.rec{border-left:4px solid #2fbf71;padding:6px 12px;background:rgba(47,191,113,.1);border-radius:6px;margin:8px 0}
button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:5px 12px;cursor:pointer}ul.rules li,ol.steps li{margin:5px 0}"""


def parts_table(block):
    refs = sorted(block[3], key=lambda r: (r[0] != "U", r[0] != "K", r[0] != "J", r[0], int("".join(c for c in r if c.isdigit()) or 0)))
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>LCSC</th><th>X mm</th><th>Y mm</th><th>Rot</th><th>Size mm (est.)</th></tr></thead><tbody>'
    for r in refs:
        x, y, w, h, rot = PL.L[r]
        t += (f'<tr data-ref="{r}"><td><input type="checkbox" class="ck" data-k="{r}"></td><td><b>{r}</b></td><td>{e(REF_NAME[r])}</td><td>{e(REF_C[r])}</td>'
              f'<td class="num">{x:.1f}</td><td class="num">{y:.1f}</td><td class="num">{rot}&deg;</td><td>{w:.1f} x {h:.1f}</td></tr>')
    return t + "</tbody></table></div>"


def crop_of(block_id):
    bx = PL.box_of(block_id)
    return (max(bx[0] - 3, -2), max(bx[1] - 3, -2), min(bx[2] + 3, BW + 2), min(bx[3] + 3, BH + 2))


def build():
    total = len(PL.L)
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot PCB Layout Guide</title><style>{CSS}</style></head><body><main>']
    o.append('<div class="hero"><h1>BorePilot - PCB layout guide by block</h1><p>100 x 90 mm, 2 layers. Every functional block (relay 1, relay 2, power, ESP32 ...) has its own zoomed drawing, a table of X / Y in mm (origin = lower-left corner, y up), a tick box per part and its own dashed silkscreen box. Click a part in a drawing or tick it in the table: both stay in sync and are saved in this browser.</p></div>')
    o.append('<div class="warn"><b>Plan stage, not a finished layout.</b> Positions and sizes are estimates for a first placement. The checker found no overlaps, no clash with the mounting holes or the slot band, 6.4 mm or more from low-voltage parts to the AC terminals, and no part or other box inside any silkscreen box. The real EasyEDA footprints will differ: compare the courtyards, then adjust. Mains is on the left of the slot: engineer review before any mains power.</div>')
    o.append('<nav><a style="background:#607d8b" href="#size">Board size</a><a style="background:#607d8b" href="#silk">Silkscreen boxes</a><a style="background:#607d8b" href="#plan">Floor plan</a>' + "".join(f'<a style="background:{b[2]}" href="#{b[0]}">{e(b[1])}</a>' for b in PL.BLOCKS) + f'<a style="background:#607d8b" href="#nets">Nets</a><a style="background:#607d8b" href="#steps">Steps</a><span class="mut">placed <b id="tot">0</b> / {total}</span><div class="bar"><div id="barfill"></div></div><button id="reset">Reset ticks</button></nav>')
    used = sum(w * h for (x, y, w, h, r) in PL.L.values())
    o.append('<section class="card" id="size"><h2>Best board size</h2>')
    o.append(f'<div class="rec"><b>Selected: 100 x 90 mm, 2 layers, 1.6 mm FR-4, 1 oz copper.</b> The footprints add up to about {used:.0f} mm&sup2; of the 9000 mm&sup2; board ({used/90:.0f} %), but the real constraint is the shape: the HLK module is 38 x 23 mm, the 1x20 display header is 51 mm long, the two relays need 19 mm each, and the left column needs a 6.4 mm slot. 100 x 100 mm or smaller was the limit set by the owner: 100 x 90 mm stays inside it and in the cheapest PCB price tier. A 100 x 80 mm board no longer fits once the J13 UART header, the 6.4 mm clearance to the AC terminals and the 51 mm display header are all kept.</div>')
    o.append('<h3>Board outline, mounting holes and slot (already in EasyEDA)</h3><div class="scroll"><table><thead><tr><th>Item</th><th>X mm</th><th>Y mm</th><th>Size</th><th>Net</th></tr></thead><tbody>')
    o.append('<tr><td>Board outline</td><td class="num">0 - 100</td><td class="num">0 - 90</td><td>100 x 90, corner radius 3 mm</td><td>-</td></tr>')
    for i, (hx, hy) in enumerate(PL.HOLES, 1):
        o.append(f'<tr><td>MH{i} M3 mounting hole</td><td class="num">{hx:.1f}</td><td class="num">{hy:.1f}</td><td>3.2 mm, non-plated, no copper pad</td><td>none (no pad, keeps the mains side clean)</td></tr>')
    o.append(f'<tr><td>Isolation slot</td><td class="num">{PL.SLOT["x"]:.1f} - {PL.SLOT["x"]+PL.SLOT["w"]:.1f}</td><td class="num">{PL.SLOT["y0"]:.0f} - {PL.SLOT["y1"]:.0f}</td><td>{PL.SLOT["w"]} mm wide, routed</td><td>none</td></tr></tbody></table></div>')
    o.append('<h3>Edge plan</h3><ul class="rules"><li><b>Top edge:</b> J2 and J3 (mains, left), J8 (OLED) and J7 (16x2), J13 (UART / boot header), U.FL end of the ESP32 module.</li><li><b>Left edge:</b> J4 and J5 relay terminals (COM / NO / NC).</li><li><b>Bottom edge:</b> J6 (PZEM), J10 and J11 (float inputs), J1 (USB-C).</li><li><b>Right edge:</b> J9 (12864 LCD, 1x20) and J12 (spare).</li></ul>')
    o.append('<p class="mut">Not on the board: ANT1 (U.FL to SMA pigtail) and ANT2 (SMA antenna). The ESP32 module has no PCB antenna; the pigtail goes to a bulkhead outside the enclosure.</p></section>')
    o.append('<section class="card" id="silk" style="--c:#f4c20d"><h2>Silkscreen box per block: a good idea</h2><ul class="rules">'
             '<li><b>Why it helps:</b> you see at a glance which parts belong to relay 1, relay 2, power or the ESP32, which makes assembly, probing and fault finding much easier.</li>'
             '<li><b>The mains boxes are a safety aid:</b> draw MAINS IN and POWER with a thicker line and a MAINS 230 V title so nobody probes them by accident.</li>'
             '<li><b>Rules:</b> use the Top Silkscreen layer; keep box lines 1 mm from pads (the fab removes silkscreen on pads anyway); never draw a box line across the isolation slot or a mounting hole; keep titles at least 0.8 mm high.</li>'
             '<li><b>This plan:</b> 13 dashed boxes, one per block. The checker confirms no box overlaps another and no foreign part sits inside a box.</li>'
             '<li><b>In EasyEDA:</b> place each block as a group, then draw its rectangle and title on the Top Silkscreen layer.</li></ul></section>')
    o.append('<section class="card" id="plan"><h2>Floor plan: 100 x 90 mm<span class="cnt">dashed boxes = silkscreen boxes; click a part to tick it</span></h2><div class="scroll">' + board_svg() + '</div></section>')
    for b in PL.BLOCKS:
        bx = PL.box_of(b[0])
        wpx = int(min(900, max(520, (bx[2] - bx[0] + 6) * 14)))
        o.append(f'<section class="card" id="{b[0]}" style="--c:{b[2]}"><h2>{e(b[1])}<span class="cnt"><span class="done">0</span> / {len(b[3])} placed &middot; silkscreen box x {bx[0]:.1f} to {bx[2]:.1f}, y {bx[1]:.1f} to {bx[3]:.1f} mm</span></h2><ul class="rules">' + "".join(f"<li>{e(t)}</li>" for t in NOTES[b[0]]) + f'</ul><div class="scroll">{board_svg(view=crop_of(b[0]), active=b[0], width_px=wpx)}</div>{parts_table(b)}</section>')
    o.append('<section class="card" id="nets"><h2>Nets and trace widths<span class="cnt">1 oz copper, IPC-2221 external layer, with margin</span></h2><div class="scroll"><table><thead><tr><th>Net</th><th>Width</th><th>Notes</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in NETS) + '</tbody></table></div></section>')
    o.append('<section class="card" id="steps"><h2>Order of work</h2><ol class="steps">' + "".join(f"<li>{e(t)}</li>" for t in STEPS) + '</ol></section>')
    o.append("""<script>
const K='borepilot-pcb-ticks2';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){const total=document.querySelectorAll('#plan .pt').length;
 document.querySelectorAll('.pt').forEach(g=>g.classList.toggle('ok',!!st[g.dataset.ref]));
 document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
 const n=Object.keys(st).length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/total)+'%';
 document.querySelectorAll('section.card[id]').forEach(sec=>{const rows=sec.querySelectorAll('tr[data-ref]');if(!rows.length)return;const d=[...rows].filter(r=>st[r.dataset.ref]).length;const c=sec.querySelector('.done');if(c)c.textContent=d});
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function tog(r){if(st[r])delete st[r];else st[r]=1;apply()}
document.querySelectorAll('.pt').forEach(g=>g.addEventListener('click',()=>tog(g.dataset.ref)));
document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>tog(c.dataset.k)));
document.getElementById('reset').onclick=()=>{st={};apply()};apply();
</script></main></body></html>""")
    return "".join(o)


def standalone_svg():
    inner = board_inner(True, standalone=True).replace("var(--fg)", "#1c2330")
    leg = "".join(f'<rect x="{-3 + (i % 5) * 21}" y="{4.6 + (i // 5) * 2.6:.1f}" width="1.6" height="1.6" fill="{b[2]}"/><text x="{-3 + (i % 5) * 21 + 2.2}" y="{5.9 + (i // 5) * 2.6:.1f}" font-size="1.35" fill="#1c2330">{e(b[1])}</text>' for i, b in enumerate(PL.BLOCKS))
    title = '<text x="-2" y="-92.5" font-size="2" font-weight="700" fill="#1c2330">BorePilot PCB floor plan - 100 x 90 mm, 2 layers, one silkscreen box per block (planning estimate)</text>'
    vh = BH + 19
    return (f'<svg viewBox="-3 -95 {BW+6} {vh}" width="1000" height="{1000*vh/(BW+6):.0f}" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">'
            f'<rect x="-3" y="-95" width="{BW+6}" height="{vh}" fill="#ffffff"/>{title}{inner}{leg}</svg>')


os.makedirs(os.path.join(ROOT, "docs/images"), exist_ok=True)
open(os.path.join(ROOT, "docs/pcb-section-guide.html"), "w", encoding="utf-8").write(build())
open(os.path.join(ROOT, "docs/images/pcb-floorplan.svg"), "w", encoding="utf-8").write(standalone_svg())
print("parts", len(PL.L), "pcb guide written")
