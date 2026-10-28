"""Generate docs/bom-by-section.html and docs/connection-diagram.html for BorePilot.

Usage: python -I tools/gen_pages.py   (run from the repo root)
Data comes from hardware/bom/pump-controller-bom-v0.csv (LCSC numbers, stock, price)
and the planned nets in PLAN.md. There is no schematic yet: all connections are PLANNED.
"""
import csv, html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(ROOT, "hardware/bom/pump-controller-bom-v0.csv"), encoding="utf-8")))
LC = {r["LCSC #"]: r for r in rows}

# ---------------------------------------------------------------- sections
S = [
 ("mains", "MAINS INPUT 230 V", "#ff4d4d", "Hazardous side. No fuse or varistor on board (owner decision): protect upstream."),
 ("power", "5 V / 3.3 V POWER", "#ff9f43", "HLK-5M05 and USB VBUS OR-ed through Schottky diodes to +5V, then SGM2212 LDO to +3V3."),
 ("usb", "USB-C PROGRAMMING", "#4895ef", "C165948 USB-C, native USB on GPIO19/20, 5.1 k CC resistors, ESD part."),
 ("mcu", "ESP32-S3 CORE", "#a66cff", "WROOM-1U (external antenna), EN/BOOT buttons, decoupling."),
 ("relay", "RELAYS 1 and 2", "#2fbf71", "Two SPDT relays, COM/NO/NC on 5.08 mm terminals, low-side AO3400A drivers."),
 ("pzem", "PZEM-004T LINK", "#00bcd4", "UART1 header for the external PZEM-004T v3 module."),
 ("disp", "DISPLAY OPTIONS", "#ff4d94", "16x2 I2C LCD (via PCA9306), I2C OLED, 12864 ST7920 (via 74AHCT125). Fit one."),
 ("ui", "BUTTONS / LEDs / INPUTS", "#f4c20d", "START, STOP, MENU, status LEDs, optional buzzer, float inputs, spare GPIO."),
]

# (section, ref, name, C#, qty, planned connections "pin->net;...")
P = [
 ("mains","J2","AC in screw terminal 2P 5.08 mm","C474952",1,"1 -> L ; 2 -> N"),
 ("mains","J3","AC tap to PZEM voltage input, 2P","C474952",1,"1 -> L ; 2 -> N"),
 ("mains","U2","HLK-5M05 AC-DC 5 V 1 A module","C209907",1,"AC1 -> L ; AC2 -> N ; +Vo -> +5V_HLK ; -Vo -> GND"),
 ("power","D4","Schottky OR-ing: HLK to +5V","C2758511",1,"A -> +5V_HLK ; K -> +5V"),
 ("power","D5","Schottky OR-ing: USB VBUS to +5V","C2758511",1,"A -> VBUS ; K -> +5V"),
 ("power","C1","470 uF 16 V bulk on +5V","C47344174",1,"+ -> +5V ; - -> GND"),
 ("power","U3","SGM2212-3.3 LDO, SOT-223","C3294699",1,"VIN -> +5V ; GND -> GND ; VOUT -> +3V3"),
 ("power","C2","10 uF 1206, LDO input","C9807",1,"+5V / GND"),
 ("power","C3","10 uF 1206, LDO output","C9807",1,"+3V3 / GND"),
 ("power","C5","10 uF 1206, +5V near relays","C9807",1,"+5V / GND"),
 ("power","C6","10 uF 1206, +5V after OR-ing","C9807",1,"+5V / GND"),
 ("power","C15","100 nF 1206, HLK output","C24497",1,"+5V_HLK / GND"),
 ("usb","J1","USB-C 16-pin receptacle (user part C165948)","C165948",1,"A4/B9/A9/B4 -> VBUS ; A1/B12/A12/B1 -> GND ; A5 -> CC1 ; B5 -> CC2 ; A6,B6 -> USB_DP ; A7,B7 -> USB_DN"),
 ("usb","U4","USBLC6-2SC6 ESD protection","C7519",1,"I/O1 -> USB_DP (GPIO20) ; I/O2 -> USB_DN (GPIO19) ; VBUS -> VBUS ; GND -> GND"),
 ("usb","R1","5.1 k, CC1 pull-down","C26033",1,"CC1 -> GND"),
 ("usb","R2","5.1 k, CC2 pull-down","C26033",1,"CC2 -> GND"),
 ("usb","C7","10 uF 1206, VBUS","C9807",1,"VBUS / GND"),
 ("usb","C11","100 nF 1206, VBUS","C24497",1,"VBUS / GND"),
 ("mcu","U1","ESP32-S3-WROOM-1U-N16R8 module","C3013946",1,"3V3 -> +3V3 ; GND -> GND ; EN -> EN ; IO0 -> BOOT ; IO19/IO20 -> USB ; IO4/IO5 -> RLY1/RLY2 ; IO8/IO9 -> I2C ; IO17/IO18 -> PZEM ; IO10-14 -> LCD ; IO1/2/6 -> buttons ; IO15 -> buzzer ; IO16 -> LED ; IO39/IO40 -> floats"),
 ("mcu","ANT1","U.FL to SMA pigtail 200 mm","C2683345",1,"U.FL -> U1 ANT ; SMA -> enclosure bulkhead"),
 ("mcu","ANT2","2.4 GHz SMA antenna (NOT CHOSEN YET)","TBD",1,"SMA -> ANT1"),
 ("mcu","SW1","Reset button (EN)","C318884",1,"1 -> EN ; 2 -> GND"),
 ("mcu","SW2","BOOT button (GPIO0)","C318884",1,"1 -> IO0 ; 2 -> GND"),
 ("mcu","R3","10 k, EN pull-up","C17902",1,"EN -> +3V3"),
 ("mcu","C4","10 uF 1206, 3V3 at module","C9807",1,"+3V3 / GND"),
 ("mcu","C8","100 nF 1206, EN to GND","C24497",1,"EN / GND"),
 ("mcu","C9","100 nF 1206, module 3V3","C24497",1,"+3V3 / GND"),
 ("mcu","C10","100 nF 1206, module 3V3","C24497",1,"+3V3 / GND"),
 ("relay","K1","Relay 1, SRD-05VDC-SL-C","C35449",1,"coil+ -> +5V ; coil- -> Q1 drain ; COM -> J4.1 ; NO -> J4.2 ; NC -> J4.3"),
 ("relay","K2","Relay 2, SRD-05VDC-SL-C","C35449",1,"coil+ -> +5V ; coil- -> Q2 drain ; COM -> J5.1 ; NO -> J5.2 ; NC -> J5.3"),
 ("relay","Q1","AO3400A driver, relay 1","C20917",1,"G -> RLY1 (GPIO4) + R18 ; D -> K1 coil- ; S -> GND"),
 ("relay","Q2","AO3400A driver, relay 2","C20917",1,"G -> RLY2 (GPIO5) + R19 ; D -> K2 coil- ; S -> GND"),
 ("relay","D1","Schottky flyback, K1 coil","C2758511",1,"A -> Q1 drain ; K -> +5V"),
 ("relay","D2","Schottky flyback, K2 coil","C2758511",1,"A -> Q2 drain ; K -> +5V"),
 ("relay","R18","100 k gate pull-down Q1","C17900",1,"Q1 gate -> GND"),
 ("relay","R19","100 k gate pull-down Q2","C17900",1,"Q2 gate -> GND"),
 ("relay","R10","1 k, LED3 series","C4410",1,"+5V -> LED3 anode side"),
 ("relay","R11","1 k, LED4 series","C4410",1,"+5V -> LED4 anode side"),
 ("relay","LED3","Green LED: relay 1 energised","C2986059",1,"A -> R10 ; K -> Q1 drain"),
 ("relay","LED4","Green LED: relay 2 energised","C2986059",1,"A -> R11 ; K -> Q2 drain"),
 ("relay","J4","Relay 1 terminal 3P: COM/NO/NC","C474953",1,"1 COM ; 2 NO ; 3 NC (mains side)"),
 ("relay","J5","Relay 2 terminal 3P: COM/NO/NC","C474953",1,"1 COM ; 2 NO ; 3 NC (mains side)"),
 ("relay","C17","100 nF 1206, +5V relay 1","C24497",1,"+5V / GND"),
 ("relay","C18","100 nF 1206, +5V relay 2","C24497",1,"+5V / GND"),
 ("pzem","J6","JST XH 4P header for PZEM-004T","C594232",1,"1 -> +5V ; 2 -> PZEM_RX line ; 3 -> PZEM_TX (via divider) ; 4 -> GND (check module label order)"),
 ("pzem","R16","4.7 k, PZEM_TX divider top","C17936",1,"J6.TX -> R16 -> GPIO18"),
 ("pzem","R4","10 k, PZEM_TX divider bottom","C17902",1,"GPIO18 -> GND"),
 ("pzem","C16","100 nF 1206, header 5 V","C24497",1,"+5V / GND"),
 ("disp","J7","1x4 header: 16x2 I2C LCD","C2691448",1,"1 GND ; 2 +5V ; 3 SDA_5V ; 4 SCL_5V (check module order)"),
 ("disp","J8","1x4 header: I2C OLED","C2691448",1,"1 GND ; 2 +3V3 ; 3 SCL ; 4 SDA (check module order)"),
 ("disp","J9","1x20 female header: 12864 ST7920","C41413628",1,"1 GND ; 2 +5V ; 3 V0 ; 4 RS=CS ; 5 R/W=MOSI ; 6 E=CLK ; 15 PSB (SJ1 to GND) ; 17 RST ; 18 VOUT ; 19 BLA ; 20 BLK"),
 ("disp","U5","PCA9306 I2C level shifter (16x2 only)","C33196",1,"VREF1 -> +3V3 ; VREF2 -> +5V ; SDA1/SCL1 -> GPIO8/9 ; SDA2/SCL2 -> J7"),
 ("disp","U6","SN74AHCT125 3.3 V to 5 V buffer (12864 only)","C155176",1,"1A..4A -> GPIO10/11/12/14 ; 1Y..4Y -> J9 RS/RW/E/RST ; VCC -> +5V ; OE low"),
 ("disp","Q3","AO3400A backlight switch","C20917",1,"G -> GPIO13 + R20 ; D -> J9 BLK ; S -> GND"),
 ("disp","RV2","10 k trimmer, 12864 contrast","C58159",1,"ends -> +5V and VOUT (verify) ; wiper -> V0"),
 ("disp","R12","4.7 k, SDA pull-up 3V3","C17936",1,"SDA -> +3V3"),
 ("disp","R13","4.7 k, SCL pull-up 3V3","C17936",1,"SCL -> +3V3"),
 ("disp","R14","4.7 k, SDA_5V pull-up (DNP with backpack)","C17936",1,"SDA_5V -> +5V"),
 ("disp","R15","4.7 k, SCL_5V pull-up (DNP with backpack)","C17936",1,"SCL_5V -> +5V"),
 ("disp","R5","10 k, PCA9306 EN pull-up","C17902",1,"EN -> +5V"),
 ("disp","R20","100 k gate pull-down Q3","C17900",1,"Q3 gate -> GND"),
 ("disp","C12","100 nF 1206, U5 VREF1","C24497",1,"+3V3 / GND"),
 ("disp","C13","100 nF 1206, U5 VREF2","C24497",1,"+5V / GND"),
 ("disp","C14","100 nF 1206, U6 VCC","C24497",1,"+5V / GND"),
 ("disp","C19","100 nF 1206, display 5 V","C24497",1,"+5V / GND"),
 ("ui","SW3","START button","C318884",1,"1 -> GPIO1 ; 2 -> GND"),
 ("ui","SW4","STOP button","C318884",1,"1 -> GPIO2 ; 2 -> GND"),
 ("ui","SW5","MENU button","C318884",1,"1 -> GPIO6 ; 2 -> GND"),
 ("ui","LED1","Red LED: power","C965798",1,"A -> R8 -> +3V3 ; K -> GND"),
 ("ui","LED2","Red LED: Wi-Fi / status","C965798",1,"A -> R9 <- GPIO16 ; K -> GND"),
 ("ui","R8","1 k, LED1 series","C4410",1,"LED1"),
 ("ui","R9","1 k, LED2 series","C4410",1,"LED2"),
 ("ui","BZ1","OPTIONAL passive buzzer MLT-8530","C94599",1,"+ -> +5V ; - -> Q4 drain"),
 ("ui","Q4","AO3400A buzzer driver (optional)","C20917",1,"G -> GPIO15 + R21 ; D -> BZ1 ; S -> GND"),
 ("ui","D3","Schottky flyback across buzzer (optional)","C2758511",1,"A -> Q4 drain ; K -> +5V"),
 ("ui","R21","100 k gate pull-down Q4 (optional)","C17900",1,"Q4 gate -> GND"),
 ("ui","J10","Float input 1 screw terminal 2P","C474952",1,"1 -> GPIO39 ; 2 -> GND"),
 ("ui","J11","Float input 2 screw terminal 2P","C474952",1,"1 -> GPIO40 ; 2 -> GND"),
 ("ui","J12","1x6 spare header","C492405",1,"+3V3 ; GND ; GPIO41 ; GPIO42 ; GPIO47 ; GPIO48"),
 ("ui","R6","10 k optional pull-up IN1 (DNP)","C17902",1,"GPIO39 -> +3V3"),
 ("ui","R7","10 k optional pull-up IN2 (DNP)","C17902",1,"GPIO40 -> +3V3"),
 ("ui","R17","4.7 k spare","C17936",1,"free"),
]
# the CSV only knows the MPN by C# (TBD for the antenna)
TOTAL = sum(p[4] for p in P)
secmap = {s[0]: s for s in S}
e = html.escape

def info(c):
    r = LC.get(c)
    if not r:
        return ("TBD", "", "", "")
    return (r["MPN"], r["Manufacturer"], r["Stock (2026-10-28)"], r["Unit price USD"])

CSS = """
:root{--bg:#f3f1fb;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#d9dde7}
@media (prefers-color-scheme:dark){:root{--bg:#0d1017;--fg:#e8ebf2;--mut:#9aa5b5;--card:#171c26;--line:#2b3340}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}
main{max-width:1280px;margin:0 auto;padding:16px 16px 56px}
.hero{border-radius:16px;padding:20px 22px;color:#fff;background:linear-gradient(120deg,#ff4d4d,#ff9f43 25%,#2fbf71 50%,#4895ef 75%,#a66cff);box-shadow:0 6px 20px rgba(0,0,0,.18)}
.hero h1{margin:0;font-size:1.6rem;text-shadow:0 1px 3px rgba(0,0,0,.35)}.hero p{margin:6px 0 0;font-size:14px;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.warn{background:var(--card);border-left:5px solid #ff4d4d;border-radius:8px;padding:8px 12px;margin:14px 0;font-size:13px}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
input[type=search]{padding:8px 12px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--fg);min-width:240px}
progress{width:220px;height:14px;accent-color:#2fbf71}button{border:0;border-radius:8px;padding:7px 12px;background:#ff9f43;color:#1b1b1b;font-weight:700;cursor:pointer}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 10px}.chip{padding:3px 10px;border-radius:999px;color:#fff;font-size:12px;font-weight:700;text-decoration:none}
.card{background:var(--card);border-radius:14px;padding:12px 14px;margin:14px 0;border-left:8px solid var(--c);box-shadow:0 2px 10px rgba(0,0,0,.08)}
.card h2{margin:0 0 4px;font-size:1.1rem;color:var(--c)}.cnt{font-weight:500;color:var(--mut);font-size:13px;margin-left:8px}
.mut{color:var(--mut);font-size:13px}.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:color-mix(in srgb,var(--c,#888) 18%,transparent)}tr:hover td{background:color-mix(in srgb,var(--c,#888) 7%,transparent)}
tr.done td{opacity:.42;text-decoration:line-through}input.ck{width:20px;height:20px;accent-color:var(--c)}
a{color:#3b82f6}.tag{display:inline-block;padding:0 7px;border-radius:6px;font-size:11px;font-weight:700;background:#ff4d4d;color:#fff}
.opt{background:#9aa5b5}.sub{margin:3px 0 8px;color:var(--mut);font-size:13px}
@media print{.bar{display:none}}
"""

def bom_page():
    out = []
    a = out.append
    a(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot BOM by Section</title><style>{CSS}</style></head><body><main>')
    a('<div class="hero"><h1>BorePilot - BOM by section</h1><p>ESP32-S3 submersible pump controller. Tick each part as you add it to the EasyEDA schematic; progress is saved in this browser.</p></div>')
    a(f'<div class="warn"><b>Plan stage, 2026-10-28.</b> {TOTAL} placed parts in {len(S)} sections. The connections column is the <b>planned</b> net list from PLAN.md, not a drawn schematic. Stock/price are LCSC page values from 2026-10-28 (quantity-1 tier); check before ordering. Mains is involved: engineer review first. Passive refs (R/C) and counts are planned and may change in the schematic.</div>')
    a(f'<div class="bar"><input type="search" id="q" placeholder="Filter by ref, name, MPN, LCSC # ..."><progress id="pg" value="0" max="{TOTAL}"></progress><span id="pt" class="mut"></span><button id="rs">Reset ticks</button></div>')
    a('<div class="chips">' + "".join(f'<a class="chip" style="background:{s[2]}" href="#{s[0]}">{e(s[1])}</a>' for s in S) + '</div>')
    gt = 0.0
    for sid, name, col, desc in S:
        parts = [p for p in P if p[0] == sid]
        cost = 0.0
        for p in parts:
            r = LC.get(p[3])
            try:
                cost += p[4] * float(r["Unit price USD"])
            except Exception:
                pass
        gt += cost
        a(f'<section class="card" id="{sid}" style="--c:{col}"><h2>{e(name)}<span class="cnt">{len(parts)} parts, about ${cost:.2f}</span></h2><p class="sub">{e(desc)}</p><div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>MPN</th><th>LCSC #</th><th>Qty</th><th>Stock</th><th>$</th><th>Planned connections (pin &rarr; net)</th></tr></thead><tbody>')
        for _, ref, nm, c, q, conn in parts:
            mpn, mk, st, pr = info(c)
            lk = f'<a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a>' if c.startswith("C") else '<span class="tag">TBD</span>'
            opt = ' <span class="tag opt">optional</span>' if "ptional" in nm or "DNP" in nm else ""
            cc = "<br>".join(e(x.strip()) for x in conn.split(";"))
            a(f'<tr data-ref="{ref}"><td><input type="checkbox" class="ck" data-k="{ref}"></td><td><b>{ref}</b></td><td>{e(nm)}{opt}</td><td>{e(mpn)}</td><td>{lk}</td><td>{q}</td><td class="mut">{e(st)}</td><td class="mut">{e(pr)}</td><td><details><summary>{len(conn.split(";"))} nets</summary>{cc}</details></td></tr>')
        a('</tbody></table></div></section>')
    a(f'<p class="mut">Rough parts total at quantity-1 prices: about ${gt:.2f} (antenna and external modules not included; PCB extra).</p>')
    a("""<script>
const K='borepilot-bom-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const cks=[...document.querySelectorAll('.ck')];
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('pg').value=n;document.getElementById('pt').textContent=n+' / '+cks.length+' placed';
cks.forEach(c=>c.closest('tr').classList.toggle('done',c.checked));try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});
document.getElementById('rs').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};
document.getElementById('q').oninput=ev=>{const v=ev.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none')};
upd();
</script></main></body></html>""")
    return "".join(out)

# ---------------------------------------------------------------- diagram
def box(x, y, w, h, col, title, lines, dashed=False):
    d = ' stroke-dasharray="7 5"' if dashed else ""
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-width="2"{d}/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{col}" fill-opacity=".9"/><text x="{x+12}" y="{y+18}" font-size="13" font-weight="700" fill="#fff">{e(title)}</text>'
    for i, l in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+46+i*17}" font-size="12" fill="currentColor">{e(l)}</text>'
    return s + "</g>"

def arrow(pts, col, label="", dashed=False, lx=None, ly=None):
    d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
    dd = ' stroke-dasharray="7 5"' if dashed else ""
    mid = pts[len(pts)//2]
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3"{dd} marker-end="url(#ah{col[1:]})"/>'
    if label:
        s += f'<text x="{lx if lx is not None else mid[0]+6}" y="{ly if ly is not None else mid[1]-6}" font-size="11" font-weight="700" fill="{col}">{e(label)}</text>'
    return s

def diagram_page():
    cols = {"mains":"#ff4d4d","pwr":"#ff9f43","v33":"#4895ef","sig":"#2fbf71","uart":"#00bcd4","i2c":"#ff4d94","usb":"#a66cff","net":"#f4c20d"}
    svg = ['<svg viewBox="0 0 1240 830" width="1240" role="img" aria-label="BorePilot connection map" style="font-family:system-ui,Segoe UI,sans-serif;color:var(--fg)"><defs>']
    for c in cols.values():
        svg.append(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    svg.append('</defs>')
    # row 1
    svg.append(box(20, 20, 370, 170, "#ff4d4d", "MAINS INPUT 230 V (hazardous)", ["J2 AC in (L, N)", "J3 AC tap -> PZEM voltage input", "U2 HLK-5M05  AC -> 5 V 1 A", "no fuse / varistor (upstream breaker)", "isolation slot between AC and 5 V pins"]))
    svg.append(box(440, 20, 360, 170, "#ff9f43", "5 V / 3.3 V POWER", ["D4 / D5 Schottky OR: HLK and USB", "C1 470 uF bulk on +5V", "U3 SGM2212 LDO  +5V -> +3V3", "C2..C6 10 uF, C15 100 nF"]))
    svg.append(box(850, 20, 370, 170, "#4895ef", "USB-C PROGRAMMING", ["J1 C165948 USB-C 16-pin", "R1, R2 5.1 k on CC1 / CC2", "U4 USBLC6-2SC6 ESD on D+/D-", "native USB: flash + log + auto-reset", "no USB-UART chip"]))
    # row 2
    svg.append(box(20, 260, 370, 190, "#2fbf71", "RELAYS 1 and 2", ["K1, K2 SRD-05VDC-SL-C (coil 5 V)", "Q1, Q2 AO3400A low-side drivers", "D1, D2 flyback, R18/R19 100 k pull-down", "LED3, LED4 green: relay energised", "J4, J5  COM / NO / NC screw terminals", "pulse a contactor, not a motor"]))
    svg.append(box(440, 260, 360, 190, "#a66cff", "ESP32-S3 CORE", ["U1 ESP32-S3-WROOM-1U-N16R8", "ANT1 U.FL->SMA pigtail + ANT2 antenna", "SW1 EN reset, SW2 BOOT", "R3 10 k EN pull-up, C8 100 nF", "Wi-Fi + ESP-NOW (2.4 GHz)", "GPIO33-37 kept free (octal PSRAM)"]))
    svg.append(box(850, 260, 370, 190, "#00bcd4", "PZEM-004T LINK", ["J6 JST XH 4P: 5V, TX, RX, GND", "UART1 9600 8N1", "R16 4.7 k + R4 10 k divider on PZEM TX", "(module TX assumed 5 V, unverified)", "PZEM voltage input from J3 (mains)", "CT clamp on the pump cable"]))
    # row 3
    svg.append(box(20, 530, 400, 235, "#ff4d94", "DISPLAY OPTIONS (fit one)", ["A  J7 16x2 I2C LCD  5 V via U5 PCA9306", "B  J8 I2C OLED  3.3 V direct", "C  J9 12864 ST7920 via U6 74AHCT125 5 V", "   RV2 contrast trimmer, Q3 backlight, SJ1 PSB=GND", "I2C: GPIO8 SDA, GPIO9 SCL", "12864: GPIO10 CS, 11 MOSI, 12 CLK, 14 RST, 13 BL", "R12/R13 pull-ups 3V3, R14/R15 5V side (DNP)"]))
    svg.append(box(450, 530, 380, 235, "#f4c20d", "BUTTONS / LEDs / INPUTS", ["SW3 START GPIO1, SW4 STOP GPIO2, SW5 MENU GPIO6", "LED1 red power, LED2 red status GPIO16", "BZ1 + Q4 + D3 optional buzzer, GPIO15", "J10, J11 float inputs GPIO39, GPIO40", "J12 spare: 3V3, GND, GPIO41/42/47/48", "TXD0 / RXD0 test pads GPIO43 / 44"]))
    svg.append(box(860, 530, 360, 235, "#f4c20d", "WIRELESS TANK UNIT (separate board)", ["second ESP32 / ESP32-C3 at the tank", "sensor: float, ultrasonic or pressure", "ESP-NOW to BorePilot, no router", "level %, state, battery, sequence no.", "BorePilot: stale > 120 s -> use floats", "run-time cap stops pump if link lost"], dashed=True))
    # arrows
    svg.append(arrow([(390,105),(440,105)], cols["pwr"], "+5V_HLK", lx=394, ly=98))
    svg.append(arrow([(850,105),(800,105)], cols["pwr"], "VBUS", lx=806, ly=98))
    svg.append(arrow([(620,190),(620,260)], cols["v33"], "+3V3", lx=626, ly=232))
    svg.append(arrow([(470,190),(470,225),(390,225),(390,300)], cols["pwr"], "+5V coils", lx=396, ly=222))
    svg.append(arrow([(930,190),(930,225),(800,225),(800,310)], cols["usb"], "D+ D- GPIO19/20", lx=808, ly=222))
    svg.append(arrow([(440,370),(390,370)], cols["sig"], "GPIO4 / 5", lx=396, ly=364))
    svg.append(arrow([(800,370),(850,370)], cols["uart"], "GPIO17/18", lx=802, ly=364))
    svg.append(arrow([(480,450),(480,490),(220,490),(220,530)], cols["i2c"], "I2C / SPI", lx=232, ly=484))
    svg.append(arrow([(640,450),(640,530)], cols["sig"], "buttons LEDs inputs", lx=646, ly=500))
    svg.append(arrow([(780,450),(780,490),(1040,490),(1040,530)], cols["net"], "ESP-NOW 2.4 GHz (wireless)", dashed=True, lx=800, ly=484))
    svg.append(arrow([(205,190),(205,260)], cols["mains"], "mains stays on this side of the slot", lx=212, ly=232))
    svg.append("</svg>")
    leg = "".join(f'<span><i style="background:{c}"></i>{n}</span>' for n, c in [("mains 230 V", cols["mains"]), ("5 V", cols["pwr"]), ("3.3 V", cols["v33"]), ("GPIO signals", cols["sig"]), ("UART", cols["uart"]), ("I2C / display", cols["i2c"]), ("USB", cols["usb"]), ("wireless", cols["net"])])
    gp = [("EN","reset button","SW1"),("0","BOOT button","SW2"),("19 / 20","USB D- / D+","J1 via U4"),("8 / 9","I2C SDA / SCL","J8, J7 via U5"),("17 / 18","PZEM TX / RX","J6"),("4","RLY1","Q1 -> K1"),("5","RLY2","Q2 -> K2"),("10","LCD CS (RS)","U6 -> J9"),("11","LCD MOSI (R/W)","U6 -> J9"),("12","LCD CLK (E)","U6 -> J9"),("14","LCD RST","U6 -> J9"),("13","LCD backlight","Q3"),("1","START button","SW3"),("2","STOP button","SW4"),("6","MENU button","SW5"),("15","buzzer (optional)","Q4 -> BZ1"),("16","status LED","LED2"),("39","float input 1","J10"),("40","float input 2","J11"),("41, 42, 47, 48","spare","J12"),("43 / 44","TXD0 / RXD0 pads","test pads")]
    gtab = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in gp)
    steps = [
     ("Power", "#ff9f43", ["J2 L, N -> U2 AC pins, and J3 (AC tap).", "U2 +Vo -> D4 anode; D4 cathode -> +5V. U2 -Vo -> GND.", "J1 VBUS -> D5 anode; D5 cathode -> +5V.", "+5V -> C1 470 uF, C6, C2, U3 VIN. U3 VOUT -> +3V3 -> C3, C4."]),
     ("USB", "#4895ef", ["J1 CC1 -> R1 -> GND, CC2 -> R2 -> GND.", "J1 D+ pins (A6, B6) -> U4 -> GPIO20; D- pins (A7, B7) -> U4 -> GPIO19.", "Shield -> GND (decide direct or 1 M || 100 nF)."]),
     ("Relays", "#2fbf71", ["GPIO4 -> Q1 gate (+ R18 to GND); Q1 drain -> K1 coil- (+ D1 to +5V); K1 coil+ -> +5V.", "GPIO5 -> Q2 gate (+ R19); Q2 drain -> K2 coil-; same as above.", "K1/K2 COM, NO, NC -> J4/J5 pins 1, 2, 3 (mains side of the slot).", "LED3/LED4 + R10/R11 between +5V and the Q drains."]),
     ("PZEM", "#00bcd4", ["J6: +5V, GND, ESP TX (GPIO17) -> PZEM RX.", "PZEM TX -> R16 4.7 k -> GPIO18, R4 10 k from GPIO18 to GND."]),
     ("Displays", "#ff4d94", ["J8 OLED: +3V3, GND, SDA GPIO8, SCL GPIO9, R12/R13 pull-ups.", "J7 16x2: GPIO8/9 -> U5 low side; U5 high side -> J7 SDA/SCL, +5V.", "J9 12864: GPIO10/11/12/14 -> U6 -> J9 pins 4, 5, 6, 17. SJ1 bridges J9 pin 15 to GND.", "Q3 gate GPIO13 + R20; drain -> J9 pin 20 (BLK). RV2 on V0/VOUT."]),
     ("UI / IO", "#f4c20d", ["SW3/SW4/SW5 from GPIO1/2/6 to GND (internal pull-ups).", "LED1 + R8 on +3V3; LED2 + R9 from GPIO16.", "J10/J11 pin 1 -> GPIO39/40, pin 2 -> GND.", "BZ1 + Q4 + D3 on GPIO15 (optional)."]),
    ]
    ctab = "".join(f'<div class="stepcard" style="--c:{c}"><h3>{n}</h3><ol>' + "".join(f"<li>{e(i)}</li>" for i in l) + "</ol></div>" for n, c, l in steps)
    extra = """
h2{font-size:1.15rem;margin:26px 0 8px}.wrap{overflow-x:auto;background:var(--card);border-radius:12px;padding:8px;box-shadow:0 2px 10px rgba(0,0,0,.08)}
svg{display:block;margin:auto}.legend span{display:inline-block;margin-right:16px;font-size:12px;color:var(--mut)}.legend i{display:inline-block;width:22px;height:4px;margin-right:5px;vertical-align:middle}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px}.stepcard{background:var(--card);border-radius:12px;padding:8px 14px;border-left:8px solid var(--c);box-shadow:0 2px 10px rgba(0,0,0,.08)}
.stepcard h3{margin:4px 0;color:var(--c)}.stepcard li{font-size:13px;margin:3px 0}
"""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot Connection Map</title><style>{CSS}{extra}</style></head><body><main>'
            '<div class="hero"><h1>BorePilot - connection map</h1><p>ESP32-S3 pump controller: mains and USB power, relays with COM/NO/NC, PZEM link, three display options, wireless tank unit. Grouped in the same eight sections as the BOM page.</p></div>'
            '<div class="warn"><b>Plan stage.</b> This is a block-level map of the <u>planned</u> design from PLAN.md. No schematic or PCB exists and nothing has been built or tested. Mains is involved: engineer review before any mains power.</div>'
            f'<p class="legend">{leg}</p><div class="wrap">{"".join(svg)}</div>'
            f'<h2>Wiring order, section by section</h2><div class="grid">{ctab}</div>'
            f'<h2>GPIO assignment (ESP32-S3-WROOM-1U-N16R8)</h2><div class="scroll"><table><thead><tr><th>GPIO</th><th>Function</th><th>Goes to</th></tr></thead><tbody>{gtab}</tbody></table></div>'
            '<p class="mut">See <a href="bom-by-section.html">bom-by-section.html</a> for the tick-list of every part, with LCSC numbers.</p></main></body></html>')

os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
open(os.path.join(ROOT, "docs/bom-by-section.html"), "w", encoding="utf-8").write(bom_page())
open(os.path.join(ROOT, "docs/connection-diagram.html"), "w", encoding="utf-8").write(diagram_page())
print("parts", TOTAL, "BOM csv lines", sum(int(r["Qty"]) for r in rows))
