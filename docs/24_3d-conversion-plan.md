# World → 3-D conversion plan

**Goal:** move the world from "3-D hero + 2-D billboard cast + primitive props" to a **cohesive 3-D look**. The guiding rule (per review): **don't ship half-billboard / half-3-D** — convert the whole *cast* first, then upgrade props.

## Pipelines we'll use (per asset type)
- **Biped characters (squirrels):** photo → InstantMesh/**Hunyuan3D-2** → Mixamo auto-rig (humanoid) → integrate. (What Dr. Mineral uses.)
- **Non-biped animals (bird, tortoise):** Mixamo can't rig these → use **sourced rigged+animated GLBs** (CC0/CC-BY), recolored to our characters. Drop-in.
- **Props:** **sourced CC0 GLB props** (direct download where possible) or improved procedural geometry. Swap the primitive/"origami" props.
- **Environment** (well, arches, chain, coins, lamps): mostly keep; light-touch polish.

## Asset inventory + status

### Characters (do these FIRST — cohesion)
| Character | Plan | Who | Status |
|---|---|---|---|
| **Dr. Mineral** (squirrel) | placeholder live; **re-rig on the Hunyuan mesh** to fix spike + face | me (rig), quota | ⏳ Hunyuan queued (GPU quota ~reset) |
| **Tally** (magpie) | sourced **rigged Sparrow** GLB → recolor to magpie (black/white/blue) | user downloads → me integrate | 🔗 link pending (research agent) |
| **Vellum** (tortoise) | sourced **rigged tortoise** GLB → decimate + warm-tint | user downloads → me integrate | 🔗 link pending |
| **Workers** (miners/haulers) | **clone Dr. Mineral's rig** + a **mining** clip | user grabs a Mixamo "mining" anim → me | ⏳ after Dr. Mineral |
| **Assistant** (teal wisp) | already 3-D geometry | — | ✅ keep (maybe refine) |

### District props (after the cast)
| District | Current (primitive) | Target |
|---|---|---|
| **Mines** | "origami" octahedron ore | a **glowing crystal/ore cluster** GLB |
| **Foundry** | box forge + ember | an **anvil + forge/furnace** GLB |
| **Ledger** | thin cylinder pillar | a carved **stone obelisk/pillar** GLB |
| **Vault** | cylinder pedestal + gem | pedestal + a **faceted gem** GLB |
| **Watch** | torus "eye" | a sentinel motif (keep stylized, or a carved eye) |
| **Notice board** ("THE WORK") | flat panel | a framed carved-stone tablet (light reframe) |
| **set-dressing** | a few boxes | **crates/barrels/lanterns** GLBs |

*(The research agent is finding direct-download CC0 GLBs — ideally one consistent "fantasy/dungeon" kit covering several props at once.)*

## Order of work
1. **Infra:** a small **GLB model-registry loader** in the world (so every model — char or prop — drops in with scale/recolor/anim wiring in one place).
2. **Cast → 3-D:** Tally, Vellum, workers (kills the fidelity split). *Needs the user's downloads.*
3. **District hero props:** crystal, anvil, gem, pillar (CC0). *I can source + integrate.*
4. **Dr. Mineral Hunyuan re-rig** (when quota resets).
5. **Polish:** consistent lighting/shadows; retire leftover billboards.

## Who does what
- **Me:** build the loader/registry; source + integrate CC0 props (direct download); integrate + recolor every GLB; wire animations/states; retire billboards.
- **You:** download the **rigged character GLBs** (Sketchfab needs a free login) — Tally(bird) + Vellum(tortoise); optionally a **Mixamo "mining"** clip for workers; run the **Hunyuan** mesh when the GPU quota resets (or ping me).
- **Blocked:** Dr. Mineral's crisp re-rig (Hunyuan GPU quota, ~a day).

## Honest scope
This is **several work sessions**, not one. Cohesion-first ordering means the world will briefly look mixed until the cast is fully 3-D — that's expected. The free-asset path lands us at **competent stylized-game tier**, not film tier; the ceiling is asset quality, which sourced rigged models + the Hunyuan mesh raise as far as free goes.
