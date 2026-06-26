# Claude Code — kickoff prompt

Unzip the bundle into a new empty folder, `cd` into it, run `claude`, and paste the block below as your first message. That's the whole setup.

---

You are setting up a new creative repo for **The Dr. Mineral Universe**, an original transmedia IP. The folder already contains `CLAUDE.md`, a `docs/` folder, and an `assets/` folder with 34 PNG renders + `index.html`.

Do this, in order:

1. **Read first:** `CLAUDE.md`, then every file in `docs/` (the Bible is canon — `docs/01_universe-bible-v1.md`). Don't skip the asset manifest or the firewall/canon rules.

2. **Scaffold the repo** without destroying anything:
   - Create `canon/`, `book-one/`, `site/`, `assets/raw/`, `assets/keyed/`, `.claude/skills/`.
   - Move `assets/index.html` → `site/index.html`. Move the 34 PNGs → `assets/raw/`.
   - Delete the two exact duplicates (`…c3ihwj…_1.png`, `…fed80p…_1.png`).
   - Split `docs/02_canon-registry.md` into living files under `canon/` (`characters.md`, `departments.md`, `lore-ledger.md`, `visual-canon.md`), seeded from the current content.
   - `git init`, sensible `.gitignore`, initial commit "Scaffold Dr. Mineral Universe repo."

3. **Copy in the skills** if I have them locally (ai-asset-generation, ai-render-keying, sprite-animation, immersive-html) into `.claude/skills/`. If not present, list them so I can add them.

4. **Don't write story prose yet.** First, surface the open creative decisions A–E from `docs/03_book-one-foundation.md` and ask me to lock them — especially (A) the first major scientific mystery. Give me your recommendation on each, but wait for my call.

5. **Then** propose: a Book I one-page synopsis → chapter outline, and a plan to re-skin `site/index.html` from the cohort token page to a canon Dr. Mineral teaser.

Throughout: obey the canon, tone, blockchain-invisible, chain-is-off-canon, personal-IP, and firewall rules in `CLAUDE.md`. When the work needs art that doesn't exist, stop and hand me a paste-ready generation brief (consistency anchor + flat keyable background) instead of working around it. The first asset I already want queued is the hero portrait in `docs/05_hero-portrait-brief.md`.

Start with step 1 and report what you found before scaffolding.
