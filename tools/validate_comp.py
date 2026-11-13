import json, re, sys, xml.etree.ElementTree as ET
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,'skins',(sys.argv[1] if len(sys.argv)>1 else 'comp-dbx234'))+'/'
CATALOG_TOGGLE={'comp.toggle','comp.mode'}
CATALOG_VALUE={'comp.attack','comp.release','comp.ratio','comp.freq','comp.threshold','comp.gain','comp.balance','comp.volume'}
CATALOG_BUTTON={'comp.reset'}
METERS={'meter.mic','meter.output','meter.sysreverb'}
FORB={'script','foreignObject','image','use','audio','video','iframe','filter','metadata'}
err=[];warn=[]
root=ET.parse(D+'skin.svg').getroot()
ns=lambda t:t.split('}')[-1]
ids={};n=0
for e in root.iter():
    n+=1
    if ns(e.tag) in FORB: err.append('terlarang '+ns(e.tag))
    for k,v in e.attrib.items():
        if k.startswith('on') or 'href' in k: err.append('atribut '+k)
        if re.search(r'https?://',v) and not k.startswith('xmlns'): err.append('url di '+k)
    if 'id' in e.attrib:
        if e.attrib['id'] in ids: err.append('ID ganda '+e.attrib['id'])
        ids[e.attrib['id']]=e
for a in ('data-skin-name','data-skin-version','data-skin-author','viewBox'):
    if a not in root.attrib: err.append('root tanpa '+a)
vb=[float(x) for x in root.attrib['viewBox'].split()]
js=json.load(open(D+'skin.json',encoding='utf-8'))
used=set()
def inside(r): 
    x,y,w,h=[float(r.attrib[k]) for k in('x','y','width','height')]
    return x>=0 and y>=0 and x+w<=vb[2] and y+h<=vb[3] and w>0 and h>0
for c in js['controls']:
    cid=c['id'];t=c['type']
    if cid not in ids: err.append(cid+' tak ada di SVG'); continue
    m=js['mapping'].get(cid)
    if not m: err.append(cid+' tanpa mapping'); continue
    fn=m['function']
    ok={'toggle':CATALOG_TOGGLE,'rotary':CATALOG_VALUE,'slider':CATALOG_VALUE,'button':CATALOG_BUTTON}[t]
    if fn not in ok: err.append(f'{cid}: function {fn} tidak cocok untuk {t}')
    if fn in used: err.append('function ganda '+fn)
    used.add(fn)
    h=ids.get(c.get('hit'))
    if h is None: err.append(cid+' tanpa hit')
    elif not inside(h): err.append(cid+' hit di luar viewBox')
    if t=='rotary':
        g=ids[cid]
        if 'data-cx' not in g.attrib or 'data-cy' not in g.attrib: err.append(cid+' tanpa data-cx/cy')
        if abs(float(g.attrib['data-value-default'])-c['defaultValue'])>1e-4: err.append(cid+' default beda')
    for s in c.get('states',{}).values():
        if s not in ids: err.append(cid+' state '+s+' tak ada')
for i in js['indicators']:
    if i['meter'] not in METERS: err.append('meter '+i['meter'])
    g=ids.get(i['on'])
    if g is None: err.append(i['id']+' tak ada on')
    else:
        r=next((x for x in g.iter() if ns(x.tag)=='rect'),None)
        if r is None or not inside(r): err.append(i['id']+' rect lampu')
hits=[(k,ids[k]) for k in ids if k.startswith('hit-')]
for a in range(len(hits)):
    for b in range(a+1,len(hits)):
        A=[float(hits[a][1].attrib[k]) for k in('x','y','width','height')];B=[float(hits[b][1].attrib[k]) for k in('x','y','width','height')]
        if A[0]<B[0]+B[2] and B[0]<A[0]+A[2] and A[1]<B[1]+B[3] and B[1]<A[1]+A[3]: warn.append('hit tumpuk '+hits[a][0]+' '+hits[b][0])
missing=CATALOG_VALUE-used
if missing: warn.append('function tak dipakai: '+str(missing))
ET.parse(D+'preview.svg')
print('elemen',n,'| kontrol',len(js['controls']),'| lampu',len(js['indicators']))
print('ERROR:',err or 'tidak ada');print('PERINGATAN:',warn or 'tidak ada')
sys.exit(1 if err else 0)
