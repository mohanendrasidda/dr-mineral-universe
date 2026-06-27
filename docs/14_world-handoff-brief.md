# Handoff Brief — "The Lab / The Chain" interactive 3D world

A self-contained brief for an analyzing agent. Goal: get back a concrete, prioritized plan + exact specs (techniques, materials, lighting, assets, references) to reach the target below at the highest quality the medium allows. Everything needed is in this doc.

---

## 1. What it is
An **interactive 3D world that runs in a web browser** (Three.js / WebGL, 60fps real-time). It's the public face of a real project: a **university cybersecurity lab's blockchain reward system** — a coin that pays out for genuine security work (bugs found, audits written, protocols hardened). The world dramatizes that as a hidden underground lab where contribution is **mined → forged onto a chain → recorded in a ledger → kept in a vault → guarded**. A campus squirrel, "Dr. Mineral," is its quiet keeper. The visitor explores it; it does not perform for them.

## 2. The visual & experience target (the most important section)
**Realistic 3D. As real as the medium allows. NOT Pixar, NOT anime, NOT cartoon.** And above all: **mysterious, ancient, hidden, underground — a place that has been quietly working in the dark for longer than anyone above is alive.** The feeling to manufacture: *"I have discovered something extraordinary and secret, and it has been here all along."* Wonder and reverence, not fun-and-antics.

**Tone lock:**
- Ancient, worn, real (rough wet stone, aged brass, glass crystal, molten metal) — never freshly-built or game-like.
- Vast and deep — a city falling away into darkness, not a small flat arena.
- Dim — light is rare, precious, pooled warmly in a deep dark; most of the frame is shadow.
- Quietly alive — figures work slowly, with weight and purpose; labor and ritual, never bouncy.
- Mysterious — always more in the dark than you can see; sealed ways, deeper levels, a hum with no clear source.

**Explicit DON'T (these made the prototype read as a "noob-built comedy game"):** bright/flat even lighting · cartoon bounce/hops · jokey antics · fast jittery motion · arcade HUD clutter · cute idle wiggles · saturated toy colors.

## 3. Story & scenes (the spatial sequence)
- **Arrival (the descent):** the visitor crosses *into* the lab — a single shaft of pale daylight falls through a hole in the rock far overhead (the way it was found); you come down into warmth, gold, and scale. Reveal gradually out of darkness; do not show everything at once.
- **First sight (the central cavern):** from a high ledge, an enormous warm-gold underground space, galleries and bridges of dark stone falling into the deep, hundreds of lamps receding into shadow. This shot must make the viewer stop and stare.
- **The five rites (zones, each a mood not a "station"):**
  1. **The Mines** — figures working a glowing crystal seam in deep shadow; slow, heavy, rhythmic labor.
  2. **The Foundry** — a great forge breathing like a slow heart, deep orange light pulsing up the walls, sparks falling slowly; old, holy industry.
  3. **The Ledger** — the quietest, most reverent place; a long chain of soft light running back into the dark, each link a kept contribution; almost a shrine.
  4. **The Vault** — deep blue, cold, silent; a single guarded treasure under light.
  5. **The Watch** — eyes in the shadow at the edges; stillness, vigilance, the sense of being kept safe by something patient and unseen.
- **The keeper (Dr. Mineral):** small, still, watchful at the hub; notices the visitor, does nothing more. Warmth through stillness, not bits.

## 4. Hard technical constraints (read before recommending)
- **Medium:** real-time browser WebGL (Three.js). NOT an offline film renderer. No path-tracing/RenderMan-level GI. Must hold ~60fps on a laptop.
- **Pixar-level is impossible here** and is not the goal; "as real as a real-time browser scene can be" is.
- **Free / low-cost only.** No paid software assumed. Available & working: free **image-to-3D** from the terminal (TripoSR / TRELLIS via HuggingFace `gradio_client`) which makes **static `.glb` props** well, but outputs **un-riggable triangle meshes** — useless for animated characters, fine for rocks/crystals/machinery.
- **Characters are the limit:** realistic *animated* 3D creatures need modeling+rigging (an artist / paid pipeline) that free tools can't do. **Chosen direction: keep figures small, distant, shadowed — silhouettes/forms at work in the gloom** — which both sidesteps the wall and *deepens* the mystery. Detailed realistic character models are an optional later paid step.
- **2D image generation** is available via the Gemini/"Nano Banana" app (the operator generates and hands over PNGs) — good for textures, set-dressing, sprite frames, concept refs.

## 5. Current state (what exists)
A working Three.js scene: an enclosed cavern (cylinder walls, a dome ceiling, stalactites, a shaft of light, glass crystals, fog), 5 zones laid out in a ring with point-lights, a metallic chain that grows as "blocks" are forged, animated 2.5D sprite figures (a keeper + miners + haulers on work loops), UnrealBloom + ACES tone mapping + soft shadows + env-map reflections + a CSS vignette/grain. It currently reads too clean/primitive (smooth cylinder geometry) and, until a recent re-tone, too bright/bouncy. The geometry is the weakest link for realism.

## 6. THE ASK (what to deliver back)
Analyze the **gap between Section 2's target and Section 5's current state**, respecting Section 4's constraints, and return:
1. **A gap analysis** — exactly why the current scene falls short of "realistic + mysterious," ranked by visual impact.
2. **The exact technical approach** to close it in Three.js, concretely: geometry strategy (e.g., how to get real cave rock — noise displacement, sculpted/sourced meshes, trim sheets), **PBR material specs** (albedo/roughness/normal/AO for wet stone, brass, molten metal, glass crystal — including where to get free textures, e.g. Poly Haven, and exact map usage), **lighting setup** (key/fill/practical lamps, the shaft as god-rays/volumetrics, exposure, shadow settings), **post-processing** (bloom params that don't clip, optional SSAO/DoF/color-grade), **fog/depth** for the "city falling away," and **performance budget** notes.
3. **An exact asset list** — every texture, prop `.glb`, and reference image needed, with how to obtain each for free (image-to-3D prompt, free-texture source, or Gemini 2D prompt), and naming.
4. **Reference direction** — named films/games/artstations that hit this exact "real, dim, mysterious, ancient underground" register to target.
5. **A prioritized build plan** — ordered steps, biggest-quality-jump first, each independently shippable.

Be specific and actionable enough that an engineer could execute it directly. Flag anything in the target that is genuinely unreachable in real-time browser WebGL and give the closest achievable substitute.
