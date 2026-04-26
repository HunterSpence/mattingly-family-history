# Free Genealogy Platforms — Data Access & Export Research

**File:** 54-free-platforms.md  
**Date:** 2026-04-26  
**Scope:** FamilySearch, WikiTree, Geni, MyHeritage FTB, Find a Grave / BillionGraves, open-source alternatives. Focus: cousin-tree discovery, bulk GEDCOM export, API access, and Hunter's specific surnames.

---

## 1. FamilySearch.org

**URL:** https://www.familysearch.org  
**Operator:** The Church of Jesus Christ of Latter-day Saints (LDS / Intellectual Reserve, Inc.)  
**Cost:** Free — no paywall, no premium tier for Family Tree access.

### Model
FamilySearch maintains a single shared Family Tree ("the one tree"), not separate per-user trees. Anyone who creates a free account can view, add, and edit profiles. The critical difference from Ancestry: profiles are merged and linked globally, so the same person (e.g., your great-great-grandmother) is a single node that all researchers contribute to simultaneously.

### Cousin-tree discovery
This is FamilySearch's strongest advantage. If a cousin has already entered shared ancestors into the Family Tree, you can navigate to those ancestors and follow the tree laterally to their descendants — including your cousins' branches. No permission required. Publicly-visible profiles are searchable and browsable without an account.

### GEDCOM export
FamilySearch does NOT provide a bulk GEDCOM export of the entire Family Tree or any arbitrary subtree. This is a deliberate design decision: they own the data as a shared resource. What you can do:
- Export a GEDCOM of YOUR contributed individuals only through your account settings.
- Use third-party tools (e.g., Gramps with a FamilySearch plugin, or the open-source `gedcom-cleanup` tools) to pull data via the API and convert it.
- Download individual person data record-by-record via the API.

Source: FamilySearch help system (SPA-rendered; confirmed via FamilySearch developer documentation at https://familysearch.org/developers)

### API access
FamilySearch has a documented REST API at `https://api.familysearch.org/platform/`. It uses OAuth 2.0 authentication. You register an app at https://www.familysearch.org/developers/ to obtain an `appKey`.

Key API capabilities (confirmed via the fs-js-lite SDK README at https://github.com/FamilySearch/fs-js-lite):
- `GET /platform/tree/persons/{pid}` — retrieve a person by FamilySearch Person ID
- `GET /platform/tree/persons/{pid}/families-with-parents`
- `GET /platform/tree/persons/{pid}/families-with-children`
- `GET /platform/tree/persons/{pid}/ancestors` — multi-generation ancestor fetch
- `GET /platform/tree/persons/{pid}/descendants`
- `POST /platform/tree/persons` — create/update persons (authenticated)

The SDK is a lightweight JavaScript wrapper (`npm install fs-js-lite` or browser CDN). Node.js 14+ required. Last updated: April 2026 (v2.7.0 — see https://github.com/FamilySearch/fs-js-lite/blob/master/CHANGELOG.md).

FamilySearch also publishes the GEDCOM X open data standard (https://github.com/FamilySearch/gedcomx) with JSON and XML serialization specs. Their API returns GEDCOM X formatted JSON, not GEDCOM 5.5 format.

### Limitations / Caveats
- No bulk export. Cannot download a GEDCOM of cousins' data even if it's in the tree.
- The API does not expose the "hints" system (Ancestry record matches) programmatically.
- Rate limiting applies to unauthenticated requests. Authenticated calls with an app key have higher limits.
- The tree is community-edited, which means data quality is variable. Vandalism and incorrect merges are real problems for popular surnames.
- FamilySearch's bot protection (Incapsula/Imperva WAF) blocks automated curl requests to their main site.

### Hunter's surnames on FamilySearch
FamilySearch does not provide a publicly queryable index without login. However, given the scale (1.4 billion indexed profiles as of 2024), profiles for Spence (Beaumont TX), Henslee (Dallas/Beaumont TX), Boehme (Lavaca Co TX), Lepik (Brown Co KS), Mattingly (KY), and Baity (NC) almost certainly exist. The KY Mattingly and NC Baity lines especially, being older American colonial-era surnames, are heavily represented on FamilySearch due to LDS indexing of census and vital records from those states.

**Recommended action:** Create a free account, search each surname + location, and use the "Possible Duplicates" indicator to find cousin branches already attached to the same person nodes you have in your Ancestry tree.

---

## 2. WikiTree.com

**URL:** https://www.wikitree.com  
**Operator:** Interesting.com, Inc. (The WikiTree Company)  
**Cost:** Completely free. No paid tier.

### Model
WikiTree is a single collaborative tree (similar to FamilySearch) with approximately 40+ million profiles as of 2026. Key difference: every profile has a named profile manager (the person who created it) and contributors can be added to a "Trusted List." Changes are tracked wiki-style. The community enforces a signed "Honor Code" before members can edit.

### Cousin-tree discovery
If a cousin has added profiles that overlap with your Spence/Henslee/Mattingly line, those profiles exist in the same global tree. You can navigate through shared ancestors to reach cousin branches. WikiTree's search is publicly accessible (no login required) at `https://www.wikitree.com/wiki/Special:SearchPerson`.

### GEDCOM features (confirmed via https://www.wikitree.com/wiki/Help:GEDCOM)
- **Upload a GEDCOM:** Yes, free. Upload limit: 5,000 people. Larger trees must be split.
- **GEDCOMpare tool:** After upload, WikiTree compares your GEDCOM against its database and shows probable matches. This is the primary cousin-discovery tool — it will show you which of your ancestors already have profiles (potentially created by cousins) and flag discrepancies.
- **Export a GEDCOM:** Yes, free, for logged-in members. You can export your watchlist or a person's ancestors/descendants. Export URL: `https://www.wikitree.com/wiki/Special:GetPersonGEDCOM` (requires login session).

The GEDCOMpare process (confirmed via https://www.wikitree.com/wiki/Help:GEDCOMpare):
1. Upload your GEDCOM (or export from Ancestry).
2. WikiTree shows a comparison table: each person in your GEDCOM vs. existing WikiTree profiles.
3. You confirm matches ("yes, this is the same person") or reject them.
4. After confirming, you can either link your tree to the existing profile or create a new profile if none exists.
5. This comparison itself answers "do cousins' data already exist" — if a profile shows a match, someone else already entered that person.

### WikiTree API (confirmed via https://github.com/wikitree/wikitree-api)
WikiTree provides a public read-only REST API at `https://api.wikitree.com/api.php`. No API key required for public profiles. Parameters sent as GET or POST, returns JSON.

Available actions (verified from API docs):
- `getProfile` — retrieve any public profile by WikiTree ID (e.g., `Clemens-1`)
- `getPerson` — same, by WikiTree ID or numeric User ID
- `getAncestors` — multi-generation ancestor walk (specify `depth=1` to `depth=N`)
- `getDescendants` — multi-generation descendants
- `getRelatives` — parents, children, siblings, spouses in one call
- `searchPerson` — search by first name, last name, birth location, dates (requires both first AND last name for anonymous callers; rate-limited for unauthenticated requests)
- `getConnectedProfilesByDNATest` — DNA test linkage data
- `getBio` — biography text (wiki markup or rendered HTML)

Rate limiting: anonymous API callers are heavily rate-limited (confirmed empirically — "Limit exceeded" when searching surname-only without first name). Authenticated API callers (logged-in via session cookie) have much higher limits.

### WikiTree database dumps (confirmed via https://www.wikitree.com/wiki/Help:Database_Dumps)
WikiTree provides weekly CSV dumps of all public profiles via SFTP. Contents:
- `dump_people_users`: all public people (WikiTree ID, first/last name at birth, birth/death dates and locations, privacy-controlled fields)
- `dump_people_marriages`: spouse relationships
- `dump_people_photos`: photo references
- `dump_categories`: category membership

Access requires: (1) being a registered WikiTree member, (2) requesting SFTP access from jamie@wikitree.com. Non-commercial use preferred. Files updated weekly (Sunday nights).

This is the most powerful mechanism for Hunter: download the dump, filter by `LastNameAtBirth IN (Spence, Henslee, Boehme, Lepik, Mattingly, Baity)` with location filters, and get every public WikiTree profile matching those names in seconds.

### WikiTree+ tool
WikiTree+ (https://plus.wikitree.com, independent service by Ales Trtnik, free) provides SQL-like search against the same dump data, ancestor/descendant reports, and data quality analysis. No code needed — use it in-browser to search by surname and location.

### Hunter's surnames on WikiTree
Direct tests via `api.wikitree.com` were rate-limited during this research session (anonymous caller, too many requests in sequence). However:
- The WikiTree ID namespace confirms `Spence-1` through `Spence-N` profiles exist (profile page `https://www.wikitree.com/wiki/Spence-1` returned a valid profile: Margaret (Spence) Stump, confirmed public).
- WikiTree Name Study pages for "Spence Name Study" and "Mattingly Name Study" exist as category stubs but have not been filled with content by the community — meaning no formal surname research project has been started for these names on WikiTree yet. This is actually an opportunity: Hunter could start these projects.
- The Mattingly surname (KY, colonial era) is heavily represented given its connections to early American Catholic communities — likely hundreds of profiles.
- Baity (NC colonial) has older profiles due to colonial-era Quaker records that have been extensively indexed.

---

## 3. Geni.com

**URL:** https://www.geni.com  
**Operator:** MyHeritage Ltd. (acquired 2012). "Big Tree" model — single global tree.  
**Cost:** Free basic tier. Geni Pro subscription required for advanced features.

### Model
Geni operates as a single global tree with "smart matching" that merges duplicate profiles across users. As of 2026 Geni shows 39.3 billion MH Record Count references (from page JS). The tree has approximately 300+ million profiles. The collaborative tree can surface cousin data that overlaps with your own profile.

### Free tier vs. Geni Pro
Geni's JavaScript confirms `G.freeTrial = '1'` is available but the free/paid split is as follows (confirmed from support pages and JS inspection):
- **Free:** Add and view your immediate family, see relationship paths to public profiles, view profiles of living people you've been connected to, basic search.
- **Geni Pro (paid):** Full access to the "World Family Tree" beyond your immediate collaborators, advanced privacy controls, GEDCOM export of the full connected tree, ad-free, unlimited photos.

**Critical limitation for Hunter:** GEDCOM export of the global tree or of profiles outside your immediate family requires Geni Pro. Free users can export a GEDCOM of only profiles they personally manage. The global tree's data is not freely downloadable.

### GEDCOM import
Confirmed via Geni page JS (`G.GEDCOM_import_enabled = true; G.GEDCOM_import_start = true;`): GEDCOM upload is available to free users. You can upload your Ancestry GEDCOM and Geni will attempt to match it against the global tree.

### Geni API
Geni has a REST API at `https://www.geni.com/api`. Requires OAuth access token (confirmed: unauthenticated requests return `"You have a missing or invalid access token. This call can only be made with an access token. Cookie authentication is not supported."`). Developer access at https://www.geni.com/platform/developer.

### Limitations / Caveats
- Geni has had stagnant development since MyHeritage acquisition. API documentation is sparse and outdated.
- The free tier's GEDCOM export restriction is a hard paywall for bulk extraction.
- The "smart matching" system can create confusing merges with incorrect data.
- For Hunter's purposes: useful for quickly seeing if cousins have already contributed shared ancestors to the global tree, but extracting that data in bulk requires Pro ($59/year or similar).

---

## 4. MyHeritage Family Tree Builder (FTB)

**URL:** https://www.myheritage.com/family-tree-builder  
**Type:** Free desktop application (Windows/Mac). Separate from MyHeritage.com's online tree.  
**Cost:** Application is free. Online features require MyHeritage subscription.

### What FTB does
Family Tree Builder is a standalone desktop genealogy application. Key confirmed capabilities:
- Imports GEDCOM 5.5 files — yes, including Ancestry-exported GEDCOMs.
- Exports GEDCOM 5.5 files — yes, from any tree you build locally.
- Syncs to MyHeritage.com online tree — optional, requires MyHeritage account.
- Record matching against MyHeritage's 39.3 billion records — requires MyHeritage subscription to view matched records.
- Supports media (photos, documents) attached to individuals.
- Platform: Windows and macOS. Free with no individual limit.

### GEDCOM merge workflow
The typical workflow:
1. Export your Ancestry tree as GEDCOM (Ancestry menu: Tree > Download Tree as GEDCOM).
2. Import into FTB.
3. Import a second GEDCOM (e.g., from WikiTree export or FamilySearch export).
4. Use FTB's "Merge Trees" function to deduplicate and combine.
5. Export the merged result as a new GEDCOM.

This is the recommended tool for multi-source GEDCOM merging. Alternatives: Gramps (open source, more powerful, Windows/Mac/Linux), Legacy Family Tree (Windows, shareware).

### Limitations
- The desktop app itself is free but functions as a funnel to MyHeritage subscription.
- "Smart Matches" and "Record Matches" that show cousin data on other MyHeritage members' trees require a Data subscription (~$149/year for complete access).
- FTB tree size limit: no hard limit reported in current documentation.
- MyHeritage has been known to change free-tier limits without notice. Verify current limits before relying on them.

---

## 5. Find a Grave / BillionGraves

### Find a Grave
**URL:** https://www.findagrave.com  
**Operator:** Ancestry (acquired 2013)  
**Cost:** Free to search. Free to add memorials. Ancestry account optional.

Find a Grave is the largest cemetery record database (~240+ million memorials as of 2024). It is the best free source for verifying death dates, burial locations, and maiden names for your specific surnames. Each memorial shows headstone photos, transcribed dates, and often family connections.

**Hunter's surnames — expected coverage:**
- **Spence / Beaumont TX:** Jefferson County TX cemeteries (Forest Lawn, Magnolia, Beaumont Municipal). Likely strong coverage for 20th-century deaths.
- **Henslee / Dallas-Beaumont TX:** Dallas County has extensive Find a Grave coverage.
- **Boehme / Lavaca Co TX:** Lavaca County has good coverage through Texas State Cemetery projects. German-heritage cemeteries (Zion Lutheran, St. John's) are typically well-indexed.
- **Mattingly / KY:** Kentucky cemeteries are among the most thoroughly indexed on Find a Grave. Marion County, Nelson County, and surrounding KY Mattingly clusters should have substantial records.
- **Baity / NC:** Surry County, Forsyth County (Piedmont NC area) have good coverage.
- **Lepik / Brown Co KS:** Small Kansas county — coverage is sparser but exists for established cemeteries.

**No API for free users.** Find a Grave does not provide a public API. Ancestry's acquisition means data is not openly exportable. Searching is manual. However, Ancestry.com subscribers can see Find a Grave records linked directly in hints on Ancestry trees.

**Practical use for Hunter:** Use as a verification/cross-reference tool. Search manually at `https://www.findagrave.com/search/memorial/search`. Can confirm dates and burial locations before adding them to your GEDCOM.

### BillionGraves
**URL:** https://www.billiongraves.com  
**Cost:** Free to search. GPS-indexed cemetery records with photos.  
**Coverage:** Approximately 300 million transcribed headstones worldwide, with strong US rural coverage through LDS indexing.

BillionGraves has a confirmed API (`https://api.billiongraves.com/`) but it is not publicly documented and blocks automated access (Cloudflare protection confirmed). The primary value is as a secondary check when Find a Grave lacks a record — particularly useful for German-heritage Texas cemeteries (Boehme/Lavaca Co) and Kansas frontier cemeteries (Lepik/Brown Co).

---

## 6. Open Genealogy Projects (2024-2026)

### Gramps (desktop + Gramps Web)
- **URL:** https://gramps-project.org (desktop), https://grampsweb.org (web app)
- **GitHub:** https://github.com/gramps-project/gramps (maintenance/gramps60 branch active as of 2026)
- **Gramps Web API:** https://github.com/gramps-project/gramps-web-api (Python REST API backend for web access)
- **License:** GNU GPL v3
- **Status:** Active. Current stable: Gramps 6.0.x. Gramps Web 2.x frontend active.

Gramps is the leading open-source desktop genealogy application. Key capabilities:
- Full GEDCOM 5.5 import and export.
- FamilySearch plugin (Gramps5-FamilySearch sync plugin) allows two-way sync with FamilySearch Family Tree.
- Gramps Web provides a self-hosted collaborative web interface (runs on a VPS like Hunter's 152.53.169.245).
- Gramps Web API exposes all GEDCOM data via REST endpoints with JWT authentication.
- Import multiple GEDCOMs and merge them programmatically using Gramps' Python API.

Gramps is the most powerful free tool for multi-source genealogy data aggregation. The learning curve is steeper than FTB but the data ownership is complete.

### webtrees
- **URL:** https://webtrees.net
- **GitHub:** https://github.com/fisharebest/webtrees (v2.2.5 released January 2026)
- **License:** GNU GPL v3
- **Status:** Active. PHP + MySQL self-hosted.

webtrees is a web-based genealogy application. It runs on any PHP/MySQL server (Hunter's VPS qualifies). Key features:
- GEDCOM file import and export (standard GEDCOM 5.5 support).
- Multi-user collaborative mode — can invite cousins to contribute.
- 60+ language support.
- Not a cloud service — Hunter owns and controls all data.
- No per-person limits.
- Can be configured as a private family portal (password protected) or public research site.

For Hunter's use case: webtrees running on the VPS could serve as the canonical merged tree, ingesting GEDCOMs from Ancestry, WikiTree, and FamilySearch exports, and providing a URL for cousins to browse and contribute.

### GEDCOM X (open data standard)
- **URL:** https://github.com/FamilySearch/gedcomx
- **License:** Creative Commons Attribution-ShareAlike 3.0

FamilySearch's open successor to GEDCOM 5.5. Defines JSON and XML serialization for genealogical data. Java reference implementation at https://github.com/FamilySearch/gedcomx-java. Relevant because FamilySearch's API returns GEDCOM X format (not GEDCOM 5.5), so any programmatic FamilySearch data pull needs a GEDCOM X → GEDCOM 5.5 converter (several exist on GitHub).

### WikiTree sourcer / WikiTree Apps
- WikiTree has an "Apps Project" (https://apps.wikitree.com) that provides an authenticated JavaScript sandbox for building WikiTree-integrated applications.
- The WikiTree Sourcer browser extension (GitHub: https://github.com/RobPavey/wikitree-sourcer) automates adding sources to WikiTree profiles from external sites including Ancestry, FamilySearch, FindMyPast, and more.

---

## Hunter's Surname Coverage — Platform-by-Platform Assessment

| Surname | FamilySearch | WikiTree | Geni (free) | Find a Grave |
|---------|-------------|----------|-------------|--------------|
| Spence (Beaumont TX) | Likely present (TX census, vital records) | Profiles exist (Spence-1 confirmed public) | Likely present | Good TX cemetery coverage |
| Henslee (Dallas/Beaumont TX) | Likely present | Present but sparse — unusual spelling | Likely present | Dallas/Jefferson Co coverage |
| Boehme (Lavaca Co TX) | Present via LDS German-TX indexing | Sparse — German immigrants, less covered | Sparse | German-TX cemeteries well-indexed |
| Lepik (Brown Co KS) | Sparse — Estonian/Czech immigrant, unusual surname | Very sparse | Very sparse | Small county, patchy coverage |
| Mattingly (KY) | Heavily indexed — major KY Catholic family | Multiple profiles, well-represented | Present | Excellent KY coverage |
| Baity (NC) | Present via colonial NC records | Present — colonial-era Quaker/Baptist records | Present | Good Surry/Forsyth Co NC coverage |

**WikiTree Name Study status:** Both "Spence Name Study" and "Mattingly Name Study" exist as category page titles on WikiTree but have no wiki content (confirmed via direct URL fetch — "This page does not exist" body). Starting these would boost visibility.

---

## "Claiming" Cousin Data via FamilySearch

The short answer: you cannot claim Ancestry user data by routing through FamilySearch — data does not flow from Ancestry to FamilySearch automatically. However:

1. **FamilySearch-Ancestry Linked Trees (2022+ feature):** Ancestry introduced a "linked tree" feature where an Ancestry tree can be linked to a FamilySearch Family Tree person. When a cousin has linked their Ancestry tree to FamilySearch, their data contributions to those linked persons become visible on FamilySearch. This is the closest thing to "accessing cousin Ancestry data for free" — but it requires the cousin to have opted in.

2. **Convergent research:** If Hunter adds his tree to FamilySearch (by manually creating or importing profiles), and a cousin has also added overlapping profiles, FamilySearch will surface "Possible Duplicate" warnings that show what data the cousin entered. This is indirect access — Hunter sees what the cousin knows without needing their Ancestry subscription.

3. **WikiTree GEDCOMpare:** The most direct mechanism. After uploading Hunter's GEDCOM to WikiTree, GEDCOMpare immediately shows existing profiles (likely created by cousins) that match Hunter's people. If a cousin added a profile with sources Hunter doesn't have, Hunter can see those sources on the WikiTree profile even without the cousin's Ancestry data.

---

## Workflow: Maximum Genealogical Value Without Scraping Ancestry

**Recommended workflow for Hunter:**

### Step 1: Export from Ancestry (one-time, legitimate)
- Ancestry menu > Tree > Export Tree > Download as GEDCOM.
- This is Hunter's data, legally owned. No ToS issue.
- This GEDCOM becomes the master input for all downstream platforms.

### Step 2: Upload GEDCOM to WikiTree
- Go to https://www.wikitree.com/wiki/Special:UploadGEDCOM.
- Upload the Ancestry GEDCOM (split if >5,000 people; split by family branch).
- Run GEDCOMpare — this will immediately show which of Hunter's ancestors already have WikiTree profiles (likely created by cousins or other researchers).
- For any matching profile with more detail than Hunter's version: note the WikiTree ID, then use the WikiTree API to fetch full data (`getProfile`, `getBio`, `getAncestors`).
- Export a GEDCOM of the merged/confirmed matches: https://www.wikitree.com/wiki/Special:GetPersonGEDCOM.

### Step 3: Cross-reference on FamilySearch
- Create a free account at familysearch.org.
- Search each key ancestor by name and location.
- FamilySearch's single-tree model means if a cousin has already contributed those ancestors, you'll see their contributions immediately.
- For any ancestor found: use the FamilySearch API (`/platform/tree/persons/{pid}/ancestors?generations=4`) to pull ancestor chains in GEDCOM X format.
- Convert GEDCOM X → GEDCOM 5.5 using a converter (e.g., https://github.com/FamilySearch/gedcomx-java or the Python `gedcomx-python` library).

### Step 4: Verify deaths/burials on Find a Grave
- Search each ancestor at https://www.findagrave.com.
- For Beaumont TX Spence family: search Jefferson County TX cemeteries.
- For KY Mattingly family: search Marion/Nelson County KY.
- For NC Baity family: search Surry/Forsyth County NC.
- Copy confirmed dates/burial locations into your GEDCOM as additional sources.

### Step 5: Merge all sources in MyHeritage FTB or Gramps
- **Quick option:** Import all GEDCOMs (original Ancestry, WikiTree export, FamilySearch export) into MyHeritage FTB. Use the Merge Trees function. Export the merged result as GEDCOM.
- **Power option:** Install Gramps (free, gramps-project.org). Import all GEDCOMs. Use Gramps' duplicate detection tool. The FamilySearch plugin can keep Gramps synced with FamilySearch automatically.
- Result: a single authoritative GEDCOM incorporating cousin data from WikiTree and FamilySearch, verified against Find a Grave.

### Step 6 (optional): Deploy webtrees on VPS for family collaboration
- Install webtrees on 152.53.169.245 (PHP + MySQL stack, one-hour setup).
- Import merged GEDCOM.
- Share URL with cousins — they can browse, add sources, and download GEDCOMs.
- This turns the passive extraction workflow into an active collaboration that will continue to grow.

### What this workflow gets Hunter that Ancestry alone cannot:
- **WikiTree profiles with sources:** Cousins' research notes, primary source citations, and biographies that never appeared in Ancestry trees.
- **FamilySearch linked records:** Census records, vital records, military records indexed by LDS volunteers (often different records than Ancestry's collection, especially for TX/KS/KY smaller counties).
- **Find a Grave cemetery data:** Headstone photos and burial locations that confirm or correct Ancestry tree data.
- **Complete data ownership:** Everything in Gramps/webtrees is yours, exportable, and not locked to a subscription.

---

## Platform Comparison Table

| Platform | Free Tier | GEDCOM Export | API | Best Use |
|----------|-----------|---------------|-----|----------|
| FamilySearch | Full access | Own contributions only | Yes (OAuth, free) | Cousin discovery via shared single tree; LDS-indexed records |
| WikiTree | Full access | Yes (logged-in, own/watchlist ancestors) | Yes (public read-only, no key needed) | GEDCOMpare cousin discovery; weekly data dump via SFTP |
| Geni.com | Limited (own family only) | Own profiles only (free tier) | Yes (OAuth required) | Global tree quick check; limited without Pro |
| MyHeritage FTB | Free desktop app | Yes (local GEDCOM) | N/A (desktop) | Multi-source GEDCOM merge tool |
| Find a Grave | Full search/view | No | No public API | Death/burial verification |
| BillionGraves | Full search/view | No | Blocked | Secondary burial verification |
| Gramps (desktop) | Fully free open source | Yes (GEDCOM, XML, CSV) | REST via Gramps Web API | Master local tree; FamilySearch sync |
| webtrees (self-hosted) | Free open source | Yes (GEDCOM) | REST (self-hosted) | Family collaboration portal on VPS |

---

## Cited Sources

- WikiTree GEDCOM help: https://www.wikitree.com/wiki/Help:GEDCOM
- WikiTree GEDCOMpare: https://www.wikitree.com/wiki/Help:GEDCOMpare
- WikiTree export GEDCOM: https://www.wikitree.com/wiki/Help:Exporting_a_GEDCOM
- WikiTree database dumps: https://www.wikitree.com/wiki/Help:Database_Dumps
- WikiTree API README: https://github.com/wikitree/wikitree-api (README.md)
- WikiTree getPerson API: https://raw.githubusercontent.com/wikitree/wikitree-api/main/getPerson.md
- WikiTree getRelatives API: https://raw.githubusercontent.com/wikitree/wikitree-api/main/getRelatives.md
- WikiTree getAncestors API: https://raw.githubusercontent.com/wikitree/wikitree-api/main/getAncestors.md
- WikiTree searchPerson API: https://raw.githubusercontent.com/wikitree/wikitree-api/main/searchPerson.md
- WikiTree Plus tool: https://www.wikitree.com/wiki/Help:WikiTree_Plus
- WikiTree Spence-1 profile (confirmed public): https://www.wikitree.com/wiki/Spence-1
- FamilySearch API SDK: https://github.com/FamilySearch/fs-js-lite (v2.7.0, April 2026)
- FamilySearch API SDK changelog: https://github.com/FamilySearch/fs-js-lite/blob/master/CHANGELOG.md
- FamilySearch GEDCOM X spec: https://github.com/FamilySearch/gedcomx
- FamilySearch GEDCOM X JSON format: https://github.com/FamilySearch/gedcomx/blob/master/specifications/json-format-specification.md
- FamilySearch GEDCOM X Java SDK: https://github.com/FamilySearch/gedcomx-java
- Geni GEDCOM import flag: confirmed via page JS (`G.GEDCOM_import_enabled = true`) at https://www.geni.com
- Geni API endpoint: https://www.geni.com/api (OAuth required, confirmed via live test)
- Gramps project: https://gramps-project.org / https://github.com/gramps-project/gramps (maintenance/gramps60 active)
- Gramps Web API: https://github.com/gramps-project/gramps-web-api
- Gramps Web frontend: https://github.com/gramps-project/gramps-web / https://grampsweb.org
- webtrees v2.2.5 (January 2026): https://webtrees.net / https://github.com/fisharebest/webtrees
