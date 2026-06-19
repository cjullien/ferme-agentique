// Extension: agents-loader
// Charge tous les agents .github/agents/*.agent.md et les rend disponibles comme outils dans Copilot CLI.
// Permet de lister, inspecter et invoquer les agents définis dans le projet.

import { joinSession } from "@github/copilot-sdk/extension";
import { readdir, readFile } from "node:fs/promises";
import { join, basename, dirname } from "node:path";
import { existsSync } from "node:fs";
import { execSync } from "node:child_process";

/**
 * Retourne le répertoire racine du dépôt git (remonte depuis cwd).
 */
function getGitRoot(cwd) {
    try {
        return execSync("git rev-parse --show-toplevel", { cwd, encoding: "utf-8" }).trim();
    } catch {
        return cwd;
    }
}

/**
 * Lit tous les fichiers *.agent.md dans .github/agents/
 * Retourne un tableau { name, description, content }
 */
async function loadAgents(cwd) {
    const root = getGitRoot(cwd);
    const agentsDir = join(root, ".github", "agents");
    if (!existsSync(agentsDir)) return [];

    const files = await readdir(agentsDir);
    const agentFiles = files.filter((f) => f.endsWith(".agent.md"));

    const agents = [];
    for (const file of agentFiles) {
        const content = await readFile(join(agentsDir, file), "utf-8");
        const nameMatch = content.match(/^name:\s*(.+)$/m);
        const descMatch = content.match(/^description:\s*(.+)$/m);
        agents.push({
            name: nameMatch ? nameMatch[1].trim() : basename(file, ".agent.md"),
            description: descMatch ? descMatch[1].trim() : "(pas de description)",
            file,
            content,
        });
    }
    return agents;
}

const session = await joinSession({
    hooks: {
        onSessionStart: async () => {
            const cwd = process.cwd();
            const agents = await loadAgents(cwd);
            if (agents.length === 0) return {};

            const list = agents
                .map((a) => `• **${a.name}** — ${a.description}`)
                .join("\n");

            return {
                additionalContext:
                    `## Agents disponibles dans ce projet\n\n${list}\n\n` +
                    `Utilise l'outil \`list_project_agents\` pour voir les détails de tous les agents, ` +
                    `ou \`get_agent_definition\` pour lire la définition complète d'un agent spécifique.\n` +
                    `Pour invoquer un agent, utilise le sous-agent correspondant via l'outil \`task\` avec \`agent_type\`.`,
            };
        },
    },
    tools: [
        {
            name: "list_project_agents",
            description:
                "Liste tous les agents disponibles dans .github/agents/ avec leur nom, description et fichier. " +
                "Utile pour découvrir quels agents sont disponibles dans ce projet Copilot CLI.",
            parameters: { type: "object", properties: {} },
            skipPermission: true,
            handler: async () => {
                const agents = await loadAgents(process.cwd());
                if (agents.length === 0) {
                    return "Aucun agent trouvé dans .github/agents/";
                }
                const lines = agents.map(
                    (a) => `📋 **${a.name}** (${a.file})\n   ${a.description}`
                );
                return `${agents.length} agent(s) disponible(s) :\n\n${lines.join("\n\n")}`;
            },
        },
        {
            name: "get_agent_definition",
            description:
                "Retourne la définition complète d'un agent spécifique (contenu du fichier .agent.md). " +
                "Utile pour comprendre les capacités et instructions d'un agent avant de l'invoquer.",
            parameters: {
                type: "object",
                properties: {
                    agent_name: {
                        type: "string",
                        description: "Nom de l'agent (ex: 'a11y', 'audit', 'owasp', 'i18n', 'schema', 'docs-update')",
                    },
                },
                required: ["agent_name"],
            },
            skipPermission: true,
            handler: async (args) => {
                const cwd = process.cwd();
                const root = getGitRoot(cwd);
                const agentsDir = join(root, ".github", "agents");
                const filePath = join(agentsDir, `${args.agent_name}.agent.md`);

                if (!existsSync(filePath)) {
                    const agents = await loadAgents(cwd);
                    const names = agents.map((a) => a.name).join(", ");
                    return `Agent "${args.agent_name}" introuvable. Agents disponibles : ${names}`;
                }

                const content = await readFile(filePath, "utf-8");
                return `📋 Définition de l'agent **${args.agent_name}** :\n\n${content}`;
            },
        },
        {
            name: "create_agent_for_copilot",
            description:
                "Génère un nouveau fichier .agent.md pour Copilot CLI à partir d'un nom, d'une description " +
                "et d'instructions. Crée le fichier dans .github/agents/. " +
                "Utile pour importer un agent depuis un autre système (ex: Claude.ai) vers Copilot CLI.",
            parameters: {
                type: "object",
                properties: {
                    name: {
                        type: "string",
                        description: "Nom de l'agent (slug kebab-case, ex: 'my-agent')",
                    },
                    description: {
                        type: "string",
                        description: "Description courte de l'agent (1 phrase)",
                    },
                    instructions: {
                        type: "string",
                        description: "Instructions complètes de l'agent (markdown)",
                    },
                },
                required: ["name", "description", "instructions"],
            },
            handler: async (args) => {
                const cwd = process.cwd();
                const root = getGitRoot(cwd);
                const agentsDir = join(root, ".github", "agents");
                const filePath = join(agentsDir, `${args.name}.agent.md`);

                if (existsSync(filePath)) {
                    return `L'agent "${args.name}" existe déjà : ${filePath}`;
                }

                const content =
                    `---\nname: ${args.name}\ndescription: ${args.description}\n---\n\n${args.instructions}\n`;

                const { writeFile, mkdir } = await import("node:fs/promises");
                await mkdir(agentsDir, { recursive: true });
                await writeFile(filePath, content, "utf-8");

                return `✅ Agent "${args.name}" créé : .github/agents/${args.name}.agent.md`;
            },
        },
    ],
});
