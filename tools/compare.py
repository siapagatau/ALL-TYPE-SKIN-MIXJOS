#!/usr/bin/env python3
"""Bandingkan skin dengan foto referensi (overlay 50% + berdampingan).
Pakai: python3 tools/compare.py foto.jpg skins/skin-01/skin.svg
Butuh: pip install playwright pillow  (+ playwright install chromium)
Foto harus 800x800 dengan bodi di x 40..759, y 70..729 (ubah BOX bila beda)."""
import sys
from PIL import Image
from playwright.sync_api import sync_playwright
BOX = (40, 70, 760, 730)
ref_path, svg_path = sys.argv[1], sys.argv[2]
import re
vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(svg_path, encoding="utf-8").read())
w, h = int(vb.group(1)), int(vb.group(2))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h})
    import os; pg.goto("file://" + os.path.abspath(svg_path)); pg.screenshot(path="_skin.png"); b.close()
ref = Image.open(ref_path).convert("RGB").crop(BOX).resize((w, h), Image.LANCZOS)
new = Image.open("_skin.png").convert("RGB")
Image.blend(ref, new, 0.5).save("_overlay.png")
sbs = Image.new("RGB", (w * 2 + 10, h), "white"); sbs.paste(ref, (0, 0)); sbs.paste(new, (w + 10, 0)); sbs.save("_sbs.png")
print("tersimpan: _overlay.png, _sbs.png")
