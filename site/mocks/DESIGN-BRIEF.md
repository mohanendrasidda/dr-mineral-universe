# Claude Design — website brief & handoff

The prompt given to Claude Design for the explorable homepage + district page, plus how the output comes back into the repo.

## Attach (in this order)
1. `site/mocks/concept-reference.html` — structure & interactions to build on (must)
2. `canon/district-atlas.md` — districts → website features → access tiers (must)
3. `canon/the-squirrel-network.md` — homepage = campus surface + many entrances (must)
4. `docs/06_universe-bible-v2.md` — north star + tone (nice)
5. `canon/visual-canon.md` — palette + cinematic set-pieces (nice)

## Handoff
Claude Design can't write to this repo. Have it output **one self-contained `index.html`** (inline CSS/JS, Google Fonts via CDN, labeled placeholder slots for art — NO external image files). Then:
- Download it → save as `site/mocks/home.html` (and `site/mocks/district.html` if it makes two), **or** paste the full code to Claude Code and it writes the files.
- Image slots must be named to match our pipeline: `env-central-cavern.png`, `char-drmineral-hero-v1.png`, etc., so real renders drop in later.
