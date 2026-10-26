# Virtuose AI Study — Version 4 : formules d'électricité intégrées

Cette version reprend la bibliothèque de cours de la version 3 et ajoute automatiquement à la base SQLite une fiche de connaissances avec les définitions, les formules principales, les unités et les références web pour :
- courant électrique;
- force de Coulomb;
- champ électrique;
- potentiel électrique;
- effet Joule.

## Ce qui change
- Au démarrage, `app.py` insère une seule fois la fiche intégrée dans la table `courses` de `virtuose_courses.sqlite3`.
- La fiche apparaît dans la bibliothèque des cours et la recherche par mots-clés peut l'ajouter au contexte envoyé à Gemini.
- Les formules et sources sont enregistrées dans la base de données de l'application; ce n'est pas un réentraînement du modèle Gemini.

## Déploiement Render
Build command : `pip install -r requirements.txt`
Start command : `gunicorn app:app`
Variables d'environnement recommandées :
- `APP_PASSWORD` : mot de passe privé du site (obligatoire)
- `GEMINI_API_KEY` : clé API privée, uniquement dans Render
- `GEMINI_MODEL=gemini-2.5-flash`
- `DAILY_LIMIT=10`
- `SESSION_SECRET` : chaîne aléatoire longue

Ne mets jamais la clé API dans GitHub ni dans le code source.

## Mise à jour d'une application déjà déployée
Téléverse les fichiers de cette archive dans le dépôt GitHub utilisé par Render, puis laisse Render redéployer. La fiche sera ajoutée au démarrage. Si le site utilise une base SQLite persistante existante, la fiche sera insérée une seule fois; si l'hébergement repart d'un stockage éphémère vide, elle sera recréée automatiquement au prochain démarrage.

## Limites
Le stockage SQLite local n'est pas garanti persistant sur Render Free. Pour garder aussi les cours importés par l'utilisateur de façon durable, configure une base de données persistante. Les extraits pertinents envoyés à Gemini quittent le serveur pour être traités par l'API Google. Vérifie les réponses et les sources originales.
