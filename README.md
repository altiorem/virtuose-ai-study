# Virtuose AI Study — archive complète

Cette archive conserve les fichiers séparés dans leur emplacement habituel pour une application Flask. Le backend est dans `app.py`, les pages HTML dans `templates/`, le CSS dans `static/css/` et le JavaScript dans `static/js/`.

## Structure

- `app.py` : serveur Flask, routes et logique de l’assistant.
- `templates/index.html` : interface principale.
- `templates/login.html` : page de connexion.
- `static/css/style.css` : styles et affichage mobile/ordinateur.
- `static/js/app.js` : navigation et interactions de l’interface.
- `requirements.txt` : dépendances Python.
- `.env.example` : exemple de variables à configurer.

## Déploiement sur Render

- Build command : `pip install -r requirements.txt`
- Start command : `gunicorn app:app --workers 1 --threads 4 --timeout 120`

Variables à configurer dans les paramètres du service : `APP_PASSWORD` (obligatoire), `GEMINI_API_KEY` (si tu utilises Gemini), et éventuellement `GEMINI_MODEL`, `DAILY_LIMIT`, `SESSION_SECRET`. Ne mets jamais ta clé API dans les fichiers publics.

## Avant de remplacer l’application actuelle

1. Télécharge et garde une copie de ton ancienne archive et de ton ancien `app.py`.
2. Ne supprime pas ta base de données SQLite si elle contient tes cours.
3. Cette archive a été vérifiée pour la syntaxe Python, mais elle n’a pas encore été testée de bout en bout sur ton compte Render.
