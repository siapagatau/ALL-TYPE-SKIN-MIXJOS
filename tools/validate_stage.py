#!/usr/bin/env python3
"""Validasi skin PANGGUNG: python3 tools/validate_stage.py [id]  (default stage-festival)"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "skins", sys.argv[1] if len(sys.argv) > 1 else "stage-festival")
err = []
st = json.load(open(os.path.join(d, "stage.json"), encoding="utf-8"))
for k in ("name", "version", "author", "aspect", "scenes"):
    if k not in st: err.append(f"stage.json tanpa '{k}'")
for name, sc in st.get("scenes", {}).items():
    f = sc.get("image", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", f) or not os.path.isfile(os.path.join(d, f)): err.append(f"scene {name}: gambar '{f}' tidak ada/tidak valid")
    elif os.path.getsize(os.path.join(d, f)) > 4 * 1024 * 1024: err.append(f"{f} > 4 MB (batas unduh app)")
    if not sc.get("slots"): err.append(f"scene {name}: tanpa slot")
    for s in sc.get("slots", []):
        if not (0 <= s["x"] and 0 <= s["y"] and s["x"] + s["w"] <= 1 and s["y"] + s["h"] <= 1 and s["w"] > 0 and s["h"] > 0): err.append(f"scene {name} slot {s['id']}: di luar gambar")
for it in st.get("schedule", []):
    if it["scene"] not in st["scenes"]: err.append(f"jadwal merujuk scene tak dikenal: {it['scene']}")
ids = set()
for l in st.get("defaultLights", []):
    if l["id"] in ids: err.append(f"id lampu ganda: {l['id']}")
    ids.add(l["id"])
    if l["type"] not in ("beam", "lamp"): err.append(f"{l['id']}: type salah")
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", l["color"]): err.append(f"{l['id']}: warna salah")
print(f"{os.path.basename(d)}: {len(st['scenes'])} scene, {len(st.get('defaultLights', []))} lampu")
print("OK (0 ERROR)" if not err else "\n".join("ERROR: " + e for e in err))
sys.exit(1 if err else 0)
