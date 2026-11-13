#!/usr/bin/env python3
"""Bangun index.json repo ALL-TYPE-SKIN-MIXJOS (sha256 + size + type).
Jalankan SETELAH semua file skin final:  python3 tools/index.py
Tipe skin dibaca otomatis:
  folder berisi stage.json -> "stage" (PANGGUNG; semua berkas folder masuk index)
  function comp.*  -> "comp"   (tab KOMPRESOR)
  function eq31.*  -> "eq"     (tab EQUALIZER)
  selain itu -> "mixer" (tab MIXER)
"""
import datetime, hashlib, json, os, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SD = os.path.join(ROOT, "skins")


def skin_type(sk):
    fns = [m.get("function", "") for m in sk.get("mapping", {}).values()]
    if any(f.startswith("comp.") for f in fns):
        return "comp"
    if any(f.startswith("eq31.") for f in fns):
        return "eq"
    return "mixer"


skins = []
for sid in sorted(os.listdir(SD)):
    p = os.path.join(SD, sid)
    if os.path.isfile(os.path.join(p, "stage.json")):
        st = json.load(open(os.path.join(p, "stage.json"), encoding="utf-8"))
        files = {}
        for fn in sorted(os.listdir(p)):
            if fn.startswith(".") or not os.path.isfile(os.path.join(p, fn)):
                continue
            b = open(os.path.join(p, fn), "rb").read()
            files[fn] = {"sha256": hashlib.sha256(b).hexdigest(), "size": len(b)}
        skins.append({"id": sid, "type": "stage", "name": st["name"], "version": st["version"], "author": st["author"],
                      "padMin": 0, "padMax": 0, "path": f"skins/{sid}/", "files": files})
        continue
    if not os.path.isfile(os.path.join(p, "skin.json")):
        continue
    sk = json.load(open(os.path.join(p, "skin.json"), encoding="utf-8"))
    files = {}
    for fn in ("skin.json", "skin.svg", "preview.svg"):
        b = open(os.path.join(p, fn), "rb").read()
        files[fn] = {"sha256": hashlib.sha256(b).hexdigest(), "size": len(b)}
    skins.append({"id": sid, "type": skin_type(sk), "name": sk["name"], "version": sk["version"],
                  "author": sk["author"], "padMin": 0, "padMax": 0, "path": f"skins/{sid}/", "files": files})

order = {"mixer": 0, "comp": 1, "eq": 2, "stage": 3}
skins.sort(key=lambda s: (order[s["type"]], s["id"]))
json.dump({"schemaVersion": 2, "repo": "ALL-TYPE-SKIN-MIXJOS", "updated": datetime.date.today().isoformat(), "skins": skins},
          open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("index.json:", len(skins), "skin ->", ", ".join(f"{s['id']}[{s['type']}]" for s in skins))
