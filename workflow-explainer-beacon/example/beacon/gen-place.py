import json,sys
R='/Users/robray/fc/videos/jobs-hunt/'
imp=json.load(open(sys.argv[1]))
ASSETS,CLIPS=imp['assets'],imp['clips']
allf=json.load(open(R+'import-funnel-hooks.json'))
AID=dict(zip(allf,ASSETS))
CONF={
 'funnel':dict(T0=160.0,LEN=[6.6,3.3,6.0,6.0,6.4,9.2],VO=[5.79,2.5,4.1,4.98,4.98,7.02],
   hl={2:[3.0,1.5],4:[1.9,0.9]},marker=[[2,1.5],[4,1.0]],success=[[4,3.2]],
   pop={1:['tab','c1'],2:['tab','k0','k1'],3:['tab','q0','q1','q2'],4:['tab','f','b'],5:['tab','t0','t1','t2']},
   who={0:['a','b','d'],3:['c']},thumb=6.05,jingle=7.15,jdur=2.0,mus='music-keep-your-focus.mp3',track='Music 4'),
 'hooks':dict(T0=210.0,LEN=[6.0,3.3,5.8,8.0,8.4,7.9],VO=[5.14,2.5,3.78,7.0,7.15,5.59],
   hl={2:[2.6,1.2],4:[6.6,0.8]},marker=[[2,1.4],[4,5.8]],success=[[4,6.7]],
   pop={1:['tab','c1'],2:['tab','k0','k1'],3:['tab','r0','r1','r2','q'],4:['tab','t0','t1'],5:['tab','d0','d1','d2']},
   who={0:['a','b','d']},thumb=4.85,jingle=5.75,jdur=2.1,mus='music-out-of-order.mp3',track='Music 5'),
}
out={}
for v,c in CONF.items():
    D=R+v+'/'
    SC=json.load(open(D+'scenes.json'))
    starts=[];t=c['T0']
    for L in c['LEN']: starts.append(round(t,3)); t+=L
    layers=[]
    for i,s in enumerate(SC):
        rects={r[0]:r[1:] for r in json.load(open(D+f'rects-s{i}.json'))}
        for l in s['layers']:
            x,y,w,h=rects[l['id']]
            layers.append({"s":i,"id":l['id'],"asset":AID[D+f"s{i}-{l['id']}.png"],"st":round(starts[i]+l['d'],3),"x":round(x+w/2-540,2),"y":round(960-(y+h/2),2),"w":w})
    out[v]=dict(T0=c['T0'],END=round(t,3),starts=starts,LEN=c['LEN'],
      vo=[{"a":AID[D+f'voices/t_{n}.mp3'],"d":d} for n,d in zip(['h','setup','ask','s3','s4','e'],c['VO'])],
      base=[AID[D+f's{i}-base.png'] for i in range(6)],layers=layers,music=AID[D+c['mus']],track=c['track'],
      hl={str(k):v2 for k,v2 in c['hl'].items()},marker=c['marker'],success=c['success'],pop={str(k):v2 for k,v2 in c['pop'].items()},who={str(k):v2 for k,v2 in c['who'].items()},
      thumb=c['thumb'],jingle=c['jingle'],jdur=c['jdur'])
    print(v,starts,round(t,3))
json.dump({"videos":out,"stage":CLIPS},open(R+'place-funnel-hooks.json','w'))
