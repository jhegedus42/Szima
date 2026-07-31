# alphaXiv MCP Tool Reference

Server: `https://api.alphaxiv.org/mcp/v1` — MCP v1.0.0, streamable HTTP transport.
11 tools in two groups. Source: https://www.alphaxiv.org/docs/mcp

## Contents

- Research tools (consume assistant quota, call alphaXiv AI models)
  - discover_papers
  - get_paper_content
  - answer_pdf_queries
  - read_files_from_github_repository
- Library tools (manage the user's alphaXiv library folders)
  - list_library, save_papers_to_folder, remove_papers_from_folder,
    move_papers_between_folders, create_folder, rename_folder, delete_folder
- Workflow recipes

---

## Research tools

### discover_papers

Agentic retrieval loop (keyword + embedding search + optional multi-round follow-ups). Best for literature discovery, related work, broad topical coverage. Returns 5–15 ranked papers with title, publication date, organizations, abstract preview, arXiv ID.

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `keywords` | string[] | yes | 3–4 concise terms: exact names, acronyms, methods, benchmarks, authors, titles. Plain text. |
| `question` | string | yes | Detailed semantic description of the papers wanted: concepts, methods, applications, related terms. |
| `difficulty` | number 1–10 | yes | Retrieval effort. Higher = slower but multi-round follow-up searches. |
| `published_after` | string | no | YYYY-MM-DD. Omit unless a real boundary is named. |
| `published_before` | string | no | YYYY-MM-DD. |
| `prioritize` | enum | no | `"default" \| "historical" \| "recency"` |

```json
{"keywords": ["RAG", "retrieval-augmented generation", "question answering"],
 "question": "Papers using retrieval-augmented generation for open-domain QA, including dense retrievers and reader-generator architectures.",
 "difficulty": 3, "prioritize": "recency"}
```

### get_paper_content

Full paper content as text. Default: structured AI-generated intermediate report optimized for LLM consumption; falls back to full extracted text if no report exists.

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `url` | string (URL) | yes | arXiv or alphaXiv URL: `https://arxiv.org/abs/2307.12307`, `https://arxiv.org/pdf/2401.12345`, `https://www.alphaxiv.org/overview/2307.12307` |
| `fullText` | boolean | no | true = raw extracted text page by page instead of the report. Default false. |

### answer_pdf_queries

Filtered page-level content of ONE pdf relevant to the queries. Returns XML `<paper id="..."><page num="N">...</page></paper>` — citation-ready. Batch every question for a paper into ONE call (extra queries are nearly free). For multiple papers, issue parallel calls.

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `paper` | string | yes | arXiv ID (`2307.12307`), URL (arXiv abs/pdf, alphaXiv abs, Semantic Scholar, direct PDF), or a title (resolved to best match, reported in `<paper>` tag). |
| `queries` | string[] | yes | Brief descriptions of the information sought. |

```json
{"paper": "https://www.alphaxiv.org/abs/2512.16649",
 "queries": ["Main hyperparameters used in experiments",
             "Evaluation metrics and benchmark datasets",
             "Limitations discussed by the authors"]}
```

### read_files_from_github_repository

Reads files/dirs from a paper's GitHub repo. `path="/"` returns the complete file tree plus all top-level files; a directory fetches all its files in parallel; a file returns its contents.

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `githubUrl` | string (URL) | yes | e.g. `https://github.com/owner/repo` |
| `path` | string | yes | `/`, `src/utils`, or `src/model.py` |

---

## Library tools

Folders are addressed by the opaque `folder_id` from `list_library` — always call it first. Default folders "Want to read" / "Reading" / "Completed" represent reading status and overlap freely.

### list_library
Entry point for all library work. Lists folders with `folder_id`, name, type, `parent_id`, `sharing_status`, `paper_count`.

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `include_papers` | boolean | no | Also list papers in each folder (capped). Default false. |
| `paper_ids_or_urls` | string[] | no | Report which folders already contain each paper (adds `paper_membership` section). |

### save_papers_to_folder (writes)
| Parameter | Type | Required | Notes |
|---|---|---|---|
| `paper_ids_or_urls` | string[] (1–50) | yes | arXiv ids or alphaXiv/arXiv URLs. Papers not yet in the DB are fetched from arXiv. Idempotent. |
| `folder_id` | string | no | Defaults to "Want to read". |

### remove_papers_from_folder (destructive)
`paper_ids_or_urls` (1–50, required), `folder_id` (required). Only affects the given folder.

### move_papers_between_folders (destructive, atomic)
`paper_ids_or_urls` (1–50, required), `from_folder_id` (required), `to_folder_id` (required). Duplicates in destination are left untouched in source.

### create_folder (writes)
`name` (1–100, required), `parent_folder_id` (optional, for nesting). Returns new `folder_id`.

### rename_folder (writes)
`folder_id` (required), `name` (1–100, required). Custom folders only.

### delete_folder (destructive)
`folder_id` (required). Papers themselves are not deleted; publications and private-papers folders cannot be deleted.

---

## Workflow recipes

### Literature review
1. `discover_papers` to surface candidates.
2. Re-run with varied keywords/questions or higher difficulty to fill gaps.
3. `answer_pdf_queries` (batch questions per paper) for citation-ready excerpts.
4. Synthesize across papers.

### Code analysis
1. `discover_papers` to find the paper.
2. Extract the GitHub URL from results/metadata.
3. `read_files_from_github_repository` with `path="/"` for overview, then drill into directories.

### Deep research
1. `discover_papers` (multiple framings in parallel).
2. `get_paper_content` for the AI report or full text.
3. `answer_pdf_queries` for citation-grade page excerpts.
4. `read_files_from_github_repository` to verify implementation claims.

### Library management
1. `list_library` to get `folder_id`s.
2. `create_folder` to organize a topic, then `save_papers_to_folder`.
3. `move_papers_between_folders` to advance papers through reading-status folders.
