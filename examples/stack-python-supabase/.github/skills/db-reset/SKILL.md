---
name: db-reset
description: Reset la BDD de dev et relance les seeds de démo
disable-model-invocation: true
---

Remet la base de données de développement à zéro.

1. Vérifier que le mode est bien **démo** (SQLite) - refuser si PostgreSQL détecté dans la config
2. Supprimer le fichier SQLite existant (`backend/*.db` ou chemin dans `conf/app.env`)
3. `cd backend && source .venv/bin/activate && python -c "from app.database import engine, Base; Base.metadata.create_all(engine)"`
4. Relancer le seed : `python -m app.demo_data` (module `app/demo_data.py`, fonction `seed_demo_data`)

Affiche : ✅ BDD recréée + seed appliqué / ❌ erreur détaillée
