"""Make the README images for BorePilot: social cards (PNG, PIL) and two animated SVGs.
Run from the repo root:  python -X utf8 -I tools/make_assets.py
Input: docs/images/board-top.png (screenshot of the routed PCB1 in EasyEDA)."""
import os, base64, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs/images")
SOC = os.path.join(IMG, "social")
os.makedirs(SOC, exist_ok=True)
F = "C:/Windows/Fonts/"
def font(name, size): return ImageFont.truetype(F + name, size)
BOLD, REG, LIGHT = "segoeuib.ttf", "segoeui.ttf", "segoeuil.ttf"
NAVY1, NAVY2, ACC, ACC2, TXT, MUT = (10, 22, 48), (16, 56, 92), (63, 208, 255), (47, 191, 113), (240, 246, 255), (150, 175, 205)

board2d = Image.open(os.path.join(IMG, "board-top.png")).convert("RGBA")
REN = os.path.join(IMG, "renders")


def cutout(path, thr=14):
    """Load a 3D render and make the black background transparent with a soft edge."""
    im = Image.open(path).convert("RGB")
    im = im.crop((0, 0, im.width, im.height - 26))
    px = im.load()
    mask = Image.new("L", im.size, 255)
    mp = mask.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if max(r, g, b) < thr:
                mp[x, y] = 0
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


iso = cutout(os.path.join(REN, "blue_iso.png"))
top3d = cutout(os.path.join(REN, "blue_top.png"))
bot3d = cutout(os.path.join(REN, "blue_bottom.png"))
board = iso


def gradient(w, h, c1=NAVY1, c2=NAVY2):
    g = Image.new("RGB", (w, h), c1)
    px = g.load()
    for y in range(h):
        for x in range(w):
            t = (0.6 * y / h + 0.4 * x / w)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return g


def board_card(size_w, rot=0, src=None):
    b = (src or board).copy()
    r = size_w / b.width
    b = b.resize((size_w, int(b.height * r)), Image.LANCZOS)
    sh = Image.new("RGBA", (b.width + 120, b.height + 120), (0, 0, 0, 0))
    a = b.split()[3].point(lambda v: 150 if v > 40 else 0)
    black = Image.new("RGBA", b.size, (0, 0, 0, 255))
    black.putalpha(a)
    sh.alpha_composite(black, (60, 78))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    sh.alpha_composite(b, (60, 60))
    return sh


def chips(im, items, x, y, fnt, fg=TXT, pad=(16, 8)):
    """Draw rounded chips (translucent) with text; returns the composited image and the next x."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    pos = []
    for t in items:
        w = od.textlength(t, font=fnt)
        od.rounded_rectangle((x, y, x + w + 2 * pad[0], y + fnt.size + 2 * pad[1] + 4), 20, fill=(255, 255, 255, 30), outline=(120, 190, 255, 140))
        pos.append((x + pad[0], y + pad[1] - 2, t))
        x += w + 2 * pad[0] + 12
    im = Image.alpha_composite(im, ov)
    d = ImageDraw.Draw(im)
    for px, py, t in pos:
        d.text((px, py), t, font=fnt, fill=fg)
    return im


CHIPS = ["ESP32-S3", "2 relays", "PZEM-004T", "Home Assistant", "5 V HLK module", "USB-C"]


def hero():
    W, H = 1200, 630
    im = gradient(W, H).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    d.text((60, 70), "OPEN-SOURCE IoT PUMP CONTROLLER", font=font(BOLD, 22), fill=ACC)
    d.text((56, 108), "BorePilot", font=font(BOLD, 112), fill=TXT)
    d.text((60, 245), "Smart borewell pump controller", font=font(LIGHT, 38), fill=TXT)
    d.text((60, 295), "Start, stop and protect a single-phase submersible", font=font(REG, 26), fill=MUT)
    d.text((60, 331), "pump from Home Assistant, with live voltage, current", font=font(REG, 26), fill=MUT)
    d.text((60, 367), "and energy readings and dry-run protection.", font=font(REG, 26), fill=MUT)
    f = font(REG, 22)
    im = chips(im, CHIPS[:3], 60, 440, f)
    im = chips(im, CHIPS[3:], 60, 500, f)
    d = ImageDraw.Draw(im)
    d.text((60, 580), "100 x 90 mm, 2 layers  |  ElectroIoT.in", font=font(REG, 20), fill=MUT)
    bc = board_card(470)
    im.alpha_composite(bc, (W - bc.width - 20, (H - bc.height) // 2 + 8))
    im.convert("RGB").save(os.path.join(SOC, "01_hero_og_1200x630.png"))


def square():
    W = H = 1080
    im = gradient(W, H).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    t = "BorePilot"
    fw = font(BOLD, 130)
    d.text(((W - d.textlength(t, font=fw)) / 2, 50), t, font=fw, fill=TXT)
    s = "ESP32-S3 smart borewell pump controller"
    fs = font(LIGHT, 38)
    d.text(((W - d.textlength(s, font=fs)) / 2, 215), s, font=fs, fill=ACC)
    bc = board_card(700)
    im.alpha_composite(bc, ((W - bc.width) // 2, 290))
    im = chips(im, ["Wi-Fi + ESPHome", "2 x SPDT relay", "Energy metering", "Dry-run guard"], 70, 960, font(REG, 24))
    d = ImageDraw.Draw(im)
    d.text((W - 270, 1030), "ElectroIoT.in", font=font(REG, 22), fill=MUT)
    im.convert("RGB").save(os.path.join(SOC, "02_square_1080x1080.png"))


FEATURES = [
    ("Pump control", "START and STOP relay with NO / COM / NC terminals, for a contactor or a small pump"),
    ("Energy and protection", "PZEM-004T v3 link: voltage, current, power, energy, frequency; dry-run and over-current stop"),
    ("Home Assistant", "Wi-Fi, ESPHome, external antenna (ESP32-S3-WROOM-1U), same entities as the ESPHome package"),
    ("Three display choices", "16x2 I2C LCD, I2C OLED or 128x64 ST7920 on one board, with START / STOP / MENU buttons"),
    ("Level inputs", "Two float-switch inputs and a spare GPIO header; optional wireless tank node over ESP-NOW"),
    ("Clean 5 V power", "Hi-Link HLK-5M05 module, 470 uF bulk, 3.3 V LDO, USB-C for flashing and logging"),
    ("Mains aware layout", "Slots between mains and the relay coils, 6.4 mm clearance goal, labelled terminals"),
    ("Open design", "Schematic, PCB, BOM and build guides in the repository, MIT licence"),
]


def features():
    W, H = 1080, 1640
    im = gradient(W, H).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    y = 250
    for i in range(len(FEATURES)):
        od.rounded_rectangle((50, y, W - 50, y + 140), 22, fill=(255, 255, 255, 22), outline=(120, 190, 255, 110))
        y += 160
    im = Image.alpha_composite(im, ov)
    d = ImageDraw.Draw(im)
    d.text((60, 50), "BorePilot", font=font(BOLD, 90), fill=TXT)
    d.text((64, 160), "What it does", font=font(LIGHT, 40), fill=ACC)
    y = 250
    for i, (t, s) in enumerate(FEATURES):
        d.ellipse((75, y + 38, 125, y + 88), fill=ACC2)
        d.text((92, y + 42), str(i + 1), font=font(BOLD, 30), fill=(8, 30, 20))
        d.text((150, y + 18), t, font=font(BOLD, 32), fill=TXT)
        line, ly = "", y + 66
        for w_ in s.split():
            test = (line + " " + w_).strip()
            if d.textlength(test, font=font(REG, 23)) > W - 250:
                d.text((150, ly), line, font=font(REG, 23), fill=MUT)
                ly += 30
                line = w_
            else:
                line = test
        d.text((150, ly), line, font=font(REG, 23), fill=MUT)
        y += 160
    d.text((60, H - 60), "ElectroIoT.in  |  github.com/ElectroIoT/ESP32-S3-BorePilot", font=font(REG, 22), fill=MUT)
    im.convert("RGB").save(os.path.join(SOC, "03_features_1080x1640.png"))


def b64png(im, width):
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), im.size


STYLE = """<style>
.t{font-family:'Segoe UI',Arial,sans-serif}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes dash{to{stroke-dashoffset:-36}}
@keyframes appear{0%,2%{opacity:0;transform:translateX(-14px)}8%,%END%{opacity:1;transform:none}%END2%,100%{opacity:0}}
</style>"""


def hero_svg():
    data, (bw, bh) = b64png(iso, 600)
    x0, y0 = 1200 - bw - 30, (520 - bh) // 2
    dots = "".join(f'<circle cx="{20 + i * 60}" cy="{20 + j * 60}" r="1.4" fill="#3fd0ff" opacity=".12"/>' for i in range(21) for j in range(9))
    style = STYLE.replace("%END%", "90%").replace("%END2%", "96%")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="1200" height="520">{style}
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1630"/><stop offset="1" stop-color="#0e4466"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3fd0ff" stop-opacity=".55"/><stop offset="1" stop-color="#3fd0ff" stop-opacity="0"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000" flood-opacity=".55"/></filter>
<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="#3fd0ff" stop-opacity="0"/><stop offset=".5" stop-color="#3fd0ff" stop-opacity=".9"/><stop offset="1" stop-color="#3fd0ff" stop-opacity="0"/></linearGradient>
<clipPath id="board"><rect x="{x0}" y="{y0}" width="{bw}" height="{bh}"/></clipPath></defs>
<rect width="1200" height="520" rx="26" fill="url(#bg)"/>{dots}
<ellipse cx="{x0 + bw / 2}" cy="{y0 + bh / 2 + 20}" rx="{bw / 2 + 40}" ry="{bh / 2 + 10}" fill="url(#glow)"><animate attributeName="opacity" values=".5;1;.5" dur="4s" repeatCount="indefinite"/></ellipse>
<g class="t">
<text x="60" y="92" fill="#3fd0ff" font-size="20" font-weight="700" letter-spacing="3">OPEN-SOURCE IoT PUMP CONTROLLER</text>
<text x="56" y="190" fill="#f0f6ff" font-size="104" font-weight="700">BorePilot</text>
<text x="60" y="245" fill="#f0f6ff" font-size="34" font-weight="300">Smart borewell pump controller</text>
<text x="60" y="292" fill="#96afcd" font-size="22">ESP32-S3  |  2 relays  |  PZEM-004T  |  Home Assistant  |  USB-C</text>
<g font-size="20" fill="#f0f6ff">
<rect x="60" y="330" width="156" height="44" rx="22" fill="#2fbf71" opacity=".28"/><text x="84" y="359">Start / Stop</text>
<rect x="230" y="330" width="156" height="44" rx="22" fill="#3fd0ff" opacity=".28"/><text x="256" y="359">V / A / kWh</text>
<rect x="400" y="330" width="178" height="44" rx="22" fill="#f4c20d" opacity=".28"/><text x="424" y="359">Dry-run guard</text>
<rect x="60" y="388" width="156" height="44" rx="22" fill="#a66cff" opacity=".28"/><text x="88" y="417">Wi-Fi + OTA</text>
<rect x="230" y="388" width="156" height="44" rx="22" fill="#ff6b6b" opacity=".28"/><text x="262" y="417">230 V aware</text>
</g>
<text x="60" y="480" fill="#96afcd" font-size="17">100 x 90 mm, 2 layers  |  MIT licence  |  ElectroIoT.in</text></g>
<g style="animation:float 5s ease-in-out infinite"><g filter="url(#sh)"><image href="data:image/png;base64,{data}" x="{x0}" y="{y0}" width="{bw}" height="{bh}"/></g>
<g clip-path="url(#board)"><rect x="{x0}" y="{y0}" width="{bw}" height="6" fill="url(#scan)"><animate attributeName="y" values="{y0};{y0 + bh};{y0}" dur="6s" repeatCount="indefinite"/></rect></g></g>
<g fill="none" stroke="#3fd0ff" stroke-width="3.5" stroke-linecap="round">
<path d="M{x0 + 330} 80 q40 -34 80 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" repeatCount="indefinite"/></path>
<path d="M{x0 + 312} 98 q58 -56 116 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" begin=".3s" repeatCount="indefinite"/></path>
<path d="M{x0 + 294} 116 q76 -78 152 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" begin=".6s" repeatCount="indefinite"/></path></g>
<circle cx="{x0 + 370}" cy="112" r="6" fill="#3fd0ff"/>
</svg>"""
    open(os.path.join(IMG, "borepilot-hero-animated.svg"), "w", encoding="utf-8").write(svg)


def flow_svg():
    def node(x, y, w, h, t, s, col):
        return (f'<g class="t"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#12263f" stroke="{col}" stroke-width="2"/>'
                f'<text x="{x + w / 2}" y="{y + 36}" text-anchor="middle" fill="#f0f6ff" font-size="21" font-weight="700">{t}</text>'
                f'<text x="{x + w / 2}" y="{y + 62}" text-anchor="middle" fill="#96afcd" font-size="14">{s}</text></g>')

    def link(pid, d, col, dur, begin="0s"):
        return (f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="10 8" style="animation:dash 1.6s linear infinite"/>'
                f'<circle r="6" fill="{col}"><animateMotion dur="{dur}" begin="{begin}" repeatCount="indefinite" calcMode="linear"><mpath href="#{pid}"/></animateMotion></circle>')
    style = STYLE.replace("%END%", "90%").replace("%END2%", "96%")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460" width="1200" height="460">{style}
<rect width="1200" height="460" rx="26" fill="#0a1630"/>
<text class="t" x="600" y="46" text-anchor="middle" fill="#3fd0ff" font-size="25" font-weight="700">How BorePilot works</text>
{node(40, 150, 230, 100, "Home Assistant", "dashboard, phone, automations", "#3fd0ff")}
{node(390, 120, 250, 160, "BorePilot", "ESP32-S3, HLK 5 V, relays, display", "#2fbf71")}
{node(760, 60, 200, 90, "Relay 1", "START contactor", "#f4c20d")}
{node(760, 250, 200, 90, "Relay 2", "STOP / spare, NO + NC", "#f4c20d")}
{node(1010, 150, 160, 100, "Pump", "single phase, 230 V", "#ff6b6b")}
{node(390, 350, 250, 80, "PZEM-004T", "V, A, W, kWh, Hz", "#3fd0ff")}
{node(40, 350, 230, 80, "Tank node", "ESP-NOW level (optional)", "#96afcd")}
{link("a1", "M270 190 L390 190", "#3fd0ff", "2.4s")}
{link("a2", "M390 215 L270 215", "#3fd0ff", "3s", "0.6s")}
{link("a3", "M640 170 C700 170 700 105 760 105", "#2fbf71", "2s")}
{link("a4", "M640 230 C700 230 700 295 760 295", "#2fbf71", "2s", "0.5s")}
{link("a5", "M960 105 C1000 105 1000 185 1010 190", "#f4c20d", "1.6s", "1s")}
{link("a6", "M960 295 C1000 295 1000 215 1010 210", "#f4c20d", "1.6s", "1.4s")}
{link("a7", "M515 350 L515 280", "#3fd0ff", "1.8s")}
{link("a8", "M270 385 C330 385 340 300 390 270", "#96afcd", "3s", "0.2s")}
<text class="t" x="330" y="180" text-anchor="middle" fill="#96afcd" font-size="14">Wi-Fi</text>
<g transform="translate(1090 296)"><g style="transform-origin:0 0;animation:spin 2.2s linear infinite"><circle r="20" fill="none" stroke="#ff6b6b" stroke-width="3"/><path d="M0 0 L16 -6 M0 0 L-12 12 M0 0 L-4 -17" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"/></g></g>
<g fill="#3fd0ff"><circle cx="1070" cy="400" r="5"><animate attributeName="cy" values="380;430" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>
<circle cx="1100" cy="400" r="5"><animate attributeName="cy" values="380;430" dur="1.6s" begin=".5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" begin=".5s" repeatCount="indefinite"/></circle>
<circle cx="1130" cy="400" r="5"><animate attributeName="cy" values="380;430" dur="1.6s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" begin="1s" repeatCount="indefinite"/></circle></g>
</svg>"""
    open(os.path.join(IMG, "borepilot-flow-animated.svg"), "w", encoding="utf-8").write(svg)


def anatomy_svg():
    data, (bw, bh) = b64png(top3d, 640)
    X, Y = 40, 40
    k = bw / 882.0
    items = [
        ("Mains in", "J2 AC in, J3 tap for the PZEM", 150, 55, "#ff6b6b"),
        ("HLK-5M05", "230 V AC to 5 V / 1 A module", 190, 220, "#ff6b6b"),
        ("ESP32-S3-WROOM-1U", "Wi-Fi, external antenna, 16 MB flash", 680, 130, "#a66cff"),
        ("START / STOP / MENU", "buttons, RESET and BOOT", 510, 380, "#3fd0ff"),
        ("128x64 LCD header", "or 16x2 I2C LCD / I2C OLED", 830, 520, "#ff4d94"),
        ("2 x SPDT relay", "NO / COM / NC, slots around the coil", 250, 580, "#f4c20d"),
        ("Relay terminals", "J4, J5: NO, COM, NC", 190, 720, "#2fbf71"),
        ("Float inputs", "J10, J11 level switches", 540, 715, "#c0a000"),
    ]
    n = len(items)
    dur = n * 1.8
    style = STYLE.replace("%END%", "11%").replace("%END2%", "13%")
    # each item visible for one slot of the cycle: use per-item delay, keyframes pattern repeats via animation-duration = dur
    style = style.replace("@keyframes appear{0%,2%{opacity:0;transform:translateX(-14px)}8%,11%{opacity:1;transform:none}13%,100%{opacity:0}}",
                          "@keyframes appear{0%{opacity:0;transform:translateX(-14px)}6%,%HOLD%{opacity:1;transform:none}%FADE%,100%{opacity:0}}").replace("%HOLD%", f"{100 / n * 0.83:.1f}%").replace("%FADE%", f"{100 / n * 0.95:.1f}%")
    W, H = 1200, bh + 2 * Y
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{style}',
           f'<rect width="{W}" height="{H}" rx="26" fill="#0a1630"/>',
           f'<image href="data:image/png;base64,{data}" x="{X}" y="{Y}" width="{bw}" height="{bh}"/>',
           f'<text class="t" x="{W - 40}" y="64" text-anchor="end" fill="#3fd0ff" font-size="28" font-weight="700">Board tour</text>']
    for i, (t, sub, px, py, col) in enumerate(items):
        cx, cy = X + px * k, Y + py * k
        ly = 130 + i * ((H - 200) / (n - 1))
        lx = 740
        out.append(f'<g style="opacity:0;animation:appear {dur}s linear infinite;animation-delay:{i * 1.8:.1f}s">'
                   f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="14" fill="none" stroke="{col}" stroke-width="3"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="5" fill="{col}"/>'
                   f'<path d="M{cx + 14:.0f} {cy:.0f} L{lx - 10} {ly:.0f}" stroke="{col}" stroke-width="2" fill="none" stroke-dasharray="6 5"/>'
                   f'<rect x="{lx}" y="{ly - 30:.0f}" width="420" height="60" rx="14" fill="#12263f" stroke="{col}" stroke-width="2"/>'
                   f'<text class="t" x="{lx + 18}" y="{ly - 4:.0f}" fill="#f0f6ff" font-size="21" font-weight="700">{t}</text>'
                   f'<text class="t" x="{lx + 18}" y="{ly + 20:.0f}" fill="#96afcd" font-size="15">{sub}</text></g>')
    out.append("</svg>")
    open(os.path.join(IMG, "borepilot-anatomy-animated.svg"), "w", encoding="utf-8").write("\n".join(out))


hero(); square(); features(); hero_svg(); flow_svg(); anatomy_svg()
print("assets written")
