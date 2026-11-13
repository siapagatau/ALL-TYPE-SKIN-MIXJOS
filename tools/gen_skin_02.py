#!/usr/bin/env python3
"""Generator skin-02 : dB Voice 602-RV (MIXJOS Mixer) v4.2 - 1966 x 900.  DIBUAT ULANG dari nol (hard create).

Struktur MENGIKUTI FOTO dB Voice 602-RV:
  - panel atas hitam: 4 jack combo + tombol PHANTOM (= toggle), panel kanan: logo + 2 XLR + jack 6,3 mm emas
  - panel bawah (lebih sempit, bertingkat): kolom kanal, KNOB BERBENTUK CINCIN (merah TRIM / putih EQ / oranye FX-PAN)
  - kanan bawah: EQ grafis (HANYA slider yang punya fungsi = 4 band), layar MATI, tombol putih, meter L/R, fader
Fungsi (id kontrol dan mapping TIDAK berubah dari v3.5): 37 knob + 8 toggle + 4 slider EQ AUDIO + 2 fader + 21 LED = 51 kontrol.
Komponen tanpa fungsi digelapkan 50%. Layar tidak menyala (tanpa angka).
Jalankan: python3 tools/gen_skin_02.py
"""
import json, math, os, re, random
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "skins", "skin-02")
NAME, VER, AUTHOR = "dB Voice 602-RV Mixer", "4.2", "MIXJOS"
FONT = "Arial, Helvetica, sans-serif"
NCH = 10
PAD = 14
W, H = 1966, 900
TXT = "#a3a8ab"; TXT_LT = "#e6e8e9"; CAP = "#f4f5f0"; ORANGE = "#ff8a1f"; RED = "#e0342b"

CH = [122 + 140 * i for i in range(NCH)]
DIV = [52 + 140 * i for i in range(NCH + 1)]
YO = 8
ROWS = [384 + YO + 88 * r for r in range(6)]
RB, TI, TO = 19, 30, 35
# warna cincin sesuai foto: merah TRIM, putih EQ, oranye-kuning FX / PAN
RING_RED, RING_WHT, RING_AMB = "#e8402f", "#f6f6f3", "#eba22b"
RING = [RING_RED, RING_WHT, RING_WHT, RING_WHT, RING_AMB, "cap"]   # baris 6 = knob besar tutup putih (seperti LEVEL di foto)
TITLE_SZ, SUB_SZ, LAB_SZ, TOG_SZ = 18, 11.5, 12, 12


def f(v): return ("%.2f" % v).rstrip("0").rstrip(".")


def dim(sv, k=0.5):
    def one(m):
        h = m.group(1)
        if len(h) == 3: h = "".join(c * 2 for c in h)
        return "#%02x%02x%02x" % tuple(int(int(h[j:j+2], 16) * k) for j in (0, 2, 4))
    return re.sub(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z-])", one, sv)


def build(preview):
    deco, ctl, hits = [], [], []
    controls, mapping, indicators = [], {}, []

    # ---------------------------------------------------------------- primitif
    def pc(x, y, r, fill, stroke=None, sw=1.0, op=None, into=None, dash=None):
        s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        d = f' stroke-dasharray="{f(dash)} {f(dash)}"' if dash else ""
        (deco if into is None else into).append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}"{o}{s}{d}/>')

    def pl(x1, y1, x2, y2, col, w, op=1.0, cap=None):
        c = f' stroke-linecap="{cap}"' if cap else ""
        return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" '
                f'stroke-width="{f(w)}" stroke-opacity="{op}"{c}/>')

    def line(x1, y1, x2, y2, col="#3a3d40", w=1.4, op=1.0, cap=None):
        deco.append(pl(x1, y1, x2, y2, col, w, op, cap))

    def t(x, y, s, size=12, fill=TXT, anchor="middle", weight="normal", ls=0, font=FONT, rot=None):
        e = f' letter-spacing="{f(ls)}"' if ls else ""
        r = f' transform="rotate({rot} {f(x)} {f(y)})"' if rot is not None else ""
        deco.append(f'<text x="{f(x)}" y="{f(y)}" font-family="{font}" font-size="{f(size)}" font-weight="{weight}" '
                    f'fill="{fill}" text-anchor="{anchor}"{e}{r}>{escape(s)}</text>')

    def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1.0, op=None, into=None):
        s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        r = f' rx="{f(rx)}"' if rx else ""
        (deco if into is None else into).append(
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{r} fill="{fill}"{o}{s}/>')

    def poly(pts, fill, stroke=None, sw=1.0, into=None):
        s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
        p = " ".join(f"{f(a)},{f(b)}" for a, b in pts)
        (deco if into is None else into).append(f'<polygon points="{p}" fill="{fill}"{s}/>')

    def hit(hid, x, y, w, h):
        a = ('fill="#ff2d55" fill-opacity="0.28" stroke="#ff2d55" stroke-width="1"' if preview
             else 'fill="#000" fill-opacity="0"')
        hits.append(f'<rect id="{hid}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" {a}/>')

    def screw(x, y, r=5.0, col="#62656a"):
        pc(x, y, r + 1.4, "#050505"); pc(x, y, r, col, "#111", 1.0)
        pc(x - r * .25, y - r * .3, r * .55, "#8a8d92", op=.55)
        deco.append(pl(x - r * .7, y + r * .5, x + r * .7, y - r * .5, "#15161a", 1.6))
        deco.append(pl(x - r * .5, y - r * .6, x + r * .5, y + r * .6, "#15161a", 1.2))

    def dimmed(fn_draw):
        d0 = len(deco); fn_draw(); deco[d0:] = [dim(x) for x in deco[d0:]]

    # ---------------------------------------------------------------- jack
    def combo(cx, cy, k=1.16):
        """Jack combo XLR/TRS seperti foto: cincin perak tebal, rumah hitam, cakram abu terang, lubang kunci."""
        pc(cx + 1, cy + 2.5, 41 * k, "#000", op=.5)
        pc(cx, cy, 40 * k, "#08080a", "#e2e4e5", 3.0)
        pc(cx, cy, 35 * k, "#101011", "#2b2b2d", 1.2)
        pc(cx, cy, 28.5 * k, "#66676b", "#1c1c1e", 1.8)
        pc(cx, cy, 25 * k, "#5a5b5f", "#78797d", 1.2)
        pc(cx - 7 * k, cy - 10 * k, 11 * k, "#ffffff", op=.10)
        deco.append(f'<path d="M{f(cx-10*k)},{f(cy-6*k)} A{f(10.5*k)},{f(10.5*k)} 0 1 1 {f(cx+10*k)},{f(cy-6*k)} L{f(cx+6*k)},{f(cy+1*k)} '
                    f'L{f(cx+8*k)},{f(cy+11*k)} L{f(cx-8*k)},{f(cy+11*k)} L{f(cx-6*k)},{f(cy+1*k)} Z" fill="#0a0a0b" stroke="#000" stroke-width="1"/>')
        pc(cx - 14 * k, cy + 3 * k, 3.4 * k, "#0a0a0b"); pc(cx + 14 * k, cy + 3 * k, 3.4 * k, "#0a0a0b")
        screw(cx - 40 * k, cy - 36 * k, 5.2, "#8a7f6a"); screw(cx + 40 * k, cy + 36 * k, 5.2, "#8a7f6a")

    def jack63(cx, cy, r=16):
        """Jack 6,3 mm: mur segi enam kuningan emas + lubang hitam (seperti foto)."""
        pc(cx + 1, cy + 2, r + 5, "#000", op=.4)
        pts = [(cx + (r + 3) * math.cos(math.radians(30 + 60 * k)), cy + (r + 3) * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
        poly(pts, "url(#g-brass)", "#4a3d1c", 1.4)
        pc(cx, cy, r * .78, "#bfa45a", "#6f5a24", 1.2)
        pc(cx, cy, r * .56, "#0a0a0a", "#2a2412", 1.4)
        pc(cx - r * .22, cy - r * .22, r * .2, "#ffffff", op=.15)

    def xlr(cx, cy):
        """XLR betina: rumah hitam, cincin perak, 3 pin emas (foto)."""
        pc(cx + 1, cy + 2, 41, "#000", op=.4)
        pc(cx, cy, 40, "url(#g-silver)", "#3a3b3d", 1.6)
        pc(cx, cy, 34, "#0c0c0d", "#9a9ca0", 1.4)
        pc(cx, cy, 27, "#1a1a1c", "#2c2c2e", 1.2)
        pc(cx, cy, 20, "#070708", "#333", 1.0)
        for dx, dy in ((-10, -6), (10, -6), (0, 11)): pc(cx + dx, cy + dy, 3.8, "#c9a94f", "#5a4a1a", 1)
        screw(cx - 34, cy - 34, 4.8); screw(cx + 34, cy + 34, 4.8)

    # ---------------------------------------------------------------- knob cincin (seperti foto)
    def knob(cx, cy, fn=None, ring=CAP, angle=-140, ti=32, to=37, nt=11, hit_w=122, kid=None, dv=0.5, tick="#c9cccf", style="ring"):
        d0 = len(deco)
        cap = (style == "cap")
        SK = 27 if cap else 26
        tw = 3.4 if cap else 2.6
        for n in range(nt):
            a = math.radians(-135 + 270 * n / (nt - 1))
            deco.append(pl(cx + ti * math.sin(a), cy - ti * math.cos(a), cx + to * math.sin(a), cy - to * math.cos(a), tick, tw, 1, "round"))
        pc(cx + 2, cy + 3.5, SK + 1.5, "#000", op=.55)
        inner = []
        pc(cx, cy, SK, "#1b1c1e", "#050506", 1.6, into=inner)                       # lingkaran PERTAMA = badan knob (kulit hitam)
        for n in range(28):
            a = math.radians(n * 360 / 28)
            inner.append(pl(cx + (SK - 5) * math.sin(a), cy - (SK - 5) * math.cos(a), cx + (SK - .6) * math.sin(a), cy - (SK - .6) * math.cos(a), "#4a4c50", 1.8))
        pc(cx, cy, SK - 7.5, "#141516", "#2c2d30", 1.2, into=inner)                # muka atas kulit
        inner.append(f'<ellipse cx="{f(cx - SK*.28)}" cy="{f(cy - SK*.5)}" rx="{f(SK*.55)}" ry="{f(SK*.17)}" fill="#fff" fill-opacity="0.10"/>')
        if cap:
            pc(cx, cy, 15.5, "#f4f5f0", "#8d8f93", 1.8, into=inner)                 # tutup putih besar
            inner.append(f'<ellipse cx="{f(cx - 4.5)}" cy="{f(cy - 7)}" rx="8" ry="4" fill="#fff" fill-opacity="0.8"/>')
            inner.append(pl(cx, cy - 15, cx, cy - SK + 2.5, "#f4f5f0", 3.6, 1, "round"))   # penunjuk di kulit
            inner.append(pl(cx, cy - 2, cx, cy - 13, "#3a3b3e", 3.0, 1, "round"))           # penunjuk di tutup
        else:
            rb = 14.5
            pc(cx, cy, rb + 1.6, "#050506", into=inner)
            pc(cx, cy, rb - 0.5, "#0b0c0d", ring, 5.6, into=inner)                   # CINCIN berwarna, tengah berlubang gelap
            pc(cx, cy, rb - 3.8, "#060607", "#1b1c1e", 1.0, into=inner)
            inner.append(f'<path d="M{f(cx - rb*.82)},{f(cy - rb*.42)} A{f(rb)},{f(rb)} 0 0 1 {f(cx - rb*.22)},{f(cy - rb*.96)}" '
                         f'fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="1.6" stroke-linecap="round"/>')
            rect(cx - 4.6, cy - rb - 4.2, 9.2, 7.5, "#0b0c0d", into=inner)          # celah cincin di atas
            rect(cx - 2.3, cy - rb - 5.4, 4.6, 12.5, ring, 1.3, "#050506", 0.8, into=inner)   # takik penunjuk
            inner.append(pl(cx, cy - rb - 7.5, cx, cy - SK + 2, "#f4f5f0", 2.6, .9, "round"))  # garis penunjuk di kulit
        if fn:
            kid = kid or "knob-" + fn.replace(".", "-")
            ctl.append(f'<g id="{kid}" data-cx="{f(cx)}" data-cy="{f(cy)}" data-angle-min="-135" data-angle-max="135" '
                       f'data-value-default="{f(dv)}">{"".join(inner)}</g>')
            hh = SK + 6
            hit("hit-" + kid, cx - hit_w / 2, cy - hh, hit_w, 2 * hh)
            controls.append({"id": kid, "type": "rotary", "hit": "hit-" + kid, "angleMin": -135, "angleMax": 135, "defaultValue": dv})
            mapping[kid] = {"function": fn}
        else:
            ctl.append(dim(f'<g transform="rotate({angle} {f(cx)} {f(cy)})">{"".join(inner)}</g>'))
            deco[d0:] = [dim(x) for x in deco[d0:]]

    # ---------------------------------------------------------------- tombol PHANTOM (toggle) + LED kuning
    def keycap(x, y, w, h, state, color):
        o = []
        rect(x - 2.5, y - 2.5, w + 5, h + 5, "#eceded", 6, into=o)
        if state:
            rect(x, y + 2, w, h - 2, color, 4, "#000", 1.0, into=o)
            rect(x + 3, y + 4, w - 6, h * .3, "#fff", 3, op=.4, into=o)
        else:
            rect(x, y, w, h, "#d3d5d6", 4, "#9a9ea1", 1.0, into=o)
            rect(x + 3, y + 2.5, w - 6, h * .36, "#fff", 3, op=.5, into=o)
        return "".join(o)

    def led_dot(x, y, on):
        if on:
            return (f'<circle cx="{f(x)}" cy="{f(y)}" r="9.5" fill="#ffe94a" fill-opacity="0.3"/>'
                    f'<circle cx="{f(x)}" cy="{f(y)}" r="5.8" fill="#ffe94a" stroke="#8a7a10" stroke-width="1"/>')
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="5.8" fill="#d6cc2c" stroke="#5a550e" stroke-width="1"/>'

    def toggle(fn, x, y, w, h, color, hx, hy, hw, hh, tid=None, led=None):
        tid = tid or "tg-" + fn.split(".")[0]
        lo = led_dot(led[0], led[1], False) if led else ""
        la = led_dot(led[0], led[1], True) if led else ""
        ctl.append(f'<g id="{tid}"><g id="{tid}-normal">{keycap(x, y, w, h, False, color)}{lo}</g>'
                   f'<g id="{tid}-active" display="none">{keycap(x, y, w, h, True, color)}{la}</g></g>')
        hit("hit-" + tid, hx, hy, hw, hh)
        controls.append({"id": tid, "type": "toggle", "hit": "hit-" + tid,
                         "states": {"normal": tid + "-normal", "active": tid + "-active"}, "trigger": "tap"})
        mapping[tid] = {"function": fn}

    def warn_tri(x, y):
        poly([(x, y - 8), (x + 8.5, y + 7), (x - 8.5, y + 7)], "#f2f3f3")
        deco.append(f'<rect x="{f(x-1)}" y="{f(y-3)}" width="2" height="6" fill="#111"/>'
                    f'<rect x="{f(x-1)}" y="{f(y+4)}" width="2" height="2" fill="#111"/>')

    # ============ 1. BODI BERTINGKAT ============
    bg = [
        f'<rect x="0" y="12" width="{W}" height="{H-12}" rx="14" fill="#0c0c0d"/>',
        f'<rect x="38" y="16" width="{W-76}" height="250" rx="8" fill="#17181b"/>',
        f'<rect x="56" y="262" width="{W-112}" height="20" fill="#08090a"/>',
        f'<line x1="56" y1="266" x2="{W-56}" y2="266" stroke="#3a3c40" stroke-width="1.2"/>',
        f'<path d="M38,280 H{W-38} V{H-22} Q{W-38},{H-14} {W-46},{H-14} H46 Q38,{H-14} 38,{H-22} Z" fill="url(#g-face)"/>',
        f'<rect x="38" y="16" width="{W-76}" height="{H-30}" rx="8" fill="none" stroke="#2f3033" stroke-width="2"/>',
        f'<line x1="48" y1="18" x2="{W-48}" y2="18" stroke="#4a4c50" stroke-width="1.4"/>',
        f'<line x1="38" y1="280" x2="{W-38}" y2="280" stroke="#6a6d72" stroke-width="1.6"/>',
    ]
    rnd = random.Random(602)
    for yy in range(286, H - 18, 7):
        bg.append(f'<line x1="40" y1="{yy}" x2="{W-40}" y2="{yy}" stroke="#ffffff" stroke-opacity="0.014" stroke-width="1"/>')
    for (gx0, gx1, gy0, gy1, n) in ((40, W - 40, 18, 258, 150), (40, W - 40, 286, H - 18, 260)):
        for _ in range(n):
            gx, gy = rnd.uniform(gx0, gx1), rnd.uniform(gy0, gy1)
            c, o = (("#ffffff", 0.07) if rnd.random() < .55 else ("#000000", 0.28))
            bg.append(f'<rect x="{f(gx)}" y="{f(gy)}" width="1.3" height="1.3" fill="{c}" fill-opacity="{o}"/>')

    # ============ 2. PANEL ATAS KANAN: logo + panel abu XLR + jack emas ============
    RW = 440; RX = W - PAD - 38 - RW
    RM = RX + RW / 2
    rect(RX, 30, RW, 84, "none", 3, "#d9dbdc", 1.4)
    deco.append(f'<text x="{f(RM)}" y="84" font-family="\'Arial Rounded MT Bold\', \'Arial Black\', Arial, sans-serif" '
                'font-size="56" font-weight="900" text-anchor="middle" letter-spacing="-2" fill="#f1f2f2">d'
                '<tspan fill="#e0342b">B</tspan>voice<tspan font-size="15" font-weight="700" dy="-26" dx="3" fill="#cfd2d4">®</tspan></text>')
    t(RM, 103, "602-RV", 18, CAP, "middle", "bold", 3)
    rect(RX, 118, RW, 128, "url(#g-panel)", 6, "#6a6c6f", 1.5)
    for yy in range(124, 244, 5): line(RX + 6, yy, RX + RW - 6, yy, "#000000", 1, .035)
    xlr(RX + 80, 176); xlr(RX + 190, 176)
    t(RX + 135, 238, "MAIN OUT", 12, "#1a1b1c", "middle", "bold", 1)
    line(RX + 264, 130, RX + 264, 234, "#80838a", 1.3)
    t(RX + 348, 137, "MAIN OUT", 10, "#1a1b1c", "middle", "bold", .6)
    jack63(RX + 316, 162, 15); jack63(RX + 380, 162, 15)
    t(RX + 348, 196, "PHONES", 10, "#1a1b1c", "middle", "bold", .6); jack63(RX + 348, 220, 12)

    # ============ 3. KANAL ============
    CHCFG = [
        dict(title="MIC", sub="Suara mic", tog=("mic.toggle", "MIC"), slots=[("mic.gate", "GATE"), ("mic.volume", "VOLUME")]),
        dict(title="EQ MIC", sub="Tone mic", tog=("eqmic.toggle", "EQ MIC"),
             slots=[("eqmic.high", "HIGH"), ("eqmic.mid", "MID"), ("eqmic.low", "LOW")]),
        dict(title="ECHO", sub="Gema mic", tog=("echo.toggle", "ECHO"),
             slots=[("echo.delay", "DELAY"), ("echo.feedback", "FEEDBACK"), ("echo.mix", "MIX")]),
        dict(title="REVERB", sub="Efek ruang", tog=("reverb.toggle", "REVERB"),
             slots=[("reverb.room", "ROOM"), ("reverb.damp", "DAMP"), ("reverb.width", "WIDTH"),
                    ("reverb.cess", "CESS"), ("reverb.wet", "WET"), ("reverb.dry", "DRY")]),
        dict(title="EQ AUDIO", sub="Tone audio", tog=("eqaudio.toggle", "EQ AUDIO"),
             slots=[("eqaudio.gain", "GAIN"), ("eqaudio.sub", "SUB"), ("eqaudio.high", "HIGH"),
                    ("eqaudio.mid", "MID"), ("eqaudio.low", "LOW")]),
        dict(title="REV AUDIO", sub="Suara app lain", tog=("sysreverb.toggle", "REV AUDIO", "tg-sysreverb"),
             slots=[("sysreverb.gain", "GAIN", 0.5)]),
        dict(title="REVERB", sub="Reverb audio", tog=("sysreverb.reverb.toggle", "REVERB", "tg-sysreverb-reverb"),
             slots=[("sysreverb.wet", "WET", 0.5), ("sysreverb.room", "ROOM", 0.6), ("sysreverb.damp", "DAMP", 0.4),
                    ("sysreverb.width", "WIDTH", 1.0), ("sysreverb.cess", "CESS", 0.4), ("sysreverb.predelay", "PRE-DLY", 0.2)]),
        dict(title="DELAY", sub="Delay audio", tog=("sysreverb.echo.toggle", "DELAY", "tg-sysreverb-echo"),
             slots=[("sysreverb.delay", "DELAY", 0.45), ("sysreverb.feedback", "FEEDBACK", 0.45), ("sysreverb.mix", "MIX", 0.4)]),
        dict(title="KIRIM", sub="Ke reverb", tog=None,
             slots=[("sysreverb.rsend.sub", "SUB", 0.0), ("sysreverb.rsend.low", "LOW", 0.3),
                    ("sysreverb.rsend.mid", "MID", 0.8), ("sysreverb.rsend.high", "HIGH", 1.0)]),
        dict(title="KIRIM", sub="Ke delay", tog=None,
             slots=[("sysreverb.esend.sub", "SUB", 0.0), ("sysreverb.esend.low", "LOW", 0.0),
                    ("sysreverb.esend.mid", "MID", 0.7), ("sysreverb.esend.high", "HIGH", 0.7)]),
    ]
    for x in DIV:
        line(x, 286, x, H - 22, "#9a9da1", 1.2, 0.5)
    for i, cx in enumerate(CH):
        cfg = CHCFG[i]
        # --- panel atas: sel bergaris putih, plat label putih, jack combo, baris PHANTOM, kotak nomor ---
        rect(cx - 62, 24, 124, 238, "none", 2, "#d9dbdc", 1.3)
        rect(cx - 56, 30, 112, 19, "#f1f2f2", 1); t(cx, 44, "LINE IN / MIC", 10.5, "#111213", weight="bold")
        combo(cx, 100)
        TY = 175
        if cfg["tog"]:
            fn, nm = cfg["tog"][:2]
            tid = cfg["tog"][2] if len(cfg["tog"]) > 2 else None
            warn_tri(cx - 45, TY)
            line(cx + 8, TY, cx + 25, TY, "#d0d3d5", 1.8)
            toggle(fn, cx - 27, TY - 13, 34, 26, ORANGE, cx - 62, 150, 124, 72, tid=tid, led=(cx + 33, TY))
            t(cx, 212, nm, TOG_SZ, TXT_LT, weight="bold")
        else:
            d0 = len(deco)
            warn_tri(cx - 45, TY)
            line(cx + 8, TY, cx + 25, TY, "#d0d3d5", 1.8)
            deco.append(keycap(cx - 27, TY - 13, 34, 26, False, ORANGE)); deco.append(led_dot(cx + 33, TY, False))
            t(cx, 212, "-", TOG_SZ, TXT_LT, weight="bold")
            deco[d0:] = [dim(x) for x in deco[d0:]]
        rect(cx - 62, 228, 124, 34, "#0e0f10", 0, "#d9dbdc", 1.3)
        t(cx, 251, str(i + 1), 16, "#f1f2f2", weight="bold")
        # --- panel bawah: band FX/PAN lebih terang, band EQ lebih gelap, plat TRIM abu terang (foto) ---
        rect(cx - 64, ROWS[4] - 53, 128, 88, "#323336", 3, op=.7)
        rect(cx - 64, ROWS[5] - 54, 128, 88, "#d3d5d8", 3)                                 # plat abu terang bawah (foto)
        rect(cx - 64, ROWS[1] - 53, 128, ROWS[3] - ROWS[1] + 53 + 33, "#0c0d0e", 3, op=.6)
        t(cx, 296 + YO, cfg["title"], TITLE_SZ, CAP, weight="bold")
        t(cx, 314 + YO, cfg["sub"], SUB_SZ, TXT)
        rect(cx - 62, 322 + YO, 124, 3, CAP, 1, op=.9)
        rect(cx - 64, 330 + YO, 128, 88, "#d3d5d8", 3)
        for r in range(6):
            cy = ROWS[r]
            if r < len(cfg["slots"]):
                fn, lab = cfg["slots"][r][:2]
                dv = cfg["slots"][r][2] if len(cfg["slots"][r]) > 2 else 0.5
                lt = r in (0, 5)
                t(cx, cy - 41, lab, LAB_SZ, "#17181a" if lt else TXT_LT, weight="bold" if lt else "normal")
                knob(cx, cy, fn, RING[r], dv=dv, tick="#2a2b2e" if lt else "#d4d6d8", style="cap" if RING[r] == "cap" else "ring")
            else:
                knob(cx, cy, None, RING[r], tick="#2a2b2e" if r in (0, 5) else "#d4d6d8", style="cap" if RING[r] == "cap" else "ring")

    # ============ 4. EQ GRAFIS: HANYA 4 slider fungsi (SUB, LOW, MID, HIGH) ============
    SY1, SY2 = 428, 332                                    # y1 = -12 dB (bawah), y2 = +12 dB (atas)
    EQY0, EQY1 = 286, 474
    rect(RX, EQY0, RW, EQY1 - EQY0, "#4c4f58", 5, "#25272b", 1.4)
    rect(RX + 6, EQY0 + 6, RW - 12, 20, "#f4f4f2", 3)
    t(RM, EQY0 + 21, "GRAPHIC EQUALIZER", 12, "#17181a", weight="900", font="'Arial Black', Arial, sans-serif")
    GX0, GX1 = RX + 62, RX + RW - 62
    for k_, (y, lab) in enumerate(zip((332, 356, 380, 404, 428), ("+12", "+6", "0", "-6", "-12"))):
        line(GX0, y + 2.2, GX1, y + 2.2, "#16171a", 2.4, .55)                    # bayangan di bawah garis (timbul seperti foto)
        line(GX0, y, GX1, y, "#f4f5f6", 3.4, 1)                                  # garis tebal berlabel
        t(RX + 52, y + 4, lab, 10, "#dfe1e4", "end"); t(RX + RW - 52, y + 4, lab, 10, "#dfe1e4", "start")
    BANDS = [("", "eqaudio.sub", "SUB"), ("", "eqaudio.low", "LOW"), ("", "eqaudio.mid", "MID"), ("", "eqaudio.high", "HIGH")]
    for k, (fq, fn, nm) in enumerate(BANDS):
        x = RX + 102 + 79 * k
        t(x, EQY1 - 14, nm, 12, "#f4f5f6", weight="bold")
        sid = "slider-" + fn.replace(".", "-")
        rect(x - 7.5, SY2 - 14, 15, SY1 - SY2 + 28, "#050506", 7, "#000", 1)      # alur hitam lebar + bayangan (foto)
        rect(x - 3.5, SY2 - 10, 2, SY1 - SY2 + 20, "#2a2b2e", 1)                  # kilau tipis di tepi kiri alur
        inner = [f'<rect x="{f(x-12)}" y="{f(SY1-14)}" width="24" height="28" fill="none"/>',          # rect PERTAMA = kotak handle, pusat = nilai 0
                 f'<rect x="{f(x-10)}" y="{f(SY1-10)}" width="20" height="25" rx="3" fill="#000" fill-opacity="0.5"/>',
                 f'<rect x="{f(x-10)}" y="{f(SY1-12)}" width="20" height="24" rx="3" fill="url(#g-eqcap)" stroke="#0a0a0b" stroke-width="1.2"/>']
        for dy in (-8.5, -5.5, 5.5, 8.5):
            inner.append(pl(x - 7, SY1 + dy, x + 7, SY1 + dy, "#6c6e72", 1.1, .9))
        inner.append(f'<rect x="{f(x-6.5)}" y="{f(SY1-2)}" width="13" height="4" rx="1.6" fill="#fafaf7"/>')   # batang putih terang
        ctl.append(f'<g id="{sid}" data-x1="{f(x)}" data-y1="{f(SY1)}" data-x2="{f(x)}" data-y2="{f(SY2)}" '
                   f'data-value-default="0.5">{"".join(inner)}</g>')
        hit("hit-" + sid, x - 22, SY2 - 16, 44, SY1 - SY2 + 32)
        controls.append({"id": sid, "type": "slider", "hit": "hit-" + sid, "defaultValue": 0.5})
        mapping[sid] = {"function": fn}

    # ============ 5. LAYAR MATI + tombol putih + knob encoder + USB + Bluetooth (hiasan, gelap 50%) ============
    DY0, DY1 = 480, 586
    def disp():
        rect(RX, DY0, RW, DY1 - DY0, "#1a1b1d", 5, "#3a3d40", 1.2)
        rect(RX + 8, DY0 + 7, 128, 38, "#030304", 3, "#2a2c2f", 1.2)             # layar kiri MATI
        rect(RX + 142, DY0 + 7, 186, 38, "#030304", 3, "#2a2c2f", 1.2)           # layar kanan MATI
        # port USB-A pada plat putih
        rect(RX + 336, DY0 + 7, 96, 38, "#e8e9ea", 3, "#222", 1.2)
        rect(RX + 346, DY0 + 12, 38, 28, "#111214", 3, "#8a8c90", 1.4); rect(RX + 350, DY0 + 21, 30, 9, "#8d9094", 1.5)
        # encoder + tombol bulat putih
        pc(RX + 78, DY0 + 75, 21, "#0d0e0f", "#3c3e42", 1.6)
        for n in range(20):
            a = math.radians(n * 18)
            deco.append(pl(RX + 78 + 15 * math.sin(a), DY0 + 75 - 15 * math.cos(a), RX + 78 + 20 * math.sin(a), DY0 + 75 - 20 * math.cos(a), "#3c3e42", 1.6))
        pc(RX + 78, DY0 + 75, 12, "#f4f5f0", "#9a9c9f", 1.4)
        for k in range(4):
            bx = RX + 168 + 50 * k
            pc(bx, DY0 + 70, 11, "#f2f3f3", "#111", 1.2); pc(bx, DY0 + 70, 5, "#26272a")
        # simbol media di bawah tombol
        bx = RX + 168 + 50 * 1
        poly([(RX + 160, DY0 + 90), (RX + 160, DY0 + 98), (RX + 166, DY0 + 94)], "#f2f3f3"); rect(RX + 168, DY0 + 90, 2, 8, "#f2f3f3")
        poly([(RX + 218, DY0 + 94), (RX + 224, DY0 + 90), (RX + 224, DY0 + 98)], "#f2f3f3"); poly([(RX + 224, DY0 + 94), (RX + 230, DY0 + 90), (RX + 230, DY0 + 98)], "#f2f3f3")
        poly([(RX + 262, DY0 + 90), (RX + 268, DY0 + 94), (RX + 262, DY0 + 98)], "#f2f3f3"); poly([(RX + 268, DY0 + 90), (RX + 274, DY0 + 94), (RX + 268, DY0 + 98)], "#f2f3f3")
        # bluetooth
        rect(RX + 370, DY0 + 54, 30, 30, "none", 4, "#e8e9ea", 1.6)
        deco.append(f'<polyline points="{f(RX+379)},{f(DY0+64)} {f(RX+392)},{f(DY0+75)} {f(RX+385)},{f(DY0+81)} {f(RX+385)},{f(DY0+57)} {f(RX+392)},{f(DY0+63)} {f(RX+379)},{f(DY0+74)}" '
                    f'fill="none" stroke="#e8e9ea" stroke-width="1.8" stroke-linejoin="round"/>')
        rect(RX + 358, DY0 + 90, 54, 12, "none", 3, "#e8e9ea", 1.4)
    dimmed(disp)
    t(RX + 72, DY0 + 19, "24-BIT DSP", 7.5, TXT, "middle", "bold"); t(RX + 235, DY0 + 19, "U-DISK MP3", 8, TXT, "middle", "bold"); t(RX + 318, DY0 + 41, "USB", 8, TXT, "end", "bold")
    t(RX + 417, DY0 + 29, "USB", 9, "#111213", "middle", "bold", rot=-90)
    t(RX + 168, DY0 + 52, "REC", 8, TXT_LT, "middle", "bold"); t(RX + 318, DY0 + 99, "MODE", 8, TXT_LT, "middle", "bold")
    t(RX + 385, DY0 + 99, "BLUETOOTH", 6.5, TXT_LT, "middle", "bold")
    t(RX + 24, DY0 + 68, "99", 15, TXT_LT, "middle", "bold"); t(RX + 24, DY0 + 81, "DSP", 8, TXT_LT, "middle", "bold")

    # ============ 6. METER (LED) + FADER di plat perak ============
    MY0 = 592
    rect(RX, MY0, RW, 280, "#161718", 5, "#3a3d40", 1.2)
    pc(RX + 50, 616, 11, RED, op=.28); pc(RX + 50, 616, 7, "#ff3a2e"); pc(RX + 50, 616, 3, "#ffe2de")
    t(RX + 68, 620, "POWER", 10.5, TXT_LT, "start", "bold")
    cols = ["#32c43a"] * 3 + ["#f3dd2a"] + ["#e8261e"] * 3
    ys = [832 - 32 * i for i in range(7)]
    labs = ["-20", "-6", "0", "+2", "+6", "+10", "PEAK"]
    MX = {"mic": RX + 50, "out": RX + 146, "sys": RX + 196}
    for side, mid_ in (("mic", "meter.mic"), ("out", "meter.output"), ("sys", "meter.sysreverb")):
        xm = MX[side]
        for s_ in range(1, 8):
            yc, col = ys[s_ - 1], cols[s_ - 1]
            pc(xm, yc, 8, col, "#050505", 1.2, op=.28)
            lid = f"led-{side}-{s_}"
            ctl.append(f'<g id="{lid}-on" display="none"><rect x="{f(xm-13)}" y="{f(yc-13)}" width="26" height="26" rx="13" fill="{col}" fill-opacity="0.3"/>'
                       f'<circle cx="{f(xm)}" cy="{f(yc)}" r="8" fill="{col}" stroke="#050505" stroke-width="1.2"/>'
                       f'<circle cx="{f(xm-2)}" cy="{f(yc-2.5)}" r="2.6" fill="#fff" fill-opacity="0.55"/></g>')
            indicators.append({"id": lid, "meter": mid_, "level": round((s_ - 0.5) / 7, 3), "on": lid + "-on"})
    for s_ in range(7):
        t(RX + 98, ys[s_] + 4, labs[s_], 10.5, TXT_LT if s_ < 6 else TXT, weight="bold")
        line(RX + 64, ys[s_], RX + 80, ys[s_], "#a4a7aa", 1.3, .8); line(RX + 116, ys[s_], RX + 132, ys[s_], "#a4a7aa", 1.3, .8)
    for xm, lab in ((MX["mic"], "L"), (MX["out"], "R"), (MX["sys"], "SYS")):                  # tag putih seperti foto
        wtag = 18 if len(lab) == 1 else 34
        rect(xm - wtag / 2, 846, wtag, 17, "#eeeeec", 3); t(xm, 859, lab, 11.5, "#17181a", weight="bold")
    # plat fader perak + skala dB
    rect(RX + 246, 600, 186, 264, "url(#g-fader)", 4, "#5d6064", 1.2)
    for yy in range(604, 860, 6): line(RX + 250, yy, RX + 428, yy, "#000000", 1, .035)
    FY1, FY2 = 810, 640
    SCALE = ["10", "5", "0", "5", "10", "20", "30", "40", "-"]
    for x, fn, lab in ((RX + 299, "mic.volume", "VOL MIC"), (RX + 379, "eqaudio.gain", "GAIN")):
        sid = "slider-fader-" + fn.replace(".", "-")
        for k in range(9):
            yt = FY2 + (FY1 - FY2) * k / 8
            line(x - 30, yt, x - 18, yt, "#2c2d30", 1.6); line(x + 18, yt, x + 30, yt, "#2c2d30", 1.6)
            t(x + 40 if x < RX + 340 else x + 40, yt + 3, SCALE[k] if k < 8 else "\u221e", 7.5, "#2a2b2e", "middle", "bold")
            if k < 8:
                for m_ in (1, 2, 3):
                    ym = yt + (FY1 - FY2) / 8 * m_ / 4
                    line(x - 26, ym, x - 20, ym, "#55575a", 1.0); line(x + 20, ym, x + 26, ym, "#55575a", 1.0)
        rect(x - 7.5, FY2 - 14, 15, FY1 - FY2 + 28, "#050506", 7.5, "#000", 1.2)               # alur hitam sempit
        rect(x - 3.5, FY2 - 10, 2, FY1 - FY2 + 20, "#2b2c2f", 1)
        inner = [f'<rect x="{f(x-21)}" y="{f(FY1-26)}" width="42" height="52" fill="none"/>',    # rect PERTAMA = kotak handle
                 f'<rect x="{f(x-17)}" y="{f(FY1-22)}" width="38" height="52" rx="8" fill="#000" fill-opacity="0.35"/>']
        for by in (FY1 - 26, FY1 + 2):                                                           # DUA blok gelap bertingkat (foto)
            inner.append(f'<rect x="{f(x-19)}" y="{f(by)}" width="38" height="23" rx="6" fill="url(#g-fcap)" stroke="#f6f6f3" stroke-width="3"/>')
            for dy in (6, 11.5, 17):
                inner.append(pl(x - 12, by + dy, x + 12, by + dy, "#8e9094", 1.3, .85))
        inner.append(pl(x - 14, FY1, x + 14, FY1, "#f6f6f3", 2.4, 1, "round"))                    # penanda nilai di celah
        ctl.append(f'<g id="{sid}" data-x1="{f(x)}" data-y1="{f(FY1)}" data-x2="{f(x)}" data-y2="{f(FY2)}" data-value-default="0.5">{"".join(inner)}</g>')
        hit("hit-" + sid, x - 22, 622, 44, 214)
        controls.append({"id": sid, "type": "slider", "hit": "hit-" + sid, "defaultValue": 0.5})
        mapping[sid] = {"function": fn}
        t(x, 855, lab, 11, "#17181a", weight="bold")

    # ============ 7. SEKRUP SAMPING ============
    for sy in (120, 330, 560, 820):
        screw(10, sy, 4.5); screw(W - 10, sy, 4.5)

    defs = ('<defs>'
            '<linearGradient id="g-face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d2e31"/><stop offset=".5" stop-color="#27282a"/><stop offset="1" stop-color="#1e1f21"/></linearGradient>'
            '<linearGradient id="g-silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e2e2dd"/><stop offset=".5" stop-color="#8c8c87"/><stop offset="1" stop-color="#c4c4bf"/></linearGradient>'
            '<linearGradient id="g-brass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9d9a0"/><stop offset=".5" stop-color="#a98d45"/><stop offset="1" stop-color="#d8c27e"/></linearGradient>'
            '<linearGradient id="g-panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8dadc"/><stop offset="1" stop-color="#b6b8ba"/></linearGradient>'
            '<linearGradient id="g-fader" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c3c4c6"/><stop offset=".5" stop-color="#dcdddd"/><stop offset="1" stop-color="#bbbcbe"/></linearGradient>'
            '<linearGradient id="g-eqcap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b4d51"/><stop offset=".5" stop-color="#2b2c2f"/><stop offset="1" stop-color="#18191b"/></linearGradient>'
            '<linearGradient id="g-fcap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f5155"/><stop offset=".5" stop-color="#2f3033"/><stop offset="1" stop-color="#1b1c1e"/></linearGradient>'
            '</defs>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" data-skin-name="{NAME}" data-skin-version="{VER}" data-skin-author="{AUTHOR}" '
           f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n<title>{NAME}</title>\n{defs}\n'
           + "\n".join(bg) + "\n" + "\n".join(deco) + "\n" + "\n".join(ctl) + "\n" + "\n".join(hits) + "\n</svg>\n")
    skin = {"schemaVersion": 1, "name": NAME, "version": VER, "author": AUTHOR, "svg": "skin.svg",
            "viewBox": f"0 0 {W} {H}", "layout": {"padZone": f"0 0 {W} {H}"},
            "controls": controls, "mapping": mapping, "indicators": indicators}
    return svg, skin


def main():
    os.makedirs(OUT, exist_ok=True)
    svg, skin = build(False)
    prev, _ = build(True)
    open(os.path.join(OUT, "skin.svg"), "w", encoding="utf-8").write(svg)
    open(os.path.join(OUT, "preview.svg"), "w", encoding="utf-8").write(prev)
    json.dump(skin, open(os.path.join(OUT, "skin.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("OK ->", OUT, "| kontrol:", len(skin["controls"]), "| led:", len(skin["indicators"]))

if __name__ == "__main__":
    main()
