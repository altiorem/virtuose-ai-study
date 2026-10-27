const CSRF=document.querySelector('meta[name=csrf]').content,_f=window.fetch.bind(window);
window.fetch=(u,o={})=>_f(u,{...o,headers:{...(o.headers||{}),'X-CSRF-Token':CSRF}});
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let lastQa=null,courses=[];
function show(v){$$('.view').forEach(e=>e.classList.toggle('on',e.id==='v-'+v));
 $$('[data-v]').forEach(b=>b.classList.toggle('on',b.dataset.v===v&&(b.closest('.side')||b.closest('.bottom'))));
 $('#side').classList.remove('open');
 if(v==='courses')loadCourses();if(v==='history')loadHistory();if(v==='settings')loadUsage()}
document.addEventListener('click',e=>{const b=e.target.closest('[data-v]');if(b)show(b.dataset.v)});
$('#burger').onclick=()=>$('#side').classList.toggle('open');
async function api(url,opt){const r=await fetch(url,opt),d=await r.json().catch(()=>({}));if(!r.ok)throw Error(d.error||'Erreur '+r.status);return d}
function bubble(t,me){const d=document.createElement('div');d.className='msg'+(me?' me':'');d.textContent=t;$('#chat').append(d);d.scrollIntoView({block:'end'});return d}
async function ask(text){text=text.trim();if(!text)return;bubble(text,true);$('#q').value='';lastQa=null;$('#learnBtn').style.display='none';
 const w=bubble('Réflexion…');
 try{const d=await api('/study',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:text,subject:$('#subject').value,mode:$('#mode').value,use_online:true})});
  w.textContent=d.answer;lastQa=d.qa_id||null;$('#learnBtn').style.display=lastQa?'':'none';
  $('#status').textContent=d.online?`Réponse Gemini. Il te reste ${d.remaining} appels aujourd’hui. Vérifie avec ton cours.`:'Réponse locale (sans IA).'}
 catch(e){w.textContent='Impossible de répondre : '+e.message}}
$('#askForm').onsubmit=e=>{e.preventDefault();ask($('#q').value)};
$$('.chips .ghost').forEach(c=>c.onclick=()=>ask(c.textContent));
$('#learnBtn').onclick=async()=>{try{const d=await api('/learn/'+lastQa,{method:'POST'});$('#status').textContent=d.added?'Réponse retenue : elle servira pour tes prochaines questions.':'Déjà dans ta bibliothèque.';$('#learnBtn').style.display='none'}catch(e){$('#status').textContent=e.message}};
function draw(){const k=$('#search').value.toLowerCase(),l=$('#list');l.innerHTML='';
 const rows=courses.filter(c=>c.title.toLowerCase().includes(k));
 if(!rows.length)l.innerHTML='<div class="item"><div class="muted">Aucun cours. Ajoute un document pour commencer.</div></div>';
 rows.forEach(c=>{const d=document.createElement('div');d.className='item';
  d.innerHTML='<span class="ic">📄</span><div><b></b><small></small></div><button title="Supprimer">🗑</button>';
  d.querySelector('b').textContent=c.title;d.querySelector('small').textContent=`${c.source} · ${Math.max(1,Math.round(c.characters/1000))} Ko · ${c.created_at.slice(0,10)}`;
  d.querySelector('button').onclick=async()=>{if(confirm('Supprimer ce cours ?')){await api('/courses/'+c.id,{method:'DELETE'});loadCourses()}};l.append(d)})}
async function loadCourses(){courses=(await api('/courses')).courses;draw()}
$('#search').oninput=draw;
async function upload(f){const s=$('#addStatus');s.textContent='Lecture du fichier…';const fd=new FormData();fd.append('file',f);
 try{const d=await api('/courses/upload',{method:'POST',body:fd});s.textContent=`« ${d.title} » ajouté (${d.characters} caractères).`}catch(e){s.textContent=e.message}}
const drop=$('#drop');drop.onclick=()=>$('#file').click();$('#file').onchange=e=>e.target.files[0]&&upload(e.target.files[0]);
drop.ondragover=e=>{e.preventDefault();drop.classList.add('over')};drop.ondragleave=()=>drop.classList.remove('over');
drop.ondrop=e=>{e.preventDefault();drop.classList.remove('over');e.dataTransfer.files[0]&&upload(e.dataTransfer.files[0])};
$('#saveText').onclick=async()=>{const s=$('#addStatus');try{await api('/courses/text',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title:$('#ctitle').value,content:$('#ctext').value})});s.textContent='Cours enregistré.';$('#ctext').value=''}catch(e){s.textContent=e.message}};
$('#quizBtn').onclick=async()=>{const o=$('#quizOut');o.hidden=false;o.textContent='Génération du quiz…';
 try{o.textContent=(await api('/study',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:$('#qtopic').value||$('#qsubject').value,subject:$('#qsubject').value,mode:'quiz',use_online:true})})).answer}catch(e){o.textContent=e.message}};
async function loadHistory(){const h=(await api('/history')).items,l=$('#hist');l.innerHTML=h.length?'':'<div class="item"><div class="muted">Aucune question pour le moment.</div></div>';
 h.forEach(i=>{const d=document.createElement('div');d.className='item';d.innerHTML='<span class="ic">💬</span><div><b></b><small></small></div>';d.querySelector('b').textContent=i.question;d.querySelector('small').textContent=`${i.subject} · ${i.created_at.slice(0,10)}`+(i.validated?' · retenue':'');l.append(d)})}
async function loadUsage(){const d=await api('/history');$('#usage').textContent=`Appels Gemini restants aujourd’hui : ${d.remaining}.`}
