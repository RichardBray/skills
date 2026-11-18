const VOICE="track-0446168e",HLT="track-61682a03",CHT="track-ef2b8d85",SA="track-17258987",SB="track-746aed43";
const POP="asset-238463b0",WHO="asset-a9d47ea9",SUC="asset-4089adba",MRK="asset-0a5daa2e",JIN="asset-bd13d232",CHW="asset-e8bfb795",CHTH="asset-14de7696";
const id=r=>typeof r==="string"?r:(r.id||r.clip||r.track||JSON.stringify(r));
const r3=v=>Math.round(v*1000)/1000;
const tf=(x,y,s,o)=>({x,y,scaleX:s,scaleY:s,rotation:0,rotationX:0,rotationY:0,opacity:o});
const AUD=v=>({audio:{gain:1,volume:v,normalize:false,muted:false}});
const POPTO={"transform.scaleX":1,"transform.scaleY":1,"transform.opacity":1};
beacon.run("clip_remove",{clips:P.stage});
const report={};
for(const name of Object.keys(P.videos)){
  const D=P.videos[name],S=D.starts,E=D.END;
  const ends=S.map((s,i)=>r3(s+D.LEN[i]));
  D.vo.forEach((v,i)=>beacon.run("clip_add",{type:"audio",assetId:v.a,start:r3(S[i]+0.05),duration:v.d,track:VOICE,props:AUD(1)}));
  D.base.forEach((a,i)=>beacon.run("clip_add",{type:"image",assetId:a,start:S[i],duration:D.LEN[i],props:{transform:tf(0,0,1,1)}}));
  for(const l of D.layers){
    const dur=r3(ends[l.s]-l.st);
    if(l.id==="hl"){
      const c=id(beacon.run("clip_add",{type:"image",assetId:l.asset,start:l.st,duration:dur,track:HLT,props:{transform:tf(l.x,l.y,1,1),crop:{left:0,top:0,right:l.w,bottom:0}}}));
      const [e,d]=D.hl[String(l.s)];beacon.run("animation_add",{clip:c,end:r3(S[l.s]+e),duration:d,easing:"easeOut",to:{"crop.right":0}});
    } else {
      const c=id(beacon.run("clip_add",{type:"image",assetId:l.asset,start:l.st,duration:dur,props:{transform:tf(l.x,l.y,0.85,0)}}));
      beacon.run("animation_add",{clip:c,end:r3(l.st+0.24),duration:0.24,easing:"backOut",to:POPTO});
    }
  }
  const mt=id(beacon.run("track_add",{name:D.track}));
  beacon.run("clip_add",{type:"audio",assetId:D.music,start:D.T0,duration:r3(E-D.T0),track:mt,props:AUD(0.075)});
  const t0=r3(D.T0+0.6);
  const ch=id(beacon.run("clip_add",{type:"image",assetId:CHW,start:t0,duration:r3(S[1]-t0),track:CHT,props:{transform:tf(-319,-330,0.85,0)}}));
  [[0.24,0.24,"backOut",POPTO],[2.0,0.15,"easeOut",{"transform.y":-300}],[2.2,0.2,"easeIn",{"transform.y":-330}],[4.0,0.15,"easeOut",{"transform.y":-300}],[4.2,0.2,"easeIn",{"transform.y":-330}]].forEach(([e,d,ea,to])=>beacon.run("animation_add",{clip:ch,end:r3(t0+e),duration:d,easing:ea,to}));
  const tt=r3(S[5]+D.thumb);
  const th=id(beacon.run("clip_add",{type:"image",assetId:CHTH,start:tt,duration:r3(E-tt),track:CHT,props:{transform:tf(328,-355,0.85,0)}}));
  [[0.24,0.24,"backOut",POPTO],[1.233,0.15,"easeOut",{"transform.y":-325}],[1.433,0.2,"easeIn",{"transform.y":-355}],[2.033,0.15,"easeOut",{"transform.y":-325}],[2.233,0.2,"easeIn",{"transform.y":-355}]].forEach(([e,d,ea,to])=>beacon.run("animation_add",{clip:th,end:r3(tt+e),duration:d,easing:ea,to}));
  const sf=[];
  for(const l of D.layers){
    if((D.pop[String(l.s)]||[]).includes(l.id)) sf.push([l.st,POP,0.197,0.45]);
    if((D.who[String(l.s)]||[]).includes(l.id)) sf.push([l.st,WHO,0.238,0.45]);
  }
  sf.push([t0,WHO,0.238,0.45]);
  D.marker.forEach(([s,o])=>sf.push([r3(S[s]+o),MRK,0.545,0.45]));
  D.success.forEach(([s,o])=>sf.push([r3(S[s]+o),SUC,1.207,0.4]));
  sf.push([tt,POP,0.197,0.45]);
  sf.push([r3(S[5]+D.jingle),JIN,D.jdur,0.5]);
  sf.sort((a,b)=>a[0]-b[0]);
  const free={A:0,B:0},T={A:SA,B:SB},bad=[];
  for(const [t,a,du,v] of sf){
    const k=free.A<=t+0.001?"A":"B"; if(free[k]>t+0.001) bad.push(t);
    free[k]=t+du;
    beacon.run("clip_add",{type:"audio",assetId:a,start:t,duration:du,track:T[k],props:AUD(v)});
  }
  if(bad.length) throw new Error(name+" sfx overlap "+bad.join(","));
  const {tracks}=beacon.query("timeline_clips",{from:D.T0,to:E,type:"image"});let trimmed=0;
  for(const tr of tracks)for(const c of tr.clips){if(c.start<D.T0-0.001)continue;const e=ends.find(x=>x>c.start+0.001);if(e&&c.end>e+0.001){beacon.run("clip_trim",{clip:c.id,end:e});trimmed++;}}
  report[name]={sfx:sf.length,music:mt,end:E,trimmed};
}
return report;
