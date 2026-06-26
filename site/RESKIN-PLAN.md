# site/index.html — Re-skin Plan (cohort token page → Dr. Mineral canon teaser)

**Decision D is locked: the page leads the public launch.** The current `index.html` is the **Lab Reward Token (UNL/cohort)** page and is an active **firewall + personal-IP risk** — it must be re-skinned before it represents the universe. This plan keeps the *tech shell*, replaces *all cohort content*.

## What's there now (audited)
- `<title>`: "Lab Reward Token — UNL SOC Cybersecurity Reward Research"
- Off-canon framing density: **token ×34, reward ×28, UNL ×14, cohort ×13, chain ×7, blockchain ×3**, names a cohort teammate (Raul Ochoa), "eight-session arc," "Tokenomics research," "attributable repository."
- Tech shell worth keeping: Three.js hero, starfield, and a RAF state-machine squirrel that wanders page elements (walk / hang / boo), with **8 keyed frames baked in as base64**.

## Re-skin scope
**Replace (all of it — this is the firewall):**
1. `<title>` + meta → "The Dr. Mineral Universe" (+ teaser description; no UNL/SOC/token terms anywhere).
2. Every section: drop Token / Reward / Tokenomics / Blockchain / Solidity / cohort / UNL / "eight-session arc" / team-roster / repository-attribution copy. Remove the teammate name and any UNL identifiers.
3. Hero H1 → lead with **Dr. Mineral + discovery**, not a product. e.g. *"Beneath an ordinary campus, a hidden laboratory of curious minds."* Subhead teases the universe; tagline *"I don't collect treasure. I collect discoveries."*
4. Sections → canon teaser blocks: **the double life**, **the Hidden Laboratory**, **contribution over wealth / discovery over competition**, **coming: Book I**. Educational + hopeful tone.
5. CTA → drop "Curious about the pilot?" (cohort funnel). Replace with a low-key universe CTA (follow / "Book I in progress" / email capture) — **no token, no pilot, no UNL**.

**Keep (the shell):**
- Three.js hero, starfield, RAF wandering-squirrel state machine, responsive layout, dark-premium aesthetic.

**Verify (canon-critical):**
- ⚠️ **Confirm the 8 baked-in base64 frames are all CLEAN (no chain).** Per `../docs/04_asset-manifest.md` the wander set is walk/hang/boo; any CHAIN frame must be swapped for a CLEAN keyed equivalent (`../assets/keyed/`). A chained squirrel on the public page = the off-canon blockchain pun shouting on the universe's first surface.
- Grep the final file for `token|reward|UNL|cohort|blockchain|chain|solidity|pilot` → must return **0** before it ships.

## Blocking asset
- The hero needs the **clean dignified portrait** that does not yet exist (`../docs/05_hero-portrait-brief.md`). The action frames can't carry the hero slot. **Queued as a paste-ready brief** — page hero stays a placeholder until that render is keyed into `../assets/keyed/`.

## Sequence
1. Generate + key the hero portrait (asset gate).
2. Branch; rewrite content top-to-bottom; swap any chain frames.
3. Grep-gate for off-canon terms; visual check the wandering squirrel is clean.
4. Commit "Re-skin landing page to Dr. Mineral canon teaser (retire cohort token page)."
