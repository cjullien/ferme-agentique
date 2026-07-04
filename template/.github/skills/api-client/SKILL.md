---
name: api-client
description: Audit des appels réseau côté client — URLs en dur, absence de gestion d'erreur, cache non configuré, typage des réponses absent. Applicable à tout client HTTP (fetch, axios, SWR, React Query, TanStack Query, Vue Query, ky, got, Retrofit, Feign…).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Audit API Client

Vérifie la robustesse et la maintenabilité des appels réseau côté client, peu importe le framework.

## Processus

### 1. Lire CLAUDE.md
Identifier le client HTTP utilisé (`{{http_client}}`), la couche d'appels (ex: `src/api/`, `lib/fetch.ts`, `services/http.py`, `infrastructure/`), et les conventions du projet.

### 2. Cartographier les appels réseau
Grep dans le code source pour les patterns d'appel HTTP :
- Appels directs : `fetch(`, `axios.`, `http.get(`, `requests.get(`, `HttpClient`, `RestTemplate`, `WebClient`
- Hooks de cache : `useQuery(`, `useSWR(`, `useMutation(`, `useInfiniteQuery(`
- Clients générés : OpenAPI codegen, gRPC stubs

### 3. Vérifier chaque point d'appel

**URLs**
- Détecter les URLs en dur (chaînes `http://`, `https://`, chemins `/api/` hors constante)
- Vérifier qu'elles proviennent d'une configuration centralisée (variable d'env, constante dédiée)

**Gestion d'erreur**
- Chaque appel dispose-t-il d'une gestion d'erreur explicite (try/catch, `.catch()`, `onError`) ?
- Les codes d'erreur HTTP (4xx, 5xx) sont-ils distingués des erreurs réseau ?
- L'erreur remonte-t-elle jusqu'à l'UI (feedback utilisateur) ou est-elle silencieuse ?

**Cache et fraîcheur des données**
- La durée de validité du cache est-elle configurée (`staleTime`, `ttl`, `max-age`) ?
- Le comportement en cas de reconnexion réseau est-il défini (retry, refetch) ?
- Les requêtes en vol sont-elles annulables (AbortController, CancelToken) ?

**Typage des réponses**
- Les types de réponse sont-ils explicites (pas de `any`, `Object`, `Map<String, Object>`) ?
- Existe-t-il un schéma de validation à la réception (Zod, Yup, Joi, class-validator, Pydantic) ?

### 4. Rapport

| Fichier | Ligne | Problème | Priorité |
|---|---|---|---|

Priorités : `P1` sécurité/crash · `P2` robustesse · `P3` maintenabilité

### 5. Corrections (si demandées)
- Centraliser les URLs dans un fichier de constantes ou variables d'env
- Wrapper le client HTTP avec gestion d'erreur centralisée
- Ajouter la validation de schéma sur les endpoints critiques

## Règles

- Ne jamais logger les réponses brutes (risque de fuite de données sensibles)
- Les tokens d'authentification ne doivent jamais apparaître dans les logs d'erreur
- Signaler tout appel réseau fait en dehors de la couche dédiée (dans un composant UI, un modèle)
