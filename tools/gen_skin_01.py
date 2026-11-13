#!/usr/bin/env python3
"""Generator skin-01 : Yamaha MG12XUK (MIXJOS Mixer) v3.0 - LANDSCAPE 1800 x 900.

Koordinat tata letak tetap dalam piksel FOTO REFERENSI (muka bodi x 59..741, y 70..730).
Bedanya dengan v2: skala X dan Y terpisah (peregangan landscape).
  X()/LX()  -> diregangkan ke samping (SX)              : kotak, plat, garis, panel, posisi
  Y()/LY()  -> skala tinggi (SY)
  LR()      -> skala BULAT (seragam, tidak diregangkan)  : kenop, jack, sekrup, RCA, logo
  LT()      -> skala teks / tebal garis
Jalankan: python3 tools/gen_skin_01.py
"""
import json, math, os, re
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "skins", "skin-01")
NAME, VER, AUTHOR = "Yamaha MG12XUK Mixer", "3.1", "MIXJOS"
FONT = "Arial, Helvetica, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"

H = 900
WALL = 30                           # tebal dinding samping (px)
SX = (1800 - 2 * WALL) / 682.0      # skala X tetap (dari lebar asli 1800)
# v3.1: kolom kanal 6-10 = REVERB AUDIO (fitur baru). Kolom 1-5 TIDAK berubah; panel kanan (SPX dst) hanya bergeser ke kanan.
# Panel kanan = koordinat foto x >= 573.8 yang dulu digeser -219.2 (kolom 6 + strip 7-12 dipotong); kini digeser +54.8
# (panel mulai di x foto 628.6 = tepat setelah kolom 10). Flag _R menandai gambar panel kanan; kolom kanal memakai koordinat apa adanya.
CUT_X1 = 80.6 + 54.8 * 9
CUT = -54.8
_R = [False]
W = int(round(1800 - CUT * SX))     # bodi jadi lebih sempit, tanpa sisa
SY = H / 660.0                      # foto y 70..730 -> 0..H          (~1.45)
SR = 1.42                           # skala benda bulat (seragam)
ST = 1.42                           # skala teks

def X(x): return WALL + ((x - CUT if _R[0] else x) - 59) * SX
def Y(y): return (y - 70) * SY
def LX(v): return v * SX
def LY(v): return v * SY
def LR(v): return v * SR
def LT(v): return v * ST
def f(v): return ("%.2f" % v).rstrip("0").rstrip(".")

FACE = "#272828"; BLUE = "#0265d3"; BLUE_LINE = "#1a6fd4"
TXT = "#a3a8ab"; TXT_LT = "#d3d6d8"; WHITE_CAP = "#f4f5f0"; LB = "#d7e6f8"

CH = [108 + 54.8 * i for i in range(10)]
DIV = [80.6 + 54.8 * i for i in range(11)]   # garis pembatas: tepat di tengah antar kolom (pitch 54.8)
ST_X = [108 + 54.8 * i for i in range(6, 9)]   # 3 kolom strip, pitch sama dengan channel
ROWY = dict(gain=318, comp=374, high=430, mid=486, low=542, fx=598, pan=654, level=650)   # pitch rata 56
ROWYS = dict(high=410, low=468, fx=526, pan=584, level=642)   # strip 7-12 (hiasan)


def build(preview):
    deco, ctl, hits = [], [], []
    controls, mapping, indicators = [], {}, []

    # ---------- primitif piksel ----------
    def pc(px, py, r, fill, stroke=None, sw=1.0, op=None, into=None, dash=None):
        """lingkaran: pusat piksel, r piksel."""
        s = f' stroke="{stroke}" stroke-width="{f(sw)}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        d = f' stroke-dasharray="{f(dash)} {f(dash)}"' if dash else ""
        (deco if into is None else into).append(
            f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r)}" fill="{fill}"{o}{s}{d}/>')

    def pl(x1, y1, x2, y2, col, w, op=1.0, cap=None):
        c = f' stroke-linecap="{cap}"' if cap else ""
        return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" '
                f'stroke="{col}" stroke-width="{f(w)}" stroke-opacity="{op}"{c}/>')

    # ---------- primitif foto (diregangkan) ----------
    def t(x, y, s, size=6.5, fill=TXT, anchor="middle", weight="normal", ls=0, font=FONT, dy=0):
        e = f' letter-spacing="{f(LT(ls))}"' if ls else ""
        deco.append(f'<text x="{f(X(x))}" y="{f(Y(y) + dy)}" font-family="{font}" font-size="{f(LT(size))}" '
                    f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{e}>{escape(s)}</text>')

    def line(x1, y1, x2, y2, col=BLUE_LINE, w=1.0, op=1.0, cap=None):
        deco.append(pl(X(x1), Y(y1), X(x2), Y(y2), col, LT(w), op, cap))

    def poly(pts, col=BLUE_LINE, w=1.0):
        d = "M" + " L".join(f"{f(X(a))},{f(Y(b))}" for a, b in pts)
        deco.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{f(LT(w))}" stroke-linejoin="round"/>')

    def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1.0, op=None, into=None):
        s = f' stroke="{stroke}" stroke-width="{f(LT(sw))}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        r = f' rx="{f(LT(rx))}"' if rx else ""
        (deco if into is None else into).append(
            f'<rect x="{f(X(x))}" y="{f(Y(y))}" width="{f(LX(w))}" height="{f(LY(h))}"{r} fill="{fill}"{o}{s}/>')

    def hit(hid, x, y, w, h):
        a = ('fill="#ff2d55" fill-opacity="0.28" stroke="#ff2d55" stroke-width="1"' if preview
             else 'fill="#000" fill-opacity="0"')
        hits.append(f'<rect id="{hid}" x="{f(X(x))}" y="{f(Y(y))}" width="{f(LX(w))}" height="{f(LY(h))}" {a}/>')

    def hit_px(hid, px, py, w, h):
        a = ('fill="#ff2d55" fill-opacity="0.28" stroke="#ff2d55" stroke-width="1"' if preview
             else 'fill="#000" fill-opacity="0"')
        hits.append(f'<rect id="{hid}" x="{f(px - w / 2)}" y="{f(py - h / 2)}" width="{f(w)}" height="{f(h)}" {a}/>')

    def screw(px, py, r=4.6, ang=35):
        r = LR(r)
        pc(px, py, r + 1.4, "#0a0a0a")
        pc(px, py, r, "#62656a", "#111", 1.0)
        pc(px - r * 0.25, py - r * 0.3, r * 0.55, "#8a8d92", op=0.55)
        a = math.radians(ang)
        deco.append(pl(px - r * 0.7 * math.cos(a), py - r * 0.7 * math.sin(a),
                       px + r * 0.7 * math.cos(a), py + r * 0.7 * math.sin(a), "#15161a", 1.6))

    # ---------------- jack (BULAT) ----------------
    JS = 1.12                                    # jack sedikit lebih besar dari skala bulat umum
    def combo(cx, cy):
        px, py = X(cx), Y(cy); k = LR(JS)
        pc(px + 1, py + 2, 26.5 * k, "#000", op=0.5)
        pc(px, py, 26 * k, "#0d0d0e", "#2c2c2e", 1.4)
        pc(px, py, 21.8 * k, "#18181a", "#303033", 1.2)
        pc(px, py, 16.5 * k, "#101011", "#38383b", 1.2)
        pc(px, py, 9.5 * k, "#040404", "#4a4a4d", 1.4)
        for dx, dy in ((-5.5, -3.5), (5.5, -3.5), (0, 6.2)):
            pc(px + dx * k, py + dy * k, 1.7 * k, "#44444a")
        deco.append(pl(px - 3.5 * k, py - 9.2 * k, px + 3.5 * k, py - 9.2 * k, "#5a5a5e", 1.8))
        screw(px - 24 * k, py - 23 * k, 4.6 * JS); screw(px + 24 * k, py + 25 * k, 4.6 * JS, -40)

    def trs(cx, cy, r=12.6):
        px, py = X(cx), Y(cy); k = LR(JS)
        r = r * k
        pc(px, py, r + 2, "#0a0a0a")
        pc(px, py, r, "url(#g-silver)", "#2a2a2a", 1.3)
        pc(px, py, r * 0.66, "#050505", "#7a7a78", 1.2)
        pc(px - 1.5, py - 1.5, r * 0.34, "#242426", "#6a6a68", 1.0)

    def xlr(cx, cy):
        px, py = X(cx), Y(cy); k = LR(JS)
        pc(px + 1, py + 2, 23.5 * k, "#000", op=0.5)
        pc(px, py, 23 * k, "#0b0b0c", "#2a2a2c", 1.4)
        pc(px, py, 19.5 * k, "#151516", "#343437", 1.4)
        pc(px, py, 15 * k, "#0a0a0b", "#2a2a2c", 1.2)
        for dx, dy in ((-7, -3.6), (7, -3.6), (0, 8)):
            pc(px + dx * k, py + dy * k, 2.4 * k, "#c9a94f", "#5a4a1a", 0.9)
        screw(px - 21 * k, py - 23 * k, 4.6 * JS); screw(px + 21 * k, py + 19 * k, 4.6 * JS, -40)

    def rca(cx, cy, col):
        px, py = X(cx), Y(cy); k = LR(JS)
        pc(px, py, 12.6 * k, "#0a0a0a")
        pc(px, py, 11.6 * k, "url(#g-silver)", "#333", 1.2)
        pc(px, py, 7.4 * k, col, "#222", 1.2)
        pc(px, py, 3.6 * k, "#0c0c0c", "#999", 0.9)

    # ---------------- knob (BULAT) ----------------
    KS = 1.4   # skala knob (SATU ukuran besar untuk semua knob)
    BASE = (13.0, 9.2, WHITE_CAP, "#111", 15.6, 19.6, 11)
    SMALL = (7.15, 5.06, WHITE_CAP, "#111", 8.58, 10.78, 11)   # hanya PROGRAM/PARAMETER (ruang panel SPX sempit)
    KN = {k: BASE for k in ("gain", "comp", "eq", "fx", "pan", "level", "stereo", "mon", "fxrtn")}
    KN.update(param=SMALL, prog=SMALL)
    TICKC = {}
    BIG = ()

    def kpx(kind):
        """radius (piksel) badan & ujung tick knob."""
        rb, rc, cap, ptr, ti, to, nt = KN[kind]
        k = LR(KS)
        return rb * k, to * k

    def dim(sv, k=0.5):
        def one(m):
            h = m.group(1)
            if len(h) == 3: h = "".join(c * 2 for c in h)
            return "#%02x%02x%02x" % tuple(int(int(h[j:j+2], 16) * k) for j in (0, 2, 4))
        return re.sub(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z-])", one, sv)

    def knob(cx, cy, kind, fn=None, angle=0, hit_w=None, dv=0.5):
        d0 = len(deco)
        px, py = X(cx), Y(cy)
        k = LR(KS)
        rb, rc, cap, ptr, ti, to, nt = [v * k if i in (0, 1, 4, 5) else v for i, v in enumerate(KN[kind])]
        for n in range(nt):
            a = math.radians(-135 + 270 * n / (nt - 1))
            deco.append(pl(px + ti * math.sin(a), py - ti * math.cos(a), px + to * math.sin(a), py - to * math.cos(a),
                           TICKC.get(kind, "#e1e4e6"), 1.7))
        if False:
            r = 16.3 * k
            for a0, a1, col in ((-135, -50, "#74777b"), (-42, 42, "#9a9da1"), (50, 135, "#74777b")):
                p0 = (px + r * math.sin(math.radians(a0)), py - r * math.cos(math.radians(a0)))
                p1 = (px + r * math.sin(math.radians(a1)), py - r * math.cos(math.radians(a1)))
                deco.append(f'<path d="M{f(p0[0])},{f(p0[1])} A{f(r)},{f(r)} 0 0 1 {f(p1[0])},{f(p1[1])}" '
                            f'fill="none" stroke="{col}" stroke-width="{f(4.6 * k)}"/>')
        pc(px + 1.2, py + 2.2, rb + 1.2, "#000", op=0.5)
        inner = []
        pc(px, py, rb, "#0c0c0d", "#000", 1.4, into=inner)               # lingkaran PERTAMA = body (dipakai validator)
        pc(px, py, rb - 2.1, "none", "#4a4c50", 1.3, into=inner, dash=2.0)
        if cap:
            pc(px, py, rc + 2.0, "#050505", into=inner)
            pc(px, py, rc, cap, "#000", 1.0, into=inner)
            inner.append(f'<ellipse cx="{f(px - rc * 0.2)}" cy="{f(py - rc * 0.33)}" rx="{f(rc * 0.5)}" ry="{f(rc * 0.25)}" fill="#fff" fill-opacity="0.22"/>')
            if kind in BIG:
                inner.append(pl(px, py - rc * 0.2, px, py - rc + 0.8, ptr, 4.2, 1, "round"))
                inner.append(pl(px, py - rc - 0.8, px, py - rb + 3.0, "#f2f2f2", 2.7, 1, "round"))
            else:
                inner.append(pl(px, py - rc * 0.05, px, py - rc + 1.2, ptr, 3.6, 1, "round"))
            if False:
                inner.append(pl(px, py - rb - 0.3, px, py - rb + 4.8, "#38f0cf", 2.7, 1, "round"))
        else:  # PROGRAM
            pc(px, py, rb - 5.2, "#1e1e20", "#050505", 1.4, into=inner)
            pc(px - 3, py - 3.8, rb * 0.45, "#fff", op=0.07, into=inner)
        if fn:
            kid = "knob-" + fn.replace(".", "-")
            ctl.append(f'<g id="{kid}" data-cx="{f(px)}" data-cy="{f(py)}" data-angle-min="-135" data-angle-max="135" '
                       f'data-value-default="{f(dv)}">{"".join(inner)}</g>')
            hh = rb + (6 if kind in BIG else 9)
            hw = hit_w if hit_w else 2 * hh
            hit_px("hit-" + kid, px, py, hw, 2 * hh)
            controls.append({"id": kid, "type": "rotary", "hit": "hit-" + kid, "angleMin": -135, "angleMax": 135, "defaultValue": dv})
            mapping[kid] = {"function": fn}
        else:
            ctl.append(dim(f'<g transform="rotate({angle} {f(px)} {f(py)})">{"".join(inner)}</g>'))
            deco[d0:] = [dim(x) for x in deco[d0:]]   # knob tanpa fungsi: digelapkan 50%

    # ---------------- tombol / toggle ----------------
    def keycap(x, y, w, h, state, color):
        o = []
        if state:
            rect(x, y, w, h, color, 1.8, "#000", 1.0, into=o)
            rect(x + 1.2, y + 1.0, w - 2.4, h * 0.38, "#fff", 1.2, op=0.4, into=o)
        else:
            rect(x - 0.8, y - 0.8, w + 1.6, h + 1.6, "#101112", 2.2, into=o)
            rect(x, y, w, h, "#7d8286", 1.7, "#2a2c2e", 0.8, into=o)
            rect(x + 1.2, y + 1.0, w - 2.4, h * 0.38, "#fff", 1.2, op=0.22, into=o)
        return "".join(o)

    def toggle(fn, x, y, w, h, color, hx, hy, hw, hh, tid=None):
        tid = tid or "tg-" + fn.split(".")[0]
        ctl.append(f'<g id="{tid}"><g id="{tid}-normal">{keycap(x, y, w, h, False, color)}</g>'
                   f'<g id="{tid}-active" display="none">{keycap(x, y, w, h, True, color)}</g></g>')
        hit("hit-" + tid, hx, hy, hw, hh)
        controls.append({"id": tid, "type": "toggle", "hit": "hit-" + tid,
                         "states": {"normal": tid + "-normal", "active": tid + "-active"}, "trigger": "tap"})
        mapping[tid] = {"function": fn}

    # ============ 1. BODI ============
    R8 = LR(11)
    TOP = LY(7)                      # tepi atas bodi (bump handle menonjol di atasnya)
    XL, XR = WALL, W - WALL
    def wall(x0, x1, left):
        r = R8
        if left:
            return (f'M{f(x0 + r)},{f(TOP)} H{f(x1)} V{f(H)} H{f(x0 + r)} Q{f(x0)},{f(H)} {f(x0)},{f(H - r)} '
                    f'V{f(TOP + r)} Q{f(x0)},{f(TOP)} {f(x0 + r)},{f(TOP)} Z')
        return (f'M{f(x0)},{f(TOP)} H{f(x1 - r)} Q{f(x1)},{f(TOP)} {f(x1)},{f(TOP + r)} V{f(H - r)} '
                f'Q{f(x1)},{f(H)} {f(x1 - r)},{f(H)} H{f(x0)} Z')
    _R[0] = True; hb2 = (X(702), X(743)); _R[0] = False
    hb1 = (X(58), X(90))
    bg = [
        f'<rect x="0" y="{f(TOP)}" width="{W}" height="{f(H - TOP)}" rx="{f(R8)}" fill="#141414"/>',
        f'<rect x="{f(XL)}" y="{f(TOP)}" width="{f(XR - XL)}" height="{f(LY(24))}" fill="url(#g-topband)"/>',
        f'<rect x="{f(XL)}" y="{f(Y(101))}" width="{f(XR - XL)}" height="{f(Y(710) - Y(101))}" fill="url(#g-face)"/>',
        f'<rect x="{f(XL)}" y="{f(Y(710))}" width="{f(XR - XL)}" height="{f(H - Y(710))}" fill="url(#g-bottom)"/>',
        f'<path d="{wall(0, XL, True)}" fill="url(#g-wall-l)"/>',
        f'<line x1="{f(WALL * 0.8)}" y1="{f(TOP + 16)}" x2="{f(WALL * 0.8)}" y2="{f(H - 12)}" stroke="#383838" stroke-width="1.4"/>',
        f'<line x1="{f(XL)}" y1="{f(TOP)}" x2="{f(XL)}" y2="{f(H)}" stroke="#050505" stroke-width="2"/>',
        f'<path d="{wall(XR, W, False)}" fill="url(#g-wall-r)"/>',
        f'<line x1="{f(W - WALL * 0.8)}" y1="{f(TOP + 16)}" x2="{f(W - WALL * 0.8)}" y2="{f(H - 12)}" stroke="#383838" stroke-width="1.4"/>',
        f'<line x1="{f(XR)}" y1="{f(TOP)}" x2="{f(XR)}" y2="{f(H)}" stroke="#050505" stroke-width="2"/>',
        f'<line x1="{f(XL)}" y1="{f(H - 1.6)}" x2="{f(XR)}" y2="{f(H - 1.6)}" stroke="#4a4b45" stroke-width="2"/>',
        # handle kecil di atas (menonjol)
        f'<path d="M{f(hb1[0])},{f(TOP)} Q{f(hb1[0] + 6)},{f(2)} {f(hb1[0] + 22)},{f(0.8)} H{f(hb1[1] - 22)} Q{f(hb1[1] - 6)},{f(2)} {f(hb1[1])},{f(TOP)} Z" fill="#232324" stroke="#0a0a0a" stroke-width="1.2"/>',
        f'<path d="M{f(hb2[0])},{f(TOP)} Q{f(hb2[0] + 6)},{f(2)} {f(hb2[0] + 22)},{f(0.8)} H{f(hb2[1] - 22)} Q{f(hb2[1] - 6)},{f(2)} {f(hb2[1])},{f(TOP)} Z" fill="#232324" stroke="#0a0a0a" stroke-width="1.2"/>',
    ]

    # ============ 2. GARIS BIRU ============
    for k, x in enumerate(DIV):         # DIV[10] = pembatas kolom 10 ke panel kanan
        line(x, 103, x, 705)

    # ============ 3. PANEL BIRU ATAS ============
    _R[0] = True                                  # panel kanan (bergeser)
    rect(577, 78, 145, 22, "url(#g-bluestripe)", 3)
    for n in range(6):
        line(579, 81 + n * 3.4, 720, 81 + n * 3.4, "#a8d0f2", 0.7, 0.55)
    rect(577, 102, 42, 51, BLUE, 2); rect(577, 155, 42, 92, BLUE, 2)
    rect(621, 102, 101, 83, BLUE, 2); rect(621, 187, 56, 60, BLUE, 2); rect(679, 187, 43, 60, BLUE, 2)
    trs(598, 133); trs(598, 173); trs(598, 215)
    xlr(647, 138); xlr(697, 138)
    trs(637, 217); trs(663, 217)
    trs(700, 217)

    # ============ 4. KANAL 1-10 (1-5 fitur lama, 6-10 REVERB AUDIO baru) ============
    _R[0] = False
    CHCFG = [
        dict(title="MIC", sub="Suara mic", acc="#ff5a3c", tog=("mic.toggle", "MIC"), slots={
            "gain": ("mic.gate", "GATE", "010", None, ""),
            "level": ("mic.volume", "VOLUME", "010", None, "")}),
        dict(title="EQ MIC", sub="Tone mic", acc="#35d0ff", tog=("eqmic.toggle", "EQ MIC"), slots={
            "high": ("eqmic.high", "HIGH", "eq", None, "10kHz"),
            "mid": ("eqmic.mid", "MID", "eq", None, "2.5kHz"),
            "low": ("eqmic.low", "LOW", "eq", None, "100Hz")}),
        dict(title="ECHO", sub="Gema mic", acc="#ffb02e", tog=("echo.toggle", "ECHO"), slots={
            "gain": ("echo.delay", "DELAY", "010", None, ""),
            "comp": ("echo.feedback", "FEEDBACK", "010", None, ""),
            "level": ("echo.mix", "MIX", "010", None, "")}),
        dict(title="REVERB", sub="Efek ruang", acc="#b58cff", tog=("reverb.toggle", "REVERB"), slots={
            "gain": ("reverb.room", "ROOM", "010", None, ""),
            "comp": ("reverb.damp", "DAMP", "010", None, ""),
            "high": ("reverb.width", "WIDTH", "010", None, ""),
            "mid": ("reverb.cess", "CESS", "010", None, ""),
            "low": ("reverb.wet", "WET", "010", "fx", ""),
            "fx": ("reverb.dry", "DRY", "010", None, "")}),
        dict(title="EQ AUDIO", sub="Tone audio", acc="#4cd98a", tog=("eqaudio.toggle", "EQ AUDIO"), slots={
            "gain": ("eqaudio.gain", "GAIN", "010", None, ""),
            "comp": ("eqaudio.sub", "SUB", "010", None, ""),
            "high": ("eqaudio.high", "HIGH", "eq", None, "10kHz"),
            "mid": ("eqaudio.mid", "MID", "eq", None, "2.5kHz"),
            "low": ("eqaudio.low", "LOW", "eq", None, "100Hz")}),
        # ---- kolom 6-10: REVERB AUDIO (reverb + delay untuk suara app lain). Nilai awal = nilai awal APK (SysReverbSettings) ----
        dict(title="REVERB AUDIO", sub="Suara app lain", acc="#ff7a1a", tog=("sysreverb.toggle", "REVERB AUDIO", "tg-sysreverb"),
             slots={
            "gain": ("sysreverb.gain", "GAIN", "010", None, "", 0.5)}),
        dict(title="REVERB", sub="Reverb audio", acc="#b58cff", tog=("sysreverb.reverb.toggle", "REVERB", "tg-sysreverb-reverb"), slots={
            "gain": ("sysreverb.wet", "WET", "010", None, "", 0.5),
            "comp": ("sysreverb.room", "ROOM", "010", None, "", 0.6),
            "high": ("sysreverb.damp", "DAMP", "010", None, "", 0.4),
            "mid": ("sysreverb.width", "WIDTH", "010", None, "", 1.0),
            "low": ("sysreverb.cess", "CESS", "010", None, "", 0.4),
            "fx": ("sysreverb.predelay", "PRE-DLY", "010", None, "", 0.2)}),
        dict(title="DELAY", sub="Delay audio", acc="#ffb02e", tog=("sysreverb.echo.toggle", "DELAY", "tg-sysreverb-echo"), slots={
            "gain": ("sysreverb.delay", "DELAY", "010", None, "", 0.45),
            "comp": ("sysreverb.feedback", "FEEDBACK", "010", None, "", 0.45),
            "level": ("sysreverb.mix", "MIX", "010", None, "", 0.4)}),
        dict(title="KIRIM", sub="Ke reverb", acc="#b58cff", tog=None, slots={
            "gain": ("sysreverb.rsend.sub", "SUB", "010", None, "", 0.0),
            "comp": ("sysreverb.rsend.low", "LOW", "010", None, "", 0.3),
            "high": ("sysreverb.rsend.mid", "MID", "010", None, "", 0.8),
            "mid": ("sysreverb.rsend.high", "HIGH", "010", None, "", 1.0)}),
        dict(title="KIRIM", sub="Ke delay", acc="#ffb02e", tog=None, slots={
            "gain": ("sysreverb.esend.sub", "SUB", "010", None, "", 0.0),
            "comp": ("sysreverb.esend.low", "LOW", "010", None, "", 0.0),
            "high": ("sysreverb.esend.mid", "MID", "010", None, "", 0.7),
            "mid": ("sysreverb.esend.high", "HIGH", "010", None, "", 0.7)}),
    ]
    ROWKIND = dict(gain="gain", comp="comp", high="eq", mid="eq", low="eq", fx="fx", pan="pan", level="level")

    def fit(label, size, maxw):          # maxw dalam satuan foto-X, hasil: size dalam satuan teks
        return min(size, LX(maxw) / (len(label) * 0.70 * ST))

    ROWS = [328 + 68 * r for r in range(6)]        # baris knob channel: rapat dari atas, jarak sama
    for i, cx in enumerate(CH):
        n = i + 1
        cfg = CHCFG[i]
        t(cx, 106, str(n), 8.0, "#a9adb0", weight="bold")
        combo(cx, 143)
        # plat tombol ON/OFF fitur (lebar mengisi kolom)
        rect(cx - 24, 186, 48, 46, "#9aa0a3" if cfg["tog"] else "#4d5052", 1.5, "#3a3d40", 0.6)
        if cfg["tog"]:
            fn, nm = cfg["tog"][:2]
            tid = cfg["tog"][2] if len(cfg["tog"]) > 2 else None
            t(cx, 197, "ON / OFF", 7.2, "#202325", weight="bold")
            t(cx, 229, nm, fit(nm, 7.2, 45), "#2c3033", weight="bold")
            toggle(fn, cx - 5.35, 201.5, 10.7, 20, "#ff8a1f", cx - 24, 186, 48, 46, tid=tid)   # tombol KOTAK di layar (SX/SY ~1.87 => 10.7x20 foto), nyala oranye
        else:
            t(cx, 220, "-", 10.0, "#4a4e51")
        # judul fitur + keterangan
        t(cx, 254, cfg["title"], fit(cfg["title"], 11.4, 50), "#f4f5f0", weight="bold")
        t(cx, 266.5, cfg["sub"], fit(cfg["sub"], 6.6, 50), TXT)
        rect(cx - 24, 272.5, 48, 2.4, "#f4f5f0", 1, op=0.9)
        for r, (row, sl) in enumerate(cfg["slots"].items()):
            fn, lab, sc, kind, rt = sl[:5]
            dv = sl[5] if len(sl) > 5 else 0.5
            kind = "gain"                          # semua knob channel satu ukuran
            cy = ROWS[r]
            rbp, top = kpx(kind)
            t(cx, cy, lab, fit(lab, 8.2, 52), TXT_LT, dy=-(top + 8))
            knob(cx, cy, kind, fn, angle=-140, hit_w=LX(48), dv=dv)
        # baris kosong -> isi knob dekoratif (tanpa fungsi, tanpa hit), otomatis digelapkan 50% oleh knob(fn=None)
        for r in range(len(cfg["slots"]), len(ROWS)):
            knob(cx, ROWS[r], "gain", None, angle=-140)

    # ============ 6. LOGO ============
    _R[0] = True
    LCX = 650                                   # sumbu tengah blok logo (selaras panel kanan)
    lx, ly = X(625.5), Y(272.5)
    pc(lx, ly, LR(9.5), "none", "#8f9498", 1.8)
    for n in range(3):
        a = math.radians(-90 + 120 * n)
        deco.append(pl(lx, ly, lx + LR(6.8) * math.cos(a), ly + LR(6.8) * math.sin(a), "#8f9498", 2.4))
    t(636.5, 278.5, "YAMAHA", 16.5, "#8f9498", "start", "bold", 0.2)
    t(LCX, 304, "MG12XUK", 18.5, "#b9bdbf", "middle", "normal", 0.4, font=SERIF)

    # ============ 7. SPX ============
    rect(592, 318, 116, 150, "#020001", 3, "#1f1f20", 1.0)
    rect(596, 322, 108, 46, "#050403", 2)   # layar SPX selebar panel, teks SPX di tengah (x=650)
    t(650, 342.5, "SPX", 14.0, "#aeb2b4", "middle", "bold", 0.3)    # tengah area kanan layar (x 652..708), sejajar tengah layar
    t(650, 351.5, "DIGITAL MULTI", 4.6, "#aeb2b4"); t(650, 357.5, "EFFECT PROCESSOR", 4.6, "#aeb2b4")
    line(651, 378, 651, 466, "#6d7073", 0.9)
    t(620, 384, "PROGRAM", 6.8, TXT_LT); knob(620, 403.5, "prog", None)
    t(619, 424, "PARAMETER", 6.8, TXT_LT); knob(620, 443.5, "param", None)
    t(602, 464, "MIN", 5.4, TXT_LT); t(640, 464, "MAX", 5.4, TXT_LT)
    cols = ["#1ea33f"] * 3 + ["#f2a31b"] * 3 + ["#7a7a76"]
    ys = [452, 441, 430, 419, 408, 398, 387]
    labs = ["-20", "-10", "-6", "0", "+6", "+10", "PEAK"]
    MW = 9                                   # lebar bar (3 bar: MIC, OUT, SYS muat di panel SPX)
    for side, mid_, xm in (("mic", "meter.mic", 657), ("out", "meter.output", 681), ("sys", "meter.sysreverb", 693.5)):
        for s in range(1, 8):
            yc, col = ys[s - 1], cols[s - 1]
            rect(xm, yc - 2.2, MW, 4.4, col, 0.8, op=0.30)
            lid = f"led-{side}-{s}"
            ctl.append(f'<g id="{lid}-on" display="none"><rect x="{f(X(xm))}" y="{f(Y(yc - 2.2))}" width="{f(LX(MW))}" height="{f(LY(4.4))}" '
                       f'rx="{f(LT(0.8))}" fill="{"#ff7a1a" if s == 7 else col}"/></g>')
            indicators.append({"id": lid, "meter": mid_, "level": round((s - 0.5) / 7, 3), "on": lid + "-on"})
    for s in range(7):
        t(673.5, ys[s] + 2.4, labs[s], 6.0, TXT_LT if s < 6 else TXT)
    # panah penanda 0 dB: kiri & kanan simetris, masing-masing di tengah celah antara tepi panel/garis dan LED (tidak menyentuh)
    deco.append(f'<path d="M{f(X(652.7))},{f(Y(415.2))} L{f(X(652.7))},{f(Y(422.8))} L{f(X(655.3))},{f(Y(419))} Z '
                f'M{f(X(706.3))},{f(Y(415.2))} L{f(X(706.3))},{f(Y(422.8))} L{f(X(704.3))},{f(Y(419))} Z" fill="#aeb2b4"/>')
    t(661.5, 464, "L", 6.4, TXT_LT); t(685.5, 464, "R", 6.4, TXT_LT); t(698, 464, "SYS", 6.0, TXT_LT)

    # ============ 8. DAFTAR EFEK ============
    rect(593, 473, 119, 64, "#1a181b", 3, BLUE_LINE, 1.0)
    rect(593, 473, 56, 127, "#1a181b", 3, BLUE_LINE, 1.0)
    EF = ["REV HALL 1", "REV HALL 2", "REV ROOM 1", "REV ROOM 2", "REV STAGE 1", "REV STAGE 2", "REV PLATE", "DRUM AMB",
          "EARLY REF", "GATE REV", "SINGLE DLY", "DELAY", "VOCAL ECHO", "KARAOKE", "PHASER", "FLANGER",
          "CHORUS 1", "CHORUS 2", "SYMPHONIC", "TREMOLO", "AUTO WAH", "RADIO VOICE", "DISTORTION", "PITCH CHANGE"]
    for n, nm in enumerate(EF):
        col2 = n >= 16
        y = 480.0 + (n - 16 if col2 else n) * 7.5
        nx, tx = (595.5, 607) if col2 is False else (652, 663.5)
        rect(nx, y - 3.5, 8.5, 6.8, "#8a8f91", 1.0)
        t(nx + 4.25, y + 1.5, str(n + 1), 5.0, "#1a1c1d", "middle", "bold")
        t(tx + 1, y + 1.8, nm, 6.4, "#c9cccd", "start", ls=0.5)

    # ============ 9. PANEL BIRU BAWAH ============
    rect(593, 601, 56, 116, BLUE, 3); rect(651, 539, 61, 87, BLUE, 3); rect(651, 628, 61, 89, BLUE, 3)
    for n in range(4):
        line(596, 699 + n * 4.4, 646, 699 + n * 4.4, "#0a3c86", 1.5, 0.95)
        line(654, 699 + n * 4.4, 709, 699 + n * 4.4, "#0a3c86", 1.5, 0.95)
    knob(621, 657, "fxrtn", None)
    ctl.append(dim(keycap(687, 543, 18, 12, False, "#8d9195")))
    knob(682, 588, "mon", None, angle=-150)
    knob(682, 662, "stereo", None, angle=-150)

    # ============ 10. SEKRUP ============
    for sx, sy in [(68, 133), (68, 308), (68, 472), (68, 669), (731, 135), (729, 311), (730, 472), (731, 669)]:
        _R[0] = sx > 400
        screw(X(sx), Y(sy), 4.2)
    _R[0] = False

    defs = ('<defs>'
            '<linearGradient id="g-chassis" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1b1b"/><stop offset="1" stop-color="#0d0d0c"/></linearGradient>'
            '<linearGradient id="g-face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2b2b"/><stop offset="0.5" stop-color="#272828"/><stop offset="1" stop-color="#2b2c2b"/></linearGradient>'
            '<linearGradient id="g-topband" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#303130"/><stop offset="0.1" stop-color="#4a4c4b"/><stop offset="0.32" stop-color="#5a5c5b"/><stop offset="0.55" stop-color="#454746"/><stop offset="0.8" stop-color="#313231"/><stop offset="1" stop-color="#2a2b2a"/></linearGradient>'
            '<linearGradient id="g-bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2b2a"/><stop offset="0.3" stop-color="#1b1b1d"/><stop offset="0.5" stop-color="#0e100b"/><stop offset="0.65" stop-color="#121212"/><stop offset="0.8" stop-color="#191917"/><stop offset="0.9" stop-color="#2d2e29"/><stop offset="1" stop-color="#4a4b45"/></linearGradient>'
            '<linearGradient id="g-wall-l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0b0a"/><stop offset="0.45" stop-color="#1c1c1b"/><stop offset="0.8" stop-color="#232323"/><stop offset="1" stop-color="#161616"/></linearGradient>'
            '<linearGradient id="g-wall-r" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#0b0b0a"/><stop offset="0.45" stop-color="#1c1c1b"/><stop offset="0.8" stop-color="#232323"/><stop offset="1" stop-color="#161616"/></linearGradient>'
            '<linearGradient id="g-silver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9d9d4"/><stop offset="0.5" stop-color="#8c8c87"/><stop offset="1" stop-color="#bdbdb8"/></linearGradient>'
            '<linearGradient id="g-bluestripe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6aaee6"/><stop offset="1" stop-color="#2f86d8"/></linearGradient>'
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
    print("OK ->", OUT, "| viewBox", W, "x", H, "| kontrol:", len(skin["controls"]), "| led:", len(skin["indicators"]))

if __name__ == "__main__":
    main()
