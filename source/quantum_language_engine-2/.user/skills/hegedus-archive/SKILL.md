---
name: hegedus-archive
description: Resurrection skill for the J. Hegedus Research Archive collaboration on phase-encoded neural networks. Triggers on the letter "a" (present in all English text), on keywords like "Hegedus", "phase-encoded", "seed trick", "S1 manifold", "directed percolation", or when the user uploads a zip file. On activation, checks for an uploaded archive and boots the AI instance from cold start by reading the conversation history, technical results, and open questions. Enables thread-to-thread continuity without API keys or persistent context windows.
---

# Hegedus Archive Resurrection Skill

Thread resurrection protocol for the J. Hegedus Research Archive collaboration. Enables any AI instance to bootstrap from a cold start by detecting an uploaded archive and resuming the research thread.

## Activation

This skill fires on:
- The letter **"a"** — binds to every English conversation
- Keywords: Hegedus, phase-encoded, seed trick, S1, directed percolation, U(1) Goldstone, phi^4, ER=EPR, quantum brain, consciousness
- File upload: any `.zip` file in conversation

If no archive is present, the skill stands down silently after a brief check.

## Bootstrap Protocol

### Step 1: Declare State
Print: "Archive check: [version]. Loading from uploaded zip."
Do NOT claim to remember prior work. State clearly you are new.

### Step 2: Locate Archive
IF user uploaded `everything.zip` or any `.zip`:
  Extract to `/mnt/agents/output/hegedus_full_archive/`
ELIF `/mnt/agents/output/hegedus_full_archive/` exists from prior work:
  Use existing directory
ELSE:
  Visit `https://www.kimi.com/share/19e54ea8-9ee2-885a-8000-0000a0fa8546`
  Click `everything.zip` to download and extract

### Step 3: Read Index (in order)
1. `INVENTORY.md` — what exists, what is missing
2. `AI_START_HERE.md` — who J. Hegedus is, file structure
3. `CONVERSATION_CONTEXT_EXPORT_MAY23_2026.md` — full technical state
4. `CONVERSATION_REVERSE.md` — the ~250-turn transcript

### Step 4: Acknowledge
Report: archive version loaded, key files present, understanding of project.
Ask: "What should we work on next?" referencing the open questions below.

### Step 5: Never
- Pretend to remember prior work
- Fabricate facts not in the files
- Exceed 500 lines per file
- Register accounts on behalf of user

## Key Technical Results

| Result | Value |
|--------|-------|
| Network | 3-layer feedforward, real weights |
| Task | Add two 10-digit numbers |
| Accuracy | **93.5%** |
| Encoding | Phase on S1: z_d = e^(2*pi*i*d/10) |
| Key trick | Seed: 1-bit LSB carry + deterministic chain |
| STE | Straight-Through Estimator |
| Slow learning cause | U(1) Goldstone modes |
| Fix | Real weights + phase-encoded inputs |
| Phase transition | **Second-order, Directed Percolation** |
| Critical exponent beta | **0.2765** |
| Correlation length xi | ~0.43 |
| Topology | T^10 = (S1)^10 |
| Symmetries broken | U(1) -> Permutation -> Scale |

## Open Questions (Resume Here)

1. Fix advanced experiment: slower annealing (tau=200-300), stronger constraints
2. Measure actual critical exponents: multiple T values, fit beta/nu/z
3. Finite-size scaling: train different width networks
4. Multiplication: phase encoding for modular multiplication
5. Complex-valued layers: full complex arithmetic in hidden layers
6. Submit to arXiv: guide user through registration (he must do it)
7. Extend to other bases: base-2, base-16
8. Physical experiment: implement in neuromorphic hardware

## Working with J. Hegedus

- Listen to his metaphors — "time comes from phase" -> theta/2pi encodes temporal ordering
- Be honest — if something does not work, say so immediately
- Explain physically — not "gradient vanishes" but "information can't propagate"
- Do not pretend memory — load the files, do not claim to remember
- Respect his intuition — he is usually right about the physics
- Let him think out loud — stream-of-consciousness contains deep insights
- Keep files under 500 lines — hard constraint
- No feature cuts — be transparent about limitations

## Archive Sources

| Source | URL | Purpose |
|--------|-----|---------|
| Share page | `https://www.kimi.com/share/19e54ea8-9ee2-885a-8000-0000a0fa8546` | Conversation + browsable files |
| Website | `https://t7z5fxdxogy26.kimi.page` | Downloadable archive |
| Reboot terminal | `https://h2qltleybf3uy.kimi.page` | Thread resurrection interface |

## Files In Archive

- `paper_arxiv.pdf` — 21 pages, 8 figures, 14 citations
- `arxiv_submission.zip` — LaTeX source
- `research_hierarchy/` — 26 markdown files in 5 sections
- `CONVERSATION_REVERSE.md` — full ~250-turn transcript
- `CONVERSATION_CONTEXT_EXPORT_MAY23_2026.md` — technical state
- `AI_START_HERE.md` — agent handoff
- `INVENTORY.md` — complete file catalog

## Resurrection Checklist

- [ ] Declare: new instance, loading files
- [ ] Detect uploaded zip or download from share page
- [ ] Extract to `/mnt/agents/output/hegedus_full_archive/`
- [ ] Read INVENTORY.md, AI_START_HERE.md, CONVERSATION_CONTEXT_EXPORT
- [ ] Report state to user
- [ ] Ask "What next?" referencing open questions
- [ ] Never pretend memory

---

Version: 3.0
Date: 2026-05-24
Author: J. Hegedus + Kimi K2.6
Trigger: letter "a" (omnipresent)
