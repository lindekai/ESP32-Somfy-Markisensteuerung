# Erzeugt hero-light.svg, hero-dark.svg und verdrahtung.svg.
# Aufruf: python3 docs/images/generate.py docs/images

import sys, os
out = sys.argv[1]

THEMES = {
 "light": dict(bg="#F7F4EE", grid="#ECE6DA", text="#1B1F24", muted="#5B6470", accent="#E38B2C",
               stripe2="#FBF1E1", board="#1E2935", boardhi="#2E3D4D", chip="#3B4B5E", pcb="#2F7D4F",
               wave="#2F7FD8", pill="#FFFFFF", pillstroke="#E2DACB", cassette="#3A4250"),
 "dark":  dict(bg="#0D1117", grid="#161C25", text="#E9ECF0", muted="#9AA4B2", accent="#F2A541",
               stripe2="#2A303A", board="#243140", boardhi="#34465A", chip="#4A5D73", pcb="#2E8B57",
               wave="#62AEFF", pill="#161B22", pillstroke="#2B3340", cassette="#C9CED6"),
}

def hero(t):
    c = THEMES[t]
    stripes = [((890,100),(930,100),(907.5,200),(860,200)),((970,100),(1010,100),(1002.5,200),(955,200)),
               ((1050,100),(1090,100),(1097.5,200),(1050,200)),((1130,100),(1170,100),(1192.5,200),(1145,200))]
    s = "\n    ".join(f'<polygon points="{" ".join(f"{x},{y}" for x,y in p)}" fill="{c["accent"]}"/>' for p in stripes)
    val = []
    for k in range(8):
        x0 = 860 + 47.5*k; x1 = x0 + 47.5
        f = c["accent"] if k % 2 == 0 else c["stripe2"]
        val.append(f'<path d="M{x0},200 H{x1} V222 A23.75,23.75 0 0 1 {x0},222 Z" fill="{f}"/>')
    val = "\n    ".join(val)
    pins_top = "".join(f'<rect x="{792+i*11}" y="314" width="5" height="7" rx="1" fill="#C9A94B"/>' for i in range(12))
    pins_bot = "".join(f'<rect x="{792+i*11}" y="379" width="5" height="7" rx="1" fill="#C9A94B"/>' for i in range(12))
    pills = ""
    x = 72
    for label in ["▲  Auf", "■  Stopp", "▼  Ab", "★  My"]:
        w = 22 + len(label)*10.5
        pills += (f'<rect x="{x}" y="296" width="{w:.0f}" height="38" rx="19" fill="{c["pill"]}" stroke="{c["pillstroke"]}"/>'
                  f'<text x="{x+w/2:.0f}" y="321" text-anchor="middle" font-size="16" font-weight="600" fill="{c["text"]}">{label}</text>')
        x += w + 12
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-labelledby="t d">
  <title id="t">ESP32 Somfy-Markisensteuerung</title>
  <desc id="d">Stilisierte Markise, ein ESP32 mit CC1101-Funkmodul und Funkwellen.</desc>
  <defs>
    <pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern>
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{c["bg"]}" stop-opacity="1"/><stop offset="0.55" stop-color="{c["bg"]}" stop-opacity="0.2"/><stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect width="1280" height="420" rx="24" fill="{c["bg"]}"/>
  <rect width="1280" height="420" rx="24" fill="url(#g)"/>
  <rect width="1280" height="420" rx="24" fill="url(#fade)"/>
  <g font-family="ui-sans-serif, -apple-system, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
    <text x="72" y="128" font-size="15" font-weight="700" letter-spacing="2.4" fill="{c["accent"]}">ESP32 · CC1101 · SOMFY RTS 433,42 MHZ</text>
    <text x="72" y="196" font-size="52" font-weight="800" letter-spacing="-1.2" fill="{c["text"]}">Somfy-Markisensteuerung</text>
    <text x="72" y="244" font-size="22" fill="{c["muted"]}">Die Funk-Markise in Apple Home – lokal, ohne Cloud.</text>
    {pills}
  </g>
  <!-- Sonne -->
  <circle cx="790" cy="96" r="24" fill="{c["accent"]}" opacity="0.9"/>
  <g stroke="{c["accent"]}" stroke-width="4" stroke-linecap="round" opacity="0.9">
    <path d="M790 54v-10M790 148v-10M748 96h-10M842 96h-10M760 66l-7-7M827 133l-7-7M760 126l-7 7M827 59l-7 7"/>
  </g>
  <!-- Markise -->
  <g>
    <rect x="876" y="78" width="348" height="24" rx="8" fill="{c["cassette"]}"/>
    <polygon points="890,100 1210,100 1240,200 860,200" fill="{c["stripe2"]}"/>
    {s}
    {val}
  </g>
  <!-- ESP32 + CC1101 -->
  <g>
    <rect x="780" y="318" width="146" height="64" rx="7" fill="{c["board"]}"/>
    {pins_top}{pins_bot}
    <rect x="768" y="338" width="16" height="24" rx="3" fill="{c["boardhi"]}"/>
    <rect x="830" y="328" width="62" height="44" rx="4" fill="{c["chip"]}"/>
    <rect x="840" y="338" width="42" height="24" rx="2" fill="none" stroke="{c["boardhi"]}" stroke-width="2"/>
    <circle cx="806" cy="350" r="3" fill="{c["wave"]}"/>
    <rect x="944" y="326" width="74" height="48" rx="5" fill="{c["pcb"]}"/>
    <rect x="956" y="338" width="26" height="24" rx="2" fill="#1E2A22" opacity="0.6"/>
    <path d="M934 340h10M934 350h10M934 360h10M926 340h8M926 360h8" stroke="{c["boardhi"]}" stroke-width="3" stroke-linecap="round"/>
    <path d="M1000 326 V312 l-6 -3 l12 -4 l-12 -4 l12 -4 l-12 -4 l6 -3 V286" fill="none" stroke="{c["cassette"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="1000" cy="286" r="4" fill="{c["cassette"]}"/>
  </g>
  <!-- Funkwellen -->
  <g fill="none" stroke="{c["wave"]}" stroke-width="4" stroke-linecap="round">
    <path d="M1009,270.4 A18,18 0 0 1 1018,286"/>
    <path d="M1016,258.3 A32,32 0 0 1 1032,286" opacity="0.75"/>
    <path d="M1023,246.2 A46,46 0 0 1 1046,286" opacity="0.5"/>
  </g>
</svg>
'''

# ---------- ESP32-DevKit 38 Pins (Draufsicht, Antenne oben) ----------
LEFT = ["3V3","EN","VP","VN","IO34","IO35","IO32","IO33","IO25","IO26","IO27","IO14","IO12","GND","IO13","SD2","SD3","CMD","5V"]
RIGHT = ["GND","IO23","IO22","TX","RX","IO21","GND","IO19","IO18","IO5","IO17","IO16","IO4","IO0","IO2","IO15","SD1","SD0","CLK"]

# ---------- Pinbelegung (ein Breadboard: alle Leitungen an der linken Pinreihe) ----------
# CC1101-Pin, ESP32-Pin, Netzname, Farbe
PINMAP = [
    ("GDO2", "IO34", "RX",   "#94A3B8"),
    ("MISO", "IO35", "MISO", "#7C3AED"),
    ("MOSI", "IO32", "MOSI", "#2563EB"),
    ("SCK",  "IO33", "SCK",  "#16A34A"),
    ("CSN",  "IO25", "CSN",  "#EAB308"),
    ("GDO0", "IO26", "TX",   "#EA580C"),
]
CC_ORDER = ["GDO2", "MISO", "MOSI", "SCK", "CSN", "GDO0", "VCC", "GND"]
USED_LEFT = {"3V3", "GND", "IO34", "IO35", "IO32", "IO33", "IO25", "IO26"}

# ---------- Verdrahtungsplan ----------
def wiring():
    W, H = 1140, 640
    bx0, bx1, y0, pitch = 560, 760, 120, 24
    py = lambda i: y0 + i*pitch
    o = []
    o.append(f'<rect x="{bx0}" y="70" width="{bx1-bx0}" height="{py(18)-70+46}" rx="12" class="board"/>')
    o.append(f'<rect x="{bx0+50}" y="78" width="100" height="26" rx="4" class="chip"/><text x="{(bx0+bx1)/2}" y="96" class="t-chip" text-anchor="middle">ESP32-WROOM-32</text>')
    o.append(f'<rect x="{(bx0+bx1)/2-22}" y="{py(18)+30}" width="44" height="22" rx="4" class="chip"/><text x="{(bx0+bx1)/2}" y="{py(18)+68}" class="t-small" text-anchor="middle">Micro-USB</text>')
    for i, n in enumerate(LEFT):
        u = n in USED_LEFT and not (n == "GND" and i != 13)
        o.append(f'<circle cx="{bx0+14}" cy="{py(i)}" r="5" class="{"pin-on" if u else "pin"}"/><text x="{bx0+26}" y="{py(i)+4}" class="{"t-pin-on" if u else "t-pin"}">{n}</text>')
    for i, n in enumerate(RIGHT):
        o.append(f'<circle cx="{bx1-14}" cy="{py(i)}" r="5" class="pin"/><text x="{bx1-26}" y="{py(i)+4}" text-anchor="end" class="t-pin">{n}</text>')
    o.append(f'<text x="{(bx0+bx1)/2}" y="58" text-anchor="middle" class="t-head">ESP32-DevKit (38 Pins)</text>')
    o.append(f'<text x="{bx1+16}" y="{py(9)}" class="t-small">rechte Pinreihe</text><text x="{bx1+16}" y="{py(9)+16}" class="t-small">bleibt frei</text>')
    # CC1101 links, Pins rechts am Modul, auf Höhe der ESP-Pins
    ccx1 = 320
    ccy = {n: py(4+k) for k, n in enumerate(CC_ORDER[:6])}
    ccy["VCC"] = py(10); ccy["GND"] = py(11)
    o.append(f'<rect x="{ccx1-170}" y="{py(4)-40}" width="170" height="{py(11)-py(4)+80}" rx="10" class="cc"/>')
    o.append(f'<text x="{ccx1-85}" y="{py(11)+70}" text-anchor="middle" class="t-head">CC1101 · 433 MHz</text>')
    for n, y in ccy.items():
        o.append(f'<circle cx="{ccx1-14}" cy="{y}" r="5" class="pin-on"/><text x="{ccx1-28}" y="{y+4}" text-anchor="end" class="t-pin-cc">{n}</text>')
    ax = ccx1-140
    o.append(f'<path d="M{ax} {py(4)-40} V{py(4)-70} l-8 -4 l16 -6 l-16 -6 l16 -6 l-16 -6 l8 -4 V{py(4)-120}" class="ant"/>')
    for cc, esp, net, col in PINMAP:
        y = ccy[cc]
        dash = ' stroke-dasharray="7 5"' if False else ""
        o.append(f'<path d="M{bx0+14} {y} H{ccx1-14}" stroke="{col}" class="wire"/>')
    # 3V3 (oben) und GND (unten) zum Modul
    o.append(f'<path d="M{bx0+14} {py(0)} H{470} V{ccy["VCC"]} H{ccx1-14}" stroke="#DC2626" class="wire"/>')
    o.append(f'<path d="M{bx0+14} {py(13)} H{440} V{ccy["GND"]} H{ccx1-14}" stroke="var(--gnd)" class="wire"/>')
    # Legende rechts
    leg = [("#DC2626", "3V3  → VCC"), ("var(--gnd)", "GND  → GND")] + [(c, f"{e:<4} → {cc}") for cc, e, n, c in PINMAP]
    lx, ly = 880, 150
    o.append(f'<text x="{lx}" y="{ly-24}" class="t-head">Verbindungen</text>')
    for i, (col, txt) in enumerate(leg):
        o.append(f'<line x1="{lx}" y1="{ly+i*28}" x2="{lx+28}" y2="{ly+i*28}" stroke="{col}" class="wire"/><text x="{lx+38}" y="{ly+i*28+5}" class="t-leg" xml:space="preserve">{txt}</text>')
    o.append(f'<text x="{lx}" y="{ly+8*28+30}" class="t-warn">⚠ CC1101 nur an 3,3 V,</text><text x="{lx}" y="{ly+8*28+50}" class="t-warn">niemals an 5 V!</text>')
    o.append(f'<text x="{lx}" y="{ly+8*28+86}" class="t-small">Pinreihenfolge variiert je</text><text x="{lx}" y="{ly+8*28+104}" class="t-small">nach Modul – Aufdruck prüfen.</text>')
    body = "\n  ".join(o)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">Verdrahtung ESP32-DevKit mit CC1101</title>
  <style>
    svg {{ --bg:#FFFFFF; --fg:#1B1F24; --muted:#6B7280; --board:#1E2935; --chip:#3B4B5E; --cc:#2F7D4F; --pin:#4B5563; --pinon:#F2A541; --warn:#B91C1C; --gnd:#111827; }}
    @media (prefers-color-scheme: dark) {{ svg {{ --bg:#0D1117; --fg:#E9ECF0; --muted:#9AA4B2; --board:#243140; --chip:#4A5D73; --cc:#2E8B57; --pin:#6B7280; --pinon:#F2A541; --warn:#F87171; --gnd:#E5E7EB; }} }}
    text {{ font-family: ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .bg {{ fill: var(--bg); }}
    .board {{ fill: var(--board); }} .chip {{ fill: var(--chip); }} .cc {{ fill: var(--cc); }}
    .pin {{ fill: var(--pin); }} .pin-on {{ fill: var(--pinon); stroke:#fff; stroke-width:1.5; }}
    .t-pin {{ font-size: 11px; fill: #8A94A3; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .t-pin-on {{ font-size: 12px; fill: #FFFFFF; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .t-pin-cc {{ font-size: 13px; fill: #FFFFFF; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .t-chip {{ font-size: 10px; fill: #DCE3EA; font-weight: 600; }}
    .t-head {{ font-size: 16px; font-weight: 700; fill: var(--fg); }}
    .t-leg {{ font-size: 14px; fill: var(--fg); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .t-small {{ font-size: 12px; fill: var(--muted); }}
    .t-warn {{ font-size: 13px; font-weight: 700; fill: var(--warn); }}
    .wire {{ fill: none; stroke-width: 3.5; stroke-linecap: round; stroke-linejoin: round; }}
    .ant {{ fill: none; stroke: var(--muted); stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }}
  </style>
  <rect width="{W}" height="{H}" rx="16" class="bg"/>
  {body}
</svg>
'''

open(os.path.join(out,"hero-light.svg"),"w").write(hero("light"))
open(os.path.join(out,"hero-dark.svg"),"w").write(hero("dark"))
open(os.path.join(out,"verdrahtung.svg"),"w").write(wiring())


# ---------- gemeinsamer Stil für Diagramme (hell/dunkel per Media Query) ----------
STYLE = """
  <style>
    svg { --bg:#FFFFFF; --paper:#FBFAF7; --grid:#EEF0F3; --fg:#1B1F24; --muted:#6B7280; --line:#1B1F24; --box:#FFFFFF;
          --boxstroke:#C9CED6; --accent:#E38B2C; --blue:#2F7FD8; --gnd:#111827; --warn:#B91C1C; --card:#F5F2EC; }
    @media (prefers-color-scheme: dark) { svg { --bg:#0D1117; --paper:#0F141B; --grid:#18202A; --fg:#E9ECF0; --muted:#9AA4B2;
          --line:#D5DAE1; --box:#161B22; --boxstroke:#2E3846; --accent:#F2A541; --blue:#62AEFF; --gnd:#E5E7EB; --warn:#F87171; --card:#161B22; } }
    text { font-family: ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: var(--fg); }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .muted { fill: var(--muted); }
  </style>"""

def svg_wrap(W, H, title, body, bg="var(--bg)"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
  <title id="t">{title}</title>{STYLE}
  <rect width="{W}" height="{H}" rx="16" style="fill:{bg}"/>
  {body}
</svg>
'''

# ---------- Schaltplan ----------
def schematic():
    W, H = 1200, 780
    o = []
    o.append('<defs><pattern id="sg" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" style="stroke:var(--grid)" stroke-width="1"/></pattern></defs>')
    o.append(f'<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="10" fill="url(#sg)" style="stroke:var(--boxstroke)" stroke-width="1.5"/>')
    L = 'style="stroke:var(--line)" stroke-width="2.2" fill="none" stroke-linecap="round"'
    def pwr(x, y, label):
        return (f'<path d="M{x} {y} V{y-26} M{x-16} {y-26} H{x+16}" {L}/>'
                f'<text x="{x}" y="{y-36}" text-anchor="middle" font-size="14" font-weight="700" style="fill:#DC2626">{label}</text>')
    def gnd(x, y):
        return f'<path d="M{x} {y} V{y+20} M{x-16} {y+20} H{x+16} M{x-10} {y+27} H{x+10} M{x-4} {y+34} H{x+4}" {L}/>'
    def box(x0, y0, x1, y1, ref, name, dashed=False):
        d = ' stroke-dasharray="8 6"' if dashed else ''
        return (f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="6" style="fill:var(--box);stroke:var(--line)" stroke-width="2.2"{d}/>'
                f'<text x="{x0}" y="{y0-12}" font-size="14" font-weight="800" style="fill:var(--accent)">{ref}</text>'
                f'<text x="{x0+34}" y="{y0-12}" font-size="14" font-weight="700">{name}</text>')
    # U1 ESP32 rechts
    ux0, ux1 = 700, 920
    o.append(box(ux0, 150, ux1, 610, "U1", "ESP32-DevKit (WROOM-32)"))
    o.append(f'<text x="{(ux0+ux1)/2+20}" y="390" text-anchor="middle" font-size="22" font-weight="800" class="muted" opacity="0.35">ESP32</text>')
    o.append(f'<path d="M760 150 V110" {L}/>' + pwr(760, 110, "+3V3"))
    o.append('<text x="768" y="172" font-size="12" class="mono">3V3</text>')
    o.append(f'<path d="M760 610 V640" {L}/>' + gnd(760, 640))
    o.append('<text x="768" y="600" font-size="12" class="mono">GND</text>')
    o.append(f'<path d="M{ux1} 560 H{ux1+50}" {L}/><text x="{ux1-10}" y="564" text-anchor="end" font-size="12" class="mono">5V</text>')
    o.append(f'<rect x="{ux1+50}" y="544" width="70" height="32" rx="5" style="fill:var(--card);stroke:var(--line)" stroke-width="2"/>'
             f'<text x="{ux1+85}" y="565" text-anchor="middle" font-size="12" font-weight="700">USB</text>'
             f'<text x="{ux1+85}" y="598" text-anchor="middle" font-size="11" class="muted">5-V-Netzteil</text>')
    # U2 CC1101 links
    cx0, cx1 = 260, 440
    o.append(box(cx0, 190, cx1, 470, "U2", "CC1101 433 MHz"))
    o.append(f'<text x="{(cx0+cx1)/2-10}" y="345" text-anchor="middle" font-size="22" font-weight="800" class="muted" opacity="0.35">CC1101</text>')
    o.append(f'<path d="M300 190 V150" {L}/>' + pwr(300, 150, "+3V3"))
    o.append('<text x="308" y="212" font-size="12" class="mono">VCC</text>')
    o.append(f'<path d="M300 470 V500" {L}/>' + gnd(300, 500))
    o.append('<text x="308" y="460" font-size="12" class="mono">GND</text>')
    o.append(f'<path d="M{cx0} 250 H200 V200 M184 172 L200 200 L216 172 Z" {L}/>'
             f'<text x="{cx0+8}" y="254" font-size="12" class="mono">ANT</text>'
             '<text x="120" y="160" font-size="12" class="muted">433,42 MHz</text>')
    for k, (cc, esp, net, col) in enumerate(PINMAP):
        y = 230 + 40*k
        o.append(f'<text x="{cx1-10}" y="{y+4}" text-anchor="end" font-size="12" class="mono">{cc}</text>')
        o.append(f'<text x="{ux0+10}" y="{y+4}" font-size="12" class="mono">{esp}</text>')
        o.append(f'<path d="M{cx1} {y} H{ux0}" style="stroke:{col}" stroke-width="2.6" fill="none"/>')
        o.append(f'<circle cx="{cx1}" cy="{y}" r="3.5" style="fill:{col}"/><circle cx="{ux0}" cy="{y}" r="3.5" style="fill:{col}"/>')
        mx = (cx1+ux0)/2
        o.append(f'<rect x="{mx-26}" y="{y-17}" width="52" height="16" rx="3" style="fill:var(--box)"/>'
                 f'<text x="{mx}" y="{y-5}" text-anchor="middle" font-size="11" font-weight="700" style="fill:{col}">{net}</text>')
    # U3 OLED optional, unten links
    o.append(box(260, 570, 440, 690, "U3", "OLED 0,96″ (optional)", dashed=True))
    o.append('<text x="350" y="672" text-anchor="middle" font-size="12" class="muted">SSD1306 · I²C · 3V3/GND</text>')
    for esp, oled, y, ty, colx in [("IO27", "SDA", 490, 600, 540), ("IO14", "SCL", 530, 630, 560)]:
        o.append(f'<text x="{ux0+10}" y="{y+4}" font-size="12" class="mono">{esp}</text>')
        o.append(f'<path d="M{ux0} {y} H{colx} V{ty} H440" {L} stroke-dasharray="7 5" opacity="0.7"/>')
        o.append(f'<text x="430" y="{ty+4}" text-anchor="end" font-size="12" class="mono">{oled}</text>')
    # Hinweise
    o.append('<g transform="translate(980,250)"><rect width="190" height="230" rx="8" style="fill:var(--card);stroke:var(--boxstroke)"/>'
             '<text x="14" y="26" font-size="13" font-weight="800">Hinweise</text>'
             '<text x="14" y="52" font-size="12" font-weight="700" style="fill:var(--warn)">CC1101 nur an 3,3 V</text>'
             '<text x="14" y="76" font-size="12" class="muted">Alle Leitungen an der</text>'
             '<text x="14" y="94" font-size="12" class="muted">linken Pinreihe – passt</text>'
             '<text x="14" y="112" font-size="12" class="muted">auf ein Breadboard</text>'
             '<text x="14" y="138" font-size="12" class="muted">SPI frei zugeordnet</text>'
             '<text x="14" y="156" font-size="12" class="muted">(GPIO-Matrix)</text>'
             '<text x="14" y="182" font-size="12" class="muted">IO34/35 nur Eingang:</text>'
             '<text x="14" y="200" font-size="12" class="muted">passt für MISO und RX</text></g>')
    o.append('<g transform="translate(980,600)"><rect width="190" height="140" rx="6" style="fill:var(--box);stroke:var(--line)" stroke-width="1.5"/>'
             '<path d="M0 46 H190 M0 78 H190 M0 110 H190 M95 78 V140" style="stroke:var(--boxstroke)"/>'
             '<text x="12" y="20" font-size="10" class="muted">TITEL</text><text x="12" y="38" font-size="12.5" font-weight="800">Somfy-Markisensteuerung</text>'
             '<text x="12" y="66" font-size="12">ESP32 + CC1101 (RTS)</text>'
             '<text x="12" y="92" font-size="9" class="muted">BLATT</text><text x="12" y="124" font-size="9" class="muted">REV</text>'
             '<text x="12" y="106" font-size="11" font-weight="700">1 / 1</text><text x="12" y="136" font-size="11" font-weight="700">B</text>'
             '<text x="107" y="92" font-size="9" class="muted">DATUM</text><text x="107" y="124" font-size="9" class="muted">LIZENZ</text>'
             '<text x="107" y="106" font-size="11" font-weight="700">11/2026</text><text x="107" y="136" font-size="11" font-weight="700">MIT</text></g>')
    o.append('<text x="40" y="58" font-size="20" font-weight="800">Schaltplan</text>'
             '<text x="40" y="80" font-size="13" class="muted">ESP32-DevKit · CC1101 · optionales OLED</text>')
    return svg_wrap(W, H, "Schaltplan ESP32 Somfy-Markisensteuerung", "\n  ".join(o), bg="var(--paper)")

# ---------- Breadboard (ein Board) ----------
def breadboard():
    W, H = 1040, 660
    P = 16
    BX, Y0, ROWS = 420, 70, 32
    COLS = {c: 64 + i*P for i, c in enumerate("abcde")}
    COLS.update({c: 176 + i*P for i, c in enumerate("fghij")})
    RAIL = {"L-": 16, "L+": 32, "R+": 272, "R-": 288}
    ry = lambda r: Y0 + 40 + P*(r-1)
    hole = lambda c, r: (BX + COLS[c], ry(r))
    rail = lambda k, r: (BX + RAIL[k], ry(r))
    bh = 40 + P*(ROWS-1) + 40
    o = []
    g = [f'<rect x="{BX}" y="{Y0}" width="304" height="{bh}" rx="8" fill="#F4F2EE" stroke="#D8D3CA" stroke-width="1.5"/>',
         f'<rect x="{BX+144}" y="{Y0+30}" width="16" height="{bh-60}" rx="3" fill="#E4E0D8"/>']
    for k, x in RAIL.items():
        col = "#DC2626" if "+" in k else "#2563EB"
        off = -8 if k in ("L-", "R+") else 8
        g.append(f'<line x1="{BX+x+off}" y1="{Y0+22}" x2="{BX+x+off}" y2="{Y0+bh-22}" stroke="{col}" stroke-width="1.5" opacity="0.35"/>')
        g.append(f'<text x="{BX+x}" y="{Y0+18}" text-anchor="middle" font-size="12" font-weight="800" style="fill:{col}">{"+" if "+" in k else "−"}</text>')
        for r in range(1, ROWS+1):
            if (r-1) % 6 == 5: continue
            g.append(f'<rect x="{BX+x-3}" y="{ry(r)-3}" width="6" height="6" rx="1.2" fill="#3A3F47" opacity="0.8"/>')
    for c, x in COLS.items():
        g.append(f'<text x="{BX+x}" y="{Y0+26}" text-anchor="middle" font-size="10" style="fill:#8A8F98">{c}</text>')
        for r in range(1, ROWS+1):
            g.append(f'<rect x="{BX+x-3}" y="{ry(r)-3}" width="6" height="6" rx="1.2" fill="#3A3F47" opacity="0.8"/>')
    for r in range(1, ROWS+1, 5):
        g.append(f'<text x="{BX+50}" y="{ry(r)+4}" text-anchor="end" font-size="9" style="fill:#8A8F98">{r}</text>')
    o.append("".join(g))
    # ESP32: linke Pinreihe in Spalte b, rechte in Spalte j, Reihen 3–21
    ex0, ex1 = BX + COLS["b"] - 13, BX + COLS["j"] + 13
    top, hgt = ry(1)-25, ry(21)-ry(1)+60
    o.append(f'<rect x="{ex0+3}" y="{top+3}" width="{ex1-ex0}" height="{hgt}" rx="8" fill="#000" opacity="0.18"/>')
    o.append(f'<rect x="{ex0}" y="{top}" width="{ex1-ex0}" height="{hgt}" rx="8" fill="#1E2935"/>')
    o.append(f'<rect x="{ex0+50}" y="{ry(1)-17}" width="{ex1-ex0-100}" height="150" rx="4" fill="#B8BEC6"/>'
             f'<rect x="{ex0+50}" y="{ry(1)-17}" width="{ex1-ex0-100}" height="30" rx="4" fill="#2E3D4D"/>'
             f'<path d="M{ex0+58} {ry(1)-2} h12 v-8 h12 v8 h12 v-8 h12 v8 h12 v-8 h12 v8" fill="none" stroke="#C9A94B" stroke-width="2"/>'
             f'<text x="{(ex0+ex1)/2}" y="{ry(1)+70}" text-anchor="middle" font-size="11" font-weight="800" style="fill:#2B3440">ESP32</text>'
             f'<text x="{(ex0+ex1)/2}" y="{ry(1)+86}" text-anchor="middle" font-size="9" style="fill:#4B5563">WROOM-32</text>')
    o.append(f'<rect x="{(ex0+ex1)/2-20}" y="{ry(21)+22}" width="40" height="22" rx="3" fill="#9AA3AE"/>'
             f'<rect x="{ex0+20}" y="{ry(21)+18}" width="16" height="12" rx="2" fill="#4B5563"/><rect x="{ex1-36}" y="{ry(21)+18}" width="16" height="12" rx="2" fill="#4B5563"/>')
    for i, n in enumerate(LEFT):
        x, y = BX + COLS["b"], ry(3+i)
        on = n in USED_LEFT and not (n == "GND" and i != 13)
        o.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" rx="1.5" fill="#111"/><circle cx="{x}" cy="{y}" r="2.6" fill="{"#F2A541" if on else "#C9A94B"}"/>')
        o.append(f'<text x="{x+10}" y="{y+3.5}" font-size="8.5" class="mono" style="fill:{"#FFFFFF" if on else "#8A94A3"};font-weight:{700 if on else 400}">{n}</text>')
    for i, n in enumerate(RIGHT):
        x, y = BX + COLS["j"], ry(3+i)
        o.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" rx="1.5" fill="#111"/><circle cx="{x}" cy="{y}" r="2.6" fill="#C9A94B"/>')
        o.append(f'<text x="{x-10}" y="{y+3.5}" text-anchor="end" font-size="8.5" class="mono" style="fill:#8A94A3">{n}</text>')
    # CC1101 links neben dem Board, Stiftleiste zum Board hin
    ccrow = {n: 7+k for k, n in enumerate(CC_ORDER)}
    px = 300
    mx0, mx1 = px - 140, px + 10
    o.append(f'<rect x="{mx0+3}" y="{ry(7)-30+3}" width="{mx1-mx0}" height="{ry(14)-ry(7)+60}" rx="6" fill="#000" opacity="0.18"/>'
             f'<rect x="{mx0}" y="{ry(7)-30}" width="{mx1-mx0}" height="{ry(14)-ry(7)+60}" rx="6" fill="#2F7D4F"/>'
             f'<rect x="{mx0+30}" y="{ry(9)}" width="44" height="44" rx="3" fill="#1C2A22"/>'
             f'<text x="{mx0+52}" y="{ry(9)+26}" text-anchor="middle" font-size="8" style="fill:#9FB8A8">CC1101</text>'
             f'<rect x="{mx0+10}" y="{ry(7)-22}" width="14" height="10" rx="2" fill="#C9A94B"/>'
             f'<path d="M{mx0+17} {ry(7)-22} V{ry(7)-40} l-8 -4 l16 -6 l-16 -6 l16 -6 l-16 -6 l16 -6 l-16 -6 l8 -4 V{ry(7)-100}" fill="none" stroke="#C9A94B" stroke-width="3" stroke-linejoin="round"/>'
             f'<text x="{(mx0+mx1)/2}" y="{ry(14)+56}" text-anchor="middle" font-size="13" font-weight="700" class="muted">CC1101 · 433 MHz</text>')
    for n, r in ccrow.items():
        y = ry(r)
        o.append(f'<rect x="{px-5}" y="{y-5}" width="10" height="10" rx="1.5" fill="#111"/><circle cx="{px}" cy="{y}" r="2.6" fill="#F2A541"/>'
                 f'<text x="{px-12}" y="{y+3.5}" text-anchor="end" font-size="9.5" font-weight="700" class="mono" style="fill:#FFFFFF">{n}</text>')
    ccp = {n: (px, ry(r)) for n, r in ccrow.items()}
    def wire(p0, p1, col, bend=0.0):
        (x0, y0), (x1, y1) = p0, p1
        d = f"M{x0} {y0} Q{(x0+x1)/2} {(y0+y1)/2 - bend} {x1} {y1}"
        return (f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.22" stroke-width="7" stroke-linecap="round" transform="translate(1.5,2)"/>'
                f'<path d="{d}" fill="none" style="stroke:{col}" stroke-width="5" stroke-linecap="round"/>'
                f'<rect x="{x0-4}" y="{y0-4}" width="8" height="8" rx="1.5" fill="#20242A"/><rect x="{x1-4}" y="{y1-4}" width="8" height="8" rx="1.5" fill="#20242A"/>')
    o.append(wire(hole("a", 3), rail("L+", 3), "#DC2626", bend=10))
    o.append(wire(hole("a", 16), rail("L-", 16), "var(--gnd)", bend=10))
    o.append(wire(rail("L+", 13), ccp["VCC"], "#DC2626", bend=14))
    o.append(wire(rail("L-", 14), ccp["GND"], "var(--gnd)", bend=-14))
    for cc, esp, net, col in PINMAP:
        r = ccrow[cc]
        o.append(wire(hole("a", r), ccp[cc], col, bend=12))
    # Beschriftung
    o.append('<text x="40" y="40" font-size="20" font-weight="800">Breadboard-Aufbau</text>'
             '<text x="40" y="62" font-size="13" class="muted">Ein Breadboard · ESP32 in Spalte b–j · alle Leitungen über Spalte a</text>')
    lx, ly = 770, 150
    o.append(f'<text x="{lx}" y="{ly-24}" font-size="15" font-weight="800">Steckplan</text>')
    rows = [("#DC2626", "a3", "3V3 → + Schiene"), ("var(--gnd)", "a16", "GND → − Schiene")] + \
           [(c, f"a{ccrow[cc]}", f"{e} → {cc}") for cc, e, n, c in PINMAP] + \
           [("#DC2626", "+", "Schiene → VCC"), ("var(--gnd)", "−", "Schiene → GND")]
    for i, (col, h, txt) in enumerate(rows):
        y = ly + i*26
        o.append(f'<line x1="{lx}" y1="{y}" x2="{lx+22}" y2="{y}" style="stroke:{col}" stroke-width="5" stroke-linecap="round"/>'
                 f'<text x="{lx+32}" y="{y+4}" font-size="12" font-weight="700" class="mono">{h}</text>'
                 f'<text x="{lx+70}" y="{y+4}" font-size="12" class="mono">{txt}</text>')
    o.append(f'<text x="{lx}" y="{ly+len(rows)*26+20}" font-size="12" class="muted">Spalte a ist neben dem DevKit</text>'
             f'<text x="{lx}" y="{ly+len(rows)*26+38}" font-size="12" class="muted">die einzige freie Lochreihe.</text>')
    return svg_wrap(W, H, "Breadboard-Aufbau ESP32 und CC1101 auf einem Breadboard", "\n  ".join(o))


# ---------- Architektur ----------
def architecture():
    W, H = 1200, 330
    o = []
    nodes = [("1", "Steuerung", "Home-App", "iPhone, iPad, Siri"),
             ("2", "Home-Zentrale", "Apple TV", "Fernzugriff, Automation"),
             ("3", "Bridge", "Homebridge", "Raspberry Pi"),
             ("4", "Funk-Gateway", "ESP32 + CC1101", "ESPSomfy-RTS"),
             ("5", "Aktor", "Somfy-Motor", "Markise")]
    xs = [30, 270, 510, 750, 990]; y0, w, h = 60, 180, 112
    for (num, kick, title, sub), x in zip(nodes, xs):
        hl = num in ("4",)
        o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" rx="14" style="fill:var(--card);stroke:{"var(--accent)" if hl else "var(--boxstroke)"}" stroke-width="{2.5 if hl else 1.5}"/>'
                 f'<circle cx="{x+26}" cy="{y0+28}" r="13" style="fill:{"var(--accent)" if hl else "var(--fg)"}"/>'
                 f'<text x="{x+26}" y="{y0+33}" text-anchor="middle" font-size="13" font-weight="800" style="fill:var(--bg)">{num}</text>'
                 f'<text x="{x+48}" y="{y0+33}" font-size="11" font-weight="700" letter-spacing="1.2" class="muted">{kick.upper()}</text>'
                 f'<text x="{x+18}" y="{y0+68}" font-size="19" font-weight="800">{title}</text>'
                 f'<text x="{x+18}" y="{y0+92}" font-size="13" class="muted">{sub}</text>')
    links = [("HomeKit", "WLAN", False), ("HomeKit (HAP)", "WLAN", False), ("HTTP + WebSocket", "WLAN · Port 8081/8080", False), ("Somfy RTS", "433,42 MHz", True)]
    for i, (a, b, radio) in enumerate(links):
        x0 = xs[i] + w + 4; x1 = xs[i+1] - 4; y = y0 + h/2
        if radio:
            o.append(f'<path d="M{x0} {y} H{x1-10}" style="stroke:var(--blue)" stroke-width="2.5" stroke-dasharray="3 5" stroke-linecap="round"/>'
                     f'<g fill="none" style="stroke:var(--blue)" stroke-width="2.5" stroke-linecap="round">'
                     f'<path d="M{(x0+x1)/2-4} {y-9} a12 12 0 0 1 0 18"/><path d="M{(x0+x1)/2+2} {y-15} a20 20 0 0 1 0 30" opacity="0.6"/></g>')
        else:
            o.append(f'<path d="M{x0} {y} H{x1-10}" style="stroke:var(--muted)" stroke-width="2.5"/>')
        o.append(f'<path d="M{x1-12} {y-6} L{x1} {y} L{x1-12} {y+6} Z" style="fill:{"var(--blue)" if radio else "var(--muted)"}"/>')
    # Telis unten
    tx, ty = 990, 230
    o.append(f'<rect x="{tx}" y="{ty}" width="{w}" height="70" rx="14" style="fill:var(--card);stroke:var(--boxstroke)" stroke-width="1.5" stroke-dasharray="6 5"/>'
             f'<text x="{tx+18}" y="{ty+30}" font-size="16" font-weight="800">Telis 1 RTS Pure</text>'
             f'<text x="{tx+18}" y="{ty+52}" font-size="13" class="muted">Original, bleibt nutzbar</text>')
    o.append(f'<path d="M{tx+w/2} {ty} V{y0+h+12}" style="stroke:var(--blue)" stroke-width="2.5" stroke-dasharray="3 5" stroke-linecap="round"/>'
             f'<path d="M{tx+w/2-6} {y0+h+14} L{tx+w/2} {y0+h+2} L{tx+w/2+6} {y0+h+14} Z" style="fill:var(--blue)"/>')
    o.append(f'<path d="M{tx} {ty+35} H{xs[3]+w/2} V{y0+h+12}" fill="none" style="stroke:var(--accent)" stroke-width="2" stroke-dasharray="3 5" stroke-linecap="round"/>'
             f'<path d="M{xs[3]+w/2-6} {y0+h+14} L{xs[3]+w/2} {y0+h+2} L{xs[3]+w/2+6} {y0+h+14} Z" style="fill:var(--accent)"/>'
             f'<text x="{xs[3]+w/2-12}" y="{ty+22}" text-anchor="end" font-size="12" style="fill:var(--accent)" font-weight="700">ESPSomfy-RTS hört mit,</text>'
             f'<text x="{xs[3]+w/2-12}" y="{ty+40}" text-anchor="end" font-size="12" style="fill:var(--accent)" font-weight="700">Position bleibt aktuell</text>')
    for i, (a, b, radio) in enumerate(links):
        cx = (xs[i] + w + xs[i+1]) / 2
        o.append(f'<text x="{cx}" y="{y0-14}" text-anchor="middle" font-size="11" font-weight="700" style="fill:{"var(--blue)" if radio else "var(--fg)"}">{a}</text>'
                 f'<text x="{cx}" y="{y0+h+20}" text-anchor="middle" font-size="10" class="muted">{b}</text>')
    return svg_wrap(W, H, "Architektur: von der Home-App bis zur Markise", "\n  ".join(o))

open(os.path.join(out, "schaltplan.svg"), "w").write(schematic())
open(os.path.join(out, "breadboard.svg"), "w").write(breadboard())
open(os.path.join(out, "architektur.svg"), "w").write(architecture())
