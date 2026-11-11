"""Generate docs/footprint-placement.html: footprint fixes done in EasyEDA, manual footprint steps,
relay isolation slots, and the placement table (X / Y / rotation) for placing parts by hand in EasyEDA.
Run from the repo root:  python -X utf8 -I tools/gen_footprint_placement.py"""
import os, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcb_layout as PL
import gen_pages as G

e = html.escape
ROOT = G.ROOT
NAME = {p[1]: p[2] for p in G.P}
BLK = {b[0]: b for b in PL.BLOCKS}
SLOT = PL.SLOT

CSS = """:root{--bg:#f3f1fb;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#c9d1dc;--acc:#2a6fd6}
@media(prefers-color-scheme:dark){:root{--bg:#12161d;--fg:#e6ebf2;--mut:#9aa6b7;--card:#1b222c;--line:#323c4a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}
main{max-width:1000px;margin:0 auto;padding:16px}h1{margin:.2em 0}h2{margin:.2em 0 .5em}h3{margin:.8em 0 .3em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}.mut{color:var(--mut)}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top;font-size:14px}
.tag{display:inline-block;padding:1px 8px;border-radius:10px;color:#fff;font-weight:700;font-size:12px;white-space:nowrap}
.done{background:#2fbf71}.todo{background:#e0a020}.warn{background:#d62a2a}
.scroll{overflow-x:auto}tr.ok td{opacity:.5;text-decoration:line-through}
nav{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
nav a{padding:4px 10px;border-radius:14px;background:#607d8b;color:#fff;text-decoration:none;font-size:12px;font-weight:700}
code{background:rgba(127,127,127,.18);padding:0 4px;border-radius:4px}
.bar{height:8px;background:var(--line);border-radius:5px;overflow:hidden;min-width:140px}.bar div{height:100%;background:#2fbf71;width:0}
@media(max-width:600px){main{padding:10px}}"""

FIXED = [
    ("J2, J3, J10, J11", "KF128-5.08-2P", "Pad holes 1.60 mm -> 1.40 mm (datasheet 1.40 +0.10), now the same as the 3-way J4 / J5. Done in PCB1 on 2026-11-11 and saved."),
    ("J1 (pins 1, 4)", "TYPE-C-31-M-12", "Shell slots next to the signal row: 0.8 x 1.5 mm -> 0.6 x 1.7 mm (datasheet 0.60 x 1.70). Done and saved."),
    ("J1 (pins 2, 3)", "TYPE-C-31-M-12", "Shell slots at the rear: 0.8 x 1.2 mm -> 0.6 x 1.4 mm (datasheet 0.60 x 1.40). Done and saved."),
    ("J4, J5", "KF128-5.08-3P", "Relay terminals are 3-way again, pin order NO / COM / NC, so COM sits in the middle and no track crosses. Final board: 81 parts, holes 1.40 mm."),
    ("Corner mounting holes", "-", "Already in PCB1: four M3 holes, 3.2 mm, no pad, at (4, 4), (96, 4), (4, 86) and (96, 86) mm. Checked 2026-11-11."),
]
MANUAL = [
    ("J1", "Add two 0.6 mm non-plated holes for the locating pegs (datasheet 2 x pin 0.50 mm at 5.78 mm). Relative to the J1 origin: (-2.89, +1.21) and (+2.89, +1.21) mm. "
           "Easiest after J1 is placed: place two mounting holes (0.6 mm, no pad) at the right spot and check them against the 3D view. Without them the connector still solders, but it can sit off by a few tenths of a mm.", "todo"),
    ("J1", "Optional: the four wide pads (A1/B12, A4/B9, B4/A9, B1/A12) each have a 0.36 mm hole that the datasheet does not show. It is harmless; remove it only if the board house flags the drill count.", "todo"),
    ("Main slot", "Shorten the main isolation slot in PCB1: it now runs only from y = 51 to y = 77 mm at x = 28.1 to 29.4 mm (HLK-5M05 area). In the file it still runs from y = 7 to y = 77 mm: delete the lower part so it ends at y = 51 mm.", "todo"),
    ("K1, K2", "Draw the two 8 x 1 mm isolation slots per relay (coordinates below, relay turned 270 degrees) on the Board Outline layer after the relay is placed, and keep copper 0.5 mm away from them.", "todo"),
    ("U2, K1, J1, J4", "After placing, switch to the 3D view and check body outline, pin 1 and the leg alignment on these four parts.", "todo"),
    ("U1, U3, U4, U5, U6, J9", "Still not compared with the datasheet drawings (see footprints.html). Do this before routing.", "todo"),
]
RELAY_SLOTS = [("A (between COM and pin 1, RLY_D)", "-3.00, +6.10", "108.4 deg", "(-1.74, +2.31)", "(-4.26, +9.89)"),
               ("B (between COM and pin 4, +5V)", "+3.00, +6.10", "71.6 deg", "(+1.74, +2.31)", "(+4.26, +9.89)")]
RELAY_PADS = [("5", "COM", "0.00, +7.10"), ("1", "RLY_D (coil)", "-6.00, +5.10"), ("4", "+5V (coil)", "+6.00, +5.10"), ("2", "NO", "-6.00, -7.10"), ("3", "NC", "+6.00, -7.10")]


def build():
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot Footprint and Placement</title><style>{CSS}</style></head><body><main>']
    o.append('<h1>BorePilot: footprints and PCB placement</h1><p class="mut">Work sheet for placing the parts by hand in EasyEDA PCB1 (board 100 x 90 mm, origin at the lower-left corner, y up, mm). '
             'Related pages: <a href="footprints.html">footprint check</a>, <a href="pcb-section-guide.html">floor plan by block</a>.</p>')
    o.append('<nav><a href="#fixed">Footprints fixed</a><a href="#manual">Still to do</a><a href="#relay">Relay placement</a><a href="#conflict">Main slot</a><a href="#table">Placement table</a>'
             '<span class="mut">placed <b id="tot">0</b> / ' + str(len(PL.L)) + '</span><div class="bar"><div id="barfill"></div></div></nav>')
    o.append('<section class="card" id="fixed"><h2>Footprints fixed in EasyEDA (PCB1, saved 2026-11-11)</h2><table><tr><th>Parts</th><th>Model</th><th>Change</th></tr>' +
             "".join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td><span class="tag done">DONE</span> {e(c)}</td></tr>' for a, b, c in FIXED) +
             '</table><p class="mut">Changed on the PCB copies of the footprints. If you use Update PCB from the schematic and EasyEDA offers to reset footprints, keep the PCB values, or the old sizes come back.</p></section>')
    o.append('<section class="card" id="manual"><h2>Still to do by hand</h2><table><tr><th>Parts</th><th>Step</th></tr>' +
             "".join(f'<tr><td><b>{e(a)}</b></td><td><span class="tag {t}">TODO</span> {e(b)}</td></tr>' for a, b, t in MANUAL) + '</table></section>')
    o.append('<section class="card" id="relay"><h2>Relay K1 / K2: how to place (decision 2026-11-11: split terminals, turned 270 degrees)</h2>'
             '<p>Place each relay at <b>rotation 270</b>. The COM pin and the two coil pins then face up, NO / NC face down. '
             'Pad positions from the relay origin at rotation 270 (x, y mm):</p>'
             '<table><tr><th>Pin</th><th>Net</th><th>x, y mm</th></tr>' +
             "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in RELAY_PADS) +
             '</table><p>COM sits 3.5 mm (pad edge to pad edge) from each coil pad, so each relay gets two slots, 8 x 1 mm with round ends, drawn on the Board Outline layer:</p>'
             '<div class="scroll"><table><tr><th>Slot</th><th>Centre (x, y) mm</th><th>Angle</th><th>End 1</th><th>End 2</th></tr>' +
             "".join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td><td>{e(f)}</td></tr>' for a, b, c, d, f in RELAY_SLOTS) +
             '</table></div><p>Creepage COM to coil pad around a slot end: 7.4 mm (goal 6.4 mm). Keep copper (also pours) 0.5 mm from every slot.</p>'
             '<h3>Routing rules for the relay</h3><ul>'
             '<li><b>COM</b> leaves the pad downward, between the two slots and under the relay body, straight to the middle pin of J4 / J5.</li>'
             '<li><b>NO / NC</b> go straight down to the outer pins of J4 / J5 below the relay body.</li>'
             '<li><b>Coil</b>: pin 1 (RLY_D) and pin 4 (+5V) go up into the low-voltage strip above the relay (Q1 / D1 / R18 / R10 / LED3 / C17). Keep that strip at least 6.4 mm (7.8 mm centre to centre) above the COM pad.</li>'
             '<li>No mains track may enter the strip, no low-voltage track may go below the relay: nothing crosses.</li></ul></section>')
    o.append('<section class="card" id="conflict"><h2><span class="tag done">DECIDED</span> Main slot and relay position</h2>'
             '<p>The long main slot is shortened to the HLK-5M05 area only: x = 28.1 to 29.4 mm, y = 51 to 77 mm. It separates the AC pin column of U2 from its DC column. '
             'The relays sit below it (K1 at x = 17.5, K2 at x = 39.5, y = 27 mm) and are isolated by their own slots, so no slot crosses a relay. '
             'Between the mains area (left, J2 / J3, U2 AC side, J4, J5) and the low-voltage area keep 6.4 mm by clearance where there is no slot.</p>'
             '<p class="mut">Why COM in the middle: on the SRD relay the coil column lies between COM and NO / NC. With the terminal order NO / COM / NC the three mains tracks run straight down and nothing crosses.</p></section>')
    # placement table
    o.append('<section class="card" id="table"><h2>Placement table</h2><p class="mut">Centre of each part in mm, rotation in degrees. These come from the floor plan in <code>tools/pcb_layout.py</code> and are estimates: check each part against its real footprint size. '
             'Relay layout updated 2026-11-11 (split terminals). Tick a row when the part is placed (saved in this browser).</p><div class="scroll"><table><tr><th>Done</th><th>Block</th><th>Ref</th><th>Part</th><th>X mm</th><th>Y mm</th><th>Rot</th><th>Size mm</th></tr>')
    for b in PL.BLOCKS:
        for ref in b[3]:
            x, y, w, h, rot = PL.L[ref]
            hold = ' <span class="tag done">270 deg</span>' if ref in ("K1", "K2") else ""
            o.append(f'<tr data-ref="{e(ref)}"><td><input type="checkbox" class="ck" data-k="{e(ref)}"></td><td style="border-left:6px solid {b[2]}">{e(b[1])}</td><td><b>{e(ref)}</b>{hold}</td>'
                     f'<td>{e(NAME.get(ref, ""))}</td><td>{x:g}</td><td>{y:g}</td><td>{rot:g}</td><td>{w:g} x {h:g}</td></tr>')
    o.append('</table></div></section>')
    o.append("""<script>
const K='borepilot-placement-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
const n=Object.keys(st).length,t=document.querySelectorAll('tr[data-ref]').length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/t)+'%';
try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>{const r=c.dataset.k;if(st[r])delete st[r];else st[r]=1;apply()}));apply();
</script></main></body></html>""")
    return "".join(o)


open(os.path.join(ROOT, "docs/footprint-placement.html"), "w", encoding="utf-8").write(build())
print("docs/footprint-placement.html written")
