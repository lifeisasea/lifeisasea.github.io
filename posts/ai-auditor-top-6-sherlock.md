---
title: An AI auditor in the top 6 at Sherlock: what it means for smart contract security
date: 2025-09-02
description: Savant.chat ranked top 6 in a public Sherlock DeFi audit contest, competing against dozens of expert human auditors — the first public result of its kind. Here is why it matters.
---

In September 2025, [Savant.chat](https://savant.chat) ranked top 6 in a public [Sherlock](https://www.sherlock.xyz/) DeFi audit contest — competing directly against dozens of expert human auditors. To our knowledge, it was the first time an AI system publicly performed on par with senior human auditors in a fiercely competitive environment.

## Why a contest, not a benchmark

Benchmarks are useful, and we track them closely — Savant scores 82% on EVMbench, the best result we know of on the market. But benchmarks are built from known vulnerabilities. A live audit contest is different: fresh code, real economic incentives, and human competitors who have every reason to find what you missed. There is no way to overfit to it.

## What actually made the difference

- **Multi-model orchestration.** Savant is not a wrapper around a single LLM. It combines several Tier-1 models to generate vulnerability hypotheses, trace code execution and filter out false positives.
- **Proprietary training data.** The system is built on a dataset of 20,000+ analyzed vulnerabilities, from which we extract optimized security skills for our agents.
- **False-positive discipline.** The single biggest reason teams abandon AI security tools is noise. Ranking in a contest requires findings that are real, reproducible and clearly explained — exactly what we optimize for.

## What it does not mean

It does not mean human auditors are obsolete. Our own recommendation to clients is a layered stack: AI in CI/CD during development, an AI deep audit as preparation, and a human audit before mainnet for high-value code. What the result does mean is that the AI layer is no longer optional — it now catches, at a fraction of the cost and time, a large share of what only humans could catch before.

> The people who built DeFi — 1inch, Lido, BGD Labs, TON — already trust Savant with their own code. The Sherlock result is public evidence of why.
