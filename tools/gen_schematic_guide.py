"""Generate docs/schematic-guide.html: page-by-page manual build guide for EasyEDA Pro (web).
Run from the repo root:  python -I tools/gen_schematic_guide.py
Reuses the part list P, wire list W and sections S from gen_pages.py.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages as G

e = html.escape
ROOT = G.ROOT

PAGES = [
 ("p1", "Page 1 - Power and USB", ["mains", "power", "usb"], "#ff9f43",
  "Sheet name: <b>1_POWER_USB</b>. Place the three mains parts (J2, J3, U2) together in the top-left corner and write a MAINS WARNING text box next to them. Everything right of them is low voltage.",
  [
   ("Place J2 (AC in) and J3 (AC tap). Pin 1 of both = L, pin 2 = N. Add net labels <b>L</b> and <b>N</b> on them.", "mains"),
   ("Place U2 HLK-5M05. Wire its AC pins to L and N. Add net label <b>+5V_HLK</b> on +Vo and a GND symbol on -Vo.", "mains"),
   ("Place D4 and D5 (SS34B). D4: anode to <b>+5V_HLK</b>, cathode to <b>+5V</b>. D5: anode to <b>VBUS</b>, cathode to <b>+5V</b>. Cathode = the end with the bar.", "power"),
   ("Place C1 (470 uF) between +5V and GND. Observe polarity: + to +5V.", "power"),
   ("Place C6 (10 uF), C15 (100 nF on +5V_HLK) and C5 (10 uF) on the +5V rail to GND.", "power"),
   ("Place U3 SGM2212-3.3: VIN to +5V, GND to GND, VOUT to <b>+3V3</b>. Add C2 (10 uF) at VIN and C3 (10 uF) at VOUT. <b>Check the symbol's pin names; do not assume the pin order.</b>", "power"),
   ("Place J1 USB-C (C165948). VBUS pins (A4, B9, A9, B4) to <b>VBUS</b>; GND pins (A1, B12, A12, B1) and shield pins to GND.", "usb"),
   ("CC1 (A5) to R1 5.1 k to GND; CC2 (B5) to R2 5.1 k to GND. SBU pins (A8, B8) left unconnected (mark No-Connect).", "usb"),
   ("D+ pins (A6 and B6 together) and D- pins (A7 and B7 together) go to U4 USBLC6, then net labels <b>USB_DP</b> and <b>USB_DN</b>. U4 VBUS pin to VBUS, GND to GND.", "usb"),
   ("Place C7 (10 uF) and C11 (100 nF) on VBUS to GND.", "usb"),
  ],
  ["VBUS, +5V, +3V3, GND, USB_DP, USB_DN, L, N are the nets that leave this page. Put a net label on each at the page edge.",
   "Do NOT connect L or N to anything except J2, J3 and U2.",
   "U2 -Vo and the USB GND are the same GND: this is the isolated secondary of the HLK module."]),
 ("p2", "Page 2 - ESP32-S3 core", ["mcu"], "#a66cff",
  "Sheet name: <b>2_MCU</b>. Put U1 in the centre and keep every GPIO as a net label going left/right: the other pages pick them up by name.",
  [
   ("Place U1 ESP32-S3-WROOM-1U-N16R8 (C3013946). 3V3 pin to <b>+3V3</b>, all GND pins and the EPAD to GND.", "mcu"),
   ("Add C4 (10 uF), C9 and C10 (100 nF) on +3V3 to GND, next to the module.", "mcu"),
   ("EN pin: R3 10 k to +3V3, C8 100 nF to GND, SW1 to GND. Net label <b>EN</b>.", "mcu"),
   ("IO0 pin: SW2 to GND (BOOT). Nothing else on IO0.", "mcu"),
   ("IO19 to net label <b>USB_DN</b>, IO20 to net label <b>USB_DP</b> (from page 1).", "mcu"),
   ("Put net labels on the GPIO pins: IO4 <b>RLY1</b>, IO5 <b>RLY2</b>, IO8 <b>SDA</b>, IO9 <b>SCL</b>, IO10 <b>LCD_CS</b>, IO11 <b>LCD_MOSI</b>, IO12 <b>LCD_CLK</b>, IO13 <b>LCD_BL</b>, IO14 <b>LCD_RST</b>, IO15 <b>BUZZ</b>, IO16 <b>LED_ST</b>, IO17 <b>PZEM_TXD</b>, IO18 <b>PZEM_RXD</b>, IO1 <b>BTN_START</b>, IO2 <b>BTN_STOP</b>, IO6 <b>BTN_MENU</b>, IO39 <b>IN1</b>, IO40 <b>IN2</b>, IO41 <b>SP1</b>, IO42 <b>SP2</b>, IO47 <b>SP3</b>, IO48 <b>SP4</b>.", "mcu"),
   ("TXD0 (IO43) and RXD0 (IO44): connect to <b>J13</b> pins 3 and 4 (net flags <b>TXD0</b>, <b>RXD0</b>). J13 pins: 1 +3V3, 2 GND, 3 TXD0, 4 RXD0, 5 EN, 6 IO0_BOOT (a standard UART flasher header, leave unpopulated if unused).", "mcu"),
   ("Leave IO3, IO45, IO46 and IO33-IO37 with No-Connect flags. IO3/45/46 are strapping pins.", "mcu"),
   ("Place ANT1 and ANT2 on the sheet as notes (no wires): the pigtail connects to the module's U.FL connector. Give them BOM entries only.", "mcu"),
  ],
  ["Check that every GPIO you used appears once on this page. Compare with the GPIO table in the connection-diagram page.",
   "IO3, IO45, IO46 and IO0 are strapping pins: nothing except SW2 on IO0."]),
 ("p3", "Page 3 - Relays and mains contacts", ["relay"], "#2fbf71",
  "Sheet name: <b>3_RELAYS</b>. Draw two identical blocks (channel 1 and channel 2). Keep the relay contact side (COM, NO, NC and J4/J5) on the right of the page; add a dashed box labelled MAINS SIDE around them.",
  [
   ("Place K1. Coil pins: one to <b>+5V</b>, the other to the drain of Q1. Contact pins COM, NO, NC go to J4 pins 1, 2, 3 (names COM / NO / NC).", "relay"),
   ("Place Q1 AO3400A: gate to net label <b>RLY1</b> and to R18 (100 k) to GND; source to GND; drain to K1 coil.", "relay"),
   ("Place D1 across the K1 coil: cathode to +5V, anode to Q1 drain.", "relay"),
   ("Place LED3 (green) with R10 (1 k): +5V -> R10 -> LED3 anode; LED3 cathode to Q1 drain. This shows the real coil state.", "relay"),
   ("Repeat for channel 2: K2, Q2 (gate net <b>RLY2</b>, R19 100 k), D2, LED4 + R11, J5.", "relay"),
   ("Place C17 and C18 (100 nF) on +5V near each relay.", "relay"),
   ("Draw a dashed rectangle around K1/K2 contacts, J4 and J5 and add the text: MAINS SIDE - keep 6.4 mm from low-voltage copper.", "relay"),
  ],
  ["Check the relay symbol: SRD-05VDC-SL-C is a 5-pin SPDT. Use the symbol pin names and compare with the datasheet drawing before layout.",
   "Pin 1 of J4 and J5 = COM, pin 2 = NO, pin 3 = NC. Silkscreen these names on the PCB."]),
 ("p4", "Page 4 - PZEM link and I/O", ["pzem", "ui"], "#00bcd4",
  "Sheet name: <b>4_PZEM_IO</b>.",
  [
   ("Place J6 JST XH 4-pin. Label pins: 1 +5V, 2 = board TX line to the PZEM RX pin, 3 = PZEM TX line to the board RX, 4 GND. <b>Check the pin order printed on your PZEM module and match it.</b>", "pzem"),
   ("Net <b>PZEM_TXD</b> (from ESP32 IO17) goes to the J6 pin that connects to the PZEM RX pin.", "pzem"),
   ("PZEM TX pin (J6) goes to R16 4.7 k, then to net <b>PZEM_RXD</b> (ESP32 IO18). Put R4 10 k from the R16/IO18 node to GND (divider).", "pzem"),
   ("Place C16 (100 nF) on J6 +5V.", "pzem"),
   ("Place SW3, SW4, SW5: one side to <b>BTN_START</b>, <b>BTN_STOP</b>, <b>BTN_MENU</b>, other side to GND.", "ui"),
   ("LED1 (red) with R8: +3V3 -> R8 -> LED1 -> GND. LED2 (red) with R9: <b>LED_ST</b> -> R9 -> LED2 -> GND.", "ui"),
   ("J10 and J11 (screw terminals): pin 1 to <b>IN1</b> / <b>IN2</b>, pin 2 to GND. Optional pull-ups R6 and R7 (10 k to +3V3) marked DNP.", "ui"),
   ("Optional buzzer: BZ1 + to +5V, - to Q4 drain; Q4 gate to <b>BUZZ</b> and R21 (100 k) to GND; D3 across BZ1 (cathode +5V). Mark Q4, D3, BZ1, R21 as optional.", "ui"),
   ("J12 header: pin 1 +3V3, pin 2 GND, pins 3-6 to <b>SP1</b>, <b>SP2</b>, <b>SP3</b>, <b>SP4</b>.", "ui"),
  ],
  ["PZEM TX is assumed to be 5 V logic: the divider protects GPIO18. If your PZEM measures 3.3 V on TX, R16 can be 0 ohm and R4 removed.",
   "Mark optional parts in the BOM column 'Not placed' so the assembly BOM leaves them out."]),
 ("p5", "Page 5 - Display options", ["disp"], "#ff4d94",
  "Sheet name: <b>5_DISPLAYS</b>. Draw three separate blocks and title them A, B, C. Fit only one display per build; the other blocks are 'DNP' (do not place) where noted.",
  [
   ("<b>Block B (OLED, simplest)</b>: J8 pins: 1 GND, 2 +3V3, 3 <b>SCL</b>, 4 <b>SDA</b>. Pull-ups R12 (SDA) and R13 (SCL), 4.7 k to +3V3. <b>Check your OLED's pin order.</b>", "disp"),
   ("<b>Block A (16x2 LCD)</b>: U5 PCA9306: VREF1 to +3V3, VREF2 to +5V, EN to +5V through R5 10 k; SDA1/SCL1 to nets <b>SDA</b>/<b>SCL</b>; SDA2/SCL2 to nets <b>SDA_5V</b>/<b>SCL_5V</b>; GND to GND. C12 on VREF1, C13 on VREF2.", "disp"),
   ("J7 pins: 1 GND, 2 +5V, 3 SDA_5V, 4 SCL_5V. R14 and R15 (4.7 k to +5V) are DNP when the backpack has its own pull-ups.", "disp"),
   ("<b>Block C (12864 ST7920)</b>: U6 SN74AHCT125: VCC to +5V (C14 100 nF), GND to GND, all OE pins to GND. Inputs 1A-4A = <b>LCD_CS</b>, <b>LCD_MOSI</b>, <b>LCD_CLK</b>, <b>LCD_RST</b>; outputs 1Y-4Y to nets <b>LCD_RS_5V</b>, <b>LCD_RW_5V</b>, <b>LCD_E_5V</b>, <b>LCD_RST_5V</b>. Tie unused gates' inputs to GND.", "disp"),
   ("J9 1x20 female header, ST7920 order: 1 GND, 2 +5V, 3 V0, 4 LCD_RS_5V, 5 LCD_RW_5V, 6 LCD_E_5V, 7-14 no-connect, 15 PSB, 16 NC, 17 LCD_RST_5V, 18 VOUT, 19 BLA, 20 BLK.", "disp"),
   ("PSB (J9 pin 15): connect to GND through solder jumper SJ1 (place a 2-pad jumper footprint, default bridged = serial mode).", "disp"),
   ("RV2 10 k trimmer: ends to J9 pin 18 (VOUT) and +5V, wiper to J9 pin 3 (V0). <b>Verify against your 12864 module and the ST7920 datasheet</b>, some modules want V0 via a pot to GND instead.", "disp"),
   ("BLA (pin 19) to +5V (check if your module has a series resistor). BLK (pin 20) to Q3 drain; Q3 gate to <b>LCD_BL</b> and R20 100 k to GND; Q3 source to GND. C19 100 nF on J9 +5V.", "disp"),
  ],
  ["SDA/SCL pass to this page by net label from page 2; do not draw them again from U1.",
   "Fit only the display you use. The 16x2 backpack and the OLED can both be wired, but configure only one in firmware."]),
 ("p6", "Page 6 - Cover and notes (no parts)", [], "#9aa5b5",
  "Sheet name: <b>0_COVER</b>. Optional first page.",
  [("Add: project name BorePilot, revision v0.1, date, author ElectroIoT, the one-line description and the safety warning (230 V AC on J2/J3/U2/J4/J5, engineer review required).", None),
   ("Add a legend of net names: L, N, +5V_HLK, +5V, +3V3, GND, VBUS and the GPIO net names from page 2.", None)],
  [])
]

SETUP = [
 "Open EasyEDA Pro (web). Create the project <b>BorePilot</b> (Project &rarr; New). Inside it create one Schematic and one PCB (empty for now).",
 "In the schematic, add 6 pages with the sheet names above (right-click the schematic in the left Project panel &rarr; New Schematic Page). You can start with 5 and skip the cover.",
 "Set the grid to 5 or 10 (snap on) so wires land on pins. Set the sheet size to A3.",
 "To place a part: open the library search, type the <b>LCSC part number (C#)</b> given in the table (for example C3294699), pick the result with the same MPN and place it. The symbol, footprint and 3D model are then tied to the LCSC part.",
 "Set each part's <b>Designator</b> to the Ref in the table (U1, J2, R3 ...) and its <b>Value</b>. The Ref numbers match the BOM pages.",
 "Use <b>Net Label</b> for every connection that leaves a page or goes more than a few cm; use <b>Power Port</b> symbols for GND, +5V, +3V3 (type the same names everywhere). Net label names are case-sensitive.",
 "Mark optional/DNP parts with the 'Not in BOM' / 'Not placed' attribute so the final BOM leaves them out.",
 "Save often. After each page run <b>Design &rarr; Check ERC</b> (design rule check for schematics) and fix every warning before moving on.",
]

FINAL = [
 "Every net label has at least two uses (one on the page that drives it, one that receives it). Single-use labels are typos.",
 "Run ERC with no errors. Check there is exactly one GND net, one +5V, one +3V3. L and N never touch low-voltage nets.",
 "Compare the part count with the BOM: 83 placed parts (incl. optional buzzer parts).",
 "Open each footprint and compare it with the datasheet drawing before layout: USB-C C165948 (shield pegs/slots), relays, HLK-5M05 pin pitch, KF128 terminals, 1x20 header.",
 "Check the PZEM pin order against your actual module and the 12864/OLED/16x2 pin orders against your actual display modules.",
 "Export the schematic PDF and compare it with the connection-diagram page.",
 "Do not order PCBs until the mains side has had an engineer review (PLAN.md section 14).",
]

CROSS = [
 ("L, N", "mains live / neutral", "page 1 only", "#e53935"),
 ("+5V_HLK", "HLK output before OR-ing", "page 1", "#fb8c00"),
 ("VBUS", "USB 5 V", "page 1", "#fb8c00"),
 ("+5V", "main 5 V rail", "all pages", "#fb8c00"),
 ("+3V3", "3.3 V rail", "all pages", "#fdd835"),
 ("GND", "ground", "all pages", "#37474f"),
 ("USB_DP, USB_DN", "USB data", "1 to 2", "#8e24aa"),
 ("EN", "reset", "page 2", "#2fbf71"),
 ("RLY1, RLY2", "relay drive (IO4, IO5)", "2 to 3", "#2fbf71"),
 ("SDA, SCL", "I2C (IO8, IO9)", "2 to 5", "#ec407a"),
 ("SDA_5V, SCL_5V", "I2C 5 V side", "page 5", "#ec407a"),
 ("LCD_CS, LCD_MOSI, LCD_CLK, LCD_RST, LCD_BL", "12864 control (IO10, 11, 12, 14, 13)", "2 to 5", "#ec407a"),
 ("LCD_RS_5V, LCD_RW_5V, LCD_E_5V, LCD_RST_5V", "12864 5 V side", "page 5", "#ec407a"),
 ("PZEM_TXD, PZEM_RXD", "PZEM UART (IO17, IO18)", "2 to 4", "#00bcd4"),
 ("BTN_START, BTN_STOP, BTN_MENU", "buttons (IO1, 2, 6)", "2 to 4", "#2fbf71"),
 ("LED_ST, BUZZ", "status LED (IO16), buzzer (IO15)", "2 to 4", "#2fbf71"),
 ("IN1, IN2", "float inputs (IO39, IO40)", "2 to 4", "#2fbf71"),
 ("SP1-SP4", "spare (IO41, 42, 47, 48)", "2 to 4", "#2fbf71"),
 ("TXD0, RXD0", "console test pads (IO43, IO44)", "page 2", "#2fbf71"),
]

CSS = G.CSS + """
.step{display:flex;gap:10px;align-items:flex-start;padding:6px 0;border-bottom:1px dashed var(--line)}.step input{margin-top:3px}
.step.done span{opacity:.42;text-decoration:line-through}ol.plain{padding-left:20px}ol.plain li{margin:6px 0}
.note li{margin:4px 0}.pagehead{display:flex;align-items:center;gap:10px}.pn{width:34px;height:34px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:800}
.nets td:first-child{font-family:ui-monospace,Consolas,monospace;font-weight:700}.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:middle}
h3{margin:14px 0 4px}
"""

def parts_table(secs, col):
    rows = [p for p in G.P if p[0] in secs]
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>Search in EasyEDA</th><th>MPN</th><th>Qty</th><th>Pins / connections (planned)</th></tr></thead><tbody>'
    for _, ref, nm, c, q, conn in rows:
        mpn, mk, st, pr = G.info(c)
        s = f'<b>{c}</b>' if c.startswith("C") else '<span class="tag">choose</span>'
        opt = ' <span class="tag opt">optional</span>' if ("ptional" in nm or "DNP" in nm) else ""
        t += f'<tr><td><input type="checkbox" class="ck" data-k="part-{ref}"></td><td><b>{ref}</b></td><td>{e(nm)}{opt}</td><td>{s}</td><td>{e(mpn)}</td><td>{q}</td><td>{e("; ".join(x.strip() for x in conn.split(";")))}</td></tr>'
    return t + "</tbody></table></div>"

def page_html(pid, title, secs, col, intro, steps, checks, n):
    h = f'<section class="card" id="{pid}" style="--c:{col}"><div class="pagehead"><div class="pn">{n}</div><h2>{e(title)}</h2></div><p class="sub">{intro}</p>'
    if secs:
        h += "<h3>1. Place these parts</h3>" + parts_table(secs, col)
    h += "<h3>2. Wire in this order</h3>"
    for i, (txt, sec) in enumerate(steps, 1):
        h += f'<div class="step"><input type="checkbox" class="ck" data-k="{pid}-s{i}"><span><b>{i}.</b> {txt}</span></div>'
    wl = [w for w in G.W if w[0] in secs]
    if wl:
        h += "<h3>3. Wire colour reference for this page</h3><div class=\"scroll\"><table><thead><tr><th>Wire</th><th>From</th><th>To</th><th>Net</th><th>Note</th></tr></thead><tbody>"
        for _, a, b, k, note in wl:
            c, nn = G.NET[k]
            h += f'<tr><td><span class="wire" style="background:{c}"></span></td><td>{e(a)}</td><td>{e(b)}</td><td>{e(nn)}</td><td class="mut">{e(note)}</td></tr>'
        h += "</tbody></table></div>"
    if checks:
        h += '<h3>4. Check before leaving the page</h3><ul class="note">' + "".join(f"<li>{c}</li>" for c in checks) + "</ul>"
    return h + "</section>"

def build():
    total = sum(len([p for p in G.P if p[0] in pg[2]]) for pg in PAGES) + sum(len(pg[5]) for pg in PAGES) + len(SETUP) + len(FINAL)
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot Schematic Guide</title><style>{CSS}</style></head><body><main>']
    o.append('<div class="hero"><h1>BorePilot - schematic build guide (EasyEDA Pro web)</h1><p>Draw the schematic by hand, page by page. Every part has its LCSC number to search, every wire has a colour, every page has a check list. Progress is saved in this browser.</p></div>')
    o.append('<div class="warn"><b>Plan stage.</b> Nets come from PLAN.md, not from a finished schematic. Pin names and orders must be checked against the EasyEDA symbols and datasheets (SGM2212, SRD relay, USB-C, PZEM, displays). 230 V AC on J2, J3, U2, J4, J5: engineer review before mains power.</div>')
    o.append(f'<div class="bar"><input type="search" id="q" placeholder="Filter parts and steps ..."><progress id="pg" value="0" max="{total}"></progress><span id="pt" class="mut"></span><button id="rs">Reset ticks</button></div>')
    o.append('<div class="chips"><a class="chip" style="background:#607d8b" href="#setup">Setup</a>' + "".join(f'<a class="chip" style="background:{p[3]}" href="#{p[0]}">{e(p[1].split(" - ")[0])}</a>' for p in PAGES) + '<a class="chip" style="background:#607d8b" href="#nets">Net names</a><a class="chip" style="background:#607d8b" href="#final">Final checks</a></div>')
    o.append('<section class="card" id="setup" style="--c:#607d8b"><h2>0. Setup in EasyEDA Pro</h2>')
    for i, s in enumerate(SETUP, 1):
        o.append(f'<div class="step"><input type="checkbox" class="ck" data-k="setup-{i}"><span><b>{i}.</b> {s}</span></div>')
    o.append('</section>')
    for n, pg in enumerate(PAGES, 1):
        o.append(page_html(pg[0], pg[1], pg[2], pg[3], pg[4], pg[5], pg[6], n))
    o.append('<section class="card" id="nets" style="--c:#3b82f6"><h2>Net names used across pages</h2><p class="sub">Type these exactly (case-sensitive). The same name on two pages joins them.</p><div class="scroll"><table class="nets"><thead><tr><th>Net</th><th>Meaning</th><th>Where</th></tr></thead><tbody>')
    for n, m, w, c in CROSS:
        o.append(f'<tr><td><span class="sw" style="background:{c}"></span>{e(n)}</td><td>{e(m)}</td><td>{e(w)}</td></tr>')
    o.append('</tbody></table></div></section>')
    o.append('<section class="card" id="final" style="--c:#2fbf71"><h2>Final checks</h2>')
    for i, s in enumerate(FINAL, 1):
        o.append(f'<div class="step"><input type="checkbox" class="ck" data-k="final-{i}"><span><b>{i}.</b> {e(s)}</span></div>')
    o.append('</section><p class="mut">Companion pages: <a href="bom-by-page.html">BOM by schematic page</a> &middot; <a href="connection-diagram.html">connection map</a> &middot; <a href="bom-by-section.html">BOM by section</a>.</p>')
    o.append("""<script>
const K='borepilot-schem-guide';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const cks=[...document.querySelectorAll('.ck')];
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('pg').value=n;document.getElementById('pt').textContent=n+' / '+cks.length+' done';
cks.forEach(c=>{const r=c.closest('tr')||c.closest('.step');if(r)r.classList.toggle('done',c.checked)});
try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});
document.getElementById('rs').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};
document.getElementById('q').oninput=ev=>{const v=ev.target.value.toLowerCase();document.querySelectorAll('tbody tr,.step').forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none')};
upd();
</script></main></body></html>""")
    return "".join(o), total

h, total = build()
open(os.path.join(ROOT, "docs/schematic-guide.html"), "w", encoding="utf-8").write(h)
print("schematic-guide.html written, tickable items:", total)
