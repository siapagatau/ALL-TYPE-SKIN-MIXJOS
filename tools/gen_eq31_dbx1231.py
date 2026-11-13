import json, math, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W,H=2048,591
SID="eq31-dbx1231"; D=os.path.join(ROOT,"skins",SID)
os.makedirs(D,exist_ok=True)
FREQ=["20","25","31.5","40","50","63","80","100","125","160","200","250","315","400","500","630","800","1k","1.25k","1.6k","2k","2.5k","3.15k","4k","5k","6.3k","8k","10k","12.5k","16k","20k"]
CX0,CX1=490,1830; STEP=(CX1-CX0)/30
DY=253
svg=[];hits=[];controls=[];mapping=[];inds=[]
mapping={}
A=svg.append
TXT='font-family="sans-serif" font-weight="bold"'
def text(x,y,s,size=10.5,fill="#e8e8ea",anchor="middle",extra=""):
    A(f'<text x="{x}" y="{y}" {TXT} font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')
A(f'<svg xmlns="http://www.w3.org/2000/svg" data-skin-name="dbx 1231 EQ" data-skin-version="1.1" data-skin-author="MIXJOS" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
A('<defs>'
 '<linearGradient id="g-panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4b4e4b"/><stop offset="1" stop-color="#3f423f"/></linearGradient>'
 '<linearGradient id="g-cap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e3e6"/><stop offset="0.5" stop-color="#b4b6ba"/><stop offset="1" stop-color="#7d7f84"/></linearGradient>'
 '<radialGradient id="g-knob" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#3a3a3a"/><stop offset="1" stop-color="#0c0c0c"/></radialGradient>'
 '<radialGradient id="g-btn" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#4a4a4a"/><stop offset="1" stop-color="#1c1c1c"/></radialGradient>'
 '</defs>')
A('<g id="layer-bg">')
A(f'<rect width="{W}" height="{H}" fill="#101012"/>')
A('<rect x="15" y="20" width="2015" height="555" rx="4" fill="url(#g-panel)"/>')
# grooves left/right
p=""
for y in range(26,572,11):
    p+=f'M18 {y}h172M1890 {y}h138'
A(f'<path d="{p}" stroke="#2d2f2d" stroke-width="3" fill="none"/>')
for r in (0,1):
    A(f'<rect x="192" y="{52+r*260}" width="1691" height="{238 if r==0 else 236}" rx="3" fill="#26282c"/>')
for sx,sy in ((132,62),(1020,38),(1912,60),(130,533),(1020,557),(1912,530)):
    A(f'<circle cx="{sx}" cy="{sy}" r="9" fill="#1b1b1c" stroke="#0b0b0b" stroke-width="2"/><rect x="{sx-5}" y="{sy-1}" width="10" height="2" fill="#444"/>')
for sx,sy in ((50,180),(1993,180),(50,418),(1993,418)):
    A(f'<rect x="{sx-24}" y="{sy-13}" width="48" height="26" rx="13" fill="#f4f4f4"/>')
A('<text x="44" y="312" font-family="sans-serif" font-weight="bold" font-size="64" fill="#c8372d">dbx</text>')
text(26,332,"PROFESSIONAL PRODUCTS",10.5,"#f0f0f0","start",'font-style="italic"')
text(2018,300,"1231",42,"#ececec","end",'font-style="italic"')
text(2018,320,"Graphic Equalizer",14,"#ececec","end",'font-style="italic"')
# freq labels
for i in range(31):
    text(round(CX0+STEP*i,1),302,FREQ[i],10.5,"#e4e5e7")
A('</g><g id="layer-deco">')
def led_dim(x,y,c): A(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{c}" stroke="#0e0e0e" stroke-width="1.2"/>')
LEDS=[(269,"#9bd447","#34501c","-10",0.25),(289,"#9bd447","#34501c","0",0.5),(309,"#f1f129","#5e5e1a","+10",0.75),(331,"#d33733","#4f1c1a","+18",0.92)]
for r in (0,1):
    dy=r*DY
    tt,bb=77+dy,265+dy
    # slots + ticks
    for i in range(31):
        cx=round(CX0+STEP*i,1)
        A(f'<rect x="{cx-5}" y="{62+dy}" width="10" height="222" rx="4" fill="#141415"/><rect x="{cx-1}" y="{66+dy}" width="2" height="214" fill="#2e2f31"/>')
    long=""; short=""
    for i in range(30):
        gx=CX0+STEP*(i+0.5)
        for k in range(-5,6):
            y=round(171+dy+k*18.8,1)
            if k in(0,5,-5): long+=f'M{gx-9:.1f} {y}h18'
            else: short+=f'M{gx-6:.1f} {y}h12'
    A(f'<path d="{short}" stroke="#a9aaad" stroke-width="2" fill="none"/><path d="{long}" stroke="#f2f2f4" stroke-width="2.4" fill="none"/>')
    for lab,yy in (("+12",tt+3),("0",171+dy+4),("-12",bb+3)):
        text(468,yy,lab,10,"#e8e8ea","end"); text(1852,yy,lab,10,"#e8e8ea","start")
    # left control cluster
    for lx,_,c,lab,_l in LEDS:
        led_dim(lx,90+dy,c); text(lx,76+dy,lab,9.5)
    text(300,108+dy,"OUTPUT",9.5); text(300,119+dy,"LEVEL (dBu)",9.5)
    text(222,128+dy,"CLIP",9.5); led_dim(222,142+dy,"#4f1c1a")
    led_dim(222,175+dy,"#4f1c1a"); led_dim(378,175+dy,"#c23a36")
    # knob scale
    kx,ky=300,192+dy
    tk=""
    for n in range(21):
        a=math.radians(-135+270*n/20); r0=37; r1=45 if n%5==0 else 41
        tk+=f'M{kx+r0*math.sin(a):.1f} {ky-r0*math.cos(a):.1f}L{kx+r1*math.sin(a):.1f} {ky-r1*math.cos(a):.1f}'
    A(f'<path d="{tk}" stroke="#e8e8ea" stroke-width="2" fill="none"/>')
    text(kx,ky-52,"0",9.5); text(kx-34,ky+50,"-12",9.5); text(kx+34,ky+50,"+12",9.5); text(kx,ky+46,"dB",9)
    text(kx,258+dy,"INPUT",10.5); text(kx,269+dy,"GAIN",10.5)
    # decor buttons LOW CUT / RANGE
    for bx in (378,):
        A(f'<circle cx="{bx}" cy="{214+dy}" r="13" fill="url(#g-btn)" stroke="#0a0a0a" stroke-width="1.5"/>')
    text(378,247+dy,"LOW",10.5); text(378,259+dy,"CUT",10.5); 
# main button (EQ ON) normal + reset normal
A(f'<circle cx="222" cy="214" r="13" fill="url(#g-btn)" stroke="#0a0a0a" stroke-width="1.5"/>')
text(222,247,"EQ",10.5); text(222,259,"ON/OFF",10.5)
A(f'<circle cx="222" cy="{214+DY}" r="13" fill="url(#g-btn)" stroke="#0a0a0a" stroke-width="1.5"/>')
text(222,247+DY,"RESET",10.5); text(222,259+DY,"FLAT",10.5)
A('</g><g id="layer-controls">')
# toggle
A('<g id="tg-eq31" data-type="toggle"><g id="tg-eq31-normal"><circle cx="222" cy="214" r="14" fill="none" stroke="#0a0a0a" stroke-width="1"/></g>'
  '<g id="tg-eq31-active" display="none"><circle cx="222" cy="214" r="16" fill="none" stroke="#3ddc84" stroke-width="3"/><circle cx="222" cy="175" r="7" fill="#3ddc84" stroke="#0e0e0e" stroke-width="1.2"/></g></g>')
hits.append(("hit-tg-eq31",205,197,34,34))
controls.append({"id":"tg-eq31","type":"toggle","hit":"hit-tg-eq31","states":{"normal":"tg-eq31-normal","active":"tg-eq31-active"},"trigger":"tap"}); mapping["tg-eq31"]={"function":"eq31.toggle"}
A(f'<g id="btn-eq-reset" data-type="button"><g id="btn-eq-reset-normal"><circle cx="222" cy="{214+DY}" r="14" fill="none" stroke="#0a0a0a" stroke-width="1"/></g>'
  f'<g id="btn-eq-reset-active" display="none"><circle cx="222" cy="{214+DY}" r="16" fill="none" stroke="#ffffff" stroke-width="3"/></g></g>')
hits.append(("hit-btn-eq-reset",205,197+DY,34,34))
controls.append({"id":"btn-eq-reset","type":"button","hit":"hit-btn-eq-reset","states":{"normal":"btn-eq-reset-normal","active":"btn-eq-reset-active"},"trigger":"tap"}); mapping["btn-eq-reset"]={"function":"eq31.reset"}
for r,key in enumerate("lr"):
    dy=r*DY; tt,bb=77+dy,265+dy
    kx,ky=300,192+dy; kid=f"knob-eq31-{key}-gain"
    A(f'<g id="{kid}" data-type="rotary" data-cx="{kx}" data-cy="{ky}" data-angle-min="-135" data-angle-max="135" data-value-default="0.5">'
      f'<circle cx="{kx}" cy="{ky}" r="30" fill="url(#g-knob)" stroke="#000" stroke-width="1.5"/>'
      f'<circle cx="{kx}" cy="{ky}" r="23" fill="none" stroke="#262626" stroke-width="1.5"/>'
      f'<line x1="{kx}" y1="{ky-7}" x2="{kx}" y2="{ky-27}" stroke="#f4f4f4" stroke-width="5" stroke-linecap="round"/></g>')
    hits.append((f"hit-{kid}",kx-35,ky-36,70,72))
    controls.append({"id":kid,"type":"rotary","hit":f"hit-{kid}","angleMin":-135,"angleMax":135,"defaultValue":0.5}); mapping[kid]={"function":f"eq31.{key}.gain"}
    for i in range(31):
        cx=round(CX0+STEP*i,1); n=i+1; sid=f"sl-eq31-{key}-{n:02d}"
        A(f'<g id="{sid}" data-type="slider" data-x1="{cx}" data-y1="{bb}" data-x2="{cx}" data-y2="{tt}" data-value-default="0.5">'
          f'<rect x="{cx-11}" y="{bb-8}" width="22" height="16" fill="none"/>'
          f'<rect x="{cx-11}" y="{bb-8}" width="22" height="16" rx="2" fill="url(#g-cap)" stroke="#2a2a2c" stroke-width="1"/>'
          f'<rect x="{cx-11}" y="{bb-1}" width="22" height="2" fill="#1d1d1f"/><rect x="{cx-9}" y="{bb-0.6}" width="18" height="1.2" fill="#ffffff"/></g>')
        hits.append((f"hit-{sid}",round(cx-20,1),58+dy,40,230))
        controls.append({"id":sid,"type":"slider","hit":f"hit-{sid}","defaultValue":0.5}); mapping[sid]={"function":f"eq31.{key}.{n:02d}"}
# lit LEDs (meter.output)
for r,key in enumerate("lr"):
    dy=r*DY
    for j,(lx,lit,_d,_l,lv) in enumerate(LEDS):
        iid=f"led-{key}-{j+1}"
        A(f'<g id="{iid}-on" display="none"><rect x="{lx-8}" y="{82+dy}" width="16" height="16" rx="8" fill="{lit}"/><circle cx="{lx}" cy="{90+dy}" r="6.5" fill="{lit}" stroke="#ffffff" stroke-opacity="0.6" stroke-width="1"/></g>')
        inds.append({"id":iid,"meter":"meter.output","level":lv,"on":f"{iid}-on"})
    iid=f"led-{key}-clip"
    A(f'<g id="{iid}-on" display="none"><rect x="{214}" y="{134+dy}" width="16" height="16" rx="8" fill="#ff3b30"/><circle cx="222" cy="{142+dy}" r="6.5" fill="#ff3b30" stroke="#ffffff" stroke-opacity="0.6" stroke-width="1"/></g>')
    inds.append({"id":iid,"meter":"meter.output","level":0.97,"on":f"{iid}-on"})
A('</g><g id="layer-hit">')
for hid,x,y,w,h in hits:
    A(f'<rect id="{hid}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>')
A('</g></svg>')
open(f"{D}/skin.svg","w").write("\n".join(svg))
skin={"schemaVersion":1,"name":"dbx 1231 EQ","version":"1.1","author":"MIXJOS","svg":"skin.svg","viewBox":f"0 0 {W} {H}","layout":{"padZone":f"0 0 {W} {H}"},
 "controls":controls,"mapping":mapping,"indicators":inds,
 "unsupportedInReference":[{"id":"deco-lowcut-l","kind":"decorative","label":"LOW CUT (atas/bawah)","reason":"Tidak ada function di APK"}]}
open(f"{D}/skin.json","w").write(json.dumps(skin,indent=1))
prev="\n".join(svg[:-1])+"".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#f0f" stroke-width="0.8"/>' for _,x,y,w,h in hits)+"</svg>"
open(f"{D}/preview.svg","w").write(prev)
