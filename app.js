const projects = document.querySelector('#projects');
const projectImages = {
  residence: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85',
  office: 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=85',
  courtyard: 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1200&q=85'
};
fetch('/api/projects').then(r=>r.json()).then(items=>projects.innerHTML=items.map(p=>`<article><div class="project-art" role="img" aria-label="${p.title}" style="background:url('${projectImages[p.image]}') center / cover no-repeat"></div><div class="project-info"><div class="project-meta">${p.type.toUpperCase()} · ${p.location.toUpperCase()} · ${p.year}</div><h3>${p.title}</h3><p>${p.description}</p></div></article>`).join(''));
document.querySelector('.menu').addEventListener('click',()=>document.querySelector('nav').classList.toggle('open'));
document.querySelector('#contactForm').addEventListener('submit',async e=>{e.preventDefault();const msg=document.querySelector('#formMessage');msg.textContent='Sending…';const data=Object.fromEntries(new FormData(e.target));try{const r=await fetch('/api/inquiries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const out=await r.json();if(!r.ok)throw Error(out.error);msg.textContent=out.message;e.target.reset()}catch(err){msg.textContent=err.message||'Unable to send your enquiry. Please try again.'}});
