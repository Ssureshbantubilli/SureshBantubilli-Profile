# MyProfile — Context

Single-file personal portfolio site (`index.html`, ~1012 lines, ~426KB — inflated by a base64 avatar on line 373). No build step, no framework, no other files. Inline CSS + inline vanilla JS. Deployed-looking markers suggest Cloudflare (email obfuscation via `/cdn-cgi/l/email-protection`).

## Owner
- **Suresh Kumar Bantubilli** — Senior Associate Director, Global Technology (Pune, India)
- Global Middleware, Messaging & Infrastructure Leader · CTO Infrastructure
- 19+ years across 3 Tier-1 banks; leads a 40+ engineer global org
- Specialities: Kafka, IBM MQ, AMQ, Solace, Pulsar, Red Panda, Hadoop/Spark, GenAI/Agentic AI, OpenShift, GCP
- GitHub: `Ssureshbantubilli` · LinkedIn: `suresh-bantubilli` · Phone: +91-8530645999

## Page structure (section IDs in order)
1. `#hero` (L331) — name, tagline, CTA buttons, terminal-style profile card, stats grid
2. `#about` (L404) — "// 01 — ABOUT" Profile Summary
3. `#achievements` (L430) — "// 02" Key achievements (Agentic AI patching, GHCP rollout, ICE compliance, etc.)
4. `#experience` (L449) — "// 03" Timeline of 6 roles: HSBC (Oct 2024–present), Barclays VP (Mar 2022–Oct 2024), Deutsche Bank (Jul 2015–Mar 2022), Barclays MQ admin (Sep 2011–Jul 2015), Barclays GTOC (Mar 2010–Sep 2011), Syntel (Aug 2006–Feb 2010)
5. `#skills` (L571) — "// 04" Tech stack: Messaging, Cloud/Infra, Data Eng, Automation/DevOps, AI/GenAI, Languages, Core Competencies
6. `#projects` (L610) — "// 05" GitHub POCs: AIVirtualDoctor, AstroMeter, jyotish_app, GodavariPushkaralu, EasyPrompting
7. `#leadership` (L655) — "// 06" Snapshot survey (98% approval, 100% favour, 100% participation), leadership principles
8. Certifications & Education (L764) — "// 07" GenAI certs, MCA/BCA
9. `#engage` (L782) — "// 08" React buttons + comment form (localStorage-backed, see `getVid()` L962)

## Visual system
- Cyberpunk/terminal aesthetic: dark bg (`#050a0f`), cyan primary (`#00d4ff`), gold/green accents
- Fonts: Share Tech Mono, Syne, Inter (Google Fonts)
- Effects: boot splash (`#boot`), animated canvas (`#canvas`), grid overlay via `body::before`, reveal-on-scroll (`.reveal`)
- Responsive: mobile-first hamburger nav, desktop nav activates via `.desk-nav` at ≥900px

## Key stats claimed
19+ yrs · 94% effort saved (GenAI reporting) · 40% cost reduced · 29+ Kafka apps · 900TB storage architecture · 40+ team members · 3 Tier-1 banks

## Gotchas when editing
- **Line 373 is ~355KB** (base64 avatar). Don't try to Read the whole file — use targeted offsets; skip around line 373.
- `wc -l` = 1012 but `Read` without limit fails on size; use offset+limit.
- Email is Cloudflare-obfuscated — don't hand-edit the encoded string.
- Everything is inline; one file is the whole site.
