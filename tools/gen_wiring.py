"""Generate docs/wiring-by-section.html: one pin-to-net wiring diagram per section,
grouped under the same 5 schematic pages as docs/schematic-guide.html.
Run from the repo root:  python -I tools/gen_wiring.py
Planned nets only (no schematic exists yet); pin names must be checked against the EasyEDA symbols.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages as G
import gen_schematic_guide as GG

e = html.escape
ROOT = G.ROOT

def pins(s):
    out = []
    for it in s.split(","):
        a, b = it.split("=")
        out.append((a.strip(), b.strip() or None))
    return out

# ref -> pin list "pin=net". Net "-" = not connected. Pin names follow the planned symbols; verify in EasyEDA.
D = {
 "J2":"1=L,2=N", "J3":"1=L,2=N", "U2":"AC(L)=L,AC(N)=N,+Vo=+5V_HLK,-Vo=GND",
 "D4":"A=+5V_HLK,K=+5V", "D5":"A=VBUS,K=+5V", "C1":"+=+5V,-=GND",
 "U3":"VIN=+5V,GND=GND,VOUT=+3V3",
 "C2":"1=+5V,2=GND","C3":"1=+3V3,2=GND","C5":"1=+5V,2=GND","C6":"1=+5V,2=GND","C15":"1=+5V_HLK,2=GND",
 "J1":"A1B12 GND=GND,B1A12 GND=GND,A4B9 VBUS=VBUS,B4A9 VBUS=VBUS,A5 CC1=CC1,B5 CC2=CC2,A6 DP1=USB_DP_J1,B6 DP2=USB_DP_J1,A7 DN1=USB_DN_J1,B7 DN2=USB_DN_J1,A8 SBU1=-,B8 SBU2=-,EH1 shell=GND,EH2 shell=GND,EH3 shell=GND,EH4 shell=GND",
 "U4":"1 I/O1 in=USB_DP_J1,6 I/O1 out=USB_DP,3 I/O2 in=USB_DN_J1,4 I/O2 out=USB_DN,5 VBUS=VBUS,2 GND=GND",
 "R1":"1=CC1,2=GND","R2":"1=CC2,2=GND","C7":"1=VBUS,2=GND","C11":"1=VBUS,2=GND",
 "U1":"3V3=+3V3,GND=GND,EN=EN,IO0=IO0_BOOT,IO19=USB_DN,IO20=USB_DP,IO4=RLY1,IO5=RLY2,IO8=SDA,IO9=SCL,IO10=LCD_CS,IO11=LCD_MOSI,IO12=LCD_CLK,IO13=LCD_BL,IO14=LCD_RST,IO15=BUZZ,IO16=LED_ST,IO17=PZEM_TXD,IO18=PZEM_RXD,IO1=BTN_START,IO2=BTN_STOP,IO6=BTN_MENU,IO39=IN1,IO40=IN2,IO41=SP1,IO42=SP2,IO47=SP3,IO48=SP4,TXD0=TXD0,RXD0=RXD0",
 "ANT1":"U.FL=ANT_RF,SMA=ANT_SMA","ANT2":"SMA=ANT_SMA",
 "SW1":"1=EN,2=GND","SW2":"1=IO0_BOOT,2=GND","R3":"1=+3V3,2=EN","C4":"1=+3V3,2=GND","C8":"1=EN,2=GND","C9":"1=+3V3,2=GND","C10":"1=+3V3,2=GND",
 "K1":"coil 1=+5V,coil 2=RLY1_D,COM=COM1,NO=NO1,NC=NC1","K2":"coil 1=+5V,coil 2=RLY2_D,COM=COM2,NO=NO2,NC=NC2",
 "Q1":"G=RLY1,D=RLY1_D,S=GND","Q2":"G=RLY2,D=RLY2_D,S=GND",
 "D1":"A=RLY1_D,K=+5V","D2":"A=RLY2_D,K=+5V","R18":"1=RLY1,2=GND","R19":"1=RLY2,2=GND",
 "R10":"1=+5V,2=LED3_A","LED3":"A=LED3_A,K=RLY1_D","R11":"1=+5V,2=LED4_A","LED4":"A=LED4_A,K=RLY2_D",
 "J4":"1 COM=COM1,2 NO=NO1,3 NC=NC1","J5":"1 COM=COM2,2 NO=NO2,3 NC=NC2","C17":"1=+5V,2=GND","C18":"1=+5V,2=GND",
 "J6":"1=+5V,2=PZEM_TXD,3=PZEM_TX_RAW,4=GND","R16":"1=PZEM_TX_RAW,2=PZEM_RXD","R4":"1=PZEM_RXD,2=GND","C16":"1=+5V,2=GND",
 "J7":"1=GND,2=+5V,3=SDA_5V,4=SCL_5V","J8":"1=GND,2=+3V3,3=SCL,4=SDA",
 "J9":"1 VSS=GND,2 VDD=+5V,3 V0=V0,4 RS=LCD_RS_5V,5 R/W=LCD_RW_5V,6 E=LCD_E_5V,15 PSB=PSB,17 RST=LCD_RST_5V,18 VOUT=VOUT,19 BLA=+5V,20 BLK=BL_K",
 "U5":"1 GND=GND,2 VREF1=+3V3,3 SCL1=SCL,4 SDA1=SDA,5 SDA2=SDA_5V,6 SCL2=SCL_5V,7 VREF2=+5V,8 EN=PCA_EN",
 "U6":"14 VCC=+5V,7 GND=GND,1 1OE=GND,4 2OE=GND,10 3OE=GND,13 4OE=GND,2 1A=LCD_CS,5 2A=LCD_MOSI,9 3A=LCD_CLK,12 4A=LCD_RST,3 1Y=LCD_RS_5V,6 2Y=LCD_RW_5V,8 3Y=LCD_E_5V,11 4Y=LCD_RST_5V",
 "Q3":"G=LCD_BL,D=BL_K,S=GND","RV2":"1=+5V,2 wiper=V0,3=VOUT","SJ1":"1=PSB,2=GND",
 "R12":"1=SDA,2=+3V3","R13":"1=SCL,2=+3V3","R14":"1=SDA_5V,2=+5V","R15":"1=SCL_5V,2=+5V","R5":"1=+5V,2=PCA_EN","R20":"1=LCD_BL,2=GND",
 "C12":"1=+3V3,2=GND","C13":"1=+5V,2=GND","C14":"1=+5V,2=GND","C19":"1=+5V,2=GND",
 "SW3":"1=BTN_START,2=GND","SW4":"1=BTN_STOP,2=GND","SW5":"1=BTN_MENU,2=GND",
 "LED1":"A=LED1_A,K=GND","R8":"1=+3V3,2=LED1_A","LED2":"A=LED2_A,K=GND","R9":"1=LED_ST,2=LED2_A",
 "BZ1":"+=+5V,-=BUZ_D","Q4":"G=BUZZ,D=BUZ_D,S=GND","D3":"A=BUZ_D,K=+5V","R21":"1=BUZZ,2=GND",
 "J10":"1=IN1,2=GND","J11":"1=IN2,2=GND","J12":"1=+3V3,2=GND,3=SP1,4=SP2,5=SP3,6=SP4",
 "R6":"1=IN1,2=+3V3","R7":"1=IN2,2=+3V3","R17":"1=-,2=-",
}
EXTRA = {"SJ1": ("disp", "Solder jumper: PSB to GND (default bridged = serial mode)", "no BOM")}

for p in G.P:
    assert p[1] in D, "missing pin data for " + p[1]

SYM = {"GND", "+5V", "+3V3", "+5V_HLK", "VBUS"}
def col(net):
    if net == "GND": return "#8a93a3"
    if net in ("+5V", "+5V_HLK", "VBUS"): return "#fb8c00"
    if net == "+3V3": return "#f4b400"
    if net == "L": return "#e53935"
    if net == "N": return "#1e88e5"
    if net.startswith(("USB_", "CC")): return "#8e24aa"
    if net in ("SDA", "SCL", "SDA_5V", "SCL_5V") or net.startswith("LCD_") or net in ("V0", "VOUT", "PSB", "BL_K", "PCA_EN"): return "#ec407a"
    if net.startswith("PZEM"): return "#00bcd4"
    if net.startswith(("COM", "NO", "NC")): return "#8d6e63"
    if net.endswith("_D") or net.endswith("_A"): return "#2fbf71"
    if net.startswith("ANT"): return "#607d8b"
    return "#2fbf71"

sec_parts = {}
for p in G.P:
    sec_parts.setdefault(p[0], []).append((p[1], p[2], p[3]))
for ref, (sid, nm, c) in EXTRA.items():
    sec_parts[sid].append((ref, nm, c))
sec_of_net = {}
for sid, lst in sec_parts.items():
    for ref, nm, c in lst:
        for pin, net in pins(D[ref]):
            if net and net != "-":
                sec_of_net.setdefault(net, set()).add(sid)
secname = {s[0]: s[1] for s in G.S}
page_of = {}
for i, pg in enumerate(GG.PAGES, 1):
    for s in pg[2]:
        page_of[s] = i

def gnd_sym(x, y, c):
    return (f'<line x1="{x}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+14}" y1="{y-6}" x2="{x+14}" y2="{y+6}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+18}" y1="{y-4}" x2="{x+18}" y2="{y+4}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+22}" y1="{y-2}" x2="{x+22}" y2="{y+2}" stroke="{c}" stroke-width="2"/>')

def section_svg(sid):
    parts = sec_parts[sid]
    PX0, PXR = 8, 300
    y = 16
    boxes, pin_pos = [], []
    for ref, nm, c in parts:
        pl = pins(D[ref])
        h = 34 + 16 * len(pl)
        boxes.append((ref, nm, c, pl, y, h))
        for k, (pin, net) in enumerate(pl):
            pin_pos.append((ref, pin, net, y + 40 + 16 * k))
        y += h + 14
    lanes = []
    for ref, pin, net, py in pin_pos:
        if net and net != "-" and net not in SYM and net not in lanes:
            lanes.append(net)
    laneX = {n: 350 + 24 * i for i, n in enumerate(lanes)}
    W = 350 + 24 * len(lanes) + 40
    H = y + 150
    o = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="dia">']
    for ref, nm, c, pl, by, bh in boxes:
        o.append(f'<g class="box"><rect x="{PX0}" y="{by}" width="{PXR-PX0}" height="{bh}" rx="7" fill="var(--card)" stroke="var(--line)"/>')
        o.append(f'<text x="16" y="{by+14}" class="ref">{e(ref)}</text><text x="{16+8*len(ref)+10}" y="{by+14}" class="role">{e(nm[:46])}</text>')
        o.append(f'<text x="16" y="{by+27}" class="lab">[{e(c)}]</text></g>')
    for ref, pin, net, py in pin_pos:
        o.append(f'<text x="{PXR-14}" y="{py+3.5}" text-anchor="end" class="pin">{e(pin)}</text>')
        if not net or net == "-":
            o.append(f'<g class="w"><line x1="{PXR}" y1="{py}" x2="{PXR+10}" y2="{py}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+10}" y1="{py-4}" x2="{PXR+16}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+16}" y1="{py-4}" x2="{PXR+10}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><text x="{PXR+22}" y="{py+3.5}" class="lab">no connect</text></g>')
            continue
        c = col(net)
        if net == "GND":
            o.append(f'<g class="w" data-net="GND">{gnd_sym(PXR, py, c)}<text x="{PXR+28}" y="{py+3.5}" class="net" fill="{c}">GND</text></g>')
        elif net in SYM:
            wd = 7 * len(net) + 10
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{PXR+14}" y2="{py}" stroke="{c}" stroke-width="3"/><rect x="{PXR+14}" y="{py-8}" width="{wd}" height="16" rx="4" fill="{c}"/><text x="{PXR+19}" y="{py+3.5}" class="flag">{e(net)}</text></g>')
        else:
            lx = laneX[net]
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{lx}" y2="{py}" stroke="{c}" stroke-width="2"/><circle cx="{PXR}" cy="{py}" r="3" fill="{c}"/><circle cx="{lx}" cy="{py}" r="2.6" fill="{c}"/></g>')
    for net in lanes:
        ys = [py for _, _, n, py in pin_pos if n == net]
        lx = laneX[net]
        c = col(net)
        others = sorted(sec_of_net[net] - {sid}, key=lambda s: page_of[s])
        ext = ""
        if others:
            ext = " -> " + ", ".join(f"p{page_of[s]}" for s in others)
        if len(ys) > 1:
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{lx}" y1="{min(ys)}" x2="{lx}" y2="{max(ys)}" stroke="{c}" stroke-width="2"/></g>')
        o.append(f'<text x="{lx+3}" y="{max(ys)+12}" class="net" fill="{c}" transform="rotate(70 {lx+3} {max(ys)+12})">{e(net)}</text>')
        if ext:
            o.append(f'<text x="{lx+3}" y="{max(ys)+12}" class="ext" transform="translate({7*len(net)+8} 0) rotate(70 {lx+3} {max(ys)+12})">{e(ext)}</text>')
    o.append("</svg>")
    return "".join(o)

CSS = """:root{--bg:#f3f1fb;--fg:#1c2330;--mut:#5b6677;--card:#fff;--line:#c9d1dc}
@media (prefers-color-scheme:dark){:root{--bg:#0d1017;--fg:#e8ebf2;--mut:#9aa5b5;--card:#171c26;--line:#323b49}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,Segoe UI,sans-serif}main{max-width:1320px;margin:0 auto;padding:16px 16px 56px}
.hero{border-radius:16px;padding:18px 22px;color:#fff;background:linear-gradient(120deg,#ff4d4d,#ff9f43 25%,#2fbf71 50%,#4895ef 75%,#a66cff);box-shadow:0 6px 20px rgba(0,0,0,.18)}
.hero h1{margin:0;font-size:1.5rem;text-shadow:0 1px 3px rgba(0,0,0,.35)}.hero p{margin:6px 0 0;font-size:14px;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.warn{background:var(--card);border-left:5px solid #ff4d4d;border-radius:8px;padding:8px 12px;margin:14px 0;font-size:13px}
.legend{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5}.legend span{display:inline-block;margin-right:14px;font-size:13px;color:var(--mut)}.legend i{display:inline-block;width:22px;height:5px;border-radius:3px;margin-right:5px;vertical-align:middle}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}.chip{padding:3px 12px;border-radius:999px;color:#fff;font-size:12px;font-weight:700;text-decoration:none}
.pagehead{display:flex;align-items:center;gap:10px;margin:26px 0 4px}.pagehead h2{margin:0;color:var(--c);font-size:1.25rem}.pn{width:34px;height:34px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:800}
.card{background:var(--card);border-radius:14px;padding:12px;margin:12px 0;border-left:8px solid var(--c);box-shadow:0 2px 10px rgba(0,0,0,.08)}
h3{margin:0 0 6px;font-size:1.05rem;color:var(--c)}.cnt{font-weight:400;color:var(--mut);font-size:13px;margin-left:8px}.mut{color:var(--mut);font-size:13px}.scroll{overflow-x:auto}
svg.dia text{font-family:system-ui,Segoe UI,sans-serif;fill:var(--fg)}.ref{font-size:12px;font-weight:700}.role{font-size:10.5px;fill:var(--mut)!important}.lab{font-size:9.5px;fill:var(--mut)!important}
.pin{font-size:11px}.net{font-size:11px;font-weight:700}.ext{font-size:10px;fill:var(--mut)!important}.flag{font-size:10px;font-weight:700;fill:#10151c!important}
.w{cursor:pointer;transition:opacity .15s}svg.hl .w{opacity:.15}svg.hl .w.on{opacity:1}.w.done line,.w.done polyline{stroke-dasharray:4 4}
a{color:#3b82f6}.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:8px 0}progress{width:260px;height:14px;accent-color:#2fbf71}
button{border:0;border-radius:8px;padding:7px 12px;background:#ff9f43;color:#1b1b1b;font-weight:700;cursor:pointer}.secck{cursor:pointer}.secck input{width:20px;height:20px;accent-color:var(--c);vertical-align:middle}
.card.alldone{box-shadow:0 0 0 3px #2fbf71 inset}.card.alldone h3{text-decoration:line-through;opacity:.7}@media print{.legend{display:none}}"""

def build():
    o = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot Wiring by Section</title><style>{CSS}</style></head><body><main>']
    o.append('<div class="hero"><h1>BorePilot - wiring by section</h1><p>One pin-to-net diagram per section, grouped under the same 5 schematic pages as the <a style="color:#fff" href="schematic-guide.html">schematic guide</a>. Draw each box as a part, then connect the pins that share a net.</p></div>')
    o.append('<div class="warn"><b>Plan stage.</b> Planned nets from PLAN.md, not a finished schematic. Each box lists pins by the names planned for the symbol (module pin numbers where I know them: USBLC6, PCA9306, 74AHCT125, J9 header; others by function). <b>Check every pin name against the EasyEDA symbol and datasheet</b> (SGM2212, SRD relay, USB-C, PZEM, display modules). 230 V AC on J2, J3, U2, J4, J5: engineer review before mains power.</div>')
    o.append('<div class="legend"><span><i style="background:#e53935"></i>L</span><span><i style="background:#1e88e5"></i>N</span><span><i style="background:#fb8c00"></i>5 V / VBUS</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#8a93a3"></i>GND</span><span><i style="background:#2fbf71"></i>GPIO / control</span><span><i style="background:#00bcd4"></i>UART</span><span><i style="background:#ec407a"></i>I2C / display</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#8d6e63"></i>relay contact</span> &middot; <b>hover</b> a wire = highlight net, <b>click</b> = mark done</div>')
    o.append('<div class="bar"><progress id="pg" value="0" max="1"></progress><span id="pt" class="mut"></span><button id="rs">Reset all ticks</button></div>')
    o.append('<div class="chips">' + "".join(f'<a class="chip" style="background:{pg[3]}" href="#{pg[0]}">{e(pg[1].split(" - ")[0])}</a>' for pg in GG.PAGES) + '</div>')
    o.append('<p class="mut">Lane labels: <b>name -&gt; p2, p3</b> means the same net continues on schematic page 2 and 3 (net label). GND, 5 V and 3.3 V are drawn as symbols/flags at the pin.</p>')
    for n, pg in enumerate(GG.PAGES, 1):
        o.append(f'<div class="pagehead" id="{pg[0]}" style="--c:{pg[3]}"><div class="pn">{n}</div><h2>{e(pg[1])}</h2></div>')
        if not pg[2]:
            o.append(f'<div class="card" style="--c:{pg[3]}"><p class="mut">No parts: cover and notes only, see the schematic guide.</p></div>')
        for sid in pg[2]:
            sc = next(s for s in G.S if s[0] == sid)
            cnt = len(sec_parts[sid])
            o.append(f'<section class="card" id="sec-{sid}" data-sec="{sid}" style="--c:{sc[2]}"><h3><label class="secck"><input type="checkbox" class="seccb" data-sec="{sid}"> {e(sc[1])}</label><span class="cnt">{cnt} parts, page {n}</span><span class="cnt secprog" data-sec="{sid}"></span></h3><p class="mut">{e(sc[3])}</p><div class="scroll">{section_svg(sid).replace("<svg ", f"<svg data-sec=\"{sid}\" ", 1)}</div></section>')
    o.append("""<script>
const K='borepilot-wiring-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const svgs=[...document.querySelectorAll('svg.dia')];
function nets(svg){return [...new Set([...svg.querySelectorAll('.w[data-net]')].map(w=>w.dataset.net))]}
function apply(){let done=0,total=0;
 svgs.forEach(svg=>{const sid=svg.dataset.sec,ns=nets(svg);let d=0;
  svg.querySelectorAll('.w[data-net]').forEach(w=>w.classList.toggle('done',!!st[sid+'|'+w.dataset.net]));
  ns.forEach(n=>{if(st[sid+'|'+n])d++});
  const card=document.getElementById('sec-'+sid);card.classList.toggle('alldone',d===ns.length&&ns.length>0);
  card.querySelector('.seccb').checked=(d===ns.length&&ns.length>0);
  card.querySelector('.secprog').textContent=d+' / '+ns.length+' nets wired';
  done+=d;total+=ns.length});
 document.getElementById('pg').max=total;document.getElementById('pg').value=done;
 document.getElementById('pt').textContent=done+' / '+total+' nets wired';
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
svgs.forEach(svg=>{const sid=svg.dataset.sec;
 svg.querySelectorAll('.w[data-net]').forEach(w=>{
  w.addEventListener('mouseenter',()=>{svg.classList.add('hl');svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.add('on'))});
  w.addEventListener('mouseleave',()=>{svg.classList.remove('hl');svg.querySelectorAll('.w.on').forEach(x=>x.classList.remove('on'))});
  w.addEventListener('click',()=>{const k=sid+'|'+w.dataset.net;if(st[k])delete st[k];else st[k]=1;apply()});
 })});
document.querySelectorAll('.seccb').forEach(cb=>cb.addEventListener('change',()=>{
 const sid=cb.dataset.sec,svg=document.querySelector('svg.dia[data-sec="'+sid+'"]');
 nets(svg).forEach(n=>{if(cb.checked)st[sid+'|'+n]=1;else delete st[sid+'|'+n]});apply()}));
document.getElementById('rs').onclick=()=>{if(confirm('Clear all ticks?')){st={};apply()}};
apply();
</script></main></body></html>""")
    return "".join(o)

open(os.path.join(ROOT, "docs/wiring-by-section.html"), "w", encoding="utf-8").write(build())

JS = """<script>
document.querySelectorAll('svg.dia').forEach(svg=>{
 svg.querySelectorAll('.w[data-net]').forEach(w=>{
  w.addEventListener('mouseenter',()=>{svg.classList.add('hl');svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.add('on'))});
  w.addEventListener('mouseleave',()=>{svg.classList.remove('hl');svg.querySelectorAll('.w.on').forEach(x=>x.classList.remove('on'))});
  w.addEventListener('click',()=>{svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.toggle('done'))});
 });
});
</script>"""
os.makedirs(os.path.join(ROOT, "docs/wiring"), exist_ok=True)
allsec = [s for s in G.S]
for i, sc in enumerate(allsec):
    sid = sc[0]
    nav = "".join(f'<a class="chip" style="background:{s[2]};opacity:{1 if s[0]==sid else .55}" href="{s[0]}.html">{e(s[1])}</a>' for s in allsec)
    rows = "".join(f'<tr><td><b>{e(r)}</b></td><td>{e(nm)}</td><td>{e(c)}</td></tr>' for r, nm, c in sec_parts[sid])
    pg = page_of[sid]
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BorePilot wiring - {e(sc[1])}</title><style>{CSS}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{padding:4px 8px;border-bottom:1px solid var(--line);text-align:left}}</style></head><body><main>'
            f'<div class="hero"><h1>{e(sc[1])}</h1><p>Schematic page {pg}. {e(sc[3])}</p></div>'
            f'<div class="chips" style="margin-top:12px">{nav}</div>'
            f'<p class="mut">Back to <a href="../wiring-by-section.html">all sections</a> &middot; <a href="../schematic-guide.html">schematic guide</a> &middot; hover a wire = highlight net, click = mark done. Planned nets; check pin names against the EasyEDA symbols.</p>'
            f'<section class="card" style="--c:{sc[2]}"><div class="scroll">{section_svg(sid)}</div></section>'
            f'<section class="card" style="--c:{sc[2]}"><h3>Parts in this section ({len(sec_parts[sid])})</h3><table><thead><tr><th>Ref</th><th>Part</th><th>LCSC</th></tr></thead><tbody>{rows}</tbody></table></section>{JS}</main></body></html>')
    open(os.path.join(ROOT, f"docs/wiring/{sid}.html"), "w", encoding="utf-8").write(page)
print("wiring-by-section.html written; sections:", len(sec_parts), "parts incl. SJ1:", sum(len(v) for v in sec_parts.values()))
