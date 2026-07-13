---
name: db-migrations
description: Audite et corrige l'idempotence des scripts de migration Flyway - CREATE TABLE/INDEX et ADD COLUMN sans garde IF NOT EXISTS.
---

Lance l'agent `db-migrations`.

Utilise l'outil Agent avec `subagent_type: db-migrations` pour auditer les scripts Flyway
(dossier(s) identifiés via `CLAUDE.md`) : `CREATE TABLE`/`CREATE INDEX` sans `IF NOT EXISTS`,
`ALTER TABLE ... ADD COLUMN` sans `IF NOT EXISTS`, contraintes sans le pattern
`DROP CONSTRAINT IF EXISTS`/`ADD CONSTRAINT`, migration de prod sans son pendant côté jeu de
test (ou l'inverse) - **puis applique les corrections** directement dans les scripts SQL.

À invoquer dès qu'un script de migration Flyway est ajouté ou modifié, ou sur toute demande
mentionnant Flyway/une migration de schéma.
