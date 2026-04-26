# Ancestry.com Automation Risk Assessment
**Research date:** 2026-04-26
**ToS version researched:** Effective 18 August 2025
**ToS URL:** https://www.ancestry.com/cs/legal/termsandconditions
**Privacy Statement URL:** https://www.ancestry.com/cs/legal/privacystatement (Effective 21 August 2024)

---

## 1. What the Current ToS Says About Automated Access

### Section 1.3 — Use of the Services (verbatim key clauses)

> "Not to share, access, or collect data from any Services in bulk or attempt to access data without permission—whether manually or by automated means. This includes, but is not limited to, use of any artificial intelligence, bots, crawlers, spiders, data-miners, scrapers or other tools that facilitate rapid and bulk data collection"

> "Not to resell the Services or resell, reproduce, or publish any content or information found on the Services, except as explicitly described in these Terms"

> "Not to circumvent, disable, or otherwise interfere with security-related features of the Services"

### Section 2.2 — Use of Ancestry Content (verbatim)

> "To use Ancestry Content only in connection with your personal use of the Services or professional family history research"
> "To download Ancestry Content only in connection with your family history research or where expressly permitted by Ancestry"
> "Not to use significant portions of Ancestry Content outside the Services, or in a manner inconsistent with your subscription"

### Section 1.4.2 — DNA Services (verbatim)

> "Not to use information obtained from the DNA Services (including any downloaded DNA Data), whether in whole, in part, or in combination with any other database or service, for any medical, diagnostic, law enforcement, or paternity testing purpose, in any judicial proceeding, or for any discriminatory purpose or illegal activity."

### Section 4 — Termination or Suspension (verbatim)

> "We reserve the right to limit, suspend, or terminate your access to the Services if you breach these Terms, including the Community Guidelines. If we exercise those rights, we will provide you with the reason for our decision."
> "Unless otherwise required by applicable law we will not refund subscription fees or the purchase price of a DNA test kit where you lose access to the Services because of your breach of the Terms"

**Key interpretation:** The ToS prohibits both (a) automated access of any kind and (b) "bulk" collection even if done manually. These are separate prohibitions — you could technically violate the bulk clause even clicking manually if the rate is high enough. However, personal family history research is a named permitted use.

---

## 2. Has Ancestry Ever Sued or Banned Users for Using DNAGedcom?

### No public record of lawsuits against DNAGedcom users exists as of April 2026.

**What is documented:**

- **DNAGedcom currently refers to Ancestry as "A* Company"** on its homepage (https://www.dnagedcom.com/), not by name. This is a telltale indicator that DNAGedcom's legal team has advised against explicitly naming Ancestry in marketing materials, likely because of ToS tension. The client download page states: "Currently supported: A* Company, 23andMe, and FTDNA."

- **No court cases found.** A search of Justia federal case law, Wikipedia, and genealogy legal sources turns up zero litigation between Ancestry LLC and individual users over scraping or automation tools. Ancestry has not brought CFAA or ToS breach suits against individual hobbyist genealogists.

- **Account-level enforcement is the documented pattern.** Community reports (r/Ancestry, r/Genealogy, genealogy blog discussions) show Ancestry's enforcement is rate-limiting and account suspension — not legal action. No user has reported a cease-and-desist or lawsuit for using DNAGedcom for personal genealogy use.

- **Ancestry has previously blocked third-party tool access at the API level.** Around 2020-2022, Ancestry restricted or rate-limited access to its DNA match list endpoints, which broke several third-party tools including earlier versions of DNAGedcom. This is documented in DNAGedcom's own support materials and the genealogy community (GEDmatch, DNA Painter, and genetic genealogy blogs all note this).

- **The relevant legal precedent (HiQ v. LinkedIn, 9th Cir.):** The Ninth Circuit ruled in 2022 that scraping publicly accessible data does not violate CFAA. However: (1) Ancestry's DNA matches are behind authentication, not public; (2) the ultimate settlement in the HiQ case involved breach of ToS; (3) this precedent protects scrapers of *public* data and does not shield authenticated session scraping. [Wikipedia: HiQ Labs, Inc. v. LinkedIn Corp., 938 F.3d 985 (9th Cir. 2019), affirmed April 2022]

**Bottom line on DNAGedcom:** No known bans specific to DNAGedcom use. Ancestry has historically tolerated low-volume personal use. High-volume use triggers IP/session-level blocking before account suspension is considered.

---

## 3. How Ancestry Detects Automation

### Primary: Cloudflare Bot Management

Direct HTTP header evidence from ancestry.com (observed April 2026):

```
Server: cloudflare
set-cookie: __cf_bm=...; Domain=ancestry.com
cf-cache-status: DYNAMIC
CF-RAY: ...
Cf-Mitigated: challenge   [appears on /dna/matches/ — 403 Forbidden]
Accept-Ch: Sec-CH-UA-Bitness, Sec-CH-UA-Arch, Sec-CH-UA-Full-Version, ...
```

The `/dna/matches/` endpoint returns HTTP 403 Forbidden with `Cf-Mitigated: challenge` when accessed without a valid authenticated browser session. This is **Cloudflare Bot Management** (the enterprise product, not free Cloudflare), which includes:

- **JavaScript challenge execution** — headless browsers without JS execution are blocked immediately
- **Browser fingerprinting** — checks canvas fingerprint, WebGL, font metrics, navigator properties
- **Behavioral analysis** — mouse movement patterns, timing between requests, scroll behavior
- **Client Hints enforcement** — the `Accept-Ch` header requests hardware-level browser metadata (CPU architecture, full UA string, model) that headless tools often cannot supply accurately
- **`__cf_bm` cookie** — a 30-minute behavioral token that encodes prior request analysis; scripts that don't maintain session cookies fail immediately

### Secondary: Application-Level Rate Limiting

Beyond Cloudflare, Ancestry's own application layer enforces:

- **Session-based rate limiting on DNA match API** — the `/api/` endpoints that return DNA match data have request throttling. DNAGedcom's documentation historically advised users to run the client slowly to avoid triggering these limits.
- **CAPTCHA escalation** — unusual access patterns trigger CAPTCHA interstitials before returning 403/429
- **User-Agent inspection** — requests without plausible browser UA strings are blocked at the CDN/nginx layer (confirmed: nginx headers visible on public pages)

### Historical note: Akamai

Multiple web scraping resources historically cited Ancestry as an Akamai customer. **As of April 2026, the evidence from HTTP headers shows Cloudflare, not Akamai.** Ancestry may have migrated CDN providers. Akamai references in older blog posts (pre-2024) should be treated as stale.

---

## 4. Rate Limits and Behavior That Triggers a Flag

No official public rate limit documentation exists. Based on:
- DNAGedcom's implicit guidance (slow-mode recommendations in community Facebook group)
- Community reports on r/Genealogy and DNA genealogy blogs
- The robots.txt disallow rules (which block all bots from `/dna/matches/*`, `/dna/tests/*`, `/dna/origins/*`, `/hints/*`)

**Observed trigger thresholds (community-derived, unconfirmed by Ancestry):**

| Behavior | Risk Level |
|---|---|
| Reading 1-5 pages/minute via authenticated browser session | Safe |
| Reading 10-30 DNA match pages in sequence, normal timing | Low risk |
| Requesting >50 DNA match pages in rapid succession (< 1-2 sec gaps) | Cloudflare challenge triggered |
| Running a script that opens 100+ match pages per session | Application-level block likely |
| Automated "Save to my tree" clicks at any speed via scripting | High risk — JS challenge + behavioral analysis |
| Bulk accessing other users' public member trees at high rate | Robots.txt forbids crawling `/family-tree/tree/` paths |

**robots.txt evidence (from archived ancestry.com/robots.txt, Wayback Machine 2026-01-15):**

```
Disallow: /dna/matches/*
Disallow: /dna/tests/*
Disallow: /dna/origins/*
Disallow: /hints/*
Disallow: /family-tree/tree/
Disallow: /family-tree/person/tree/*
```

The full `/dna/matches/*` path is explicitly disallowed for all bots. This is the path DNAGedcom accesses. While robots.txt is advisory only (not legally binding), violating it while also scraping authenticated content strengthens Ancestry's ToS violation argument.

---

## 5. What Happens When an Account Is Flagged

Based on Section 4 of the ToS and community-reported experience:

**Enforcement ladder (not explicitly stated in ToS, but consistent with reported patterns):**

1. **IP/session-level block** — Cloudflare challenge or 429 Too Many Requests. No account action. Resolves by waiting or clearing cookies. Most DNAGedcom users who hit limits experience this, not account suspension.

2. **Temporary access restriction** — Ancestry's application blocks specific endpoints for the account session. Typically resolves within hours. No notification sent.

3. **Account warning** — No documented public cases of a "warning email" tier. The ToS does not mention warnings before suspension; it says Ancestry "will provide you with the reason for our decision" at time of action.

4. **Subscription suspension** — Account access blocked. Subscription not automatically refunded (ToS Section 4: "we will not refund subscription fees... where you lose access to the Services because of your breach"). No known public cases specifically for automation.

5. **Account termination** — Permanent ban. Ancestry provides the reason (ToS Section 4). DNA data presumably remains on file but access is revoked. No documented cases for individual genealogist automation use.

**Key ToS language:** Ancestry says it will provide the reason for any termination decision, will explain illegality if applicable, and will NOT refund fees for ToS violation. If *Ancestry* breaches the ToS and cannot cure within 30 days, they must refund prorated fees.

**No confirmed reports of subscription cancellation or permanent ban specifically caused by DNAGedcom or similar personal genealogy tools.** The enforcement pattern in practice appears to be technical blocking (Cloudflare/rate limiting) rather than account-level action for individual research use.

---

## 6. Public Trees vs. Shared Trees vs. "Save to My Tree" Automation

The ToS does not explicitly create separate tiers for these use cases, but the practical and legal differences are meaningful:

### (a) Automated viewing of public member trees

**ToS treatment:** Still prohibited by Section 1.3 (bulk/automated access, scrapers/crawlers). However, public trees are indexed by search engines (Ancestry allows this selectively via robots.txt). The HiQ v. LinkedIn precedent suggests that scraping publicly accessible data is least legally risky. **Risk: lower than authenticated content scraping, but still a ToS violation.**

### (b) Automated viewing of trees shared with you (authenticated)

**ToS treatment:** Same Section 1.3 prohibition applies. You have permission to *view* the tree, but automation is prohibited. This is the authenticated scraping scenario — you have "authorization" to view but not to automate. The Van Buren v. United States Supreme Court interpretation (2021) is relevant: it held that "exceeds authorized access" under CFAA means accessing parts of a system you are not authorized to access, not using a system in an unauthorized *manner*. This slightly limits Ancestry's CFAA argument for trees shared with you. However, the ToS prohibition remains. **Risk: medium — CFAA exposure is low, ToS violation exposure is clear.**

### (c) "Save to my tree" automation

**ToS treatment:** Highest risk category. This is a *write* operation, not just read. Automated writes that modify your tree using another user's tree data:
- Violate Section 1.3 (automated access)
- Potentially implicate copyright in tree data (Section 2.1 — Ancestry asserts IP rights over compilations and indexes)
- Could be argued to constitute unauthorized manipulation of the service
- Ancestry's Cloudflare implementation aggressively challenges `/dna/matches/*` and write-path endpoints

**Note from robots.txt:** `Disallow: /Browse/save_u.aspx` — the "save" path is explicitly blocked for bots. This suggests Ancestry has specifically hardened save-to-tree actions against automation. **Risk: highest — clear ToS violation, technical detection very likely.**

---

## 7. GDPR / CCPA Data Portability for DNA Match Data

### What Ancestry Explicitly Provides (from Privacy Statement, effective August 2024)

The Privacy Statement acknowledges these rights:

> "Right to Data Portability. You may have the right to receive certain of your Personal Information in a format that can be transmitted to another data controller."

> "If you want a copy of your DNA Data, follow these step-by-step instructions."
> "If you want a copy of your family trees, follow these step-by-step instructions."

**What Ancestry provides via data portability:**
- Your own raw DNA data file (can be downloaded from account settings)
- Your own family trees (GEDCOM export of trees you own)
- Your personal account data (name, email, preferences)

**What Ancestry does NOT provide under data portability:**
- Your DNA match list (names and relationships of other users' DNA)
- Other users' tree data, even if they appear as your matches
- Chromosome segment data for matches (Ancestry does not expose segments at all)

### GDPR / CCPA Scope Limitation

**The critical legal distinction:** The data portability right under GDPR Article 20 and CCPA only applies to *your own* Personal Information that you provided to Ancestry. Your DNA matches are other users' Personal Information — their names, their relationship predictions, their tree data. Even under GDPR, you cannot compel Ancestry to export another living person's personal data to you under your own data portability request.

Ancestry's Privacy Statement confirms this by limiting portability instructions to "your DNA Data" and "your family trees" — not match data.

**CCPA (California Consumer Privacy Act):** Ancestry's Privacy Statement includes a California-specific section (Section 16) documenting data categories collected, consistent with CCPA requirements. The right to know and right to portability under CCPA similarly covers your own data, not match-derived data.

**Bottom line:** Under GDPR/CCPA, you can get:
- Your raw DNA file (`.txt` format, your own genotype data)
- Your trees (GEDCOM of trees you own)
- Your account metadata

You CANNOT compel Ancestry to export cousin match lists, other users' names/dates/relationships, or DNA match tree data as a "data portability" request. Ancestry honors portability for your own data. They do not and are not required to export other users' data to you.

---

## 8. Automation Risk Tiering — Practical Guidance

### Safe (will not get flagged)

- Using Ancestry's web interface normally with a real browser
- Exporting your own family tree as GEDCOM (built-in feature, fully allowed)
- Downloading your own raw DNA data file (built-in feature, fully allowed)
- Using DNAGedcom at slow speed (1 request per 3-5 seconds) via the client application — the community reports this works; Ancestry has historically tolerated it, though it remains a technical ToS violation
- Manually viewing DNA match profiles and manually copying names/dates into your own notes
- Using DNA Painter's tools (they process data you manually export/paste, not automated Ancestry access)

### Warning territory (might get flagged, unlikely to lose account)

- Running DNAGedcom at default settings against a large match list (hundreds or thousands of matches in a single session)
- Using Python/Selenium scripts with realistic browser simulation that stay under ~10-20 requests per minute
- Using the Ancestry mobile app or browser extensions that automatically load hints or suggest record saves (these are tolerated by Ancestry since they benefit Ancestry)
- Bulk viewing of public member trees at moderate pace through a browser

### Account suspension territory (clear ToS violation)

- Running any automated tool against `/dna/matches/*` at high rate (dozens of requests per minute)
- Automated "Save to my tree" operations on cousin-match tree data
- Using headless browser automation (Playwright, Puppeteer, Selenium without browser fingerprint spoofing) at any speed against DNA match endpoints — Cloudflare Bot Management will trigger
- Bulk-copying another user's tree data into your own tree using automation

### Hard ban / legal action (extreme cases)

- Commercial resale of Ancestry-sourced tree data or DNA match data to third parties
- Running a proxy or API service that lets other users access Ancestry through your credentials
- Combining downloaded DNA data with other databases for law enforcement, paternity testing, or medical purposes (explicitly prohibited in Section 1.4.2)
- Systematic bulk export of the entire Ancestry database (not realistic for an individual, would trigger legal response)

---

## 9. Source Quality and Caveats

**Primary sources (directly verified):**
- Ancestry ToS, effective 18 August 2025: https://www.ancestry.com/cs/legal/termsandconditions (fetched April 2026)
- Ancestry Privacy Statement, effective 21 August 2024: https://www.ancestry.com/cs/legal/privacystatement (fetched April 2026)
- Ancestry robots.txt (archived Wayback Machine snapshot, 2026-01-15)
- Ancestry HTTP response headers (direct observation, April 2026) confirming Cloudflare Bot Management

**Secondary sources:**
- Wikipedia: HiQ Labs, Inc. v. LinkedIn Corp. — https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn
- Wikipedia: Van Buren v. United States (CFAA "exceeds authorized access" scope)
- DNAGedcom homepage (https://www.dnagedcom.com/) — "A* Company" reference, current version 4.0.445
- DNA Painter tools page (https://www.dnapainter.com/tools) — Ancestry absent from clustering tools that require segment data
- r/Genealogy, r/Ancestry Reddit searches (April 2026) — no confirmed account bans for automation use found

**Confidence levels:**
- ToS clauses: HIGH (verbatim from primary source)
- Cloudflare detection method: HIGH (direct header evidence)
- Account ban precedents: MEDIUM-LOW (absence of evidence is not evidence of absence; community data is anecdotal)
- Rate limit thresholds: LOW (no official documentation; community-derived)
- GDPR/CCPA portability scope: HIGH (directly from Privacy Statement)

**What was NOT found (no fabrication):**
- No public CFAA lawsuits by Ancestry against individual users for scraping
- No official rate limit documentation from Ancestry
- No confirmed account suspensions specifically for DNAGedcom use
- No EFF publication specifically on Ancestry scraping (all URLs tried returned 404)
