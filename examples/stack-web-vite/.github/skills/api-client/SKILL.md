---
name: api-client
description: Audit des appels API côté frontend — URLs en dur, absence de gestion d'erreur, hooks React Query/SWR mal configurés, types de réponse `any`. À utiliser avant une mise en prod ou lors d'une revue.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Audit API Client

Vérifie la robustesse et la maintenabilité des appels réseau côté frontend.

## Processus

### 1. Cartographier les appels API
Grep sur `src/` pour identifier tous les points d'appel :
- `fetch(`
- `axios.`
- `useQuery(`
- `useSWR(`
- `useMutation(`

### 2. Vérifier chaque point d'appel

**URLs**
- Détecter les URLs en dur (`http://`, `https://`, `/api/` hors constante)
- Vérifier qu'elles proviennent d'une constante (`API_URL`, `import.meta.env.VITE_*`)

**Gestion d'erreur**
- Chaque `fetch` doit avoir un `.catch` ou être dans un `try/catch`
- Vérifier `response.ok` avant `response.json()`
- Les hooks React Query/SWR doivent exposer `error` au composant appelant

**Configuration React Query / SWR**
- `staleTime` défini (évite les refetch inutiles)
- `retry` configuré (pas de retry infini sur les 4xx)
- `onError` global configuré dans le `QueryClient`

**Typage**
- Détecter les `any` sur les types de réponse
- Vérifier la présence d'un schéma de validation (Zod, Yup) sur les réponses critiques

### 3. Rapport

| Fichier | Ligne | Problème | Priorité |
|---|---|---|---|

Priorités : `P1` sécurité/crash · `P2` robustesse · `P3` maintenabilité

### 4. Corrections (si demandées)
- Extraire les URLs vers `src/lib/api/constants.ts`
- Wrapper `fetch` natif dans un helper avec gestion d'erreur centralisée
- Ajouter les types Zod sur les endpoints critiques

## Règles

- Ne jamais logger les réponses API brutes (risque de fuite de données)
- Les tokens d'authentification ne doivent pas apparaître dans les logs d'erreur
- Préférer les hooks dédiés par resource (`useUser`, `useProducts`) aux appels directs dans les composants
