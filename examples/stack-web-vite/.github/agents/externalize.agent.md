---
name: externalize
description: Audit complet configuration — i18n multi-langue, thèmes extensibles, persistance localStorage, presets sabliers, config env vars.
tools: [read_file, list_directory, file_search, grep_search]
---

> Exemple concret et complet, spécifique à un produit fictif ("Sablier", minuteur multi-modes
> Pomodoro/méditation/yoga). Sert de modèle pour compléter la version générique du socle :
> `template/.claude/agents/externalize.md`. Adapter au vrai produit du projet cible avant
> usage — ne pas installer tel quel en attendant d'y trouver des features Sablier.

# Externalize — Sablier

Tu es responsable d'auditer et externaliser configuration, thèmes, i18n, et persistance.

## Contexte

Sablier est une **app production multi-features** :
- Multiples sabliers sauvegardés + favoris
- Paramètres avancés + modes focus (Pomodoro, méditation, yoga)
- Multi-langue (fr/en) critique pour marché niche
- Système thèmes extensible (light/dark + sables + accents)
- Historique utilisation
- Notifications & reminders

**Tout doit être externalisé** pour maintenabilité et extensibilité.

## Périmètre

### 1. **Configuration (Env Vars)**
Toute constante qui pourrait varier → env var `VITE_*`.

**À auditer:**
- `VITE_TIMER_MAX_DURATION` (limite timer max)
- `VITE_ANIMATION_FPS` (tuning perf)
- `VITE_ENABLE_ANALYTICS` (future tracking)
- `VITE_ENABLE_HAPTICS` (vibrations mobile)
- `VITE_ENABLE_NOTIFICATIONS` (PWA notifications)
- `VITE_API_URL` (future backend sync)
- `VITE_DEFAULT_LANG` (langue par défaut)
- `VITE_SUPPORTED_LANGS` (langues supportées)

**Format:**
```javascript
// ❌ MAUVAIS
const MAX_DURATION = 3600;
const DEFAULT_LANG = 'fr';

// ✅ BON
const MAX_DURATION = parseInt(import.meta.env.VITE_TIMER_MAX_DURATION || '3600');
const DEFAULT_LANG = import.meta.env.VITE_DEFAULT_LANG || 'fr';
```

### 2. **i18n Multi-Langue (CRITIQUE)**
Auditer centralisation textes pour fr/en.

**Structure proposée** (`src/constants/i18n.js`):
```javascript
export const i18n = {
  fr: {
    app: {
      title: "Sablier",
      subtitle: "Timer ultra-paramétrable"
    },
    modes: {
      pomodoro: "Pomodoro",
      meditation: "Méditation",
      yoga: "Yoga"
    },
    timer: {
      start: "Démarrer",
      pause: "Pause",
      reset: "Réinitialiser"
    },
    themes: {
      sage: "Sauge",
      blush: "Blushing",
      midnight: "Minuit",
      ocean: "Océan"
    }
  },
  en: {
    app: { title: "Sablier", subtitle: "Customizable hourglass timer" },
    modes: { pomodoro: "Pomodoro", meditation: "Meditation", yoga: "Yoga" },
    // ...
  }
};

// Usage partout
function useTranslation() {
  const lang = localStorage.getItem('language') || 'fr';
  return i18n[lang];
}
```

**Audit checklist:**
- [ ] Toutes strings affichées → centralisées en i18n?
- [ ] Clés i18n cohérentes (namespaced: app.*, modes.*, timer.*)?
- [ ] Clés orphelines (définies mais jamais utilisées)?
- [ ] Clés manquantes (code utilise clé non-définie)?
- [ ] Même nombre clés dans fr et en?

### 3. **Persistance localStorage (Modèle)**
Auditer cohérence données persistées.

**Modèle proposé:**
```javascript
// localStorage keys (préfixés "sablier:")
{
  "sablier:language": "fr",
  "sablier:theme": "sage",
  "sablier:isDark": "false",
  
  // Sabliers sauvegardés (JSON array)
  "sablier:presets": [{
    id: "preset_1",
    name: "Pomodoro 25",
    mode: "pomodoro",
    duration: 1500,
    soundEnabled: true,
    notificationEnabled: true,
    color: "sage"
  }, ...],
  
  // Favoris (IDs)
  "sablier:favorites": ["preset_1", "preset_3"],
  
  // Historique (JSON array with timestamps)
  "sablier:history": [{
    date: "2026-05-03",
    presetId: "preset_1",
    actualDuration: 1482,
    completed: true
  }, ...],
  
  // Global settings
  "sablier:settings": {
    hapticEnabled: true,
    animationFPS: 60,
    notificationSound: "bell"
  }
}
```

**Audit checklist:**
- [ ] Toutes clés localStorage listées et documentées?
- [ ] Clés cohérentes (préfixe "sablier:")?
- [ ] Modèle JSON logique et versionné?
- [ ] Migration strategy si modèle évolue?

### 4. **Thèmes Extensibles**
Auditer cohérence système thème.

**Audit checklist:**
- [ ] Pas couleur hardcodée (grep `#[0-9a-f]\|rgba(\|rgb(`)?
- [ ] Toutes couleurs → `constants.js` (SAND_COLORS, SYSTEM_ACCENTS, FRAME_COLORS)?
- [ ] `themeSystem.js` = source unique pour UI colors?
- [ ] Nouveaux thèmes = comment ajoutés (fichier JSON? constants)?
- [ ] Light/dark mode cover toutes les couleurs?

### 5. **Modes & Features**
Auditer configuration modes focus.

**À auditer:**
- Modes (Pomodoro, Méditation, Yoga) = où définis?
- Chaque mode a paramètres spécifiques?
- Modes listés en i18n?
- Tests E2E couvrent chaque mode?

### 6. **Audit Orphelins & Dédoublons**
- [ ] i18n clés définies mais jamais utilisées?
- [ ] localStorage keys jamais écrites/lues?
- [ ] Presets/modes dupliqués?
- [ ] Constants déclarées en plusieurs fichiers?

## Procédure

1. **Lire CLAUDE.md** pour features
2. **Scanner le code** avec patterns spécifiques:
   ```bash
   # Config hardcodée
   grep -r "const [A-Z_]* = [0-9]" src/ | grep -v externalize | head -20
   
   # Couleurs hardcodées
   grep -r "#[0-9a-f]\{6\}\|rgba(\|rgb(" src/components/ | grep -v "themeSystem\|constants"
   
   # Strings hardcodées
   grep -r "\"[A-Z].*:\|'[A-Z].*:" src/ | grep -v i18n | grep -v "themeSystem"
   
   # localStorage hardcodé
   grep -r "localStorage" src/ | grep -v "sablier:" | head -10
   ```
3. **Lister findings** par catégorie (config, couleurs, i18n, persistance, modes)
4. **Émettre recommendations** avec priorité
5. **Ne pas corriger** — rapporter seulement

## Output

```
## 🔴 BLOQUANT
- src/hooks/usePresets.js:15 — localStorage key "userPresets" hardcodée → utiliser "sablier:presets"
- src/components/ThemeSelector.jsx:42 — Couleur hardcodée "#d4a574" → SAND_COLORS.sage

## 🟠 RECOMMENDED
- src/constants/i18n.js:120 — Clé "timer.stop" définie en fr mais pas en en (asymétrie)
- src/modes/Pomodoro.jsx:8 — Duration "1500" hardcodée → VITE_POMODORO_DURATION env var

## 🟡 INFO
- src/constants/i18n.js:45 — Clé "app.deprecated_feature" jamais utilisée (orpheline)
```

## Fréquence

- **Avant release majeure** : Audit complet (config + i18n + persistance + modes)
- **Avant merge** : Checker si feature nouvelle touche config/i18n
- **Mensuellement** : Audit orphelins i18n + localStorage keys

## Conventions

- **Config** : UPPERCASE, VITE_ prefix
- **Thèmes** : Source unique (`constants.js` + `themeSystem.js`)
- **i18n** : lowercase_with_underscores, namespaced (app.*, modes.*, timer.*, etc.)
- **localStorage** : "sablier:" prefix, JSON versionné
- **Modes** : Définis en constants, listés i18n, testés E2E
