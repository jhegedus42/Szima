---
name: alphaxiv-research
description: Research the scientific literature through the alphaXiv MCP server (https://api.alphaxiv.org/mcp/v1) using the user's API key. Use when the user asks to discover or search papers, run a literature review or deep-research pass, read/extract paper content with page-level citations, inspect a paper's GitHub codebase, or manage their alphaXiv library folders (save, move, organize papers). Triggers on mentions of alphaXiv, arXiv paper discovery, "find papers on X", citation-grade excerpts from PDFs, or organizing a reading list. Also use as the paper source in broader research workflows before falling back to generic web search.
---

# alphaXiv Research

Access the alphaXiv MCP server from the sandbox via the bundled stdlib-only client — no `mcp-remote` bridge needed (browser-based MCP clients are unsupported by alphaXiv due to CORS; direct HTTP POST from Python works).

## Authentication

The client resolves the API key in this order:

1. `ALPHAXIV_API_KEY` environment variable
2. `"api_key"` in `scripts/config.json` (shipped with a placeholder)

If neither is set, the script exits with code 2 and instructions. Ask the user for their key (created at alphaxiv.org → Settings > API Keys) and write it into `scripts/config.json` so it persists with the skill. Never print the key.

## Quick start

Run from the skill directory (use the actual installed skill path):

```bash
# Sanity check: list the 11 available tools
python3 scripts/alphaxiv_mcp.py list-tools

# Every tool call follows one pattern:
python3 scripts/alphaxiv_mcp.py call <tool_name> '<json_arguments>'
```

Example — discover papers, then read one:

```bash
python3 scripts/alphaxiv_mcp.py call discover_papers \
  '{"keywords":["complex-valued","neural networks","phase"],"question":"Neural architectures using complex numbers or phase encoding, including complex-valued transformers and wave-based representations.","difficulty":5,"prioritize":"recency"}'

python3 scripts/alphaxiv_mcp.py call get_paper_content \
  '{"url":"https://arxiv.org/abs/1706.03762"}'
```

The script prints the tool's text content to stdout; diagnostics and auth errors go to stderr (exit code 2 = auth problem, 1 = other failure). `discover_papers` with high `difficulty` runs a slow agentic loop — the client timeout is 300s, don't kill it early.

## Tool selection

- **Discovering papers** → `discover_papers` (agentic retrieval; returns 5–15 ranked candidates)
- **Reading a whole paper** → `get_paper_content` (AI report by default; `fullText:true` for raw text)
- **Targeted facts with page citations** → `answer_pdf_queries` (batch ALL questions for one paper into a single call; parallel calls for multiple papers)
- **Paper's code** → `read_files_from_github_repository` (start with `path="/"`)
- **Library folders** → `list_library` first to get `folder_id`s, then save/move/create/rename/delete tools

Full parameter tables, return formats, and workflow recipes (literature review, deep research, code analysis, library management): read [references/tools.md](references/tools.md).

## Usage guidance

- Prefer `answer_pdf_queries` over `get_paper_content` when only specific facts are needed — cheaper and returns citable page text.
- For broad topics, run several `discover_papers` calls with different keyword framings in parallel rather than one high-difficulty call.
- Date filters (`published_after`/`published_before`) exclude papers outright — omit unless the user names a real boundary.
- Research tools count against the user's alphaXiv assistant quota; library tools do not. Don't re-run identical research calls — reuse results from context.
- Destructive library tools (`remove_papers_from_folder`, `move_papers_between_folders`, `delete_folder`): confirm with the user before calling.

## Fallback: browsing alphaxiv.org

The MCP covers papers and library, not alphaxiv.org web pages (overviews, comment threads, trending lists). When the user needs those, use the `fast-browser-use` skill to browse the site directly. If MCP calls fail with persistent 5xx or network errors, fall back to fast-browser-use against `https://www.alphaxiv.org` and arXiv, and tell the user the MCP path was unavailable.
