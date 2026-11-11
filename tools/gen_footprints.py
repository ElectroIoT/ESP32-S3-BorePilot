"""Generate docs/footprints.html: BorePilot footprint check (EasyEDA pads vs datasheet drawings).
Run from the repo root:  python -X utf8 -I tools/gen_footprints.py
Pad data was read from the open EasyEDA PCB1 (2026-11-10), units mm, origin = part origin, y up.
Datasheet values were read from the LCSC datasheet PDFs of the parts in the BOM."""
import os, html

e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# pads: (number, net, x, y, shape R/E/O, w, h, hole)
K1 = [("1", "RLY1_D (coil)", -5.1, -6, "E", 2.79, 2.79, 1.52), ("4", "+5V (coil)", -5.1, 6, "E", 2.79, 2.79, 1.52),
      ("5", "COM1 (mains)", -7.1, 0, "E", 2.79, 2.79, 1.52), ("2", "NO1 (mains)", 7.1, -6, "E", 2.79, 2.79, 1.52),
      ("3", "NC1 (mains)", 7.1, 6, "E", 2.79, 2.79, 1.52)]
U2 = [("1", "AC2", -16.8, 3, "E", 2.0, 2.0, 1.2), ("2", "AC1", -16.8, -3, "E", 2.0, 2.0, 1.2),
      ("3", "GND (-Vo)", 16.8, 9, "E", 2.0, 2.0, 1.2), ("4", "+5V_HLK (+Vo)", 16.8, -9, "E", 2.0, 2.0, 1.2)]
J4 = [("1", "COM1", -5.08, 0, "E", 2.4, 2.4, 1.4), ("2", "NO1", 0, 0, "E", 2.4, 2.4, 1.4), ("3", "NC1", 5.08, 0, "E", 2.4, 2.4, 1.4)]
J2 = [("1", "AC1", -2.54, 0, "E", 2.4, 2.4, 1.6), ("2", "AC2", 2.54, 0, "E", 2.4, 2.4, 1.6)]
BZ = [("1", "+ lead", -3.6, -3.6, "R", 2.4, 2.4, 0), ("2", "- lead", 3.6, -3.6, "R", 2.4, 2.4, 0),
      ("3", "dummy", 3.6, 3.6, "R", 2.4, 2.4, 0), ("4", "dummy", -3.6, 3.6, "R", 2.4, 2.4, 0)]
J1_SIG = [("B8", -1.75), ("A5", -1.25), ("B7", -0.75), ("A6", -0.25), ("A7", 0.25), ("B6", 0.75), ("A8", 1.25), ("B5", 1.75)]


def svg(w, h, body, cx=0, cy=0, scale=10):
    vw, vh = w * scale, h * scale
    return (f'<svg viewBox="{-vw/2:.1f} {-vh/2:.1f} {vw:.1f} {vh:.1f}" width="100%" style="max-width:{min(vw*1.1,760):.0f}px" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">{body}</svg>')


def pad(p, s=10, col="#b87333", flip=True):
    n, net, x, y, sh, w, h, hole = p
    X, Y = x * s, (-y if flip else y) * s
    if sh == "E":
        shape = f'<ellipse cx="{X}" cy="{Y}" rx="{w*s/2}" ry="{h*s/2}" fill="{col}" fill-opacity=".85" stroke="#6b3f12" stroke-width="1"/>'
    else:
        shape = f'<rect x="{X-w*s/2}" y="{Y-h*s/2}" width="{w*s}" height="{h*s}" fill="{col}" fill-opacity=".85" stroke="#6b3f12" stroke-width="1"/>'
    hl = f'<circle cx="{X}" cy="{Y}" r="{hole*s/2}" fill="#fff" stroke="#333" stroke-width=".8"/>' if hole else ""
    lab = f'<text x="{X}" y="{Y+3}" font-size="9" font-weight="700" text-anchor="middle" fill="#111">{e(n)}</text>'
    return shape + hl + lab


def dim(x1, y1, x2, y2, text, col="#2a6fd6", off=0, vertical=False):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    t = (f'<text x="{mx+(6 if vertical else 0)}" y="{my-4 if not vertical else my}" font-size="9" fill="{col}" '
         f'text-anchor="{"start" if vertical else "middle"}">{e(text)}</text>')
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1" marker-start="url(#a)" marker-end="url(#a)"/>' + t)


DEFS = '<defs><marker id="a" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,3 L6,3" stroke="#2a6fd6" stroke-width="1"/><circle cx="3" cy="3" r="1.5" fill="#2a6fd6"/></marker></defs>'


def k1_svg():
    s = 10
    b = DEFS + f'<rect x="{-9.6*s-12*0}" y="-78" width="{19.2*s}" height="{15.6*s}" rx="3" fill="none" stroke="#999" stroke-dasharray="4 3"/>'
    b = DEFS + f'<rect x="{-9.6*s+0.4*s}" y="{-7.8*s}" width="{19.2*s}" height="{15.6*s}" rx="3" fill="#f3f3f3" stroke="#999" stroke-dasharray="4 3"/>'
    b += "".join(pad(p, s) for p in K1)
    b += dim(-5.1 * s, 78, 7.1 * s, 78, "12.2 (datasheet 12.2)")
    b += dim(-100, -6 * s, -100, 6 * s, "12 (12)", vertical=True) if False else ""
    b += f'<line x1="{-5.1*s-40}" y1="{-6*s}" x2="{-5.1*s-40}" y2="{6*s}" stroke="#2a6fd6"/><text x="{-5.1*s-120}" y="3" font-size="9" fill="#2a6fd6">12 (12)</text>'
    b += f'<line x1="{-7.1*s}" y1="95" x2="{-5.1*s}" y2="95" stroke="#2a6fd6"/><text x="{-7.1*s-4}" y="107" font-size="9" fill="#2a6fd6">2.0 (2)</text>'
    # COM to coil gap
    b += f'<line x1="{-7.1*s+0.95*s*0.3}" y1="{-0}" x2="{-5.1*s}" y2="{-6*s+13}" stroke="#d62a2a" stroke-width="1.6" stroke-dasharray="3 2"/>'
    b += f'<text x="{-7.1*s-110}" y="-28" font-size="9" fill="#d62a2a" font-weight="700">COM to coil pad:</text><text x="{-7.1*s-110}" y="-17" font-size="9" fill="#d62a2a" font-weight="700">3.5 mm edge to edge</text>'
    for cy, ang in ((-3.0, 18.4), (3.0, -18.4)):
        # y up in EasyEDA: SVG y is flipped, so the rotation sign flips too
        b += (f'<g transform="translate({-6.1*s},{-cy*s}) rotate({-ang})"><rect x="{-4.0*s}" y="{-0.5*s}" width="{8.0*s}" height="{1.0*s}" rx="{0.5*s}" '
              f'fill="#d62a2a" fill-opacity=".25" stroke="#d62a2a" stroke-width="1.4"/></g>')
    b += f'<text x="{-4.9*s}" y="{-9.2*s}" font-size="9" fill="#d62a2a" font-weight="700">proposed slots 8 x 1 mm</text>'
    return svg(40, 20, b)


def u2_svg():
    s = 8
    b = DEFS + f'<rect x="{-19*s}" y="{-11.5*s}" width="{38*s}" height="{23*s}" rx="3" fill="#f3f3f3" stroke="#999" stroke-dasharray="4 3"/>'
    b += "".join(pad(p, s) for p in U2)
    b += dim(-16.8 * s, 12.5 * s, 16.8 * s, 12.5 * s, "33.6 (35.8 - 2.2 = 33.6)")
    b += f'<line x1="{-22*s}" y1="{-3*s}" x2="{-22*s}" y2="{3*s}" stroke="#2a6fd6"/><text x="{-27*s}" y="3" font-size="9" fill="#2a6fd6">6 (6)</text>'
    b += f'<line x1="{22*s}" y1="{-9*s}" x2="{22*s}" y2="{9*s}" stroke="#2a6fd6"/><text x="{22.5*s}" y="3" font-size="9" fill="#2a6fd6">18 (18)</text>'
    b += f'<text x="{-18*s}" y="{-12*s}" font-size="9" fill="#555">top view, body 38 x 23 mm</text>'
    return svg(54, 29, b, scale=8)


def kf_svg():
    s = 14
    b = DEFS + "".join(pad(p, s) for p in J4)
    b += dim(-5.08 * s, 36, 0, 36, "5.08 (5.08)") + dim(0, 36, 5.08 * s, 36, "5.08 (5.08)")
    b += f'<text x="{-5.08*s}" y="-26" font-size="9" fill="#555">3-way J4 / J5: hole 1.40 = datasheet 1.40</text>'
    return svg(14, 5, b, scale=14)


def j1_svg():
    s = 28
    b = DEFS
    for n, x in J1_SIG:
        b += f'<rect x="{(x-0.15)*s}" y="{(-2.47-0.65)*s}" width="{0.3*s}" height="{1.3*s}" fill="#b87333" stroke="#6b3f12" stroke-width=".6"/>'
    for x, lab in [(-3.2, "GND"), (-2.4, "VBUS"), (2.4, "VBUS"), (3.2, "GND")]:
        b += f'<circle cx="{x*s}" cy="{-2.47*s}" r="{0.3*s}" fill="#b87333" stroke="#6b3f12" stroke-width=".6"/><text x="{x*s}" y="{-2.47*s-12}" font-size="8" text-anchor="middle" fill="#333">{lab}</text>'
    for x, y, L in [(4.32, 2.47, 1.8), (4.32, -1.71, 2.0), (-4.32, -1.71, 2.0), (-4.32, 2.47, 1.8)]:
        b += f'<rect x="{x*s-0.6*s}" y="{y*s-L/2*s}" width="{1.2*s}" height="{L*s}" rx="{0.6*s}" fill="#b87333" fill-opacity=".8" stroke="#6b3f12" stroke-width=".6"/>'
        b += f'<rect x="{x*s-0.4*s}" y="{y*s-0.6*s}" width="{0.8*s}" height="{1.2*s}" rx="{0.4*s}" fill="#fff" stroke="#333" stroke-width=".5"/>'
    b += dim(-4.32 * s, 4.2 * s, 4.32 * s, 4.2 * s, "8.64 (datasheet 8.65)")
    b += dim(-1.75 * s, -5.2 * s, 1.75 * s, -5.2 * s, "3.5 (3.50)")
    b += dim(-3.2 * s, 5.6 * s, 3.2 * s, 5.6 * s, "6.4 (6.40)")
    b += f'<text x="{-9.2*s}" y="{-5.2*s}" font-size="8" fill="#555">USB-C TYPE-C-31-M-12, component side, y down = board edge</text>'
    return svg(21, 14, b, scale=28)


def bz_svg():
    s = 14
    b = DEFS + f'<rect x="{-4.25*s}" y="{-4.25*s}" width="{8.5*s}" height="{8.5*s}" rx="4" fill="#ddd" stroke="#555"/><circle cx="0" cy="0" r="{2.75*s}" fill="none" stroke="#999" stroke-dasharray="3 3"/>'
    b += "".join(pad(p, s) for p in BZ)
    b += dim(-3.6 * s, 6.2 * s, 3.6 * s, 6.2 * s, "pad centres 7.2")
    b += dim(-4.25 * s, -6.2 * s, 4.25 * s, -6.2 * s, "body 8.5 (8.5)")
    return svg(14, 15, b, scale=14)


ROWS = [
 # part, refs, lcsc, status, evidence
 ("K1, K2", "SRD-05VDC-SL-C", "C35449", "ACTION",
  "Pin grid matches the datasheet (12.2 mm coil column to contact column, 12 mm coil spacing, COM 2 mm outside the coil column). Hole 1.52 mm vs 1.3 mm drawn (loose, fine). "
  "<b>But COM (pin 5) sits only 3.5 mm edge to edge from each coil pad</b> and the coil column lies between COM and NO / NC, so one straight slot cannot separate mains from the 5 V coil. "
  "Decision 2026-11-11: two 8 x 1 mm slots per relay between COM and the coil pins (details below), creepage 7.4 mm."),
 ("U2", "HLK-5M05", "C209907", "OK",
  "AC pins 6 mm apart, DC pins 18 mm apart, 33.6 mm between the AC and DC columns, all equal to the datasheet (2.2 mm in from each end, pin 0.8 mm). Pad 2.0 mm, hole 1.2 mm. "
  "Pin 3 = -Vo (GND), pin 4 = +Vo (+5V_HLK): check orientation on the 3D view, the datasheet top view is mirrored against EasyEDA y-up."),
 ("J4, J5", "KF128-5.08-3P", "C474953", "OK", "5.08 mm pitch, hole 1.40 mm, pad 2.4 mm: equal to the datasheet PCB layout (hole 1.40 +0.10)."),
 ("J2, J3, J10, J11", "KF128-5.08-2P", "C474952", "OK",
  "Holes were 1.60 mm, datasheet 1.40 +0.10. Fixed in PCB1 on 2026-11-11 (all four now 1.40, same as J4 / J5)."),
 ("J1", "TYPE-C-31-M-12", "C165948", "CHECK",
  "Equal to the drawing: 0.5 mm signal pitch, 3.5 mm B8 to B5 span, power pads 4.8 apart, GND pads 6.4 apart, shell slots 8.65 apart and 4.18 mm front to rear. "
  "Shell slots fixed on 2026-11-11 to the drawing (0.6 wide, 1.70 near / 1.40 rear; were 0.8 x 1.5 / 1.2). Still open: the two 0.6 mm locating-peg holes (5.78 mm apart) are missing and the four wide pads carry a 0.36 mm hole the drawing does not show (see footprint-placement.html)."),
 ("BZ1", "MLT-8530", "C94599", "OK",
  "Datasheet gives body 8.5 x 8.5 mm and corner pads (+ lead, - lead, two dummy) but no land pattern. Footprint: 2.4 mm square pads at 7.2 mm centres, 0.55 mm beyond the body: fine for hand or reflow solder."),
 ("U1", "ESP32-S3-WROOM-1U-N16R8", "C3013946", "NOT COMPARED",
  "Pads 1.5 x 0.9 mm at 1.27 mm pitch, 49 pads (41 + ground pad). Same values as the Espressif recommended footprint, but the datasheet drawing was not read."),
 ("U3", "SGM2212-3.3 (SOT-223)", "C3294699", "NOT COMPARED", "Pins 2.5 x 1.1 mm at 2.3 mm pitch plus tab: standard SOT-223. Datasheet drawing not compared. Datasheet electrical limits still unread (PLAN.md)."),
 ("J6", "B4B-XH-A (JST XH 4P)", "C594232", "CHECK", "2.5 mm pitch, pad 1.52 mm, hole 0.91 mm for a 0.64 mm square pin (diagonal 0.9): tight, widen to 1.0 mm if the module will not seat."),
 ("J7, J8, J12, J13", "PZ254V-11-xP", "C2691448 / C492405", "OK", "2.54 mm pitch, pad 1.7 mm, hole 1.1 mm: standard 0.1 inch header."),
 ("J9", "PZ254R-11-20P", "C41413628", "NOT COMPARED", "1x20 right-angle header, 2.54 mm pitch assumed. Check the footprint length 50.8 mm against the real part."),
 ("U4, U5, U6, Q1 to Q4, D1 to D5, passives", "SOT-23-6 / VSSOP-8 / TSSOP-14 / SOT-23 / SMB / 1206", "-", "NOT COMPARED", "Standard EasyEDA / LCSC library footprints. Low risk, but not compared with the datasheets."),
]

CSS = """:root{--bg:#f3f1fb;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#c9d1dc;--acc:#2a6fd6}
@media(prefers-color-scheme:dark){:root{--bg:#12161d;--fg:#e6ebf2;--mut:#9aa6b7;--card:#1b222c;--line:#323c4a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}
main{max-width:980px;margin:0 auto;padding:16px}h1{margin:.2em 0}h2{margin:.2em 0 .4em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}.mut{color:var(--mut)}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;font-size:14px}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;color:#fff;font-weight:700;font-size:12px;white-space:nowrap}
.OK{background:#2fbf71}.CHECK{background:#e0a020}.ACTION{background:#d62a2a}.NC{background:#7a8594}
.fig{overflow-x:auto;background:#fff;border-radius:8px;border:1px solid var(--line);padding:6px}.fig svg{display:block;margin:auto}
@media(max-width:600px){main{padding:10px}}"""


def build():
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot Footprint Check</title><style>{CSS}</style></head><body><main>']
    o.append('<h1>BorePilot footprint check</h1><p class="mut">EasyEDA footprints in PCB1 (read 2026-11-10) compared with the datasheet drawings of the BOM parts. '
             'Drawings are to scale, copper in orange, blue numbers are <b>EasyEDA value (datasheet value)</b> in mm. Datasheets: LCSC PDFs of the parts in the BOM.</p>')
    cnt = {}
    for r in ROWS:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    o.append('<div class="card"><h2>Summary</h2><p>' + " ".join(f'<span class="tag {k.replace(" ", "").replace("NOTCOMPARED", "NC")}">{k}</span> {v}&nbsp;&nbsp;' for k, v in cnt.items()) + '</p>'
             '<table><tr><th>Part</th><th>Model</th><th>LCSC</th><th>Result</th><th>What was compared</th></tr>')
    for ref, mpn, lc, st, txt in ROWS:
        cls = st.replace(" ", "").replace("NOTCOMPARED", "NC")
        o.append(f'<tr><td><b>{e(ref)}</b></td><td>{e(mpn)}</td><td>{e(lc)}</td><td><span class="tag {cls}">{st}</span></td><td>{txt}</td></tr>')
    o.append('</table></div>')
    figs = [("K1 / K2 relay SRD-05VDC-SL-C (top view, y up)", k1_svg(), "COM1 (pin 5) is 2 mm from the coil column; the dashed red line is the 3.5 mm gap to the nearest coil pad. Datasheet: 5 holes 1.3 mm, drawing bottom view."),
            ("U2 HLK-5M05 (top view)", u2_svg(), "AC pins left, DC pins right. All spacings equal the datasheet."),
            ("J4 / J5 KF128-5.08-3P", kf_svg(), "Datasheet PCB layout: holes 1.40 +0.10, pitch 5.08 +-0.03."),
            ("J1 USB-C TYPE-C-31-M-12", j1_svg(), "Signal pads 0.3 x 1.3 mm. Orange slots are the four shell tabs."),
            ("BZ1 MLT-8530 buzzer", bz_svg(), "Pads 1 and 2 are the + and - leads, 3 and 4 are mechanical dummy pads (no-connect flags set in the schematic).")]
    for t, s, n in figs:
        o.append(f'<div class="card"><h2>{e(t)}</h2><div class="fig">{s}</div><p class="mut">{e(n)}</p></div>')
    o.append('<div class="card"><h2>Relay K1 / K2: slots around the coil pins</h2>'
             '<p>Decision 2026-11-11: cut two slots in each relay footprint, one between COM (pin 5) and each coil pin (pins 1 and 4), so the mains pin and the 5 V coil are separated by a longer path through the board.</p>'
             '<table><tr><th>Slot</th><th>Centre (x, y) mm</th><th>Angle</th><th>Size</th><th>Ends (x, y) mm</th><th>Creepage COM to coil pad</th></tr>'
             '<tr><td>A (towards pin 1)</td><td>-6.10, -3.00</td><td>18.4 deg</td><td>8.0 x 1.0, round ends</td><td>(-2.31, -1.74) and (-9.89, -4.26)</td><td>7.4 mm around the slot end</td></tr>'
             '<tr><td>B (towards pin 4)</td><td>-6.10, +3.00</td><td>-18.4 deg</td><td>8.0 x 1.0, round ends</td><td>(-2.31, +1.74) and (-9.89, +4.26)</td><td>7.4 mm around the slot end</td></tr></table>'
             '<ul><li>Coordinates are relative to the relay origin with the relay at rotation 0 (y up, as in the EasyEDA PCB). The floor plan places both relays at rotation 270: use the rotated coordinates in footprint-placement.html.</li>'
             '<li>Creepage is measured pad edge to pad edge along the shortest path round the slot end: 7.4 mm against the 6.4 mm goal in PLAN.md (a 7 mm slot would give 6.6 mm, 6 mm only 5.9 mm).</li>'
             '<li>Slot edge to the nearest pad: 1.27 mm. The slots lie under the relay body, so the relay does not need extra board area.</li>'
             '<li>Routing rules: COM leaves to the left through the gap between the slots; coil pins leave up (pin 4) and down (pin 1), never across a slot. NO / NC are 12.2 mm from the coil, no slot needed.</li>'
             '<li>Make the slots on the Board Outline layer like the existing isolation slot, and no copper (also no pour) within 0.5 mm of them.</li>'
             '<li>This is a board-level measure. The relay itself still needs its own coil-to-contact rating checked, and the whole mains section needs the engineer review in PLAN.md section 14.</li></ul></div>')
    o.append('<div class="card"><h2>Open items before routing</h2><ol>'
             '<li>Relay K1 / K2: slots decided (see above). Update the floor plan and the main isolation slot position in PLAN.md section 14, since the relays no longer straddle the slot.</li>'
                          '<li>J1: add the two locating-peg holes (see footprint-placement.html).</li>'
             '<li>Read the remaining datasheet drawings: U1, U3, U4, U5, U6, J9 and the SOT-23 / SMB parts.</li>'
             '<li>Look at the 3D view of U2, K1, J1 and J4 once placed.</li></ol></div>')
    o.append('</main></body></html>')
    return "".join(o)


open(os.path.join(ROOT, "docs/footprints.html"), "w", encoding="utf-8").write(build())
print("docs/footprints.html written")
