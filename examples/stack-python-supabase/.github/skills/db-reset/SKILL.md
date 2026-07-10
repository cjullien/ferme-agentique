---
name: db-reset
description: Reset la BDD de dev et relance les seeds de démo
disable-model-invocation: true
---

Remet la base de données de développement à zéro.

1. Lire `CLAUDE.md` pour identifier le mode de BDD de dev du projet : fichier SQLite local
   (mode démo/offline) ou instance Postgres/Supabase de développement (jamais la production —
   vérifier l'URL/l'environnement avant toute action destructive).
2. **Mode SQLite local** : supprimer le fichier existant (chemin identifié via `CLAUDE.md`,
   ex: `backend/*.db`), puis recréer le schéma via l'ORM (commande identifiée via `CLAUDE.md`).
3. **Mode Postgres/Supabase dev** : ne jamais `DROP DATABASE` — utiliser la commande de reset
   du système de migration en place (ex: `alembic downgrade base && alembic upgrade head`, ou
   l'équivalent Supabase CLI `supabase db reset` si applicable), après confirmation explicite
   de l'utilisateur que la cible n'est pas la production.
4. Relancer le seed de démo (commande/module identifié via `CLAUDE.md`).

Affiche : ✅ BDD recréée + seed appliqué / ❌ erreur détaillée
