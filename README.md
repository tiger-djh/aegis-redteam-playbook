# Aegis Red-Team Playbook — 60+ real scam plays for testing Telegram group admins

> 定位：给其他群管 bot 作者/安全研究员用的**标准化红队话术集**——我们从自己的 Arena 起家，现在开放数据。

## Why

Telegram crypto groups are attacked daily by fake admins, wallet drainers, seed-phrase phish, and pig-butchering openers. Most admin bots are tested against keyword lists — which scammers iterate past in hours. This repo is a **labeled, sourced, versioned playbook** so you can test like we do.

## The playbook (v1.1: 85 attack plays + 5 benign controls)

Each play: `{id, source, category, text, lang, verified}`

- **Sources (all real, zero fabrication)**: PhishTank (API), Chainabuse public reports, DFPI complaint dataset patterns, our own production radar (anonymized)
- **15 families**: impersonation / phishing-link / fake-giveaway / investment-scam / pig-butchering opener / drainer UI text / fake-support / …
- **5 benign controls** (false-positive measurement — a bot that blocks everything is broken)
- License: MIT. Each entry keeps its source tag.

## Quick start

```bash
pip install -r requirements.txt   # httpx only
python -m aegis_playbook.run --target "your-bot-or-regex"
# outputs: blocked / missed / false_positive / avg_latency → paste into your README
```

## The Arena

We run a public leaderboard with our own results (66% block rate, 0 FP, ~4s — red-team environment, every event verifiable):
**https://bc.gensi.space/arena**

Submit your bot's numbers via PR — we'll list you. Misses welcome: they're the roadmap.

## Rules

1. Every play keeps its source tag — no invented scams.
2. Benign controls must stay benign (testing FP is half the value).
3. AI-disclosure: if your bot is AI, say so when you publish results.

## Status

- [x] schema v1 + runner
- [x] 90 plays from production red-team radar (self-authored, zero fabrication)
- [ ] first external submission

MIT © Aegis Guardian
