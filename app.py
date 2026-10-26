import os, re, json, random, urllib.request, urllib.error
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
DAILY_LIMIT = max(1, int(os.getenv("DAILY_LIMIT", "10")))
usage = {}

PAGE = r"""
<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111111"><title>Virtuose AI Study</title>
<style>
:root{--bg:#0b0b0d;--panel:#151519;--line:#303036;--gold:#d8b45a;--text:#f4f4f5;--muted:#aaaab4}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,sans-serif}
header{padding:22px 16px;background:linear-gradient(135deg,#171717,#292317);border-bottom:1px solid #4b4027}
.wrap{max-width:900px;margin:auto;padding:0 14px}h1{font-size:1.55rem;margin:0;color:var(--gold)}header p{margin:5px 0 0;color:#ddd}
main{padding:18px 0 36px}.grid{display:grid;grid-template-columns:1fr;gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px}
label{display:block;font-weight:650;margin:10px 0 6px}select,textarea{width:100%;background:#0e0e11;color:var(--text);border:1px solid #414149;border-radius:10px;padding:11px;font:inherit}
textarea{min-height:130px;resize:vertical}button{border:0;border-radius:10px;padding:12px 15px;background:var(--gold);color:#17130a;font-weight:750;font-size:1rem;cursor:pointer}
button.secondary{background:#28282f;color:var(--text);border:1px solid #45454d}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.notice{color:var(--muted);font-size:.9rem}.answer{white-space:pre-wrap;overflow-wrap:anywhere;background:#101014;border:1px solid var(--line);border-radius:12px;padding:14px;margin-top:12px;min-height:80px}
footer{color:var(--muted);font-size:.85rem;text-align:center;padding:18px}@media(min-width:760px){.grid{grid-template-columns:1fr 1fr}.wide{grid-column:1/-1}}
</style></head><body><header><div class="wrap"><h1>✦ VIRTUOSE AI STUDY</h1><p>Ton compagnon d’apprentissage universitaire</p></div></header>
<main class="wrap"><div class="grid">
<section class="card"><h2>📚 Espace d’apprentissage</h2>
<label for="subject">Matière</label><select id="subject"><option>Informatique</option><option>Mathématiques</option><option>Comptabilité</option><option>Économie et gestion</option><option>Statistiques</option><option>Droit</option><option>Électricité et électronique</option><option>Autre matière</option></select>
<label for="mode">Mode de travail</label><select id="mode"><option value="expliquer">Comprendre un cours</option><option value="exercice">Résoudre un exercice</option><option value="resume">Faire une fiche de révision</option><option value="quiz">Créer un mini-quiz</option><option value="plan">Préparer un plan d’étude</option></select>
<label for="question">Question ou contenu de cours</label><textarea id="question" placeholder="Écris ta question ou colle un extrait de tes notes…"></textarea>
<div class="actions"><button onclick="ask(false)">Mode local gratuit</button><button onclick="ask(true)">Demander à Gemini (Internet)</button><button class="secondary" onclick="document.getElementById('question').value=''">Effacer</button></div>
<p class="notice">Gemini n’est appelé que si tu appuies sur son bouton et confirmes. Le texte sera transmis à Google. N’envoie pas de données sensibles.</p></section>
<section class="card"><h2>💡 Réponse pédagogique</h2><div id="answer" class="answer" aria-live="polite">Ta réponse apparaîtra ici.</div>
<div class="actions"><button class="secondary" onclick="copyAnswer()">Copier la réponse</button><button class="secondary" onclick="saveSession()">Télécharger la séance</button></div><p id="status" class="notice"></p></section>
<section class="card wide"><h2>📝 Mes notes de cours</h2><p class="notice">Les notes sont conservées dans ce navigateur sur cet appareil.</p>
<textarea id="notes" placeholder="Colle ici tes définitions, formules ou points importants…"></textarea>
<div class="actions"><button onclick="saveNotes()">Enregistrer mes notes</button><button class="secondary" onclick="loadNotes()">Recharger</button><button class="secondary" onclick="deleteNotes()">Supprimer</button></div><p id="notesStatus" class="notice"></p></section>
<section class="card wide"><h2>🔐 Confidentialité et coûts</h2><ul><li>Le mode local n'appelle pas de service externe.</li><li>Le mode Gemini exige Internet et transmet la question à Google.</li><li>La clé API reste côté serveur, pas dans le navigateur.</li><li>Le quota local n'est pas une garantie de facturation.</li></ul></section>
</div></main><footer>Virtuose AI Study — prototype expérimental</footer>
<script>
let lastAnswer="";
async function ask(online){
 const question=document.getElementById('question').value.trim(),subject=document.getElementById('subject').value,mode=document.getElementById('mode').value;
 const out=document.getElementById('answer'),status=document.getElementById('status');
 if(!question){status.textContent="Écris une question d'abord.";return}
 if(online&&!confirm("Envoyer ce texte à Gemini via Internet ? N’inclus pas de données sensibles."))return;
 out.textContent="Préparation…";status.textContent="";
 try{const r=await fetch('/study',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,subject,mode,use_online:online})});
 const d=await r.json();if(!r.ok)throw Error(d.error||"Erreur");lastAnswer=d.answer;out.textContent=d.answer;
 status.textContent=d.online?"Réponse générée par Gemini. Vérifie les informations avec ton cours.":"Réponse locale : pas de grand modèle d’IA utilisé.";
 }catch(e){out.textContent="Impossible de répondre : "+e.message;status.textContent="Vérifie la configuration et le serveur."}
}
async function copyAnswer(){try{await navigator.clipboard.writeText(lastAnswer||document.getElementById('answer').textContent);document.getElementById('status').textContent="Réponse copiée."}catch(e){document.getElementById('status').textContent="Sélectionne le texte manuellement."}}
function saveSession(){let t="VIRTUOSE AI STUDY\nMatière : "+document.getElementById('subject').value+"\nQuestion :\n"+document.getElementById('question').value+"\n\nRéponse :\n"+(lastAnswer||document.getElementById('answer').textContent);let u=URL.createObjectURL(new Blob([t],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download='seance-virtuose.txt';a.click();URL.revokeObjectURL(u)}
function saveNotes(){localStorage.setItem('vas_notes',document.getElementById('notes').value);document.getElementById('notesStatus').textContent="Notes enregistrées sur cet appareil."}
function loadNotes(){document.getElementById('notes').value=localStorage.getItem('vas_notes')||''}
function deleteNotes(){localStorage.removeItem('vas_notes');document.getElementById('notes').value='';document.getElementById('notesStatus').textContent="Notes supprimées."}loadNotes();
</script></body></html>
"""

def summary(text, n=5):
    s = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text).strip())
    if len(s) <= n: return "\n".join("• " + x for x in s if x)
    chosen = sorted(sorted(enumerate(s), key=lambda p: len(p[1]), reverse=True)[:n])
    return "\n".join("• " + x for _, x in chosen)

def local_reply(subject, mode, q):
    intro = f"Matière : {subject}\n"
    if mode == "resume": return intro + "RÉSUMÉ SIMPLE\n\n" + summary(q) + "\n\nComplète avec les définitions et exemples du cours."
    if mode == "quiz":
        chunks = [s.strip() for s in re.split(r"(?<=[.!?])\s+", q) if len(s.strip()) > 20] or [q]
        random.shuffle(chunks)
        return intro + "MINI-QUIZ\n\n" + "\n\n".join(f"{i}. Explique avec tes propres mots : « {s[:180]} »" for i,s in enumerate(chunks[:5],1)) + "\n\nCompare tes réponses au cours : le corrigé intelligent n'est pas disponible en mode local."
    if mode == "plan": return intro + "PLAN D'ÉTUDE\n1. Définis ton objectif.\n2. Découpe le sujet en petites notions.\n3. Étudie 20 à 25 minutes.\n4. Ferme le cours et restitue ce que tu as retenu.\n5. Fais des exercices.\n6. Révise tes erreurs demain puis dans trois jours.\n\nSujet : " + q
    if mode == "exercice": return intro + "MÉTHODE\n1. Identifie ce qui est demandé.\n2. Liste les données et inconnues.\n3. Choisis la formule ou règle du cours.\n4. Résous étape par étape avec les unités.\n5. Vérifie le résultat.\n\nÉnoncé : " + q + "\n\nLe mode local ne garantit pas une correction spécifique exacte."
    return intro + "EXPLICATION GUIDÉE\nSujet reçu : " + q + "\n\n1. Repère les mots difficiles.\n2. Cherche leur définition dans le cours.\n3. Reformule avec tes propres mots.\n4. Trouve un exemple concret.\n5. Explique la notion sans regarder tes notes.\n\nCe mode applique des règles simples, pas un modèle génératif."

def gemini_reply(subject, mode, q):
    if not API_KEY: raise ValueError("Clé Gemini non configurée. Mets ta nouvelle clé dans .env puis redémarre.")
    instructions = {
      "expliquer":"Explique progressivement à un étudiant universitaire en français, avec définitions et exemples.",
      "exercice":"Résous l'exercice étape par étape, explique les formules et calculs. Si des données manquent, demande-les.",
      "resume":"Fais une fiche fidèle au texte : idées principales, définitions et formules. N'invente rien d'absent du texte.",
      "quiz":"Crée cinq questions de révision puis donne un corrigé expliqué.",
      "plan":"Crée un plan d'étude pratique et progressif."
    }
    prompt = f"Tu es Virtuose AI Study, tuteur universitaire. Réponds en français clair, signale les incertitudes et n'invente pas de sources.\nMatière : {subject}\nConsigne : {instructions.get(mode, instructions['expliquer'])}\nQuestion/contenu :\n{q[:12000]}"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.3,"maxOutputTokens":1800}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json","x-goog-api-key":API_KEY}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as res: data=json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        detail=e.read().decode(errors="replace")[:500]
        if e.code == 429: raise ValueError("Quota Gemini atteint. Réessaie plus tard et vérifie les quotas du compte.")
        if e.code in (401,403): raise ValueError("Clé API refusée ou accès non autorisé. Vérifie la clé dans Google AI Studio.")
        raise ValueError(f"Erreur Gemini HTTP {e.code}: {detail}")
    except urllib.error.URLError: raise ValueError("Internet indisponible. Utilise le mode local.")
    try: return "".join(p.get("text","") for p in data["candidates"][0]["content"]["parts"]).strip()
    except (KeyError,IndexError,TypeError): raise ValueError("Réponse Gemini inexploitable. Réessaie avec une question plus courte.")

@app.get("/")
def home(): return render_template_string(PAGE)

@app.post("/study")
def study():
    d=request.get_json(silent=True) or {}
    q=str(d.get("question","")).strip()
    subject=str(d.get("subject","Autre matière"))[:100]
    mode=str(d.get("mode","expliquer"))
    online=bool(d.get("use_online",False))
    if not q: return jsonify(error="La question est vide."),400
    if len(q)>12000: return jsonify(error="Question trop longue : maximum 12 000 caractères."),413
    if mode not in {"expliquer","exercice","resume","quiz","plan"}: mode="expliquer"
    if not online: return jsonify(answer=local_reply(subject,mode,q),online=False)
    day=datetime.now().strftime("%Y-%m-%d")
    if usage.get(day,0)>=DAILY_LIMIT: return jsonify(error=f"Limite locale de {DAILY_LIMIT} questions en ligne atteinte. Continue en mode local."),429
    try:
        answer=gemini_reply(subject,mode,q)
        usage[day]=usage.get(day,0)+1
        return jsonify(answer=answer,online=True,remaining=DAILY_LIMIT-usage[day])
    except ValueError as e: return jsonify(error=str(e)),502

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=False)
