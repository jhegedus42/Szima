# Troubleshooting Paper Downloads

## Paywall Bypass Strategies (in order of preference)

### 1. ArXiv Mirror

If a paper is on arXiv but the main site is slow:
- `https://ar5iv.labs.arxiv.org/html/[id]` — HTML version
- `https://arxiv.org/pdf/[id].pdf` — PDF version

### 2. Unpaywall

Many papers have free copies. Try:
- Search DOI on unpaywall.org via browser
- Look for institutional repository (e.g., mit.edu/~author, cam.ac.uk/~author)
- Check author's personal page for free PDFs

### 3. Semantic Scholar

Often hosts free copies:
- `https://www.semanticscholar.org/search?q=[title]&sort=relevance`
- Look for "View PDF" button

### 4. Google Scholar "All N Versions"

Click "All N versions" under a result to find free copies.

### 5. Institutional Repository

Search university repositories:
- `https://dspace.mit.edu/handle/1721.1/[id]`
- `https://ora.ox.ac.uk/objects/[uuid]`
- `https://www.repository.cam.ac.uk/[handle]`

### 6. Internet Archive / Wayback Machine

Some papers archived:
- `https://web.archive.org/web/*/[URL]`

### 7. Last Resort: Sci-Hub

Only when all legitimate methods fail:
- `https://sci-hub.se/[DOI]`
- `https://sci-hub.st/[DOI]`

Use only for papers the user has legal right to access.

## Common Problems

### Problem: PDF opens in browser but doesn't download

Solution: Use `browser_screenshot` with `download_screenshot_path` to save the rendered PDF.

### Problem: Cloudflare blocks the page

Solution: Try alternative URLs:
- ar5iv.org for arXiv papers
- Semantic Scholar for other papers
- Direct publisher PDF link if available

### Problem: File is HTML instead of PDF

Solution: The URL points to abstract page, not PDF. Look for `.pdf` at end of URL or PDF download button.

### Problem: Download is very slow

Solution: Use arXiv mirrors or try at different time. Do NOT use wget/curl — stick with browser.

### Problem: File downloads as 0 bytes

Solution: Try different source. If all fail, note the failure and move to next paper. Come back later.

## Metadata Extraction

After downloading, record metadata:
- Full citation (authors, year, title, journal, DOI)
- Keywords from abstract
- Why this paper was downloaded (for which project)
- File path where saved

Store metadata in CSV alongside PDFs.
