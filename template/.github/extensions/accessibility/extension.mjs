// Extension: accessibility
// Audit d'accessibilité WCAG 2.2 Level AA sur le frontend React/CSS vanilla

import { joinSession } from "@github/copilot-sdk/extension";
import { readdir, readFile } from "node:fs/promises";
import { join, extname, relative } from "node:path";
import { existsSync } from "node:fs";

async function collectFrontendFiles(dir, collected = []) {
    if (!existsSync(dir)) return collected;
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isDirectory() && !["node_modules", "dist", ".git", "__tests__"].includes(entry.name)) {
            await collectFrontendFiles(fullPath, collected);
        } else if (entry.isFile() && [".jsx", ".tsx", ".js", ".ts"].includes(extname(entry.name))) {
            collected.push(fullPath);
        }
    }
    return collected;
}

const session = await joinSession({
    hooks: {
        onSessionStart: async () => {
            return {
                additionalContext:
                    "L'extension a11y est active. Tu peux lancer un audit WCAG 2.2 Level AA " +
                    "avec l'outil `a11y_audit`. Cet outil lit le code source frontend et " +
                    "retourne les fichiers à analyser avec leur contenu.",
            };
        },
    },
    tools: [
        {
            name: "a11y_audit",
            description:
                "Lance un audit d'accessibilité WCAG 2.2 Level AA sur le frontend React/CSS vanilla. " +
                "Lit le code source de src/ et retourne le contenu des fichiers à auditer " +
                "(pages, composants, composants UI, i18n). À utiliser en début d'audit a11y pour " +
                "fournir le code source à analyser.",
            parameters: {
                type: "object",
                properties: {
                    focus: {
                        type: "string",
                        description:
                            "Sous-dossier optionnel à cibler (ex: 'pages', 'components', 'components/ui'). " +
                            "Par défaut, analyse tout src/.",
                    },
                },
            },
            skipPermission: true,
            handler: async (args) => {
                const cwd = process.cwd();
                const baseDir = args.focus
                    ? join(cwd, "src", args.focus)
                    : join(cwd, "src");

                if (!existsSync(baseDir)) {
                    return `Dossier introuvable : ${baseDir}`;
                }

                const files = await collectFrontendFiles(baseDir);
                if (files.length === 0) {
                    return `Aucun fichier JS/JSX/TS/TSX trouvé dans ${baseDir}`;
                }

                const MAX_FILES = 40;
                const toRead = files.slice(0, MAX_FILES);
                const results = [];

                for (const filePath of toRead) {
                    try {
                        const content = await readFile(filePath, "utf-8");
                        const relPath = relative(cwd, filePath);
                        results.push(`\n${"=".repeat(60)}\n📄 ${relPath}\n${"=".repeat(60)}\n${content}`);
                    } catch {
                        results.push(`[Erreur lecture: ${filePath}]`);
                    }
                }

                const header =
                    `Audit a11y — ${toRead.length} fichier(s) collecté(s)` +
                    (files.length > MAX_FILES ? ` (${files.length - MAX_FILES} fichier(s) ignoré(s))` : "") +
                    "\n\nAnalyse ces fichiers selon WCAG 2.2 Level AA (catégories : structure/sémantique, " +
                    "clavier/focus, contrôles/labels, formulaires, modals/menus, images/icônes, " +
                    "contrastes, responsive, high-contrast). Pour chaque finding : fichier:ligne, " +
                    "critère WCAG, description, recommandation React/CSS vanilla.\n";

                return header + results.join("\n");
            },
        },
        {
            name: "a11y_check_file",
            description:
                "Lit un fichier frontend spécifique pour l'audit d'accessibilité. " +
                "Utile pour approfondir l'analyse d'un fichier particulier.",
            parameters: {
                type: "object",
                properties: {
                    path: {
                        type: "string",
                        description: "Chemin relatif du fichier à lire (ex: 'src/pages/HomePage.jsx')",
                    },
                },
                required: ["path"],
            },
            skipPermission: true,
            handler: async (args) => {
                const fullPath = join(process.cwd(), args.path);
                if (!existsSync(fullPath)) {
                    return `Fichier introuvable : ${args.path}`;
                }
                try {
                    const content = await readFile(fullPath, "utf-8");
                    return `📄 ${args.path}\n${"=".repeat(60)}\n${content}`;
                } catch (err) {
                    return `Erreur lecture ${args.path}: ${err.message}`;
                }
            },
        },
    ],
});
