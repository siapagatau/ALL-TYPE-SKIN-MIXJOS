import math, json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=1280,118
OUT=os.path.join(ROOT,'skins','comp-dbx234')
os.makedirs(OUT,exist_ok=True)
def f(x): return ('%.1f'%x).rstrip('0').rstrip('.')
def ang(cx,cy,a,r):
    t=math.radians(a); return cx+r*math.sin(t), cy-r*math.cos(t)
def logInv(v,lo,hi): return math.log(v/lo)/math.log(hi/lo)
EL,ER=74,1198
CY=60
# id, function, label, caption, cx, min, mid, max, default
KNOBS=[
 ('attack','comp.attack','ATTACK','ms',150,'0.1','4.5','200',logInv(10,.1,200)),
 ('release','comp.release','RELEASE','ms',235,'1','45','2k',logInv(100,1,2000)),
 ('ratio','comp.ratio','RASIO',':1',320,'1','10','20',1/19),
 ('freq','comp.freq','FREKUENSI','Hz',405,'20','600','19k',1.0),
 ('threshold','comp.threshold','THRESHOLD','dB',490,'-80','-40','0',0.75),
 ('gain','comp.gain','GAIN','dB',575,'0','20','40',0.0),
 ('balance','comp.balance','KESEIMBANGAN','L-R',745,'L','C','R',0.5),
 ('volume','comp.volume','VOLUME','%',830,'0','50','100',1.0),
]
F='font-family="Arial,Helvetica,sans-serif"'
s=[];a=s.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" data-skin-name="DBX 234 Kompresor" data-skin-version="2.0" data-skin-author="MIXJOS" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a("""<defs>
<linearGradient id="gPanel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1e1f"/><stop offset="0.5" stop-color="#161617"/><stop offset="1" stop-color="#1a1a1b"/></linearGradient>
<linearGradient id="gEar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3a3d"/><stop offset="1" stop-color="#232325"/></linearGradient>
<linearGradient id="gSlot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d4d4d7"/></linearGradient>
<linearGradient id="gBtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2c2e"/><stop offset="1" stop-color="#0a0a0b"/></linearGradient>
<radialGradient id="gKnob" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#303033"/><stop offset="0.55" stop-color="#151516"/><stop offset="1" stop-color="#050505"/></radialGradient>
<radialGradient id="gCap" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#2a2a2c"/><stop offset="1" stop-color="#0a0a0b"/></radialGradient>
<radialGradient id="gLedOff" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#7a1a14"/><stop offset="1" stop-color="#35090a"/></radialGradient>
<radialGradient id="gLedOn" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#ffb3a8"/><stop offset="0.45" stop-color="#ff2a1f"/><stop offset="1" stop-color="#b3120c"/></radialGradient>
</defs>""")
a('<g id="layer-bg">')
a(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#050505"/>')
for x0,w0 in ((0,EL),(ER,W-ER)):
    a(f'<rect x="{x0}" y="0" width="{w0}" height="{H}" fill="url(#gEar)"/>')
    for y in range(5,H-4,4): a(f'<rect x="{x0}" y="{y}" width="{w0}" height="1.4" fill="#000" fill-opacity="0.35"/><rect x="{x0}" y="{y+1.4}" width="{w0}" height="0.8" fill="#fff" fill-opacity="0.07"/>')
a(f'<rect x="{EL}" y="0" width="{ER-EL}" height="{H}" fill="url(#gPanel)"/>')
a(f'<rect x="{EL}" y="0" width="2" height="{H}" fill="#000"/><rect x="{ER-2}" y="0" width="2" height="{H}" fill="#000"/>')
a(f'<rect x="{EL+2}" y="0" width="1" height="{H}" fill="#fff" fill-opacity="0.1"/>')
a(f'<rect x="{EL+2}" y="7" width="{ER-EL-4}" height="1.6" fill="#c9c9cc"/><rect x="{EL+2}" y="96" width="{ER-EL-4}" height="1.6" fill="#c9c9cc"/>')
a(f'<rect x="{EL+2}" y="8.6" width="{ER-EL-4}" height="1" fill="#000" fill-opacity="0.6"/><rect x="{EL+2}" y="97.6" width="{ER-EL-4}" height="1" fill="#000" fill-opacity="0.6"/>')
a(f'<rect x="0" y="0" width="{W}" height="1.5" fill="#fff" fill-opacity="0.2"/><rect x="0" y="{H-2}" width="{W}" height="2" fill="#000" fill-opacity="0.8"/>')
a('</g><g id="layer-deco">')
for ex in (EL//2,(ER+W)//2):
    for ey in (21,97):
        a(f'<rect x="{ex-19}" y="{ey-10}" width="38" height="20" rx="10" fill="url(#gSlot)" stroke="#0a0a0a" stroke-width="1.5"/>')
for sx in (EL+14,ER-14):
    for sy in (20,98):
        a(f'<circle cx="{sx}" cy="{sy}" r="3.8" fill="#2c2c2e" stroke="#000" stroke-width="1"/><line x1="{sx-2.2}" y1="{sy-.6}" x2="{sx+2.2}" y2="{sy+.6}" stroke="#000" stroke-width="1"/>')
a(f'<text x="{EL//2}" y="62" {F} font-weight="bold" font-style="italic" font-size="14.5" fill="#d8231d" text-anchor="middle" fill-opacity="0.9">MIXJOS</text>')
a(f'<text x="{EL//2}" y="70" {F} font-weight="bold" font-size="4.2" fill="#d8231d" text-anchor="middle">PROFESSIONAL PRODUCTS</text>')
cx2=(ER+W)//2
a(f'<text x="{cx2}" y="62" {F} font-weight="bold" font-style="italic" font-size="30" fill="#f4f4f4" text-anchor="middle">234</text>')
a(f'<text x="{cx2}" y="73" {F} font-style="italic" font-size="8" fill="#dcdcdc" text-anchor="middle">Dynamics</text>')
a(f'<text x="{cx2}" y="82" {F} font-style="italic" font-size="8" fill="#dcdcdc" text-anchor="middle">Compressor</text>')
for (id_,fn,lab,cap,cx,mn,md,mx,dv) in KNOBS:
    cy=CY
    for i in range(21):
        t=-135+13.5*i; major=i%5==0
        x1,y1=ang(cx,cy,t,24.5); x2,y2=ang(cx,cy,t,24.5+(6 if major else 3.5))
        a(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="#ececec" stroke-width="{1.5 if major else 0.9}"/>')
    tx,ty=ang(cx,cy,0,37)
    a(f'<text x="{f(tx)}" y="{f(ty+2.5)}" {F} font-size="7" fill="#d6d6d9" text-anchor="middle">{md}</text>')
    lx,ly=ang(cx,cy,-135,34); rx,ry=ang(cx,cy,135,34)
    a(f'<text x="{f(lx-4)}" y="{f(ly+2)}" {F} font-size="7" fill="#d6d6d9" text-anchor="middle">{mn}</text>')
    a(f'<text x="{f(rx+4)}" y="{f(ry+2)}" {F} font-size="7" fill="#d6d6d9" text-anchor="middle">{mx}</text>')
    a(f'<text x="{cx}" y="{cy+33}" {F} font-weight="bold" font-size="6" fill="#e8e8ea" text-anchor="middle">{cap}</text>')
    a(f'<text x="{cx}" y="109" {F} font-weight="bold" font-style="italic" font-size="9.5" fill="#f2f2f2" text-anchor="middle">{lab}</text>')
B1,B2=642,1118
for bx,lab,cap in ((B1,'KOMPRESOR','ON / OFF'),(B2,'SETEL ULANG','RESET')):
    a(f'<text x="{bx}" y="109" {F} font-weight="bold" font-style="italic" font-size="9.5" fill="#f2f2f2" text-anchor="middle">{lab}</text>')
    a(f'<text x="{bx}" y="{CY-17}" {F} font-size="6.5" fill="#d6d6d9" text-anchor="middle">{cap}</text>')
a(f'<text x="982" y="109" {F} font-weight="bold" font-style="italic" font-size="9.5" fill="#f2f2f2" text-anchor="middle">OUTPUT</text>')
a('</g><g id="layer-controls">')
for (id_,fn,lab,cap,cx,mn,md,mx,dv) in KNOBS:
    cy=CY
    a(f'<g id="knob-comp-{id_}" data-type="rotary" data-cx="{cx}" data-cy="{cy}" data-angle-min="-135" data-angle-max="135" data-value-default="{dv:.4f}">')
    a(f'<circle cx="{cx}" cy="{cy}" r="22" fill="url(#gKnob)" stroke="#000" stroke-width="1.5"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="19" fill="none" stroke="#3a3a3d" stroke-width="0.8"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="12.5" fill="url(#gCap)" stroke="#000" stroke-width="0.8"/>')
    a(f'<rect x="{cx-2}" y="{cy-20}" width="4" height="18" rx="2" fill="#ffffff"/>')
    a('</g>')
def ledbtn(bx,cy,lit):
    lx=bx+32
    b=f'<rect x="{bx-17}" y="{cy-10}" width="34" height="20" rx="10" fill="url(#gBtn)" stroke="#000" stroke-width="1.2"/><rect x="{bx-14}" y="{cy-8.5}" width="28" height="1.5" rx="0.7" fill="#fff" fill-opacity="0.12"/>'
    if lit: b+=f'<circle cx="{lx}" cy="{cy}" r="10" fill="#ff2a1f" fill-opacity="0.28"/>'
    b+=f'<circle cx="{lx}" cy="{cy}" r="5.5" fill="url(#{"gLedOn" if lit else "gLedOff"})" stroke="{"#5a0a06" if lit else "#1a0504"}" stroke-width="1"/>'
    return b
a('<g id="tg-comp" data-type="toggle"><g id="tg-comp-normal">'+ledbtn(B1,CY,False)+'</g><g id="tg-comp-active" display="none">'+ledbtn(B1,CY,True)+'</g></g>')
a('<g id="btn-comp-reset" data-type="button"><g id="btn-comp-reset-normal">'+ledbtn(B2,CY,False)+'</g><g id="btn-comp-reset-active" display="none">'+ledbtn(B2,CY,True)+'</g></g>')
N=8;inds=[]
for i in range(N):
    x=890+i*22; y=CY-6
    col='#3DDC84' if i<5 else ('#FFB020' if i<7 else '#FF4B4B')
    dim={'#3DDC84':'#143a22','#FFB020':'#3d2c0a','#FF4B4B':'#3d1414'}[col]
    a(f'<rect x="{x}" y="{y}" width="12" height="12" rx="6" fill="{dim}" stroke="#000" stroke-width="0.8"/>')
    a(f'<g id="led-out-{i+1}-on" display="none"><rect x="{x}" y="{y}" width="12" height="12" rx="6" fill="{col}"/></g>')
    inds.append({'id':f'led-out-{i+1}','meter':'meter.output','level':round((i+0.5)/N,3),'on':f'led-out-{i+1}-on'})
a('</g><g id="layer-hit">')
HITS={}
for (id_,fn,lab,cap,cx,mn,md,mx,dv) in KNOBS: HITS[f'hit-knob-comp-{id_}']=(cx-42,12,84,82)
HITS["hit-tg-comp"]=(622,30,80,60)
HITS['hit-btn-comp-reset']=(B2-30,30,92,60)
for k,(x,y,w,h) in HITS.items():
    a(f'<rect id="{k}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>')
a('</g></svg>')
svg='\n'.join(s)+'\n'
open(f'{OUT}/skin.svg','w',encoding='utf-8').write(svg)
controls=[];mapping={}
for (id_,fn,lab,cap,cx,mn,md,mx,dv) in KNOBS:
    cid=f'knob-comp-{id_}'
    controls.append({'id':cid,'type':'rotary','hit':'hit-'+cid,'angleMin':-135,'angleMax':135,'defaultValue':round(dv,4)})
    mapping[cid]={'function':fn}
controls.append({'id':'tg-comp','type':'toggle','hit':'hit-tg-comp','states':{'normal':'tg-comp-normal','active':'tg-comp-active'},'trigger':'tap'})
mapping['tg-comp']={'function':'comp.toggle'}
controls.append({'id':'btn-comp-reset','type':'button','hit':'hit-btn-comp-reset','states':{'normal':'btn-comp-reset-normal','active':'btn-comp-reset-active'},'trigger':'tap'})
mapping['btn-comp-reset']={'function':'comp.reset'}
js={'schemaVersion':1,'name':'DBX 234 Kompresor','version':'2.0','author':'MIXJOS','svg':'skin.svg','viewBox':f'0 0 {W} {H}',
 'layout':{'padZone':f'0 0 {W} {H}'},'controls':controls,'mapping':mapping,'indicators':inds,
 'unsupportedInReference':[
  {'id':'layer-deco','kind':'decorative','label':'Telinga rack, sekrup, judul, skala','reason':'Dekorasi'},
  {'id':'ref-lowcut','kind':'control','label':'Tombol LOW CUT / MONO-STEREO / knob input dan crossover pada gambar referensi','reason':'Tidak ada padanan di kompresor APK'}]}
json.dump(js,open(f'{OUT}/skin.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
pv=svg.rstrip()[:-6]
pv+='<g id="preview-hits" font-family="monospace" font-size="7">'
for k,(x,y,w,h) in HITS.items():
    pv+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#00e5ff" stroke-width="1" stroke-dasharray="4 3"/>'
pv+='</g></svg>\n'
open(f'{OUT}/preview.svg','w',encoding='utf-8').write(pv)
print('ok',len(svg))
