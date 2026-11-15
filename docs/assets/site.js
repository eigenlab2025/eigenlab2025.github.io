
(() => {
 const app = document.getElementById('app');
 const isPreview = typeof REVIEW_PAGES !== 'undefined';
 function filterPublications(){
  const q=(document.getElementById('pub-search')?.value||'').trim().toLowerCase();
  const type=document.getElementById('pub-type')?.value||'';
  const year=document.getElementById('pub-year')?.value||'';
  const student=document.getElementById('pub-student')?.checked||false;
  let count=0;
  document.querySelectorAll('.publication').forEach(p=>{const show=(!type||p.dataset.type===type)&&(!year||p.dataset.year===year)&&(!student||p.dataset.student==='true')&&p.textContent.toLowerCase().includes(q);p.hidden=!show;count+=show;});
  const counter=document.getElementById('pub-count');if(counter)counter.textContent=count;
  const empty=document.getElementById('empty-results');if(empty)empty.hidden=count!==0;
 }
 function renderPreview(){
  const parts=location.hash.slice(1).split('/');
  const lang=['ja','en','zh'].includes(parts[0])?parts[0]:'ja';
  const page=REVIEW_PAGES[lang+'/'+parts[1]]?parts[1]:'home';
  const item=REVIEW_PAGES[lang+'/'+page];
  document.documentElement.lang=item.lang;document.title=item.title;
  document.body.dataset.lang=lang;document.body.dataset.page=page;
  app.innerHTML=item.html;
  app.querySelectorAll('a[data-route]').forEach(a=>{a.href='#'+a.dataset.route+(a.dataset.section?'/'+a.dataset.section:'');});
  app.querySelectorAll('[data-asset]').forEach(im=>{im.src=REVIEW_ASSETS[im.dataset.asset];});
  document.getElementById('review-label').textContent=REVIEW_COPY[lang].reviewLabel;
  document.getElementById('review-open').textContent=REVIEW_COPY[lang].reviewButton;
  const dialog=document.getElementById('review-dialog');
  dialog.innerHTML='<h2>'+REVIEW_COPY[lang].reviewTitle+'</h2><p>'+REVIEW_COPY[lang].reviewIntro+'</p><ol>'+REVIEW_COPY[lang].reviewItems.map(x=>'<li>'+x+'</li>').join('')+'</ol><button class="button" id="review-close">'+REVIEW_COPY[lang].close+'</button>';
  window.scrollTo(0,0);
  if(parts[2])requestAnimationFrame(()=>document.getElementById(parts[2])?.scrollIntoView());
 }
 document.addEventListener('click',ev=>{
  if(isPreview&&ev.target.closest('.skip-link')){ev.preventDefault();document.getElementById('main').focus();document.getElementById('main').scrollIntoView();return;}
  const toggle=ev.target.closest('.menu-toggle');if(toggle){const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',open);document.getElementById('main-nav').classList.toggle('open',open);return;}
  const route=ev.target.closest('a[data-route]');
  if(route&&isPreview&&!ev.ctrlKey&&!ev.metaKey&&!ev.shiftKey){ev.preventDefault();const target=route.dataset.route+(route.dataset.section?'/'+route.dataset.section:'');if(location.hash.slice(1)===target){window.scrollTo(0,0);}else{location.hash=target;}return;}
  if(ev.target.closest('#pub-reset')){document.getElementById('pub-search').value='';document.getElementById('pub-type').value='';document.getElementById('pub-year').value='';document.getElementById('pub-student').checked=false;filterPublications();}
  if(ev.target.closest('#review-open'))document.getElementById('review-dialog').showModal();
  if(ev.target.closest('#review-close'))document.getElementById('review-dialog').close();
 });
 document.addEventListener('keydown',ev=>{if(ev.key==='Escape'){document.querySelector('.main-nav')?.classList.remove('open');document.querySelector('.menu-toggle')?.setAttribute('aria-expanded','false');}});
 document.addEventListener('input',ev=>{if(ev.target.id==='pub-search')filterPublications();});
 document.addEventListener('change',ev=>{if(['pub-type','pub-year','pub-student'].includes(ev.target.id))filterPublications();});
 if(isPreview){window.addEventListener('hashchange',renderPreview);renderPreview();}
})();
