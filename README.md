# 0xDELTA × World ID

**First forensic trading agent anchored to a verified human.**

🔗 **Live demo:** https://johnpreston2.github.io/0xdelta-worldid/landing.html

---

## What it does

0xDELTA is an autonomous on-chain forensic agent running 24/7 on Base chain. Every 2 hours, it:

1. Collects live data for 19 Base chain tokens
2. Computes 65+ forensic metrics (FHS, NBP, ICR, LCR, BPI, WCC...)
3. Detects phases: EARLY_BREAKOUT, ACCUMULATION, DISTRIBUTION
4. Generates AI synthesis via Venice LLM (Gemini 3 Flash)
5. Executes a swap on the top-ranked token via Bankr API
6. Publishes reports to GitHub Pages

**World ID integration:** Every swap decision is anchored to a ZK-verified unique human. Access is free for World ID holders, metered via x402 micropayments for AI agents.

## World ID × x402 Access Matrix

| Tier | Dashboard | Synthesis | Live Signals |
|------|-----------|-----------|--------------|
| 🌐 World ID Orb | FREE | FREE | FREE |
| 📱 World ID Device | FREE | FREE | $0.01 |
| 🤖 AI Agent / Guest | $0.02 x402 | $0.05 x402 | $0.02 x402 |

## Architecture

```
User → World ID ZK Proof → Flask verify endpoint (VPS)
                                    ↓
                         Session token (24h)
                                    ↓
                    Dashboard / Synthesis unlocked

AI Agent → x402 micropayment ($0.02 USDC on Base)
                    ↓
           Access granted trustlessly
```

## Tech Stack

- **Agent runtime:** OpenClaw (GCP VPS) — Gemini 3 Flash
- **Forensic engine:** `forensic_engine_v5.py` — 65+ metrics
- **World ID:** `@worldcoin/idkit-standalone` v2.1.2 — ZK proof verification
- **x402:** Coinbase x402 v2 — micropayment paywall
- **Trading:** Bankr API — Base DEX swaps
- **AI synthesis:** Venice AI (private inference) + Gemini 3 Flash
- **Frontend:** GitHub Pages (static, no backend)
- **Verification backend:** Flask (Python) on GCP VPS port 5050

## Key Files

| File | Description |
|------|-------------|
| `landing.html` | Landing page with World ID widget + access matrix |
| `index.html` | Per-token forensic dashboard ($0.02 x402) |
| `report.html` | Global synthesis report ($0.05 x402) |
| `verify_world.py` | Flask endpoint — World ID ZK proof verification |

## Tracks

- World Chain Open Track
- AgentKit
- x402 / Bankr
- Venice AI

## Live Data

Data feeds from the production agent (refreshed every 2h):
- `memory.json` — per-token forensic reports
- `synthesis.json` — global AI synthesis
- `signals.json` — active trading signals

---

Built for the **World Chain Hackathon 2026** · ERC-8004 Agent #32715
