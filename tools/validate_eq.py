import json, re, sys, xml.etree.ElementTree as ET
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d=os.path.join(ROOT,"skins",sys.argv[1] if len(sys.argv)>1 else "eq31-dbx1231")
sk=json.load(open(f"{d}/skin.json")); root=ET.parse(f"{d}/skin.svg").getroot()
ns="{http://www.w3.org/2000/svg}"
ids={}
for e in root.iter():
    i=e.get("id")
    if i:
        assert i not in ids,"dup "+i; ids[i]=e
    assert e.tag.replace(ns,"") not in ("script","foreignObject","image","use","filter","audio","video","iframe"),e.tag
    for k,v in e.attrib.items():
        assert not k.startswith("on") and "href" not in k and "http" not in v or k.startswith("{") or k=="xmlns",(k,v)
vb=[float(x) for x in root.get("viewBox").split()]
funcs={f"eq31.{s}.{n:02d}" for s in "lr" for n in range(1,32)}|{"eq31.l.gain","eq31.r.gain"}
allowed={"toggle":{"eq31.toggle","eq31.mode"},"button":{"eq31.reset"},"rotary":funcs,"slider":funcs}
used=set()
for c in sk["controls"]:
    assert c["id"] in ids and c["hit"] in ids
    h=ids[c["hit"]]; x,y,w,hh=[float(h.get(k)) for k in "x y width height".split()]
    assert x>=0 and y>=0 and x+w<=vb[2] and y+hh<=vb[3],c["id"]
    f=sk["mapping"][c["id"]]["function"]; assert f in allowed[c["type"]],(c["id"],f)
    assert f not in used,f; used.add(f)
    g=ids[c["id"]]
    if c["type"]=="slider":
        first=[e for e in g.iter() if e.tag==ns+"rect"][0]; assert first.get("fill")=="none"
        assert all(g.get(k) for k in("data-x1","data-y1","data-x2","data-y2"))
    if c["type"]=="rotary": assert g.get("data-cx")
    if c["type"]=="toggle": assert all(s in ids for s in c["states"].values())
# overlaps
hs=[(c["id"],[float(ids[c["hit"]].get(k)) for k in "x y width height".split()]) for c in sk["controls"]]
for i in range(len(hs)):
    for j in range(i+1,len(hs)):
        a=hs[i][1];b=hs[j][1]
        assert not(a[0]<b[0]+b[2] and b[0]<a[0]+a[2] and a[1]<b[1]+b[3] and b[1]<a[1]+a[3]),(hs[i][0],hs[j][0])
print("OK",len(sk["controls"]),"controls, funcs",len(used))
