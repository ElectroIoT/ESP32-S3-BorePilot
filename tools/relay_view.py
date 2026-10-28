"""Relay circuit view: an easy-to-read picture of one relay channel (used by gen_wiring.py)."""
import html

e = html.escape
C5, CS, CR, CG = "#fb8c00", "#2fbf71", "#8d6e63", "#8a93a3"


def pill(x, y, text, c, anchor="l"):
    pw = 6.6 * len(text) + 14
    x0 = x if anchor == "l" else x - pw
    return (f'<rect x="{x0:.0f}" y="{y-9}" width="{pw:.0f}" height="18" rx="9" fill="{c}"/>'
            f'<text x="{x0+8:.0f}" y="{y+4}" class="pill">{e(text)}</text>')


def flag(x, y, text, c):
    pw = 7 * len(text) + 12
    return (f'<rect x="{x-pw/2:.0f}" y="{y-8}" width="{pw:.0f}" height="16" rx="4" fill="{c}"/>'
            f'<text x="{x-pw/2+6:.0f}" y="{y+4}" class="flag">{e(text)}</text>')


def ln(pts, c, w=2):
    return '<polyline points="' + " ".join(f"{a},{b}" for a, b in pts) + f'" fill="none" stroke="{c}" stroke-width="{w}"/>'


def dot(x, y, c):
    return f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c}"/>'


def gnd(x, y):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+8}" stroke="{CG}" stroke-width="2"/>'
            f'<line x1="{x-10}" y1="{y+8}" x2="{x+10}" y2="{y+8}" stroke="{CG}" stroke-width="2"/>'
            f'<line x1="{x-6}" y1="{y+12}" x2="{x+6}" y2="{y+12}" stroke="{CG}" stroke-width="2"/>'
            f'<line x1="{x-2}" y1="{y+16}" x2="{x+2}" y2="{y+16}" stroke="{CG}" stroke-width="2"/>'
            f'<text x="{x+14}" y="{y+14}" class="net" fill="{CG}">GND</text>')


def res_v(x, y1, y2, c, label):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y1+6}" stroke="{c}" stroke-width="2"/>'
            f'<rect x="{x-6}" y="{y1+6}" width="12" height="{y2-y1-12}" fill="var(--card)" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x}" y1="{y2-6}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="2"/>'
            f'<text x="{x+12}" y="{(y1+y2)/2+4}" class="pin">{e(label)}</text>')


def relay_circuit(ch):
    n = str(ch)
    K, Q, D = f"K{n}", f"Q{n}", f"D{n}"
    R = "R18" if ch == 1 else "R19"
    RL = "R10" if ch == 1 else "R11"
    LED = "LED3" if ch == 1 else "LED4"
    J = f"J{3 + ch}"
    gp = 4 if ch == 1 else 5
    o = ['<svg viewBox="0 0 720 500" width="720" height="500" class="cdia">']
    o.append(f'<text x="14" y="26" class="ref" style="font-size:15px">RELAY {n}: GPIO{gp} to RLY{n} to {Q} to {K} coil, contacts to {J}</text>')
    o.append('<rect x="36" y="92" width="424" height="62" rx="6" fill="#e53935" fill-opacity=".06" stroke="#e53935" stroke-width="1.5" stroke-dasharray="6 4"/>')
    o.append('<text x="456" y="150" text-anchor="end" class="lab" style="fill:#e53935!important;font-weight:700">MAINS SIDE (230 V)</text>')
    o.append('<rect x="200" y="60" width="140" height="150" rx="7" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>')
    o.append(f'<text x="208" y="78" class="ref">{K}</text><text x="232" y="78" class="role">SRD-05VDC-SL-C</text><text x="208" y="90" class="lab">[C35449]</text>')
    o.append('<text x="206" y="114" class="pin">5 COM</text><text x="206" y="139" class="pin">3 NC</text><text x="334" y="114" text-anchor="end" class="pin">2 NO</text>')
    o.append('<rect x="250" y="174" width="40" height="22" fill="none" stroke="var(--fg)" stroke-width="1.5"/><text x="270" y="189" text-anchor="middle" class="lab">coil</text>')
    o.append('<text x="206" y="204" class="pin">4</text><text x="334" y="204" text-anchor="end" class="pin">1</text>')
    o.append(ln([(200, 110), (150, 110)], CR) + pill(150, 110, f"COM{n}", CR, "r"))
    o.append(ln([(200, 135), (150, 135)], CR) + pill(150, 135, f"NC{n}", CR, "r"))
    o.append(ln([(340, 110), (390, 110)], CR) + pill(390, 110, f"NO{n}", CR, "l"))
    o.append(flag(60, 160, "+5V", C5) + ln([(60, 168), (60, 300)], C5, 3))
    o.append(ln([(200, 185), (60, 185)], C5) + dot(60, 185, C5))
    o.append(ln([(340, 185), (420, 185), (420, 300)], CS) + dot(420, 300, CS))
    o.append(pill(430, 300, f"RLY{n}_D", CS, "l"))
    o.append(ln([(60, 300), (190, 300)], C5) + ln([(230, 300), (420, 300)], CS))
    o.append('<polygon points="230,288 230,312 192,300" fill="var(--card)" stroke="var(--fg)" stroke-width="2"/><line x1="190" y1="288" x2="190" y2="312" stroke="var(--fg)" stroke-width="3"/>')
    o.append(dot(60, 300, C5))
    o.append(f'<text x="160" y="278" class="ref">{D}</text><text x="182" y="278" class="role">UMW SS34B</text><text x="120" y="332" class="lab">bar (cathode) toward +5V = flyback clamp</text>')
    o.append(ln([(420, 300), (420, 350)], CS))
    o.append(f'<rect x="390" y="350" width="60" height="70" rx="6" fill="var(--card)" stroke="var(--line)" stroke-width="2"/><text x="396" y="366" class="ref">{Q}</text><text x="396" y="381" class="lab">AO3400A</text>')
    o.append('<text x="438" y="364" class="pin">D</text><text x="394" y="410" class="pin">G</text><text x="438" y="416" class="pin">S</text>')
    o.append(ln([(390, 395), (300, 395)], CS) + dot(330, 395, CS) + pill(300, 395, f"RLY{n}", CS, "r"))
    o.append(res_v(330, 405, 445, CG, f"{R} 100k") + ln([(330, 445), (330, 470)], CG) + gnd(330, 470))
    o.append(ln([(420, 420), (420, 470)], CG) + gnd(420, 470))
    o.append(flag(560, 66, "+5V", C5) + ln([(560, 74), (560, 95)], C5))
    o.append(res_v(560, 95, 135, C5, f"{RL} 1k") + ln([(560, 135), (560, 160)], CS))
    o.append('<polygon points="548,160 572,160 560,184" fill="var(--card)" stroke="var(--fg)" stroke-width="2"/><line x1="548" y1="186" x2="572" y2="186" stroke="var(--fg)" stroke-width="3"/>')
    o.append(f'<text x="582" y="178" class="pin">{LED} green</text><text x="582" y="192" class="lab">on when relay is on</text>')
    pw = 6.6 * len(f"RLY{n}_D") + 14
    o.append(ln([(560, 186), (560, 231)], CS) + pill(560 - pw / 2, 240, f"RLY{n}_D", CS, "l"))
    o.append(f'<text x="14" y="420" class="ref">{J} screw terminal</text><text x="14" y="437" class="pin">pin 1 = COM{n}</text><text x="14" y="453" class="pin">pin 2 = NO{n}</text><text x="14" y="469" class="pin">pin 3 = NC{n}</text><text x="14" y="485" class="lab">(same names as the brown flags)</text>')
    o.append("</svg>")
    return "".join(o)


EXPLAIN = (
    '<ol class="how">'
    '<li><b>Idle:</b> the GPIO is low and the 100 k resistor holds the gate low, so the MOSFET is off and no current flows in the coil. COM is connected to <b>NC</b>.</li>'
    '<li><b>ON:</b> the ESP32 pulls the <b>RLYn</b> flag high. The MOSFET turns on and pulls the <b>RLYn_D</b> node to GND. Current flows +5V, coil, MOSFET, GND, and the relay switches: COM is now connected to <b>NO</b>.</li>'
    '<li><b>LED:</b> +5V, resistor, LED, <b>RLYn_D</b>. It lights only while the MOSFET is on.</li>'
    '<li><b>Diode:</b> when the MOSFET switches off the coil kicks voltage back. The diode (bar on the +5V side) gives that current a loop so the MOSFET is not damaged.</li>'
    '<li><b>Net flags that must exist:</b> <b>RLYn</b> on the MOSFET gate (from page 2) and <b>RLYn_D</b> on the coil / diode / drain node. Without them the relay never switches and the LED never lights.</li>'
    '</ol>')


def relay_view_card():
    return ('<section class="card" id="relayview" style="--c:#2fbf71"><h3>Relay circuit view: one picture per channel</h3>'
            '<p class="mut">How one channel really works: GPIO, MOSFET, relay coil, with the contacts on the mains side. Wire colours: orange = +5V, green = signals, brown = relay contacts, grey = GND.</p>'
            '<div class="flexrow"><div class="scroll">' + relay_circuit(1) + '</div><div class="scroll">' + relay_circuit(2) + '</div></div>' + EXPLAIN + '</section>')
