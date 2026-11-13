#!/usr/bin/env python3
"""Validator skin MIXJOS Mixer. Pakai: python3 tools/validate.py skins/skin-NN"""
import json, os, re, sys
import xml.etree.ElementTree as ET

TOG = {"mic.toggle", "reverb.toggle", "echo.toggle", "eqmic.toggle", "eqaudio.toggle",
       "sysreverb.toggle", "sysreverb.reverb.toggle", "sysreverb.echo.toggle"}
ROT = {"mic.volume", "mic.gate", "reverb.wet", "reverb.dry", "reverb.width", "reverb.damp", "reverb.room", "reverb.cess",
       "echo.delay", "echo.feedback", "echo.mix", "eqmic.low", "eqmic.mid", "eqmic.high",
       "eqaudio.gain", "eqaudio.sub", "eqaudio.low", "eqaudio.mid", "eqaudio.high",
       "sysreverb.wet", "sysreverb.room", "sysreverb.damp", "sysreverb.width", "sysreverb.cess", "sysreverb.predelay",
       "sysreverb.delay", "sysreverb.feedback", "sysreverb.mix", "sysreverb.gain",
       "sysreverb.rsend.sub", "sysreverb.rsend.low", "sysreverb.rsend.mid", "sysreverb.rsend.high",
       "sysreverb.esend.sub", "sysreverb.esend.low", "sysreverb.esend.mid", "sysreverb.esend.high"}
BTN = {"floating.toggle", "theme.open", "skin.pick"}
METER = {"meter.mic", "meter.output", "meter.sysreverb"}
OKFN = {"toggle": TOG, "rotary": ROT, "slider": ROT, "button": BTN, "display": {"display.status"}}
BAD_TAGS = {"script", "foreignobject", "image", "use", "audio", "video", "iframe"}
WARN_TAGS = {"filter", "mask"}

def tag(e):
    return e.tag.split("}")[-1].lower()

def main(d):
    errs, warns = [], []
    E, Wn = errs.append, warns.append
    try:
        root = ET.parse(os.path.join(d, "skin.svg")).getroot()
        sk = json.load(open(os.path.join(d, "skin.json"), encoding="utf-8"))
    except Exception as ex:
        print("ERROR: gagal baca file:", ex); return 1
    for a in ("data-skin-name", "data-skin-version", "data-skin-author", "viewBox"):
        if a not in root.attrib: E(f"root: atribut {a} hilang")
    vb = [float(x) for x in root.get("viewBox", "0 0 1 1").split()]
    ids, els = {}, {}
    for e in root.iter():
        tg = tag(e)
        if tg in BAD_TAGS: E(f"elemen terlarang <{tg}>")
        if tg in WARN_TAGS: Wn(f"<{tg}> tidak dirender")
        for k, v in e.attrib.items():
            kn = k.split("}")[-1].lower()
            if kn.startswith("on"): E(f"atribut on*: {k}")
            if kn == "href": E("atribut href dilarang")
            if re.search(r"https?://", v): E(f"URL dilarang di atribut {k}")
        if e.text and re.search(r"https?://", e.text): E("URL dilarang di teks")
        i = e.get("id")
        if i:
            if i in ids: E(f"id duplikat: {i}")
            if not re.fullmatch(r"[a-z][a-z0-9-]*", i): E(f"id tidak valid: {i}")
            ids[i] = e
    def box(i):
        r = ids.get(i)
        if r is None or tag(r) != "rect": return None
        x, y, w, h = (float(r.get(k, 0)) for k in ("x", "y", "width", "height"))
        return x, y, x + w, y + h
    hb = {}
    ctrls = {c["id"]: c for c in sk.get("controls", [])}
    if not ctrls: E("minimal 1 kontrol")
    for cid, c in ctrls.items():
        t = c.get("type")
        m = sk.get("mapping", {}).get(cid)
        if cid not in sk.get("mapping", {}): E(f"{cid}: tidak ada di mapping"); continue
        if m.get("function") not in OKFN.get(t, set()): E(f"{cid}: function '{m.get('function')}' tidak cocok untuk type {t}")
        if t == "display":
            if cid not in ids: E(f"{cid}: grup display tidak ada")
            continue
        b = box(c.get("hit"))
        if not b: E(f"{cid}: hit rect tidak ada"); continue
        hb[cid] = b
        if b[0] < vb[0] or b[1] < vb[1] or b[2] > vb[0] + vb[2] or b[3] > vb[1] + vb[3]: E(f"{cid}: hit di luar viewBox")
        if t in ("toggle", "button"):
            for s in c.get("states", {}).values():
                if s not in ids: E(f"{cid}: state {s} tidak ada")
        if t == "rotary":
            g = ids.get(cid)
            if g is None: E(f"{cid}: grup knob tidak ada"); continue
            cx, cy = float(g.get("data-cx")), float(g.get("data-cy"))
            circ = next((x for x in g.iter() if tag(x) == "circle"), None)
            r = float(circ.get("r")) if circ is not None else 0
            if not (b[0] <= cx - r and cx + r <= b[2] and b[1] <= cy - r and cy + r <= b[3]): E(f"{cid}: knob tidak muat di hit")
        if t == "slider":
            g = ids.get(cid)
            if g is None or not all(g.get(k) for k in ("data-x1", "data-y1", "data-x2", "data-y2")): E(f"{cid}: slider data-x1..y2 kurang")
    names = list(hb)
    for a in range(len(names)):
        for b_ in range(a + 1, len(names)):
            A, B = hb[names[a]], hb[names[b_]]
            ox, oy = min(A[2], B[2]) - max(A[0], B[0]), min(A[3], B[3]) - max(A[1], B[1])
            if ox > 0 and oy > 0:
                sm = min((A[2]-A[0])*(A[3]-A[1]), (B[2]-B[0])*(B[3]-B[1]))
                (E if ox*oy > 0.1*sm else Wn)(f"hit tumpang tindih: {names[a]} x {names[b_]}")
    for ind in sk.get("indicators", []):
        if ind.get("meter") not in METER: E(f"{ind.get('id')}: meter tidak resmi")
        if ind.get("on") not in ids: E(f"{ind.get('id')}: grup {ind.get('on')} tidak ada")
    n = sum(1 for _ in root.iter())
    print(f"{os.path.basename(d.rstrip('/'))}: {len(ctrls)} kontrol, {len(sk.get('indicators', []))} led, {n} elemen")
    for w in warns: print("WARN :", w)
    for e in errs: print("ERROR:", e)
    print("OK (0 ERROR)" if not errs else f"GAGAL ({len(errs)} ERROR)")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]) if len(sys.argv) > 1 else 2)
