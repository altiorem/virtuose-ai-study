# Virtuose AI Study — déploiement Render

## Déployer gratuitement depuis un téléphone

1. Téléchargez et décompressez ce dossier ZIP.
2. Sur GitHub, créez un nouveau dépôt (repository) appelé `virtuose-ai-study`. Ne mettez aucune clé API dans le dépôt.
3. Depuis le navigateur, ouvrez le dépôt GitHub, choisissez **Add file > Upload files**, puis téléversez `app.py`, `requirements.txt` et `.gitignore` (vous pouvez aussi téléverser ce README).
4. Sur Render, choisissez **New + > Web Service**, connectez GitHub et sélectionnez le dépôt.
5. Paramètres :
   - Runtime/Language : Python
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `gunicorn app:app`
   - Instance type : Free
6. Dans **Environment Variables**, ajoutez `GEMINI_API_KEY` avec votre nouvelle clé privée, `GEMINI_MODEL` avec `gemini-2.5-flash`, et `DAILY_LIMIT` avec `10`.
7. Cliquez sur **Create Web Service** et attendez la fin du déploiement. Render donnera une adresse publique en `onrender.com`.

## Sécurité et limites
- Ne publiez jamais la clé Gemini dans GitHub, dans le code HTML ou dans une conversation. Si une ancienne clé a été partagée, révoquez-la et créez-en une nouvelle.
- Le mode local ne nécessite pas de clé Gemini; les questions envoyées au mode en ligne sont transmises à Google Gemini.
- L'offre gratuite de Render met le service en veille après environ 15 minutes sans activité; le premier chargement après veille peut prendre environ une minute.
- Le système de limite `DAILY_LIMIT` est seulement un compteur en mémoire et se réinitialise quand le service redémarre. Il ne constitue pas une limite de facturation.
- Les notes sont conservées dans le navigateur de l'appareil; elles ne se synchronisent pas entre appareils.
