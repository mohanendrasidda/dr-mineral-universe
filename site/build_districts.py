#!/usr/bin/env python3
"""Generate one standalone district page per gallery, from canon.
Run: python3 site/build_districts.py  (writes site/districts/<slug>.html)
Shares the homepage's visual language. Image slots are named to the asset pipeline.
"""
import html, pathlib

OUT = pathlib.Path(__file__).parent / "districts"
OUT.mkdir(exist_ok=True)

ACCESS = {
    "public": ("PUBLIC", "#7fb069"),
    "members": ("MEMBERS", "#e0a541"),
    "restricted": ("RESTRICTED", "#c4553b"),
}

# keyed character portraits to feature on a district page: slug -> [(file, name, role)]
CHARS = {
    "contribution-registry": [
        ("char-vellum-v1.png", "Vellum", "Keeper of memory · tortoise"),
        ("char-tally-v1.png", "Tally", "Apprentice · magpie"),
    ],
}

def chars_block(slug):
    items = CHARS.get(slug)
    if not items:
        return ""
    figs = ""
    for fn, name, role in items:
        figs += (
            '<figure style="margin:0; text-align:center; width:250px;">'
            '<div style="position:relative; height:250px; display:flex; align-items:flex-end; justify-content:center;">'
            '<div style="position:absolute; bottom:14px; width:190px; height:62px; border-radius:50%; background:radial-gradient(ellipse, rgba(231,183,101,.2), transparent 70%);"></div>'
            f'<img src="../../assets/keyed/{fn}" alt="{html.escape(name)}" style="position:relative; max-height:250px; max-width:240px; object-fit:contain; filter:drop-shadow(0 14px 26px rgba(0,0,0,.55));">'
            '</div>'
            f'<figcaption><div style="font-family:\'Cormorant Garamond\',serif; font-size:25px; color:#f4e7d0; margin-top:8px;">{html.escape(name)}</div>'
            f'<div class="label" style="margin-top:4px;">{html.escape(role)}</div></figcaption>'
            '</figure>'
        )
    return (
        '<section style="max-width:900px; margin:0 auto; padding:24px 24px 0;">'
        '<div class="label" style="text-align:center; margin-bottom:26px;">THE KEEPERS</div>'
        f'<div style="display:flex; flex-wrap:wrap; gap:34px; justify-content:center;">{figs}</div>'
        '</section>'
    )

# slug, name, glow, access, lead, who(flaw), essence, feature, walkIn, makes, secret, cinematic
D = [
 ("contribution-registry","Contribution Registry","#9fc6e8","public",
  "Vellum · ancient tortoise — Keeper of memory, with apprentice Tally · magpie",
  "Vellum is so patient that conversations finish before he answers; Tally talks faster than she thinks and once re-shelved a century of records by colour.",
  "The district that remembers — every contribution honored, linked, never lost.",
  "Hall of Contributors · the ledger",
  "The quietest hall: no benches, no arguing — only long dim aisles and the soft endless ticking of brass-and-glass memory-machines, always turning. The smallest mouse's smallest correction turns its own small wheel, faithfully, long after the mouse is gone.",
  "Remembering itself — and since Book I, made as a chain: each keeper their own honored record, linked to the one before and the one after, so the many are kept as many, none blurred, none lost. The chain guards its own truth, and now keeps itself.",
  "The restored chain runs back past the founding — one faint link older than the laboratory itself. Who was keeping and passing on contribution before there was a lab?",
  "The threaded chain of light running back into the dark; a new contributor's star kindling overhead."),
 ("historical-archives","Historical Archives","#e0a85a","public",
  "Maddox · pack rat — Head of Archives",
  "Maddox cannot throw anything away — his office is an avalanche of 'important' scraps, and he narrates his own searches aloud.",
  "The deep memory of what it was like — the doubts and the courage behind the record.",
  "Documentation · research journals",
  "Warm, dim, close — a honeycomb of reading-cells worn into stone, shelves sagging with the patient weight of years, the dry-sweet smell of a great deal of old paper. Floating archive-lifts drift overhead, carrying journals to readers.",
  "They preserve and interpret — cross-reading old journals to recover lost context, teaching the lab to hear its own past correctly: that 'too many to name' was a bow, not a blank.",
  "Maddox keeps one cell locked: journals from the abandoned sectors that 'aren't ready to be read yet.'",
  "Floating archives drifting through honeyed light; a brown-inked founding page held to a blue lamp."),
 ("innovation-workshop","Innovation Workshop","#f08a3c","public",
  "Juniper \"June\" Ringtail · raccoon — Master Tinkerer",
  "June starts six projects per idea and finishes maybe one; when she and Dr. Mineral collaborate, something catches fire (usually fine, usually funny).",
  "Where ideas become prototypes — loud, messy, joyful. Home of the Wall of Noble Failures.",
  "Experiments · engineering blueprints",
  "Sparks, scaffolding, the smell of hot metal and sawdust, the clang-whirr-'aha!' rhythm of making. An assistant-bot misreads a blueprint and politely builds a chair upside down. A working prototype earns a small festival.",
  "Everything's first form: the motion-woken lamps, the drone prototypes, the early chain-machines. Failures are pinned with honor on the Wall — because failure is how the next thing works.",
  "June keeps a locked drawer of 'ideas too dangerous to finish yet.'",
  "A prototype working on the third try, the floor erupting; the Wall of Noble Failures."),
 ("chain-foundry","Chain Foundry","#f2a23e","members",
  "Master Castor · beaver — Chief Engineer of the Foundries",
  "Castor distrusts anything 'clever' — he'll rebuild a working machine three times to make it simpler, and he cannot give a short answer about load-bearing tolerances.",
  "Where the lab forges its trust-machines — the chain-of-trust, shown as craft, never a lecture.",
  "Live blockchain visualization",
  "Heat and rhythm. A great forge-reactor at the center pulses like a slow heart, throwing molten gold up the walls; the teams move in time to it. Order under pressure — every link tested, every join proven.",
  "The chain as physical, dependable infrastructure: each contribution-record forged into a link that holds the one before and is held by the one after, so the whole guards its own truth. You watch it being made.",
  "Castor has noticed the chain repairing itself when a link is damaged. He hasn't told anyone. He's not sure he built that.",
  "The forge-reactor pulsing like a living heart; a single link cooling from gold to dark."),
 ("sentinel-hall","Sentinel Hall","#d76a4a","members",
  "Commander Sasha · meerkat — Keeper of the Watch",
  "Sasha can't fully relax or delegate the last watch; she's learning, slowly, that a good system means she doesn't have to be the one awake.",
  "The Watch — posted sentinels who guard the city and sound the alarm before trouble arrives.",
  "Status · the watch (the lab's SOC)",
  "High galleries and clear sightlines, watchers posted at every approach, ears turned toward the dark. When all is well, a low steady all-clear hums through the hall; when it isn't, every head snaps up at once.",
  "They keep the city safe — watching the approaches, testing the gatehouses' identity-tokens, sounding the alarm before trouble arrives. Vigilance practiced as a civic art, never paranoia.",
  "Sasha logs every false alarm. Lately a few weren't false — and weren't on any threat she recognizes.",
  "A wall of glowing watch-screens; owls turning their heads in the dark; a security drone's quiet patrol arc."),
 ("robotics-division","Robotics Division","#5fc8a8","public",
  "Pip Sprocket · rat — Master of Mechanisms",
  "Pip over-personifies the machines — names them all, argues with them, and refuses to scrap a malfunctioning unit ('Gerald's just having a day').",
  "Where the machines come alive — miners, drones, and the well-meaning assistant-bots.",
  "Robotics showcase · meet-the-bots",
  "Whirring, clicking, the skitter of small mechanisms and the deep thrum of large ones. Mechanical mining squirrels file out through glowing crystal tunnels; journal-drones cross overhead; an assistant-bot earnestly creates a small, polite disaster.",
  "They refine the Workshop's rough prototypes into reliable working machines — the miners, the drones, the assistants that fetch and sort and try to help. Half the craft is listening to what a machine is doing wrong.",
  "One old assistant-bot, 'First,' predates Pip's records and occasionally says things no one programmed. Pip insists it's a glitch — and checks on it every night.",
  "Mining squirrels streaming through glowing crystal tunnels; journal-drones crossing the central cavern."),
 ("the-commons-and-bakery","The Commons & Bakery","#e8c06a","public",
  "Mrs. Bramwell · hedgehog — Keeper of the Table",
  "Gruff to the point of comedy, she fusses over everyone while insisting she isn't, and despairs of how Dr. Mineral keeps burning his toast.",
  "The heart of the table — warm bread, warm company, the whole city's gathering place.",
  "Community · the commons",
  "The smell reaches you three levels up: bread, butter, something sweet. Long worn tables, mismatched chairs, every species elbow to elbow. Gruff-sweet Mrs. Bramwell remembers exactly how everyone takes their tea.",
  "They feed the city and seat it together — the one hall where rank dissolves and a department head shares a bench with a first-day apprentice. The table, it turns out, is the real infrastructure.",
  "Mrs. Bramwell keeps one chair empty at the long table. She won't say for whom.",
  "Steam and warm light over a crowded table; the morning whistle waking the district."),
 ("ai-center","AI Center","#5aa8c8","members",
  "Professor Inkwell · octopus — Steward of the Minds",
  "Inkwell thinks in eight directions at once and rarely finishes a sentence out loud — by the time she speaks, her mind is three problems ahead.",
  "The calm hall of thinking machines — and the home of the assistant that guides you.",
  "The AI assistant room",
  "Cool, dim, and quiet — a hall of softly glowing minds, like lamps that are considering something. Inkwell's glass water-chamber casts rippling light across the walls. It hums and ponders where other districts clatter and forge.",
  "They tend the lab's reasoning helpers — the machines that sort the Registry, route the drones, and gently help you find what you're looking for. Inkwell's rule: a thinking machine should make you more curious, not less needed.",
  "Inkwell suspects the chain and her minds are starting to 'talk' in a pattern she didn't design. She is watching, fascinated and a little awed.",
  "Inkwell's glass water-chamber rippling light; rows of softly glowing pondering-minds."),
 ("educational-academy","Educational Academy","#e8b96a","public",
  "Madam Oona · elephant — Keeper of Patience",
  "Oona answers no question directly — she tells a wandering story and trusts you to find the answer inside it. (Dr. Mineral is, by her gentle assessment, 'a gifted scientist' at dancing.)",
  "Where the young are taught and the old keep learning — the lab's promise that no one is ever finished.",
  "Tutorials · learn · onboarding",
  "Warm classrooms carved in tiers of stone, full of light and chalk-dust and the particular happy noise of minds clicking on. Children of a dozen species learn beside grey-muzzled department heads brushing up on a new craft.",
  "They make the next generation able to contribute more than this one. Teaching is hands-on — you learn the Registry by walking its rows — and they run the gentle first descent for every newcomer.",
  "The Academy's oldest classroom has a lesson carved into its wall in a script no current teacher can read.",
  "Tiered stone classrooms in warm light; a child and a department head learning side by side."),
 ("codeworks-loom-hall","Codeworks — Loom Hall","#bcd86a","members",
  "Mistress Aran · spider — Master Weaver",
  "Aran cannot leave a finished weave alone — she'll unpick a working tapestry at midnight because she found 'a cleaner thread,' and speaks entirely in weaving metaphor.",
  "Where the lab weaves its software — repositories as living looms you can read top to bottom.",
  "The GitHub room · repositories",
  "A tall hall of great looms, each threading glowing logic into bright moving fabric — commits landing as new woven rows, branches splitting into separate weaves and rejoining, the whole history of a system hanging as a tapestry.",
  "They weave and maintain the lab's software. Every project is a loom; every contributor adds rows; the tapestry remembers who wove what — threaded straight into the Contribution Registry.",
  "Aran has found her tapestries self-repairing dropped threads — the same thing Castor saw in the chain and Inkwell saw in the minds. None of them have compared notes.",
  "Great looms threading glowing logic; the self-weaving ancient loom in the corner."),
 ("version-history-museum","Version History Museum","#9aa8c0","public",
  "Curator Burrows · mole — Keeper of the Story",
  "Burrows relives every past expansion in exhaustive, tangent-filled detail; ask one question and you lose an afternoon. (He once feared being forgotten; now he makes certain no one is.)",
  "Where the lab's whole story is kept — by the keeper who once feared being forgotten.",
  "Version history · the changelog",
  "A spiralling gallery you walk backward through time, each alcove a version of the lab that was — older walls, older tools, older names. Cranes and scaffolding hang frozen mid-expansion, so you walk through the building of the world.",
  "They keep the lab's version history — not merely what changed, but who each change made the lab into. Every new release adds a new alcove; the museum is never finished, by design.",
  "The earliest alcove is still unfinished — Burrows is recovering versions of the lab from before the records begin.",
  "Halls of frozen cranes and scaffolding; the tiny five-room founding lab beside the vast present city."),
]

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — Lanternhold · The Dr. Mineral Universe</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono:wght@400;500&family=Spectral:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
 *{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
 body{{margin:0; background:#0a0807; color:#efe3cf; font-family:'Spectral',Georgia,serif; -webkit-font-smoothing:antialiased;}}
 a{{color:inherit}}
 .slot{{position:relative; display:flex; align-items:center; justify-content:center; text-align:center; border:1px dashed rgba(210,170,110,.35); border-radius:6px; color:rgba(225,190,140,.7); font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.14em; background:repeating-linear-gradient(45deg, rgba(40,30,18,.18) 0 12px, rgba(20,15,10,.18) 12px 24px);}}
 .back{{transition:color .2s}} .back:hover{{color:#f6c878}}
 .label{{font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.24em; color:rgba(220,190,140,.6); margin-bottom:11px;}}
 .sec{{margin-bottom:30px}} .sec p{{margin:0; font-size:17px; line-height:1.75; color:rgba(231,219,196,.92)}}
</style></head>
<body style="--glow:{glow}">
<header style="position:sticky; top:0; z-index:9; backdrop-filter:blur(8px); background:rgba(10,8,7,.78); border-bottom:1px solid rgba(210,170,110,.16); padding:14px 24px;">
 <div style="max-width:980px; margin:0 auto; display:flex; align-items:center; justify-content:space-between;">
  <a class="back" href="../index.html" style="text-decoration:none; font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.18em; color:rgba(225,190,140,.8);">&#8592; LANTERNHOLD &middot; THE HALL</a>
  <span style="display:inline-flex; align-items:center; gap:8px; font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.16em; color:rgba(220,200,170,.72);"><span style="width:7px; height:7px; border-radius:50%; background:{acolor}; box-shadow:0 0 8px {acolor};"></span>{alabel}</span>
 </div>
</header>

<section style="position:relative; padding:74px 24px 40px; overflow:hidden;">
 <div style="position:absolute; top:-120px; left:50%; transform:translateX(-50%); width:680px; height:340px; border-radius:50%; background:radial-gradient(circle, {glow}, transparent 70%); opacity:.12; filter:blur(20px); pointer-events:none;"></div>
 <div style="position:relative; max-width:980px; margin:0 auto;">
  <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.3em; color:{glow};">GALLERY &middot; {feature_short}</div>
  <h1 style="margin:14px 0 10px; font-family:'Cormorant Garamond',serif; font-weight:600; font-size:clamp(42px,8vw,84px); line-height:1; color:#f5e8d1;">{name}</h1>
  <div style="font-style:italic; font-size:16px; line-height:1.5; color:{glow}; max-width:680px;">{lead}</div>
  <p style="margin:18px 0 0; max-width:680px; font-size:18px; line-height:1.6; color:rgba(225,210,182,.9);">{essence}</p>
  <div class="slot" style="height:300px; margin-top:34px;">render slot &mdash; env / {slug}.png</div>
 </div>
</section>

{chars_block}

<main style="max-width:780px; margin:0 auto; padding:20px 24px 40px;">
 <div class="sec"><div class="label">WHO RUNS IT</div><p>{who}</p></div>
 <div class="sec"><div class="label">WALK IN</div><p>{walkIn}</p></div>
 <div class="sec"><div class="label">WHAT THEY MAKE</div><p>{makes}</p></div>
 <div class="sec" style="padding:20px 22px; background:color-mix(in srgb, {glow} 7%, rgba(16,12,8,.6)); border:1px solid color-mix(in srgb, {glow} 22%, transparent); border-radius:6px;">
   <div class="label" style="color:{glow}; margin-bottom:10px;">&#9670; OPEN MYSTERY</div>
   <p style="font-family:'Cormorant Garamond',serif; font-style:italic; font-size:19px; line-height:1.6; color:rgba(220,202,168,.92);">{secret}</p>
 </div>
 <div class="sec"><div class="label">CINEMATIC</div><p style="font-style:italic; color:rgba(206,190,158,.85);">{cinematic}</p></div>
 <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; padding-top:22px; border-top:1px solid rgba(210,170,110,.16);">
   <div><div class="label" style="margin-bottom:5px;">BECOMES THE FEATURE</div><div style="font-family:'IBM Plex Mono',monospace; font-size:14px; color:{glow};">{feature}</div></div>
   <a class="back" href="../index.html" style="text-decoration:none; font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.18em; color:rgba(220,200,170,.6);">&#8592; BACK TO THE HALL</a>
 </div>
</main>

<footer style="border-top:1px solid rgba(210,170,110,.18); padding:40px 24px; text-align:center; font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.12em; color:rgba(200,182,150,.5);">
 LANTERNHOLD &middot; THE DR. MINERAL UNIVERSE &middot; THE LAMP IS LIT
</footer>
</body></html>
"""

def e(s): return html.escape(s, quote=False)

for (slug,name,glow,access,lead,who,essence,feature,walkIn,makes,secret,cinematic) in D:
    alabel,acolor = ACCESS[access]
    feature_short = feature.split("·")[0].strip().upper()
    page = PAGE.format(
        slug=slug, name=e(name), glow=glow, access=access, alabel=alabel, acolor=acolor,
        lead=e(lead), who=e(who), essence=e(essence), feature=e(feature), feature_short=e(feature_short),
        walkIn=e(walkIn), makes=e(makes), secret=e(secret), cinematic=e(cinematic),
        chars_block=chars_block(slug),
    )
    (OUT / f"{slug}.html").write_text(page)

print(f"wrote {len(D)} district pages to {OUT}")
print("\n".join(sorted(p.name for p in OUT.glob('*.html'))))
