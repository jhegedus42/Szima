# AGENTS.md

`/Users/joco/opencode` is an empty working folder, **not** a git repository — use it as scratch space. Facts below were verified on 2026-07-29.

## Hard Rules (never violate)
1. **No server writes without explicit permission.** Do not create, edit, or delete files on the Hetzner server (88.99.218.155) unless the user explicitly asks. This includes: knowledge files, skills, why-chain entries, SSH config, config files, Docker containers. Read-only is fine. Ask first.
2. **Three identical errors → fix in infrastructure, not in retries.** If you hit the same error 3 times, stop retrying and fix the root cause permanently (add to AGENTS.md, update tooling, change approach).

## Environment
- macOS (arm64), shell `zsh`. `~/.zshenv` references a missing `~/.cargo/env`, which prints an error on every shell start — harmless, do not "fix" unless asked.
- Package managers: Homebrew (`brew`), npm (Node v25).
- opencode global config: `~/.config/opencode/opencode.jsonc` (currently just the schema). Persistent cross-session rules belong in `~/.config/opencode/AGENTS.md` (does not exist yet).
- opencode data/auth: `~/.local/share/opencode/` (includes `mcp-auth.json`). Skills: `~/.agents/skills/`.

## Installed tooling
- `gws` (Google Workspace CLI) v0.22.5 — `brew install googleworkspace-cli`.
- `gcloud` (Google Cloud SDK) — `brew install --cask google-cloud-sdk`. **Gotcha:** not on PATH until the SDK's `path.zsh.inc` is sourced in the shell profile; if `gcloud` isn't found in a fresh shell, source `/opt/homebrew/share/google-cloud-sdk/path.zsh.inc` first.
- Skills installed: `bx`, `find-skills`, `firecrawl-research-index`, `research-agent`, `gws-gmail`.
- MCP already authed: `exa-search`.

## Gmail access (gws-gmail skill)
- Needs the `gws` binary (installed) **plus** a one-time Google OAuth login.
- `gws auth setup` is interactive (browser) and requires `gcloud`. For a `@gmail.com` account the unverified-app 25-scope limit applies, so log in with individual scopes: `gws auth login --scopes gmail`.
- **Auth status: NOT yet completed.** Before assuming Gmail works, verify with `gws gmail users getProfile`.
- Common usage: `gws gmail +triage`, `gws gmail +read`, `gws gmail +reply --message-id <id> --body "..."`.

## Sensitive files — DO NOT read, print, or expose
In the ProtonDrive root (`~/Library/CloudStorage/ProtonDrive-chickenloop42@proton.me-folder/`):
- `1Password*.zip`, `1password-credentials*.json`, `1PasswordExport-*.1pux`
- `AccessKey.csv`, `RAM Access Key AliBaba.txt`, `R12.der`
- `proton-recovery-phrase.pdf`, `ai/dev/secret_1pw.env`
- Any `*.env`, recovery phrases, or credentials files in general.

If a task needs a secret, ask the user — do not hunt through these files.

## User's AI research (context; don't edit unless asked)
- Active work under `…/ai/dev/` (Obsidian vault, opencode source) and a large research dump in `…/ai/` covering: complex-valued / temporal transformers (GPT-2 based), neural networks × QFT, and related arXiv drafts.
- Works across many AI providers (DeepSeek, Kimi, Gemini, Claude, Z.ai/GLM).
