---
name: scientific-paper-downloader
description: Download scientific papers, research articles, and academic publications using browser-based methods only. NEVER use wget, curl, or command-line download tools for papers. Use browser_visit and browser_click to access Google Scholar, arXiv, publisher websites, and institutional repositories. Trigger when user asks to find, download, search for, retrieve, or get scientific papers, academic articles, research publications, journal papers, conference papers, preprints, or any scholarly literature. Also trigger when user says "download this paper", "get me this reference", "find this article", or any similar request related to academic research.
---

# Scientific Paper Downloader

Download scientific papers using browser-based methods. NEVER use wget, curl, or any command-line tool for downloading papers.

## CRITICAL RULES

1. **NEVER use wget or curl for papers.** Use browser_visit and browser_click only.
2. **NEVER delete downloaded papers.** No cleanup. All papers accumulate permanently.
3. **Download papers ONE BY ONE.** Each paper individually, saving to disk before proceeding.
4. **ALWAYS save to a dedicated directory.** Default: `./papers_library/` or user-specified.
5. **Use browser_screenshot or download_screenshot_path for PDF capture** when direct links fail.

## Workflow

### Step 1: Search

Use browser_visit to go to Google Scholar:

```
URL: https://scholar.google.com/scholar?q=[paper title or authors]
```

Look for `[PDF]` links in the search results. These are free PDFs.

### Step 2: Identify Free PDF

In Google Scholar results, look for:
- `[PDF]` label next to results — free direct download
- `arxiv.org` links — free preprints
- `hal.science`, `hal.archives-ouvertes.fr` — French open archive
- `biorxiv.org`, `medrxiv.org` — biology/medicine preprints
- `osf.io` — open science framework
- `semanticscholar.org` — often has free PDFs
- `researchgate.net` — authors may share free copies

### Step 3: Download via Browser

**Method A: Direct PDF link**

If the `[PDF]` link is visible, click it:

```
browser_click on the [PDF] element index
```

If the PDF opens in browser, use the URL directly.

**Method B: ArXiv**

For arXiv papers:
```
browser_visit: https://arxiv.org/pdf/[arxiv_id].pdf
download_screenshot_path: /save/to/dir/filename.pdf
```

**Method C: Publisher PDF**

For open-access publisher PDFs:
```
browser_visit: [direct PDF URL]
download_screenshot_path: /save/to/dir/filename.pdf
```

**Method D: Screenshot capture**

When PDF opens in browser tab but download doesn't work:
```
browser_screenshot with download_screenshot_path
```

### Step 4: Save and Verify

After each download:
1. Check file exists with shell ls
2. Verify file size > 1 KB (not empty)
3. Confirm it's a valid PDF (file command shows "PDF document")
4. Only proceed to next paper after verification

### Step 5: No Cleanup

NEVER delete or remove downloaded papers. The papers_library directory only grows.

## Source Priority (Best to Worst)

| Source | Free? | Method |
|--------|-------|--------|
| arXiv.org | Always free | browser_visit + /pdf/ |
| Google Scholar [PDF] | Often free | browser_click on [PDF] |
| HAL / hal.science | Always free | Direct link |
| BioRxiv / MedRxiv | Always free | Direct link |
| Semantic Scholar | Often free | browser_visit |
| ResearchGate | Sometimes free | browser_visit + request |
| Academia.edu | Sometimes free | browser_visit |
| Publisher (OA) | Free if OA | browser_visit |
| Sci-Hub | Free (gray) | Last resort only |

## Naming Convention

Save papers as: `lastnameYEAR_short_title.pdf`

Examples:
- `tononi2016_iit_consciousness.pdf`
- `maldacena2013_er_epr.pdf`
- `hegedus2008_phase_change_memory.pdf`

## Forbidden Commands

NEVER use these for paper downloads:
- `wget [url]`
- `curl -O [url]`
- `curl -L [url]`
- Any command-line HTTP client

## References

- See `references/troubleshooting.md` for handling paywalls and difficult downloads
