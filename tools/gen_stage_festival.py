#!/usr/bin/env python3
"""Bangun skin PANGGUNG 'stage-festival' dari tiga gambar green screen.
Pakai:  python3 tools/gen_stage_festival.py <folder berisi CERAH.png SUNSET.png MALAM.png>
Hasil:  skins/stage-festival/{stage.json, scene-cerah.webp, scene-sunset.webp, scene-malam.webp}
Layar hijau diubah jadi TRANSPARAN (chroma key + despill) sehingga media pengguna (foto/GIF/video) yang digambar di
belakang gambar panggung muncul tepat di dalam layar, dan rangka/tiang tetap di depan media."""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools", "src")
OUT = os.path.join(ROOT, "skins", "stage-festival")
os.makedirs(OUT, exist_ok=True)
SCENES = [("cerah", "CERAH.png", 0.30), ("sunset", "SUNSET.png", 0.65), ("malam", "MALAM.png", 1.00)]
PAD = 5  # px di sekeliling kotak hijau yang ikut diproses (rumput di bagian bawah gambar TIDAK disentuh)


def find_boxes(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (g > 180) & (r < 110) & (b < 110) & (g - r > 100) & (g - b > 100)
    lab, k = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1, k + 1))
    boxes = []
    for sl, sz in zip(ndi.find_objects(lab), sizes):
        if sz > 2000:
            boxes.append((sl[1].start, sl[0].start, sl[1].stop - sl[1].start, sl[0].stop - sl[0].start))
    return boxes


def slot_ids(boxes, W):
    tall = [b for b in boxes if b[1] < 330]
    mid = sorted([b for b in boxes if b[1] >= 330], key=lambda b: b[0])
    named = {}
    for b in tall:
        named["kiri" if b[0] < W / 2 else "kanan"] = b
    named["tengah-kiri"], named["tengah"], named["tengah-kanan"] = mid
    return [dict(id=k, x=round(v[0] / W, 4), y=round(v[1] / H, 4), w=round(v[2] / W, 4), h=round(v[3] / H, 4))
            for k, v in named.items()]


def key(a, boxes):
    h, w, _ = a.shape
    alpha = np.ones((h, w), dtype=float)
    out = a.astype(float).copy()
    for (x, y, bw, bh) in boxes:
        x0, y0, x1, y1 = max(0, x - PAD), max(0, y - PAD), min(w, x + bw + PAD), min(h, y + bh + PAD)
        reg = out[y0:y1, x0:x1]
        gr = reg[..., 1] - np.maximum(reg[..., 0], reg[..., 2])
        al = 1.0 - np.clip((gr - 45) / 80.0, 0, 1)
        alpha[y0:y1, x0:x1] = np.minimum(alpha[y0:y1, x0:x1], al)
        edge = al > 0.01  # despill: hilangkan semburat hijau di tepi
        reg[..., 1] = np.where(edge, np.minimum(reg[..., 1], np.maximum(reg[..., 0], reg[..., 2])), reg[..., 1])
    return out, alpha


scene_json, W, H = {}, None, None
for name, fn, gain in SCENES:
    a = np.asarray(Image.open(os.path.join(SRC, fn)).convert("RGB"))
    H, W = a.shape[:2]
    boxes = find_boxes(a)
    assert len(boxes) == 5, f"{fn}: harus 5 layar hijau, ketemu {len(boxes)}"
    rgb, alpha = key(a, boxes)
    rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, f"scene-{name}.webp"), "WEBP", quality=86, alpha_quality=100, method=6)
    scene_json[name] = {"image": f"scene-{name}.webp", "lightGain": gain, "slots": slot_ids(boxes, W)}

BEAM = "beam"; LAMP = "lamp"
_n = [0]
def L(i, t, x, y, col, **kw):
    d = {"id": i, "type": t, "x": x, "y": y, "color": col, "on": True, "phase": round((_n[0] * 0.137) % 1, 3)}
    _n[0] += 1
    d.update(kw); return d

lights = [
    # lampu sorot di tiang kiri-kanan
    L("sorot-1", BEAM, .134, .225, "#00E5FF", angle=18, angleTo=-10, motion="ayun", period=6, length=.45, spread=13, intensity=.9, blink="tetap", bpm=0),
    L("sorot-2", BEAM, .244, .225, "#FF2DAA", angle=-12, angleTo=14, motion="ayun", period=5, length=.45, spread=13, intensity=.9, blink="tetap", bpm=0),
    L("sorot-3", BEAM, .755, .228, "#FF2DAA", angle=12, angleTo=-14, motion="ayun", period=5, length=.45, spread=13, intensity=.9, blink="tetap", bpm=0),
    L("sorot-4", BEAM, .865, .228, "#00E5FF", angle=-18, angleTo=10, motion="ayun", period=6, length=.45, spread=13, intensity=.9, blink="tetap", bpm=0),
    # lampu sorot di rangka tengah
    L("sorot-5", BEAM, .380, .415, "#FFD60A", angle=-25, angleTo=25, motion="sapu", period=8, length=.42, spread=11, intensity=.85, blink="tetap", bpm=0),
    L("sorot-6", BEAM, .440, .415, "#FFFFFF", angle=15, angleTo=-30, motion="ayun", period=7, length=.42, spread=11, intensity=.85, blink="tetap", bpm=0),
    L("sorot-7", BEAM, .500, .415, "#7C4DFF", angle=0, angleTo=0, motion="diam", period=6, length=.42, spread=12, intensity=.8, blink="denyut", bpm=60),
    L("sorot-8", BEAM, .560, .415, "#FFFFFF", angle=-15, angleTo=30, motion="ayun", period=7, length=.42, spread=11, intensity=.85, blink="tetap", bpm=0),
    L("sorot-9", BEAM, .620, .415, "#FFD60A", angle=25, angleTo=-25, motion="sapu", period=8, length=.42, spread=11, intensity=.85, blink="tetap", bpm=0),
    # lampu biasa (glow) di rangka atas
    L("lampu-1", LAMP, .310, .335, "#FF9F0A", size=.030, intensity=.9, blink="kedip", bpm=120),
    L("lampu-2", LAMP, .690, .335, "#FF9F0A", size=.030, intensity=.9, blink="kedip", bpm=120),
]
stage = {"schemaVersion": 1, "name": "Panggung Festival", "version": "1.0", "author": "MIXJOS", "aspect": [W, H],
         "scenes": scene_json,
         # jadwal otomatis menurut jam lokal HP: dari jam "from" sampai jam berikutnya
         "schedule": [{"from": "00:00", "scene": "malam"}, {"from": "06:00", "scene": "cerah"},
                      {"from": "17:00", "scene": "sunset"}, {"from": "18:30", "scene": "malam"}],
         "defaultLights": lights}
json.dump(stage, open(os.path.join(OUT, "stage.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(os.path.join(OUT, f)))
print(json.dumps({k: v["slots"] for k, v in scene_json.items()}["malam"]))
