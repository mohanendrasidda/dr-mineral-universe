# LOAD FIRST — two ways to stand up the Dr. Mineral project

Projects/repos can't auto-import from each other — you add these files yourself. Pick ONE path.

## Path A — Claude Code (recommended for building)
Best home for the repo + website + asset pipeline + git-tracked canon.
1. Unzip this bundle into a new empty folder.
2. `cd` into it, run `claude`.
3. Open `CLAUDE-CODE-KICKOFF.md`, paste its prompt block as your first message. Done — it scaffolds everything.
`CLAUDE.md` is already the repo's persistent memory; the kickoff prompt does the rest.

## Path B — claude.ai project (good for pure ideation/canon chat)
1. New project → **The Dr. Mineral Universe**.
2. Paste `docs/00_PROJECT-INSTRUCTIONS-v2.md` into **custom instructions** (this is text in the instructions box, NOT a file).
3. Add as **project files**: `docs/01`, `docs/02`, `docs/03`, `docs/04`, `docs/05`.
4. Do NOT dump all 34 PNGs into project knowledge — it clutters context and the model can't use them well there. The asset manifest (`docs/04`) already tells it what exists. Bring specific images into a conversation only when working on them visually.
5. First message: "Read the Bible and Book I foundation. Lock decisions A–E, then draft Chapter 1's opening image. Tell me what art you need as we go."

## What's a project file vs. what's not
| Item | claude.ai project | Claude Code |
|---|---|---|
| `00_PROJECT-INSTRUCTIONS-v2.md` | paste into custom instructions | (CLAUDE.md covers this) |
| `CLAUDE.md` | not used | repo root — auto-loaded |
| `docs/01`–`05` | project files | in `docs/` |
| 34 PNGs | keep OUT of project knowledge; load per-chat | `assets/raw/` |
| `index.html` | load per-chat when editing | `site/index.html` |

## Bundle contents
```
README-LOAD-FIRST.md
CLAUDE.md                       ← Claude Code repo memory
CLAUDE-CODE-KICKOFF.md          ← the single paste prompt
docs/00_PROJECT-INSTRUCTIONS-v2.md
docs/01_universe-bible-v1.md
docs/02_canon-registry.md
docs/03_book-one-foundation.md
docs/04_asset-manifest.md
docs/05_hero-portrait-brief.md
assets/  (34 PNGs + index.html)
```
