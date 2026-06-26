# The Real Product — UNL Cybersecurity Lab Reward Coin

What the site is actually the face of. Sourced from the cohort deck *"Web2 to Web3: Building dApps"* (Lab Reward Token Cohort, Session 2). Dr. Mineral's world is the **brand skin**; this is the **substance**.

## The mission (the hero of the site)
Build a **blockchain reward system — the University of Nebraska coin** — for the university's **security-led cybersecurity lab**: a token that rewards **genuine security work** (bugs found, audits done, writeups, protocols hardened), recorded on-chain and honored. Built by the cohort; the people building it are part of the story.

## What it must do (deck constraints)
- **Reward genuine security work** — bugs, audits, writeups.
- **Resist gaming** — Sybil, collusion, metric-gaming (Goodhart's law: when a metric becomes a target, people game it).
- **Have a real sink** an institution can actually control.
- **Don't accidentally build a financial security.**
- Open questions: fungible points vs non-fungible reputation (or both)? fixed supply vs mint-on-demand? campus Sybil-resistance? what campus rules a token would trip?

## Tokenomics levers (the six)
Supply · Distribution · Utility/demand · Sinks · Incentive alignment · Governance. Watch alignment hardest.

## The Web3 reality (what changes from Web2)
Only three layers change: **server → smart contract** (public, immutable), **database → blockchain** (permanent public ledger), **login → key** (no reset). React frontend barely changes. "An integrity machine, not a secrecy one — never put on-chain what you wouldn't put on a billboard."

## The 2026 stack we build with
- **Contracts:** Solidity + OpenZeppelin (ERC-20 reward token; maybe 721 for reputation/badges)
- **Dev/test:** Foundry (forge/anvil) + Hardhat; Remix for prototyping
- **Frontend↔chain:** viem + wagmi (React); MetaMask · WalletConnect · RainbowKit
- **RPC:** Alchemy · Infura · QuickNode
- **Indexing:** The Graph
- **Security (home-field advantage):** Slither · Aderyn · Echidna · OZ Defender — in CI

## How it maps to Dr. Mineral's world (the skin)
The blockchain-mining metaphor *is* the reward system:
| World zone | Real meaning |
|---|---|
| **The Mines** | Doing the security work (the "mining" — bugs, audits, writeups) |
| **The Foundry** | Minting the reward token / forging the on-chain record |
| **The Ledger** | The on-chain ledger of who earned what (Hall of Contributors = reward/bug-bounty winners) |
| **The Vault** | Treasury + the institutional **sink** |
| **The Watch** | Security & audit (Slither/Echidna/monitoring) — the cohort's edge |

**Dr. Mineral** is the keeper "under the hood" — the mascot/face, not the headline. The **lab, the coin, and the team** are the headline.
