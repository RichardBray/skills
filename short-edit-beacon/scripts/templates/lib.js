const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const prog=(t,a,b)=>clamp((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3);
const back=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
// hand-drawn red ellipse around a box (canvas px), drawn over dur seconds from t0
function ring(id,t,t0,dur=0.45){const p=document.getElementById(id);if(!p)return;const L=p.getTotalLength();const k=eo(prog(t,t0,t0+dur));p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-k);p.style.opacity=t>=t0?1:0;}
function ellipsePath(cx,cy,rx,ry){let d='';const n=60;for(let i=0;i<=n*1.12;i++){const a=-2.4+i/n*Math.PI*2;const w=1+0.04*Math.sin(i*0.7)+0.03*(i/n);d+=(i?'L':'M')+(cx+rx*w*Math.cos(a)).toFixed(1)+','+(cy+ry*w*Math.sin(a)).toFixed(1);}return d;}
function addRing(svg,id,cx,cy,rx,ry){const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.id=id;p.setAttribute('d',ellipsePath(cx,cy,rx,ry));p.setAttribute('class','ring');svg.appendChild(p);}
function typed(el,text,t,t0,t1){const k=prog(t,t0,t1);el.textContent=text.slice(0,Math.round(text.length*k));}
