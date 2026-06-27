# The Living Lab — what the world *does*

The 3D world (`site/world/`) isn't a diorama — it's the public face of a working lab that perpetually **mines real security work → forges it onto the chain → mints tokens → records & keeps them**, while it researches tokenomics and builds on-chain. Everything moves with purpose.

## Built (this pass)
- **Notice board** — posts the lab's roadmap; clickable for the full announcement. *This is the announcements/releases surface.*
- **Keeper patrol** — Dr. Mineral walks a slow round overseeing the lab, with a **hovering assistant orb** beside him; click him for his **scroll** (bio + current directive).
- **Token minting** — coins struck at the Foundry arc to the Vault, continuously. The chain also grows (Foundry→Ledger) as blocks forge.

## The roadmap on the board (UPDATE WEEKLY)
- **This week:** forging the blockchain core.
- **Next 2 weeks:** first version of the **tokenomics ecosystem** + the **test-token dApp on testnet**.
- The board also reserves space for **releases, versions, and reward/bounty winners** (Hall of Contributors feed — future).

> To change the board: edit `boardTex()` (the canvas drawing) **and** `boardPanel.userData.panel.mean` (the click panel) in `site/world/index.html`, and update this doc.

## Next increments (not built yet)
- **Basic lab equipment** — research desks, glowing terminals (code/chain on screen), pipes/cables ("connections") linking zones, so it reads as a real blockchain lab.
- **Richer worker behaviour** — more workers, varied tasks; the keeper occasionally *directing* a worker (a brief tether/voice-line beat) — "talking to his workers."
- **Assistant scroll as a live notes feed** — the orb projects Dr. Mineral's notes/announcements on demand.
- **Hall of Contributors** — wire the board's "winners" area to real (or illustrative) contributors once the coin ships.
