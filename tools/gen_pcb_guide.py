"""Generate docs/pcb-section-guide.html and docs/images/pcb-floorplan.svg (+png) for BorePilot.
Run from the repo root:  python -I tools/gen_pcb_guide.py
Placement data: tools/pcb_layout.py (estimates; footprints must be checked in EasyEDA)."""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages as G
import pcb_layout as PL

e = html.escape
ROOT = G.ROOT
SC = 7.2            # px per mm
M = 24              # margin px
BW, BH = PL.BOARD_W, PL.BOARD_H
VW, VH = BW * SC + 2 * M, BH * SC + 2 * M + 8

SEC = {s[0]: s for s in G.S}
REF_SEC = {p[1]: p[0] for p in G.P}
REF_NAME = {p[1]: p[2] for p in G.P}
REF_C = {p[1]: p[3] for p in G.P}
REF_SEC["SJ1"] = "disp"
REF_NAME["SJ1"] = "Solder jumper (PSB to GND, default bridged) - removed: PSB is wired to GND in the schematic"
REF_C["SJ1"] = "-"

ORDER = ["mains", "power", "usb", "mcu", "relay", "pzem", "disp", "ui"]
SEC_TITLE = {"mains": "Mains input 230 V", "power": "5 V / 3.3 V power", "usb": "USB-C programming", "mcu": "ESP32-S3 core",
             "relay": "Relays and mains contacts", "pzem": "PZEM-004T link", "disp": "Display options", "ui": "Buttons, LEDs, inputs"}

LABELS = {"J2": "AC IN", "J3": "AC TAP", "J4": "RELAY 1 COM/NO/NC", "J5": "RELAY 2 COM/NO/NC", "J1": "USB-C", "J6": "PZEM",
          "J10": "FLOAT 1", "J11": "FLOAT 2", "J9": "12864 LCD", "J7": "16x2", "J8": "OLED", "J12": "SPARE", "U2": "HLK-5M05", "U1": "ESP32-S3 (U.FL)"}


def X(x): return M + x * SC
def Y(y): return M + (BH - y) * SC


def rect_of(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return x, y, w, h


def board_svg(active=None, interactive=True, standalone=False):
    o = [f'<svg viewBox="0 0 {VW:.0f} {VH:.0f}" width="{VW:.0f}" height="{VH:.0f}" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">']
    fg = "#1c2330" if standalone else "var(--fg)"
    bd = "#e8efe4" if standalone else "var(--board)"
    ln_ = "#c9d1dc" if standalone else "var(--line)"
    o.append(f'<rect x="{M}" y="{M}" width="{BW*SC:.0f}" height="{BH*SC:.0f}" rx="22" fill="{bd}" stroke="{fg}" stroke-width="2"/>')
    # grid
    for gx in range(10, int(BW), 10):
        o.append(f'<line x1="{X(gx):.1f}" y1="{M}" x2="{X(gx):.1f}" y2="{M+BH*SC:.0f}" stroke="{ln_}" stroke-width=".5" stroke-dasharray="2 4"/><text x="{X(gx):.1f}" y="{M-8}" text-anchor="middle" font-size="9" fill="#5b6677">{gx}</text>')
    for gy in range(10, int(BH), 10):
        o.append(f'<line x1="{M}" y1="{Y(gy):.1f}" x2="{M+BW*SC:.0f}" y2="{Y(gy):.1f}" stroke="{ln_}" stroke-width=".5" stroke-dasharray="2 4"/><text x="{M-8}" y="{Y(gy)+3:.1f}" text-anchor="end" font-size="9" fill="#5b6677">{gy}</text>')
    # mains zone tint
    zx = PL.SLOT["x"]
    o.append(f'<rect x="{M+1}" y="{M+1}" width="{zx*SC-1:.0f}" height="{BH*SC-2:.0f}" rx="21" fill="#e53935" fill-opacity=".07"/>')
    o.append(f'<text x="{X(zx/2):.0f}" y="{M+BH*SC+40:.0f}" text-anchor="middle" font-size="10" font-weight="700" fill="#e53935">MAINS ZONE 230 V</text>')
    o.append(f'<text x="{X((zx+BW)/2):.0f}" y="{M+BH*SC+40:.0f}" text-anchor="middle" font-size="10" font-weight="700" fill="#2fbf71">LOW VOLTAGE ZONE (isolated 5 V / 3.3 V)</text>')
    s = PL.SLOT
    o.append(f'<rect x="{X(s["x"]):.1f}" y="{Y(s["y1"]):.1f}" width="{s["w"]*SC:.1f}" height="{(s["y1"]-s["y0"])*SC:.1f}" fill="#b71c1c" stroke="#b71c1c"/>')
    o.append(f'<text x="{X(s["x"]+s["w"]/2):.1f}" y="{Y(s["y0"]-2):.1f}" text-anchor="middle" font-size="8" fill="#b71c1c">SLOT 1.3 mm</text>')
    # holes
    for (hx, hy) in PL.HOLES:
        o.append(f'<circle cx="{X(hx):.1f}" cy="{Y(hy):.1f}" r="{3.2*SC:.1f}" fill="none" stroke="#9aa5b5" stroke-width="1.5" stroke-dasharray="3 2"/><circle cx="{X(hx):.1f}" cy="{Y(hy):.1f}" r="{1.6*SC:.1f}" fill="{bd}" stroke="#9aa5b5"/>')
    # parts
    for ref, v in PL.L.items():
        x, y, w, h = rect_of(v)
        sec = REF_SEC.get(ref, "ui")
        col = SEC[sec][2]
        dim = active is not None and sec != active
        op = ".25" if dim else "1"
        fs = 9 if min(w, h) * SC > 22 else 7
        label = ref if (w * SC > len(ref) * 5.5 or h * SC > 20) else ref
        rot = ' transform="rotate(-90 %.1f %.1f)"' % (X(x), Y(y)) if h > 1.6 * w and h * SC > 40 else ""
        o.append(f'<g class="pt" data-ref="{ref}" opacity="{op}"><title>{e(ref)}: {e(REF_NAME[ref])} [{e(REF_C[ref])}]  x={x:.1f} y={y:.1f} mm</title>'
                 f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*SC:.1f}" height="{h*SC:.1f}" rx="2" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="1.6"/>'
                 f'<text x="{X(x):.1f}" y="{Y(y)+fs/3:.1f}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{fg}"{rot}>{e(label)}</text></g>')
    # connector captions
    for ref, cap in LABELS.items():
        if ref not in PL.L or (active is not None and REF_SEC.get(ref) != active):
            continue
        x, y, w, h = rect_of(PL.L[ref])
        ty = Y(y - h / 2) + 11
        if ref in ("J9",):
            o.append(f'<text x="{X(x)-14:.1f}" y="{Y(y):.1f}" text-anchor="end" font-size="9" fill="{fg}">{cap}</text>')
        elif ref in ("J4", "J5"):
            o.append(f'<text x="{X(x+w/2)+4:.1f}" y="{Y(y-h/2)+2:.1f}" font-size="8" fill="{fg}">{cap}</text>')
        elif ref in ("U1",):
            o.append(f'<text x="{X(x):.1f}" y="{Y(y)+18:.1f}" text-anchor="middle" font-size="8" fill="{fg}">U.FL connector: antenna edge up</text>')
        else:
            o.append(f'<text x="{X(x):.1f}" y="{ty:.1f}" text-anchor="middle" font-size="8" fill="{fg}">{cap}</text>')
    o.append("</svg>")
    return "".join(o)


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
svg.plan{max-width:100%;height:auto}svg text{pointer-events:none}.pt{cursor:pointer}.pt.ok rect{fill-opacity:.1;stroke-dasharray:2 3}.pt.ok text{opacity:.4}
.rec{border-left:4px solid #2fbf71;padding:6px 12px;background:rgba(47,191,113,.1);border-radius:6px;margin:8px 0}.legend span{display:inline-block;margin-right:12px;font-size:12px;color:var(--mut)}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:middle}
button{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:5px 12px;cursor:pointer}ul.rules li,ol.steps li{margin:5px 0}.tag{display:inline-block;background:#ff9f43;color:#10151c;border-radius:4px;padding:0 6px;font-size:11px;font-weight:700}"""


def parts_table(sec):
    refs = [r for r in PL.L if REF_SEC.get(r) == sec]
    refs.sort(key=lambda r: (r[0] != "U", r[0] != "J", r[0], int("".join(c for c in r if c.isdigit()) or 0)))
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>LCSC</th><th>X mm</th><th>Y mm</th><th>Rot</th><th>Size mm (est.)</th></tr></thead><tbody>'
    for r in refs:
        x, y, w, h, rot = PL.L[r]
        t += (f'<tr data-ref="{r}"><td><input type="checkbox" class="ck" data-k="{r}"></td><td><b>{r}</b></td><td>{e(REF_NAME[r])}</td><td>{e(REF_C[r])}</td>'
              f'<td class="num">{x:.1f}</td><td class="num">{y:.1f}</td><td class="num">{rot}&deg;</td><td>{w:.1f} x {h:.1f}</td></tr>')
    return t + "</tbody></table></div>", len(refs)


SEC_NOTES = {
 "mains": ["Mains parts stay left of the red slot. J2 and J3 sit on the top edge so the cables enter from the top.",
           "U2 (HLK-5M05, 38 x 23 mm) lies across the slot: AC pins on the left end, 5 V pins on the right end. Check the real pin pitch on the HLK drawing before routing the slot.",
           "Keep 6.4 mm (8 mm better) between any mains copper and low-voltage copper, 2 mm from mains copper to the board edge. No pour or vias across the slot."],
 "power": ["Put D4, D5 and C1 right next to the HLK +5V pin so the 5 V path is short. U3 and its caps sit beside C1.", "C15 100 nF goes directly across the HLK output pins."],
 "usb": ["J1 sits on the bottom edge, shield tabs to the board edge. Route D+ / D- as a pair, short, 90 ohm if the fab stack allows, straight through U4 to the ESP32.", "R1 / R2 (5.1 k) right at the J1 CC pins."],
 "mcu": ["J13 (UART / boot header) sits on the top edge next to J12: unpopulated by default.", "U1 at the top right. The module has a U.FL connector, so no PCB antenna and no overhang is needed: keep the U.FL connector near the top edge and nothing tall right next to it.", "Decoupling caps C4, C9, C10 directly under the module's 3V3 pin side; SW1 / SW2 within reach of a finger on the edge."],
 "relay": ["K1 and K2 straddle the slot: contact pins on the mains side (left), coil pins on the low-voltage side (right).", "Q1, Q2, D1, D2 and the LED parts sit just right of each relay. J4 and J5 are on the left edge, cable entry to the left.", "Contact tracks: 1.5 mm and short; they must never come within 6.4 mm of low-voltage copper."],
 "pzem": ["J6 on the bottom edge. R16 / R4 divider next to the header.", "Mains does not reach this section: the PZEM module has its own mains terminals (fed from J3)."],
 "disp": ["J9 (1x20) runs down the right edge so the 12864 plugs in or cables out at the edge. J7 / J8 are on the top edge.", "U6, Q3, RV2 and the passives cluster between J9 and the ESP32. U5 (PCA9306) is near J7/J8 and the I2C lines."],
 "ui": ["Buttons SW3 to SW5 in a row, LEDs behind them. J10 / J11 (float inputs) on the bottom edge. J12 spare header on the top edge.", "BZ1, Q4, D3, R21 are optional: leave the pads, fit them only if you want the buzzer."],
}

NETS = [
 ("L, N (mains)", "1.0 mm min", "Mains conductors: spacing and slot matter more than width. Keep short; 1 oz copper."),
 ("Relay contacts COMn / NOn / NCn", "1.5 mm", "Control-circuit currents only (contactor coil). Mains side, left of the slot."),
 ("+5V_HLK, +5V", "0.8 mm", "Peak about 0.75 A in the plan; 0.8 mm on 1 oz is comfortable."),
 ("+3V3", "0.6 mm", "ESP32 bursts to about 0.45 A."),
 ("GND", "pour on both layers", "Low-voltage side only. No pour on the mains side or across the slot."),
 ("Relay coil nodes RLYn_D", "0.5 mm", "About 72 mA each."),
 ("USB_DP / USB_DN", "0.2 mm pair, 90 ohm diff", "Keep short, no stubs; U4 close to J1."),
 ("PZEM_TXD / PZEM_RXD, SDA, SCL, LCD_*, BTN_*, IN1/IN2, BUZZ, LED_ST", "0.25 mm", "Plain signals."),
 ("Isolation slot", "1.3 mm wide", "Milled slot, ends at least 3.2 mm past the nearest mains copper so the creepage path around it stays above 6.4 mm."),
]

STEPS = [
 "In EasyEDA PCB, set the board outline to 100 x 90 mm with 3 mm corners and place the four M3 pads (4, 4), (96, 4), (4, 86), (96, 86) mm.",
 "Draw the isolation slot (x 28.1 to 29.4 mm, y 7 to 77 mm) on the board-outline layer as a routed slot. Add keep-out rectangles 3.2 mm around it on both copper layers.",
 "Import the schematic (Design > Update/Convert Schematic to PCB). Check every footprint against its datasheet first: J1 USB-C, K1/K2 relays, U2 HLK, KF128 terminals, J9 1x20.",
 "Place section by section in this order: mains, relays, power, USB, ESP32, displays, PZEM and I/O. Use the X / Y tables as a start, then tick each part here.",
 "Draw the net classes from the table above (widths and the USB pair), then pour GND on the low-voltage side only.",
 "Route mains and relay contacts first, then 5 V and 3.3 V, then USB, then the rest by hand.",
 "Run the PCB DRC with the 6.4 mm mains clearance rule applied between the mains and low-voltage net classes. Add silkscreen: MAINS WARNING, COM / NO / NC labels, J2 L and N.",
 "Export Gerber and have the PCB maker check the slot and 6.4 mm spacing. Do not power from mains before the engineer review (PLAN.md section 14).",
]


def build():
    total = len(PL.L)
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot PCB Layout Guide</title><style>{CSS}</style></head><body><main>']
    o.append('<div class="hero"><h1>BorePilot - PCB layout guide by section</h1><p>100 x 90 mm, 2 layers. Where every part goes, section by section, with X / Y in mm (origin = lower-left corner, y up), a tick box per part and the trace width of every net. Click a part in a drawing or tick it in the table: both stay in sync and are saved in this browser.</p></div>')
    o.append('<div class="warn"><b>Plan stage, not a finished layout.</b> Positions and sizes are estimates for a first placement (the checker found no overlaps and no clashes with the mounting holes or the slot band), but the real footprints from EasyEDA will differ: compare the courtyards, then adjust. Mains is on the left side of the slot: engineer review before any mains power.</div>')
    o.append('<nav>' + '<a style="background:#607d8b" href="#size">Board size</a><a style="background:#607d8b" href="#plan">Floor plan</a>' + "".join(f'<a style="background:{SEC[s][2]}" href="#{s}">{e(SEC_TITLE[s])}</a>' for s in ORDER) + f'<a style="background:#607d8b" href="#nets">Nets</a><a style="background:#607d8b" href="#steps">Steps</a><span class="mut">placed <b id="tot">0</b> / {total}</span><div class="bar"><div id="barfill"></div></div><button id="reset">Reset ticks</button></nav>')
    # size
    used = sum(w * h for (x, y, w, h, r) in PL.L.values())
    o.append('<section class="card" id="size"><h2>Best board size</h2>')
    o.append(f'<div class="rec"><b>Selected: 100 x 90 mm, 2 layers, 1.6 mm FR-4, 1 oz copper.</b> The footprints add up to about {used:.0f} mm&sup2; of the 9000 mm&sup2; board ({used/90:.0f} %), but the real constraint is the shape: the HLK module is 38 x 23 mm and the 1x20 display header is 51 mm long, the two relays need 19 mm each, and the left column needs a 6.4 mm slot. 100 x 100 mm or smaller was the limit set by the owner: 100 x 90 mm stays inside it and in the cheapest PCB price tier. A 100 x 80 mm board no longer fits once the J13 UART header, the 6.4 mm clearance to the AC terminals and the 51 mm display header are all kept; a 90 x 70 mm board would not hold even the relays and the HLK module.</div>')
    o.append('<h3>Board outline, mounting pads and slot</h3><div class="scroll"><table><thead><tr><th>Item</th><th>X mm</th><th>Y mm</th><th>Size</th><th>Net</th></tr></thead><tbody>')
    o.append('<tr><td>Board outline</td><td class="num">0 - 100</td><td class="num">0 - 90</td><td>100 x 90, corner radius 3 mm</td><td>-</td></tr>')
    for i, (hx, hy) in enumerate(PL.HOLES, 1):
        o.append(f'<tr><td>MH{i} M3 mounting pad</td><td class="num">{hx:.1f}</td><td class="num">{hy:.1f}</td><td>pad 6.4 mm, hole 3.2 mm</td><td>GND (low-voltage side only: use NPTH on the mains-side pads)</td></tr>')
    o.append(f'<tr><td>Isolation slot</td><td class="num">{PL.SLOT["x"]:.1f} - {PL.SLOT["x"]+PL.SLOT["w"]:.1f}</td><td class="num">{PL.SLOT["y0"]:.0f} - {PL.SLOT["y1"]:.0f}</td><td>{PL.SLOT["w"]} mm wide, routed</td><td>none</td></tr></tbody></table></div>')
    o.append('<h3>Edge plan</h3><ul class="rules"><li><b>Top edge:</b> J2 and J3 (mains, left), J8 / J7 (OLED / 16x2), J12 spare, J13 UART / boot header, U.FL end of the ESP32 module.</li><li><b>Left edge:</b> J4 and J5 relay terminals (COM / NO / NC).</li><li><b>Bottom edge:</b> J6 (PZEM), J10 / J11 (float inputs), J1 (USB-C).</li><li><b>Right edge:</b> J9 (12864 LCD, 1x20).</li></ul>')
    o.append('<p class="mut">Not on the board: ANT1 (U.FL to SMA pigtail) and ANT2 (SMA antenna). The ESP32 module has no PCB antenna; the pigtail goes to a bulkhead outside the enclosure.</p></section>')
    # plan
    o.append('<section class="card" id="plan"><h2>Floor plan: 100 x 90 mm<span class="cnt">grid 10 mm; click a part to tick it</span></h2><p class="legend">' + "".join(f'<span><i style="background:{SEC[s][2]}"></i>{e(SEC_TITLE[s])}</span>' for s in ORDER) + '</p><div class="scroll">' + board_svg() + '</div></section>')
    # sections
    for s in ORDER:
        tb, n = parts_table(s)
        o.append(f'<section class="card" id="{s}" style="--c:{SEC[s][2]}"><h2>{e(SEC_TITLE[s])}<span class="cnt"><span class="done">0</span> / {n} placed</span></h2><p class="mut">{e(SEC[s][3])}</p><ul class="rules">' + "".join(f"<li>{e(t)}</li>" for t in SEC_NOTES[s]) + f'</ul><div class="scroll">{board_svg(active=s)}</div>{tb}</section>')
    o.append('<section class="card" id="nets"><h2>Nets and trace widths<span class="cnt">1 oz copper, IPC-2221 external layer, with margin</span></h2><div class="scroll"><table><thead><tr><th>Net</th><th>Width</th><th>Notes</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in NETS) + '</tbody></table></div></section>')
    o.append('<section class="card" id="steps"><h2>Order of work</h2><ol class="steps">' + "".join(f"<li>{e(t)}</li>" for t in STEPS) + '</ol></section>')
    o.append("""<script>
const K='borepilot-pcb-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){let n=0;const total=document.querySelectorAll('#plan .pt').length;
 document.querySelectorAll('.pt').forEach(g=>g.classList.toggle('ok',!!st[g.dataset.ref]));
 document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
 n=Object.keys(st).length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/total)+'%';
 document.querySelectorAll('section.card[id]').forEach(sec=>{const rows=sec.querySelectorAll('tr[data-ref]');if(!rows.length)return;const d=[...rows].filter(r=>st[r.dataset.ref]).length;const c=sec.querySelector('.done');if(c)c.textContent=d});
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function tog(r){if(st[r])delete st[r];else st[r]=1;apply()}
document.querySelectorAll('.pt').forEach(g=>g.addEventListener('click',()=>tog(g.dataset.ref)));
document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>tog(c.dataset.k)));
document.getElementById('reset').onclick=()=>{st={};apply()};apply();
</script></main></body></html>""")
    return "".join(o)


os.makedirs(os.path.join(ROOT, "docs/images"), exist_ok=True)
open(os.path.join(ROOT, "docs/pcb-section-guide.html"), "w", encoding="utf-8").write(build())
svg = board_svg(standalone=True)
leg = "".join(f'<rect x="{M + i*150}" y="{VH+6:.0f}" width="12" height="12" rx="3" fill="{SEC[s][2]}"/><text x="{M + i*150 + 17}" y="{VH+16:.0f}" font-size="10" fill="#1c2330">{e(SEC_TITLE[s])}</text>' for i, s in enumerate(ORDER[:5]))
leg2 = "".join(f'<rect x="{M + i*150}" y="{VH+24:.0f}" width="12" height="12" rx="3" fill="{SEC[s][2]}"/><text x="{M + i*150 + 17}" y="{VH+34:.0f}" font-size="10" fill="#1c2330">{e(SEC_TITLE[s])}</text>' for i, s in enumerate(ORDER[5:]))
title = f'<text x="{M}" y="14" font-size="13" font-weight="700" fill="#1c2330">BorePilot PCB floor plan - 100 x 90 mm, 2 layers (planning estimate)</text>'
full = svg.replace(f'viewBox="0 0 {VW:.0f} {VH:.0f}" width="{VW:.0f}" height="{VH:.0f}"', f'viewBox="0 0 {VW:.0f} {VH+44:.0f}" width="{VW:.0f}" height="{VH+44:.0f}"').replace("</svg>", leg + leg2 + title + "</svg>")
full = full.replace('<rect x="24" y="24"', f'<rect x="0" y="0" width="{VW:.0f}" height="{VH+44:.0f}" fill="#ffffff"/><rect x="24" y="24"', 1)
open(os.path.join(ROOT, "docs/images/pcb-floorplan.svg"), "w", encoding="utf-8").write(full)
print("parts", len(PL.L), "pcb guide written")
