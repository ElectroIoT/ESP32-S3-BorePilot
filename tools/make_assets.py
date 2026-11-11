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

board = Image.open(os.path.join(IMG, "board-top.png")).convert("RGBA")


def gradient(w, h, c1=NAVY1, c2=NAVY2):
    g = Image.new("RGB", (w, h), c1)
    px = g.load()
    for y in range(h):
        for x in range(w):
            t = (0.6 * y / h + 0.4 * x / w)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return g


def board_card(size_w, rot=0):
    b = board.copy()
    r = size_w / b.width
    b = b.resize((size_w, int(b.height * r)), Image.LANCZOS)
    sh = Image.new("RGBA", (b.width + 80, b.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 50, 40 + b.width, 50 + b.height), 18, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    sh.alpha_composite(b, (40, 40))
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


def board_b64():
    b = board.convert("RGB")
    b = b.resize((480, int(480 * b.height / b.width)), Image.LANCZOS)
    buf = io.BytesIO()
    b.save(buf, "JPEG", quality=86)
    return base64.b64encode(buf.getvalue()).decode(), b.size


def hero_svg():
    data, (bw, bh) = board_b64()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460" width="1200" height="460" font-family="Segoe UI,Arial,sans-serif">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a1630"/><stop offset="1" stop-color="#10385c"/></linearGradient>
<filter id="sh"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-opacity=".5"/></filter></defs>
<rect width="1200" height="460" rx="24" fill="url(#bg)"/>
<g fill="none" stroke="#3fd0ff" stroke-width="3" stroke-linecap="round"><path d="M80 130 q40 -40 80 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" repeatCount="indefinite"/></path>
<path d="M62 150 q58 -62 116 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" begin=".3s" repeatCount="indefinite"/></path>
<path d="M44 170 q76 -84 152 0"><animate attributeName="opacity" values="0;1;0" dur="2.4s" begin=".6s" repeatCount="indefinite"/></path></g>
<circle cx="120" cy="170" r="7" fill="#3fd0ff"/>
<text x="230" y="120" fill="#3fd0ff" font-size="20" font-weight="700" letter-spacing="3">OPEN-SOURCE IoT PUMP CONTROLLER</text>
<text x="226" y="215" fill="#f0f6ff" font-size="96" font-weight="700">BorePilot</text>
<text x="230" y="265" fill="#f0f6ff" font-size="32" font-weight="300">Smart borewell pump controller</text>
<text x="230" y="310" fill="#96afcd" font-size="22">ESP32-S3  |  2 relays  |  PZEM-004T  |  Home Assistant  |  USB-C</text>
<g font-size="20" fill="#f0f6ff"><rect x="230" y="340" width="150" height="42" rx="21" fill="#2fbf71" opacity=".25"/><text x="252" y="368">Start / Stop</text>
<rect x="394" y="340" width="150" height="42" rx="21" fill="#3fd0ff" opacity=".25"/><text x="420" y="368">V / A / kWh</text>
<rect x="558" y="340" width="170" height="42" rx="21" fill="#f4c20d" opacity=".25"/><text x="582" y="368">Dry-run guard</text></g>
<g filter="url(#sh)"><image href="data:image/jpeg;base64,{data}" x="{1200-bw-40}" y="{(460-bh)//2}" width="{bw}" height="{bh}"/></g>
<circle cx="{1200-bw-40+bw*0.26}" cy="{(460-bh)//2+bh*0.64}" r="9" fill="#2fbf71"><animate attributeName="opacity" values="1;.15;1" dur="1.6s" repeatCount="indefinite"/></circle>
<circle cx="{1200-bw-40+bw*0.53}" cy="{(460-bh)//2+bh*0.64}" r="9" fill="#2fbf71"><animate attributeName="opacity" values="1;.15;1" dur="1.6s" begin=".8s" repeatCount="indefinite"/></circle>
<text x="1160" y="438" text-anchor="end" fill="#96afcd" font-size="16">ElectroIoT.in</text>
</svg>'''
    open(os.path.join(IMG, "borepilot-hero-animated.svg"), "w", encoding="utf-8").write(svg)


def flow_svg():
    def box(x, y, w, h, t, s, col):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#12263f" stroke="{col}" stroke-width="2"/>'
                f'<text x="{x+w/2}" y="{y+38}" text-anchor="middle" fill="#f0f6ff" font-size="22" font-weight="700">{t}</text>'
                f'<text x="{x+w/2}" y="{y+66}" text-anchor="middle" fill="#96afcd" font-size="15">{s}</text>')
    def arrow(x1, y1, x2, y2, col, d="3s"):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="3" stroke-dasharray="10 8">'
                f'<animate attributeName="stroke-dashoffset" from="36" to="0" dur="{d}" repeatCount="indefinite"/></line>'
                f'<polygon points="{x2},{y2} {x2-10*(1 if x2>x1 else -1)},{y2-6} {x2-10*(1 if x2>x1 else -1)},{y2+6}" fill="{col}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420" font-family="Segoe UI,Arial,sans-serif">
<rect width="1200" height="420" rx="24" fill="#0a1630"/>
<text x="600" y="44" text-anchor="middle" fill="#3fd0ff" font-size="24" font-weight="700">How BorePilot works</text>
{box(40,150,230,100,"Home Assistant","phone, dashboard, automations","#3fd0ff")}
{box(380,130,250,140,"BorePilot","ESP32-S3 + HLK 5 V + relays","#2fbf71")}
{box(740,70,210,90,"Relay 1","START contactor / pump","#f4c20d")}
{box(740,240,210,90,"Relay 2","STOP / spare, NO + NC","#f4c20d")}
{box(1000,150,170,100,"Pump","single phase, 230 V","#ff6b6b")}
{box(380,320,250,80,"PZEM-004T","V, A, W, kWh, Hz","#3fd0ff")}
{box(40,320,230,80,"Tank node (optional)","ESP-NOW level","#96afcd")}
{arrow(270,200,380,200,"#3fd0ff")}{arrow(380,215,270,215,"#3fd0ff","4s")}
{arrow(630,170,740,115,"#2fbf71")}{arrow(630,230,740,285,"#2fbf71")}
{arrow(950,115,1000,185,"#f4c20d")}{arrow(950,285,1000,215,"#f4c20d")}
{arrow(505,320,505,270,"#3fd0ff")}
{arrow(270,360,380,300,"#96afcd","5s")}
<text x="325" y="190" text-anchor="middle" fill="#96afcd" font-size="14">Wi-Fi</text>
</svg>'''
    open(os.path.join(IMG, "borepilot-flow-animated.svg"), "w", encoding="utf-8").write(svg)


hero(); square(); features(); hero_svg(); flow_svg()
print("assets written")
