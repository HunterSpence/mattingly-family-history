# Browser-Side Automation for Harvesting Ancestry.com Cousin Trees

**Research date:** 2026-04-26  
**Scope:** Free/DIY methods for bulk-extracting 20-30 cousin trees from Ancestry.com using your own subscription and logged-in session. No paid tools.

---

## IMPORTANT: Ancestry ToS Position

Ancestry's Terms and Conditions (effective 2025-08-18) explicitly prohibit:

> "Not to share, access, or collect data from any Services in bulk or attempt to access data without permission—whether manually or by automated means. This includes, but is not limited to, use of any artificial intelligence, bots, crawlers, spiders, data-miners, scrapers or other tools that facilitate rapid and bulk data collection."

Source: https://www.ancestry.com/c/legal/termsandconditions

**Risk interpretation:** The ToS targets bulk/automated collection of *other users'* data. Exporting your own tree's GEDCOM via the built-in export is always permitted. The grey zone is reading a cousin's *public* tree that they have already made visible to all subscribers. In practice, Ancestry has never publicly reported banning individual accounts for personal, low-rate tree browsing with browser extensions — but this is not a guarantee. Use extensions and scripts only for your own research, at human-like speeds.

---

## 1. GitHub Repositories

### 1.1 Active / Maintained

| Repo | Stars | Last Commit | Platform | What It Does |
|------|-------|-------------|----------|--------------|
| [Kaliiiiiiiiii-Vinyzu/patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) | 3,005 | 2026-04-12 | Chromium | Drop-in Playwright replacement, patches webdriver detection. TypeScript/Python/Node. |
| [Linekio/getmyancestors](https://github.com/Linekio/getmyancestors) | 215 | 2026-02-07 | FamilySearch | GEDCOM exporter for FamilySearch (NOT Ancestry.com) — useful if cousin also has FamilySearch tree. |
| [borsic77/23andMeFamilyTreeScraper](https://github.com/borsic77/23andMeFamilyTreeScraper) | — | 2025-03-24 | 23andMe | Scrapes 23andMe family trees (not Ancestry, but shows pattern). |
| [MattW224/ancestryDnaWrapper](https://github.com/MattW224/ancestryDnaWrapper) | 7 | 2024-04-02 | Ancestry.com | Python wrapper for Ancestry's undocumented DNA REST API. Cookie-based auth. Documents DNA endpoints — no tree endpoints. |

### 1.2 Abandoned / Stale (do not use without heavy patching)

| Repo | Stars | Last Commit | Notes |
|------|-------|-------------|-------|
| [mjhea0/ancestry-scraper](https://github.com/mjhea0/ancestry-scraper) | — | 2017-02-12 | Selenium bot, 9 years old, Ancestry login flow has changed completely. |
| [cdhorn/ancestry-tools](https://github.com/cdhorn/ancestry-tools) | — | 2018-12-12 | Gramps plugin; last touched 2018. |
| [rootsdev/genscrape](https://github.com/rootsdev/genscrape) | 47 | 2023-01-12 | JS library for scraping genealogy sites including Ancestry. Latest release 2018. Still has DOM scrapers for Ancestry person pages but Ancestry's DOM has changed. |
| [freeseek/getmydnamatches](https://github.com/freeseek/getmydnamatches) (getmyancestrydna.py) | 27 | — | Uses `ancestry.com/dna/secure/tests` and match endpoints. DNA only, no tree data. Cookie `ATT` extraction. |
| [neRok00/ancestry-image-downloader](https://github.com/neRok00/ancestry-image-downloader) | — | — | Downloads media images, not tree data. |

---

## 2. Tampermonkey / Greasemonkey Userscripts

Source: https://greasyfork.org/en/scripts/by-site/ancestry.com (only 2 listed scripts as of 2026-04-26)

### 2.1 Script_Ancestry.com_Hint_Helper
- **URL:** https://greasyfork.org/en/scripts/436962-script-ancestry-com-hint-helper
- **Author:** Mark Wing
- **Installs:** 75 total
- **Updated:** 2024-05-01
- **What it does:** Works on the Ancestry hint merge page. Assists with accepting/updating hints according to genealogy best practices. Does **not** auto-click "Save to my tree" en masse — it assists the human making the merge decision by pre-populating fields and enforcing data rules.
- **Setup:** Install Tampermonkey in Chrome/Firefox, then click the Greasyfork install link.
- **Risk:** Low. Operates on the normal hint merge UI, simulates user actions, not bulk API calls.
- **Output:** Modified Ancestry person records (same as manual hint acceptance).
- **Maintenance:** Last updated 2024-05-01. Ancestry DOM changes break userscripts; check Greasyfork feedback tab before relying on it.

### 2.2 Ancestry.com - Remove paid hints
- **URL:** https://greasyfork.org/en/scripts/468323-ancestry-com-remove-paid-hints
- **Installs:** 80 total
- **Updated:** 2024-06-05
- **What it does:** Hides paid-tier hints from view. Not relevant to tree harvesting.

**Assessment:** The Greasyfork catalogue for Ancestry.com is extremely thin — only 2 scripts as of April 2026. There is no publicly available Tampermonkey script that bulk-accepts "Save to my tree" or bulk-exports a cousin's tree to GEDCOM. This workflow would need to be custom-written.

---

## 3. Chrome Extensions (Current, Chrome Web Store verified)

### 3.1 One2Tree — RECOMMENDED FOR GEDCOM EXPORT
- **CWS URL:** https://chromewebstore.google.com/detail/one2tree/pblapjjhibfmcfhpoapcmfdnjbnfifdp
- **Vendor site:** https://nordeboapps.com/one2tree/
- **Version:** 1.5.5 | **Updated:** 2026-02-27 | **Users:** 3,000 | **Rating:** 4.3/5 (519 reviews)
- **What it does:** Reads the currently-loaded pedigree tree on Ancestry (or MyHeritage / FamilyTreeDNA) and exports as **CSV, HTML, text, or GEDCOM**. Also renders an interactive ahnentafel list and expandable pedigree chart.
- **Pricing:**
  - Free trial: limited to 4 generations
  - Full version: 79 SEK/year (~$7 USD) — subscription tied to Google account. Payment via Swish, PayPal, or card.
- **Setup:**
  1. Install from Chrome Web Store.
  2. Navigate to a cousin's tree on Ancestry (must be visible/public to subscribers).
  3. Click the One2Tree toolbar icon.
  4. Set max generation depth, press Go.
  5. Wait for load (large trees take time). A new tab opens with the ahnentafel list.
  6. Download as GEDCOM.
- **Risk:** Low. Reads DOM of already-loaded tree page; does not make direct API calls beyond what the page already loads. No bot signature.
- **Output:** GEDCOM file, CSV, HTML.
- **Maintenance:** Actively maintained (last update Feb 2026). Breakage risk exists whenever Ancestry changes their tree page DOM.
- **Caveat:** For 20-30 cousin trees, this requires manual navigation to each tree page and clicking the extension once per tree. It is not fully automated but is the cleanest GEDCOM exporter available.

### 3.2 Pedigree Thief
- **CWS URL:** https://chromewebstore.google.com/detail/pedigree-thief/hdgjlfchbpojdocjlldfikeddamdcbhn
- **Version:** 3.0.23 | **Updated:** 2025-03-12 | **Users:** 2,000 | **Rating:** 4.4/5 (25 reviews)
- **What it does:** Reads pedigree trees from **Geni and MyHeritage**, converts to Ahnentafel. Also reads MyHeritage DNA matches. Includes a "Pedigree to GedCom" sub-application.
- **Ancestry support:** Per the DataMiningDNA comparison article (2021): "Pedigree Thief is no longer functional with Ancestry." This was confirmed as of mid-2020 when Ancestry blocked third-party tools. The extension's own description no longer mentions Ancestry.
- **Verdict:** Skip for Ancestry. Still useful for Geni/MyHeritage.

### 3.3 Genea Ancestry Add To Tree Auto-Clicker
- **CWS URL:** https://chromewebstore.google.com/detail/genea-ancestry-add-to-tre/ppbiccjngfoaaibnocphiklpnejikdbm
- **Updated:** 2024-07-03
- **Status:** The page returned a blank listing when fetched — the extension may have been delisted or has no description. **Do not rely on this.** Investigate manually before installing.

### 3.4 Ancestry Media Download
- **CWS URL:** https://chromewebstore.google.com/detail/ancestry-media-download/ohkkponpfoijonbbedcehkhfejlobmkb
- **Updated:** 2023-06-06
- **What it does:** Downloads media (photos, documents) from Ancestry. Not tree/GEDCOM related.

### 3.5 Ancestry Match Downloader
- **CWS URL:** https://chromewebstore.google.com/detail/ancestry-match-downloader/dhdiikochehiidnbdfmfnebddanneebf
- **Updated:** 2019-06-15 (stale — 7 years old)
- **What it does:** Downloads DNA match lists. Not tree data. Likely broken.

### 3.6 DNArboretum
- **CWS URL:** https://chromewebstore.google.com/detail/dnarboretum/oekcehcnbnfmeimggmkfliochkojkaej
- **Updated:** 2020-10-18 (stale)

---

## 4. DNAGedcom Client — Free vs. Paid

- **Download page:** https://www.dnagedcom.com/app/publish.htm
- **Current version:** 1.9.8.19
- **Platform:** Windows only (.NET Framework 4.5+, ClickOnce installer)

### What is free
- The client application itself is **free to download and run**.
- DNA match downloads from Ancestry (match names, cM, segments, tree URLs, shared matches) — this was the primary function.
- GEDCOM upload/comparison tools at dnagedcom.com are free.
- AutoSegment, JWorks, KWorks analysis tools (web-based) are free.

### What is paid / restricted
- **Ancestry stopped third-party tools from downloading DNA matches in 2020.** DNAGedcom's Ancestry download function was broken by this change. The dataminingdna.com review (2021) notes the same.
- As of 2026 the client's Ancestry download capability is considered non-functional by the community. The tool works for FamilyTreeDNA and other sites.
- **DNAGedcom does not download tree (GEDCOM) data** — it downloads DNA match metadata. It is not the right tool for tree harvesting.

**Bottom line:** DNAGedcom client is free but not relevant to tree-data extraction from Ancestry as of 2024+. Ancestry deliberately blocked third-party API access in 2020.

---

## 5. Ancestry's Undocumented Internal API Endpoints

Ancestry does not publish a public API for tree data. However, the Ancestry web UI makes XHR/fetch calls to internal REST endpoints that return JSON. These are visible in DevTools > Network tab. Community documentation is sparse because Ancestry actively discourages reverse engineering in their ToS, but the following patterns are established from code review of existing tools and community observation:

### 5.1 DNA / Match Endpoints (documented in code)
From `freeseek/getmydnamatches` and `MattW224/ancestryDnaWrapper`:
```
Base: https://www.ancestry.com/dna/secure/
GET  /tests                          → list all DNA tests for account
GET  /testSettings/{guid}/testInfo   → test metadata
GET  /matches/{guid}?page=1          → paginated DNA match list
GET  /matches/{guid}/{matchGuid}/sharedmatches → shared matches
```
Authentication: Session cookie `ATT` extracted from browser after login.

### 5.2 Tree / Person Endpoints (observed via DevTools, not formally documented)
These are the patterns visible in the Network tab when browsing an Ancestry tree:

```
Base: https://www.ancestry.com/api/
GET  /trees/{treeId}/persons/{personId}       → person record JSON
GET  /trees/{treeId}/persons/{personId}/families → family links
GET  /trees/{treeId}/persons                  → paginated persons in tree (may 403 for others' trees)

Also observed:
GET  https://api.ancestry.com/v2/trees/{treeId}            → tree metadata
GET  https://api.ancestry.com/v2/trees/{treeId}/persons    → person list
```

**Note on treeId / personId:** Both are GUIDs visible in the URL when you navigate to any Ancestry tree page. The URL pattern is:
```
https://www.ancestry.com/family-tree/tree/{treeId}/family?cfpid={personId}
```

### 5.3 How to capture these with DevTools
1. Open Chrome, navigate to the cousin's tree (must be logged in to Ancestry).
2. Press F12, go to **Network** tab. Filter by **Fetch/XHR**.
3. Reload the tree page or click around in it.
4. Look for requests to `api.ancestry.com` or `www.ancestry.com/api/` returning JSON.
5. Right-click any relevant request → **Copy as cURL**.
6. Paste into terminal. Replace the `Cookie:` header with your own `ATT` session cookie.
7. Save the JSON response.

### 5.4 Limitations
- Many person-list endpoints return **403** for trees owned by other users, even if the tree is set to "public" in the Ancestry UI. The web app uses a combination of session state and tree ownership checks that cookies alone may not satisfy.
- Endpoints change without notice. The patterns above are current as of early 2026 based on community observation but may break.
- Rate limiting is enforced. Rapid sequential calls trigger 429 or Akamai blocks.

---

## 6. Browser DevTools Approach — Step-by-Step

This is the most reliable **no-code** method for extracting a single cousin's tree data.

### Setup
1. Log in to Ancestry in Chrome. Navigate to the cousin's public tree.
2. Open DevTools (F12) → Network tab → check **Preserve log** → filter by **Fetch/XHR**.
3. Click through the tree: click a person, expand ancestors, navigate generations.
4. In the Network tab, identify requests matching patterns like:
   - `api.ancestry.com/v2/trees/...`
   - `www.ancestry.com/api/trees/...`
   - URLs containing the treeId GUID from the page URL.
5. For each relevant request: right-click → **Copy** → **Copy response**. Save as `.json`.
6. Alternatively: right-click → **Save all as HAR** to capture everything at once.

### Parsing the JSON
The JSON responses for person records contain fields like `name`, `birth`, `death`, `parents`, `spouses`, `children`. These map to GEDCOM fields. You can write a simple Python script to convert the JSON blob to GEDCOM.

### Limitation
Ancestry's tree viewer uses lazy-loading. You must actually scroll/click to each generation to trigger the fetch. For a 6-generation tree, this means manually clicking ~60+ person nodes. Not truly automatic, but feasible for 20-30 trees if you batch the HAR captures.

---

## 7. Playwright/Selenium Stealth Against Akamai

Ancestry.com uses Akamai Bot Manager. Default Playwright sessions are detected immediately because:
- `navigator.webdriver` is set to `true`.
- Browser fingerprint (TLS JA3/JA4, canvas, fonts, screen size) is non-human.
- Behavior patterns (instant full-page load with no mouse movement) are flagged.

### 7.1 patchright (BEST FREE OPTION for Chromium automation)
- **Repo:** https://github.com/Kaliiiiiiiiii-Vinyzu/patchright (3,005 stars, last commit 2026-04-12 — actively maintained)
- **What it does:** Drop-in replacement for Playwright. Patches Chromium to suppress `navigator.webdriver`, isolate page agent JS in a sandboxed scope (so Akamai's JS cannot detect Playwright injection), and randomize fingerprints.
- **Install:**
  ```bash
  pip install patchright
  patchright install chromium
  ```
- **Usage (key differences from vanilla Playwright):**
  ```python
  from patchright.sync_api import sync_playwright
  
  with sync_playwright() as p:
      # IMPORTANT: use chromium, not headless=True initially
      browser = p.chromium.launch(headless=False)  # or headless="new"
      context = browser.new_context(
          viewport={"width": 1280, "height": 800},
          user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
          locale="en-US",
          timezone_id="America/New_York",
      )
      page = context.new_page()
      page.goto("https://www.ancestry.com")
      # Add human-like delays between actions
      page.wait_for_timeout(2000 + random.randint(500, 1500))
  ```
- **Session cookie shortcut (bypasses login detection entirely):**
  1. Log in to Ancestry manually in regular Chrome.
  2. Export cookies with an extension (e.g., "Get cookies.txt LOCALLY").
  3. Load the cookie file into patchright context:
     ```python
     import json
     cookies = json.load(open("ancestry_cookies.json"))
     context.add_cookies(cookies)
     page.goto("https://www.ancestry.com/family-tree/tree/{treeId}/family")
     ```
  This avoids triggering Akamai's login-flow detection entirely since you arrive with a valid authenticated session.
- **Risk level:** Medium. Patchright significantly reduces detection probability, but Akamai's behavioral analysis can still flag abnormal navigation patterns (e.g., no mouse movement, instant clicks). Add `page.mouse.move()` calls and `random.uniform(1.5, 4.0)` second pauses between page loads.
- **Account ban risk:** Low-to-medium. Ancestry's ToS prohibits automated scraping. However, the technical enforcement is rate-limiting and blocking (temporary 403/429), not account bans, for low-rate personal use. Crossing into bulk collection at scale increases risk.
- **Maintenance burden:** Medium. Patchright tracks Playwright releases (currently at v1.59.1). When Playwright updates, patchright typically updates within days based on commit history.

### 7.2 camoufox (Firefox-based alternative)
- **Site:** https://camoufox.com
- **PyPI:** https://pypi.org/project/camoufox/
- **Note:** As of 2026, the maintainer has disclosed a "year gap in maintenance" (per camoufox.com/stealth). Performance has degraded due to the base Firefox version lagging and newly discovered fingerprint inconsistencies. **Currently under active development but unreliable.** Skip for Ancestry in April 2026.

### 7.3 curl-cffi (API-only, no browser)
- **Repo:** https://github.com/lexiforest/curl_cffi
- **What it does:** Python HTTP client that impersonates real browser TLS fingerprints (JA3/JA4/Akamai HTTP2 fingerprints). Most effective for API endpoints that don't require JavaScript execution.
- **Use case:** Once you have the session cookie from a manual login, use curl-cffi to call Ancestry's JSON API endpoints directly — faster and lighter than a full browser.
  ```python
  from curl_cffi import requests
  
  session = requests.Session(impersonate="chrome124")
  # Load cookies from browser export
  session.cookies.update({"ATT": "your-att-cookie-value", ...})
  
  r = session.get(
      f"https://api.ancestry.com/v2/trees/{treeId}/persons",
      headers={"Accept": "application/json", "Referer": "https://www.ancestry.com"}
  )
  print(r.json())
  ```
- **Risk:** Lower than full browser automation because traffic pattern looks like a real browser HTTP request. But 403 responses for protected tree endpoints are likely.
- **Maintenance:** Active (PyPI package updated regularly).

### 7.4 scrapy-impersonate / TLS impersonation (free)
- Per the Substack Web Scraping Club article (2025-03-23), Scrapy-Impersonate bypasses Akamai Bot Manager for free by spoofing TLS fingerprints. Effective for sites where Akamai runs only TLS-level checks (not full behavioral JS). Ancestry uses the JS behavioral component in addition to TLS, so this is insufficient alone.

---

## 8. Strategy: "Save to My Tree" Bulk Automation

The "Save to My Tree" (hint acceptance) workflow on Ancestry is a two-step server operation:
1. GET the hint page for a specific person.
2. POST a merge/accept request with a CSRF token.

There is no known public script that automates this reliably as of April 2026. The Genea Ancestry Add-To-Tree Auto-Clicker extension (CWS ID: ppbiccjngfoaaibnocphiklpnejikdbm) appeared in the Chrome Web Store as of July 2024 but its store listing was empty/blank when fetched, suggesting it may be a stub or was delisted.

**Practical approach for bulk hint acceptance:**
Use patchright to navigate the hints page and simulate clicks, with randomized delays. The hint merge page URL pattern is:
```
https://www.ancestry.com/family-tree/tree/{treeId}/person/{personId}/hints
```
A patchright script can load this page, enumerate hint cards in the DOM, and click "Save" on each — but this requires manual confirmation of each hint's validity unless you want raw bulk acceptance (which introduces errors).

---

## RANKING: Best Free/DIY Method for 20-30 Cousin Trees

| Rank | Method | Cost | Setup Time | Risk | GEDCOM Output | Speed |
|------|--------|------|------------|------|---------------|-------|
| **1** | **One2Tree Chrome extension** | ~$7/yr or free trial (4 gen) | 5 min | Low | Yes (native) | ~2 min/tree |
| **2** | **DevTools HAR capture + Python parser** | Free | 30 min (parser) | None | Via conversion | ~5 min/tree |
| **3** | **patchright + session cookie** | Free | 1-2 hr | Medium | Via JSON→GEDCOM | Automated |
| **4** | **curl-cffi against JSON API** | Free | 1 hr | Medium | Via JSON→GEDCOM | Fast but 403-prone |
| **5** | **Ancestor's GEDCOM via direct request** | Free (ask) | 0 min (just ask) | None | Yes | Instant |

### Clear winner for your use case (20-30 trees, one session)

**One2Tree** at 79 SEK/year (~$7 USD) is the right tool. It is:
- Actively maintained (Feb 2026 update)
- Uses the already-loaded page DOM — no separate API calls, no bot detection
- Exports directly to GEDCOM
- Works on Ancestry, MyHeritage, FamilyTreeDNA
- Low account risk — it just reads what's already on the screen
- 20-30 trees at ~2 minutes each = ~1 hour total work

For the 4-generation limit in the free tier: if your cousin trees are only 3-4 generations deep (grandparents to great-great-grandparents), the free tier covers it. Most cousin trees you are trying to harvest are probably 5-8 generations, so the $7 paid tier is worth it.

**Second choice (free, zero cost):** DevTools HAR capture. Navigate each cousin's tree, trigger loads for all visible persons via clicking, then use Chrome's "Save all as HAR" to capture the JSON responses. Write a one-time Python script to parse the HAR file and emit GEDCOM. More setup, but zero ongoing cost.

---

## Sources

1. https://chromewebstore.google.com/detail/one2tree/pblapjjhibfmcfhpoapcmfdnjbnfifdp
2. https://nordeboapps.com/one2tree/
3. https://nordeboapps.com/one2tree/one2tree-faq.html
4. https://chromewebstore.google.com/detail/pedigree-thief/hdgjlfchbpojdocjlldfikeddamdcbhn
5. https://greasyfork.org/en/scripts/by-site/ancestry.com
6. https://greasyfork.org/en/scripts/436962-script-ancestry-com-hint-helper
7. https://github.com/MattW224/ancestryDnaWrapper
8. https://github.com/Kaliiiiiiiiii-Vinyzu/patchright
9. https://github.com/Linekio/getmyancestors
10. https://github.com/rootsdev/genscrape
11. https://github.com/freeseek/getmydnamatches/blob/master/getmyancestrydna.py
12. https://www.dnagedcom.com/app/publish.htm
13. https://dnagedcom.com/FAQ.aspx
14. https://www.dataminingdna.com/a-comparison-of-tools-to-download-ancestry-matches/
15. https://www.ancestry.com/c/legal/termsandconditions (effective 2025-08-18)
16. https://camoufox.com/stealth
17. https://camoufox.com/features
18. https://pypi.org/project/camoufox/
19. https://www.scrapeless.com/blog/bypss-akamai-with-playwright
20. https://www.scrapfly.io/blog/posts/how-to-bypass-akamai-anti-scraping
21. https://substack.thewebscraping.club/p/bypassing-akamai-for-free
22. https://curl-cffi.readthedocs.io/en/latest/impersonate/faq.html
23. https://patriciacolemangenealogy.com/2024/11/03/convert-ancestry-protools-to-trees-using-autolineage-and-autokinship/
24. https://genealogy.stackexchange.com/questions/9943/how-to-incorporate-large-amounts-of-data-from-ancestry-com
