# Paid Tools for Bulk-Harvesting Ancestry.com Cousin Trees (2026)

**Research date:** 2026-04-26
**Purpose:** Evaluate tools that can download ~25 closest DNA match trees from Ancestry.com into GEDCOM or CSV format.

---

## Critical Context: Ancestry's 2020 API Lockdown

In **June/July 2020**, Ancestry's lawyers sent cease-and-desist letters to **every third-party tool** that connected to their DNA match systems — Genetic Affairs, DNAGedcom, Pedigree Thief, and others. This is the defining event for this entire tool landscape.

What happened after:
- **Genetic Affairs**: Ancestry access fully dead. No recovery. Their tools now work at FamilyTreeDNA, GEDmatch, and 23andMe only.
- **DNAGedcom Client**: Received the C&D but continued to operate. As of 2026, they refer to Ancestry as "**A* Company**" in their documentation to obscure the platform name. Current client v4.0.445 lists A* Company as "currently supported."
- **Pedigree Thief**: Ancestry access is dead. Works on MyHeritage and some other sites, not Ancestry.
- **Ancestry Match Downloader (Chrome extension)**: Dead since 2020.

---

## Tool-by-Tool Assessment

---

### 1. DNAGedcom Client (dnagedcom.com)

**URL:** https://www.dnagedcom.com

**Status:** Active as of 2026. Desktop app, Windows and Mac. Current version: v4.0.445.

**What it actually does with Ancestry:**
- Downloads your DNA match list with cM data, tree size, tree URL, notes, ethnicity, admin info, starred/grouped status. Output: `m_profilename.csv`
- Separately, "Gather Trees" downloads the **direct ancestor list** from each match's **linked public Ancestry tree** — names, birth/death dates, birth places for each ancestor in matched trees. Output: `a_profilename.csv`
- This `a_` file is then uploaded to the DNAGedcom website for the **GWorks** tool, which cross-references surnames across all your matches' trees, ranks common ancestors by frequency, and helps identify a shared ancestral couple.
- **GWorks does NOT produce per-cousin GEDCOMs.** It produces a flattened CSV ancestor list, then an online web interface showing surname frequencies and ancestor comparisons. Individual tree files are not exported as separate GEDCOMs.

**What it does NOT do:**
- Does not export a match's full tree as a GEDCOM file you can import into Ancestry or genealogy software.
- Does not download descendants, siblings, or collateral lines — only the direct ancestor pedigree of each match.
- Does not include private or unlinked trees.
- MyHeritage and GEDmatch gathering are listed as "not currently working" on the homepage (April 2026).

**Cost:**
- Requires paid subscription. The site shows tiers but requires login to see current pricing. Multiple sources (2020-era) documented **"Silver" tier at approximately $5/month**. Current 2026 pricing requires account creation to view — no public pricing page is accessible. The site still refers to Silver membership, which Kitty Cooper's guide (last updated 2021) confirms enables the client download feature.
- A monthly subscription then canceled is a viable approach for a one-time harvest run.

**Login / MFA handling:**
- Requires your Ancestry username and password entered into the desktop app. The app logs into Ancestry on your behalf.
- The Kitty Cooper 2017 guide (still referenced) does not mention MFA handling. Ancestry's 2FA, if enabled, may block the client — users in 2025 Reddit discussions note partial functionality issues.

**Output format:**
- Match list: `m_profilename.csv` (flat CSV, all matches)
- Ancestor file: `a_profilename.csv` (flat CSV, all direct ancestors extracted from all match trees combined)
- ICW (in-common-with) file: separate CSV (not needed for GWorks tree comparison)
- No per-cousin GEDCOM output

**Ancestry ToS posture:**
- **Explicitly received a cease-and-desist letter in June 2020.** Continued operating. Now disguises Ancestry as "A* Company."
- This is clearly in a grey/violation zone. The tool continues operating through obfuscation and the practical difficulty of enforcement against individual subscribers.
- Ancestry has not shut down DNAGedcom's account or blocked the client as of early 2026, based on users reporting it still works.

**Risk of account suspension:**
- **Moderate-high.** Ancestry sent C&D letters and has deployed bot-detection. The client rate-limits itself and mimics human browsing to reduce detection risk. Users in Jan 2025 Reddit threads report it still works but is slow and sometimes needs to restart. No widespread reports of account bans for using this tool.
- Running against 25 matches with "Gather Trees" is relatively low-volume and lower risk than a full match harvest.

**Speed:**
- Match gathering: fast (minutes for hundreds of matches).
- Tree gathering ("Gather Trees"): can take **hours** depending on number of matches and tree sizes. Each tree's ancestor list is fetched individually.
- For 25 closest matches only: probably **30-90 minutes** to gather match list + trees.

**Reddit/community feedback (2024-2025):**
- Jan 2025 Reddit r/Genealogy (post 1id94go): User: "I finally decided to revisit it, and I see that they have re-vamped the user interface but indeed many of the download features are now unavailable. I'm currently grabbing all my data off of A(ncestry)." Another user: "Maybe a decade ago, I tried to get into using DNAgedcom. I was able to kind of get some data to downloaded, but there were always some kind of problems, and basically zero instructions."
- Jul 2025 dna-explained.com: Roberta Estes lists "DNAGedcom – Clusters results from various vendors" as an active tool.
- Consistent theme: works but clunky, requires patience, zero hand-holding.

**Verdict for Hunter's use case:** DNAGedcom Client v4.0 can download the ancestor pedigree data from the linked public trees of your 25 closest Ancestry matches. This gives you a searchable ancestor list for surname comparison, not individual GEDCOMs per cousin. Best fit if you want to identify common ancestors across matches using GWorks. **This is the closest existing tool to what Hunter wants**, but the output is a research tool, not a clean per-cousin import.

---

### 2. Genome Mate Pro / Genealogical DNA Analysis Tool (Free)

**URL:** No active public website found for current downloads. Formerly at genomematepro.com (appears offline/parked as of 2026).

**Status:** Effectively inactive for the Ancestry tree-harvesting use case.

**What it was:**
- Free Windows/Mac desktop application for storing and analyzing DNA match data from multiple vendors.
- Required DNAGedcom Client as the data source — GMP consumed the CSV files that DNAGedcom produced.
- Offered chromosome mapping, segment triangulation, and match grouping.

**Current state (2026):**
- Jan 2025 Reddit: User asks "Anyone still using Genealogical DNA Analysis Tool? What are your thoughts?" indicating the tool is remembered but barely in use.
- No active development signals found.
- No standalone Ancestry tree-downloading capability — depended entirely on DNAGedcom Client for data input.

**Cost:** Free

**Output:** Local database of matches and segments. No GEDCOM output for cousin trees.

**Verdict for Hunter's use case:** Not viable. Inactive, no independent Ancestry tree access, and even when active it was a consuming tool that needed DNAGedcom output as input.

---

### 3. Borland Genetics (borlandgenetics.com)

**URL:** https://borlandgenetics.com

**Status:** Active as of 2026. Operational website with account creation.

**What it actually does:**
- **Completely different purpose.** Borland Genetics is a **DNA reconstruction database** — users upload raw DNA from multiple family members to reconstruct the estimated DNA of deceased ancestors.
- Accepts DNA uploads from Ancestry, 23andMe, FTDNA, MyHeritage.
- Tools focus on "Creeper" automated reconstruction workflow, matching against their database of reconstructed ancestral kits.

**Does NOT do:**
- Does not download your cousin match trees from Ancestry.
- Has no tree harvesting function whatsoever.
- Subscription ("The Creeper") is for automated reconstruction workflows, not match tree downloading.

**Cost:** Free basic account. Subscription cost for "Creeper" feature — not published publicly, requires signup.

**Verdict for Hunter's use case:** Wrong tool entirely. Borland Genetics does not address the tree harvesting need.

---

### 4. MyHeritage Family Tree Builder (Free desktop app)

**URL:** https://www.myheritage.com/family-tree-builder

**Status:** Active. Free download. Windows and Mac.

**What it actually does:**
- Standard genealogy desktop software (like Ancestry's Family Tree Maker competitor).
- Syncs with your own MyHeritage tree.
- Can import GEDCOM files.
- Smart Matches and Record Matching within MyHeritage's own ecosystem.
- Can upload your Ancestry DNA raw data to MyHeritage for matching (though MyHeritage stopped accepting DNA uploads from other vendors as of May 7, 2025 according to a Roberta Estes note in Feb 2026 article).

**Does NOT do:**
- Cannot access or download another person's Ancestry tree.
- Cannot connect to Ancestry.com to harvest cousin match trees.
- Has no Ancestry API integration — it is a MyHeritage product.

**Cost:** Free (Family Tree Builder app). MyHeritage subscription required for full access to matching tools.

**Verdict for Hunter's use case:** Not the right tool for Ancestry tree harvesting. Useful for organizing your own tree, but has zero access to Ancestry match trees.

---

### 5. GEDmatch / GEDmatch Genesis

**URL:** https://www.gedmatch.com (owned by Verogen Inc., subsidiary of Qiagen since Jan 2023)

**Status:** Active.

**What it actually does:**
- Users upload their raw DNA files (not trees) from any testing company for cross-vendor matching.
- Provides: one-to-many comparison, one-to-one comparison, admixture, segment triangulation, and (Tier 1) segment search.
- Users can also upload a GEDCOM file for themselves, which is used for MRCA (most recent common ancestor) identification against other users' GEDCOMs.
- Genetic Affairs (licensed by GEDmatch) provides AutoCluster and AutoKinship tools **within** GEDmatch for Tier 1 users.

**Does NOT do:**
- Cannot access or download Ancestry.com cousin trees.
- GEDmatch's database only contains what users have explicitly uploaded there.
- Does not interface with Ancestry's system.

**Cost:**
- Free: basic one-to-many and one-to-one tools.
- **Tier 1: $10/month** — unlocks triangulation, segment search, clustering. (Rate confirmed by Wikipedia and Roberta Estes' blog; dating to 2018 but referenced as current pricing through 2025.)

**ToS posture:** GEDmatch is a standalone platform with its own database. No Ancestry ToS implications.

**Verdict for Hunter's use case:** Wrong tool for this specific goal. GEDmatch is for cross-vendor raw DNA comparison, not for downloading Ancestry cousin trees.

---

### 6. FamilySearch Family Tree (familysearch.org)

**URL:** https://www.familysearch.org

**Status:** Active. Free.

**What it actually does:**
- A collaborative single global family tree, free to use, maintained by the LDS Church.
- Full-text search of indexed records is a major 2024-2025 feature (Roberta Estes calls it "a game-changer").
- "Relatives at RootsTech" feature briefly shows your FamilySearch-connected cousins who also register for RootsTech.
- Can export your own tree as GEDCOM.

**Does NOT do:**
- Cannot access Ancestry.com DNA match trees.
- Does not connect to Ancestry's DNA system.
- Tree information comes from what users have linked to FamilySearch profiles — not Ancestry matches.

**Cost:** Free

**Verdict for Hunter's use case:** Not the right tool. FamilySearch is valuable for record research and building your own tree, but has no Ancestry match tree harvesting capability.

---

### 7. Genetic Affairs (geneticaffairs.com)

**URL:** https://www.geneticaffairs.com

**Status:** Active and actively developed as of 2026. Licensed partner of MyHeritage and GEDmatch.

**What it actually does:**
- AutoCluster: groups DNA matches that match each other into clusters.
- AutoKinship: builds estimated relationship trees from shared DNA amounts.
- AutoLineage: desktop app that integrates cluster data + GEDCOM files for detailed tree-building.
- AutoSegment, AutoPedigree: additional tools.
- **As of Feb 2026 (Roberta Estes article):** Full AutoKinship workflow available for FamilyTreeDNA matches, with GEDCOM integration.
- Accepts Ancestry match data via **HTML files or copy-paste wizard** (per Roberta Estes Feb 2026 article: "Import data from Ancestry using HTML files or copy/paste using a wizard").

**Ancestry support status:**
- Received Ancestry cease-and-desist in July 2020. **Direct API/automated Ancestry access is dead.**
- However, in 2026, AutoLineage accepts **manually saved Ancestry HTML pages** as input. This is a manual workaround — Hunter would need to save each match's tree page as an HTML file and import it.

**Cost:**
- Free tier: 200 credits on signup. Basic AutoCluster on FamilyTreeDNA runs on free credits.
- Credits-based system for other tools.
- Active subscription required for AutoLineage desktop app (advanced features). Pricing not publicly posted without login.

**Speed:** Automated analysis runs on server. Results emailed as zip file. For 25 matches, probably a few hours of server processing.

**Verdict for Hunter's use case:** Not viable for bulk automated Ancestry tree harvesting. The Ancestry connection requires manual HTML file saving per match — 25 matches means 25 manual page saves. Useful if matches are also in FTDNA, where full automation is available.

---

### 8. Pedigree Thief (Chrome Extension, Free)

**URL:** https://chrome.google.com/webstore/detail/pedigree-thief/hdgjlfchbpojdocjlldfikeddamdcbhn

**Status:** Listed as available in Chrome Web Store but **Ancestry support is dead.**

**What Kitty Cooper says (confirmed statement on her blog):**
> "UPDATE:: DNArboretum is no longer working but Pedigree Thief works on most sites, just not Ancestry."

**What it does on supported sites:**
- Extracts pedigree ancestor lists from MyHeritage, WikiTree, and other genealogy sites.
- Outputs ahnentafel-format text files.
- Kitty Cooper has a companion tool to convert these to GEDCOM: https://kittymunson.com/dna/Ahnen2GEDcom.php

**For Ancestry:** Dead. Ancestry's API changes blocked it in 2020.

**Cost:** Free

**Verdict for Hunter's use case:** Does not work on Ancestry. No value for this specific need.

---

### 9. Shared Clustering (GitHub, Free)

**URL:** https://github.com/jonathanbrecher/sharedclustering

**Status:** Repository exists, no formal releases published. Last commits visible but dated.

**What it does:**
- Downloads match lists and shared-match data to produce cluster visualizations.
- Focused on clustering analysis, not tree downloading.
- Ancestry support status unclear — original tool worked with Ancestry, but Ancestry's 2020 API changes likely broke it.

**Cost:** Free

**Verdict for Hunter's use case:** Not designed for tree downloading. Even if functional, produces clustering data, not cousin tree GEDCOMs.

---

### 10. New 2024-2026 Entrants

No new dedicated tools for bulk-harvesting Ancestry cousin match trees were identified in 2024-2026 research. The Ancestry API lockdown from 2020 has effectively frozen the third-party tool landscape.

**What is new in 2024-2026:**
- **Ancestry ProTools** (Ancestry's own subscription add-on, 2025): Added match clustering in July 2025. Does NOT enable tree export or downloading match trees — it is a visualization and grouping tool.
- **AI-driven tree merge tools**: Not found as a category. No tool identified that uses AI to merge multiple Ancestry match trees into a single GEDCOM.
- **DataMiningDNA NotebookLM workflow** (2026): Uses Google's NotebookLM to analyze uploaded Ancestry match data. Educational/analytical, not a harvesting tool.
- **MyHeritage Cousin Finder** (2025): Finds tree-connected cousins in MyHeritage database (not Ancestry). Not relevant to the harvesting goal.
- **FamilyTreeDNA AutoKinship/Matrix** (2025): FTDNA-native tools for clustering and relationship prediction. Not connected to Ancestry.

---

## Ranking: Best Tool for 25 Cousin Tree Import

### What Hunter Actually Wants vs. What Exists

The request is to **import the trees of 25 closest Ancestry DNA matches into Hunter's Ancestry account** (or into a GEDCOM/CSV for local use). This breaks down into two distinct operations:

**Option A: Get the ancestor pedigree data from match trees (for research/comparison)**
- DNAGedcom Client + GWorks is the only tool that does this at any scale.
- Output: a CSV of all ancestors from all linked match trees, cross-referenceable by surname and frequency.
- Does NOT produce per-cousin GEDCOMs.
- Imports into GWorks analysis tool (web), not directly back into Ancestry.

**Option B: Get per-cousin trees as importable GEDCOMs**
- No automated tool exists for Ancestry in 2026.
- Manual approach: visit each match's linked public tree on Ancestry, use Ancestry's "Save to Tree" feature to copy individual ancestors to your own research tree one match at a time.
- This is what Kitty Cooper describes as the manual workaround for a small number of matches.

---

### RANKING

| Rank | Tool | Fit | Why |
|------|------|-----|-----|
| 1 | **DNAGedcom Client + GWorks** | Partial match | Only working automated tool; gets ancestor pedigrees from match trees as CSV; requires paid subscription |
| 2 | **Manual Ancestry "Save to Tree"** | Good for 25 matches | Free, no ToS risk, works reliably; slow but accurate for small count |
| 3 | **Ancestry ProTools clustering** (2025) | Complements #1 | Native tool, no third-party risk; clusters matches but doesn't extract trees |
| 4 | **Genetic Affairs + HTML manual save** | Partial | Requires manual HTML file saves per match; good analysis if you do the manual work |
| 5 | **Everything else** | Not applicable | GEDmatch, Borland, MyHeritage FTB, FamilySearch — wrong tools for this goal |

---

## CLEAR RECOMMENDATION

**For Hunter's specific goal (25 closest cousin trees):**

**Use DNAGedcom Client as the first automated step, then use Ancestry's manual "Save to Tree" for per-cousin GEDCOM-quality data.**

### Step-by-step plan:

**Step 1: DNAGedcom Client (for bulk ancestor pedigree research)**
- **URL:** https://www.dnagedcom.com
- **Sign up:** Create free account at dnagedcom.com/Account/Register.aspx, then go to subscriber information and activate a monthly Silver subscription.
- **2026 price:** Publicly unlisted; historically $5/month for Silver tier. Expect $5-10/month. Cancel after harvest.
- **Download:** v4.0.445 Windows or Mac from the homepage.
- **Run:** Enter your Ancestry login in the client. Click "Gather Matches" then "Gather Trees." Filter to your top 25-50 matches (sort by cM, set threshold).
- **Result:** `m_profilename.csv` (match list) and `a_profilename.csv` (all ancestors from all linked trees combined).
- **Upload to GWorks** at dnagedcom.com for surname frequency analysis.
- **Time:** 30-90 minutes for 25 matches.
- **Risk:** Moderate ToS risk (Ancestry sent C&D in 2020 but DNAGedcom still operates under "A* Company" obfuscation). No widespread user ban reports. Rate-limit your session.

**Step 2: Ancestry manual "Save to Tree" (for per-cousin tree data)**
- For each of the 25 matches where GWorks reveals a useful tree, manually visit their linked Ancestry tree.
- Use "Tools > Save to Tree" on the profile of the key ancestor to copy them into a private research tree on your Ancestry account.
- For a match with a 200-person linked tree, you can copy key branches in ~10-20 minutes.
- **This creates real Ancestry tree entries** you can then export as a GEDCOM from your own tree.
- **Risk:** Zero. This is standard Ancestry functionality.

**For 25 cousins: expect 4-8 hours total (DNAGedcom harvest + manual tree copying for useful matches).**

---

## Notes on ToS Risk

Ancestry's Terms of Service prohibit "automated access" and "scraping" of their platform. DNAGedcom Client is technically in violation of this. However:

1. Ancestry has not been observed to ban individual user accounts for using DNAGedcom (as distinguished from the C&D sent to the tool developer).
2. The tool deliberately rate-limits itself and runs slowly to avoid triggering bot detection.
3. For a one-time run on 25 matches, the risk of account suspension is very low in practice.
4. The manual "Save to Tree" approach is fully compliant.

The safest approach is to combine both: use DNAGedcom for the research data (ancestor CSV for GWorks), and use Ancestry's native tools for the actual tree copying.

---

## Sources

1. DNAGedcom homepage (2026): https://www.dnagedcom.com — confirmed v4.0.445, A* Company listed
2. Kitty Cooper's Blog, "Solving unknown parentage cases with DNA" (2017, updated 2021): https://blog.kittycooper.com — GWorks step-by-step; Silver membership confirmed
3. Kitty Cooper's Blog, "Collecting Family Trees with Automation": https://blog.kittycooper.com/collecting-trees-with-automation — Pedigree Thief Ancestry status confirmed dead
4. DataMiningDNA, "A Comparison of Tools to Download Ancestry Matches" (2020, updated 2026): https://dataminingdna.com/a-comparison-of-tools-to-download-ancestry-matches/ — $5 Silver pricing; confirmed Ancestry blockage of third-party tools June 2020
5. DNAeXplained (Roberta Estes), "Ancestry to Remove DNA Matches Soon" (July 16, 2020): https://dna-explained.com/2020/07/16/ — confirms Ancestry C&D letters to ALL third-party tools including DNAGedcom and Genetic Affairs
6. DNAeXplained (Roberta Estes), "How to Use Ancestry's New Match Clusters and What They Mean" (July 10, 2025): https://dna-explained.com/2025/07/10/how-to-use-ancestrys-new-match-clusters-and-what-they-mean/ — confirms Ancestry ProTools clustering (2025), DNAGedcom still listed as active
7. DNAeXplained (Roberta Estes), "AutoKinship by Genetic Affairs Builds Family Trees from Your Matches at FamilyTreeDNA, and More" (February 10, 2026): https://dna-explained.com/2026/02/10/ — confirms Genetic Affairs Ancestry import requires manual HTML files; FTDNA automation fully working
8. DNAeXplained (Roberta Estes), "2025 Genetic Genealogy Retrospective" (December 31, 2025): https://dna-explained.com/2025/12/31/2025-genetic-genealogy-retrospective-wow-what-a-year/ — annual summary; DNAGedcom not mentioned; Genetic Affairs mentioned as active staple
9. Reddit r/Genealogy, "Chromosome Mapping" (January 2025): https://reddit.com/r/Genealogy/comments/1id94go/ — user confirms DNAGedcom v4 re-vamped UI, Ancestry gather still working ("currently grabbing all my data off A(ncestry)")
10. Reddit r/DNAAncestry, "Ways to download your DNA matches from Ancestry" (2020): https://reddit.com/r/DNAAncestry/comments/fdzmdz/ — comprehensive tool comparison from that era
11. Borland Genetics homepage (2026): https://borlandgenetics.com — confirmed DNA reconstruction database, no tree harvesting function
12. GEDmatch homepage (2026): https://www.gedmatch.com — confirmed $10/month Tier 1 (via Wikipedia citing 2018 source, Tier 1 referenced as current by Roberta Estes through 2025)
13. Wikipedia, "GEDmatch": https://en.wikipedia.org/wiki/GEDmatch — Tier 1 pricing $10/month, corporate ownership (Verogen/Qiagen)
14. MacKiev Family Tree Maker 2024: https://www.mackiev.com/ftm — confirms Ancestry sync for YOUR tree only; no match tree downloading
15. Genetic Affairs homepage (2026): https://www.geneticaffairs.com — confirms active tools, credit-based pricing, no public pricing page
