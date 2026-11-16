// cfg: {cwd, prompt, typeFrom, typeTo, enter, lines:[{at, html}], rings:[{at, sel, pad}]}
function buildTerm(cfg){
 const w=document.getElementById('w');
 w.innerHTML=`<div class=box><div class=h><b>✻</b> Welcome to <b>Claude Code</b>!</div><div class=dim>  cwd: ${cfg.cwd}</div></div>`+
 (cfg.before||'')+`<div class=in id=inp><span class=or>&gt; </span><span id=ty></span><span class=c id=cur></span></div><div id=out></div>`;
 const out=document.getElementById('out');
 cfg.lines.forEach((l,i)=>{const d=document.createElement('div');d.className='ln';d.innerHTML=l.html;d.id='l'+i;d.style.opacity=0;out.appendChild(d);});
 const sv=document.getElementById('sv');
 window.__frame=t=>{
  const ty=document.getElementById('ty');
  if(t<cfg.enter){typed(ty,cfg.prompt,t,cfg.typeFrom,cfg.typeTo);}else ty.textContent=cfg.prompt;
  document.getElementById('cur').style.opacity=(t>=cfg.enter)?0:(Math.floor(t*2.5)%2?0.2:1);
  cfg.lines.forEach((l,i)=>{document.getElementById('l'+i).style.opacity=t>=l.at?1:0;});
  (cfg.rings||[]).forEach((r,i)=>{
    if(!document.getElementById('rg'+i)&&t>=r.at-0.01){const e=document.querySelector(r.sel).getBoundingClientRect();addRing(sv,'rg'+i,e.left+e.width/2,e.top+e.height/2,e.width/2+(r.pad||30),e.height/2+(r.padY||22));}
    ring('rg'+i,t,r.at);});
 };
}
