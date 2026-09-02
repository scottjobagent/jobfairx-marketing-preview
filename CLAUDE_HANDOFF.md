# JobFairX — Master Claude Code Handoff

**Written:** 25 Aug 2026, by the session that also built the product video (HANDOFF-VIDEO.md stream).
**Purpose:** the single entry point for any new Claude Code session inheriting this project. It synthesizes every stream's handoff into one map, states the laws that must never be violated, and routes you to the authoritative deep-dive doc for each area. It does not replace those docs — read them in the order given in §21 and §33.
**Prime directive:** behave as if you inherited the previous conversations' working knowledge. Do not make Scott repeat decisions documented here. Do not rebuild what exists. Do not reintroduce rejected ideas (§26/§28). Do not change approved messaging without discussing it first. Do not start coding until Scott tells you what to work on.

---

## 0. LATE-BREAKING SUPERSESSIONS (Aug 25 evening — read before trusting §2/§13/§24)

The parallel event-page session advanced past this document's freeze the same evening. Where the two conflict, THESE win (full detail in the memory entries named, and in that session's own records):

1. **Early registration is 30 days — SETTLED by Scott** ("Thirty days or more is early registration"). Marketing copy uses 30 everywhere. The live server code says `minDays:31` (proven at the boundary: badge present at 31 days out, absent at 30) — the CODE must change to 30; flag as a developer task. The long-open 30-vs-31 question is closed. (memory: `early-registration-30-days`)
2. **All FIVE event types publish live stats** — Healthcare 91%/35/8 · Veterans 89%/35/7 · Diversity 87%/35/11 · Entry-Level 86%/73/19 · Technology 84%/53/11. This kills the "only three show rates exist / Diversity and Technology have no stats" rule, and reframes 73/19 as the Entry-Level type averages (not a Portland outlier). Caveat: only healthcare's figures are Scott-confirmed as real 2025 platform data; confirming the other four is an open question. (memory: `event-page-live-type-stats`)
3. **The event lifecycle has EIGHT states, not five** — empirically captured from 15 live events at 0–45 days out, with verbatim banner copy, colors, and CTA behavior per state (registration closes at 1 day out; event day has no banner). Any event-page work uses that table, not the A–E model in HANDOFF.md §3 / §13 below. (memory: `event-lifecycle-states-verified`; implemented in `build-event-healthcare.py`'s STATES object)
4. **The redesigned event page is BUILT and deployed**: `employer-event-detail-v2.html` (Austin healthcare, authored redesign — not a clone) via `build-event-healthcare.py`, with fresh Austin clinical captures including the first live event-day lobby shot. NO on-page state toggles (Scott rejected two attempts — the page renders one true state). Deployed to the preview repo. This supersedes §24's "event details not started." (memory: `event-page-v2-healthcare-build`)
5. The **video stream** also advanced the same evening — see §23 (4:12 seven-section rebuild).

---

## 1. Project Overview

JobFairX runs **hiring events** for employers (jobfairx.com). This repository (`/Users/scottl./Desktop/jobfairx-marketing/`) is the marketing-site workspace: a full 52-page redesign in three concept languages, live-site clone prototypes built by Python builders, strategy/audit documents, a screenshot pipeline against Scott's product prototypes, and a self-narrating product video.

The business trigger for everything here: **the product launched in-person interviews** (as an interview *location*, not an event type — see §2, the most important fact in this document), and the live site still markets the old "Virtual Hiring Event Platform" identity. Every stream exists to move employer-facing marketing to the new model and hand the developer pixel-exact prototypes.

**The work is organized in parallel streams**, each with its own handoff doc:

| Stream | What it is | Authoritative doc | State |
|---|---|---|---|
| Redesign (original) | 28 `page-*` pages, concepts 1–3, design system, strategy docs | `HANDOFF.md` (§1–§14) | Reference set; complete through the AI Flow fan-out |
| Concept 4 "vid" | 6 `vid-*` pages | `HANDOFF.md` §12 | Complete, reference |
| Concept 5 "AI Flow" | `concept-5-aiflow.html` + 19 `af-*` pages | `HANDOFF.md` §13–14, `AF-BRIEF.md` | Built, verified, deployed to preview |
| Concept 6 "Fairs AI" | `concept-6-fairs.html`, `page-events.html` calendar, `page-pricing.html` | `HANDOFF-3.md` | Active concept stream; nothing half-finished |
| Live-site clone (employer) | `employer-home/pricing/faq/event-detail.html` via Python builders | `HANDOFF-2.md`, `HANDOFF-4.md`, `EMPLOYER-HOME-DEV-NOTES.md` | Homepage FINAL (signed off desktop+mobile); pricing/FAQ clones final |
| Product video | `build-video.py` → `video-event-day-lobby.html` | `HANDOFF-VIDEO.md` (+ §23 note below) | ACTIVE in a parallel session — rebuilt Aug 25 ~15:40 as a 4:12 seven-section Ava build; HANDOFF-VIDEO.md predates that rebuild |
| Seeker prototype | Separate project on `~/Desktop` (HANDOFF-2 §5 records its state) | `~/Desktop/HANDOFF-4.md` chain + memory | Not this repo's concern unless Scott says so |

**Scott has NOT chosen a winning homepage concept.** Six exist side by side. The live-site clone stream and the Fairs AI stream are the two he actively iterates on.

## 2. Current Product State

**THE PRODUCT MODEL — LAW.** This was the session's biggest recurring error; the live site's own copy teaches the wrong model, so it WILL recur if you are careless:

- An **event is a market moment**: "Dallas Healthcare Hiring Event, Sep 22, 11:00 AM–3:00 PM CT". Every employer joins the SAME event.
- There are exactly **five event types (audiences)**: Healthcare, Diversity, Veteran, Technology, Entry-Level. Never invent a sixth.
- **Interview location is a PER-EMPLOYER setting**, not an event property. Four options, set independently per event: **JobFairX video** ("JobFairX video call") · **Phone** ("You call each candidate") · **In person** (the employer's street address; candidates see it on their confirmation and reminders, never on the public event) · **Your own link** (Teams/Zoom/Meet — a sub-choice inside Video in the product's setup flow).
- Two employers at the same event can interview completely differently. The dashboard's INTERVIEW LOCATION column showing all four side by side (`assets/product/dashboard-events.png`) is the single best proof asset owned.
- **What launched is the in-person interview LOCATION, not "in-person events."** Scott verbatim: "It's not their own event. They're still joining a Dallas healthcare event... They could just set where they want their interviews to go."
- Candidates **REQUEST** interviews (the request carries a candidate-chosen time slot); employers **ACCEPT**, and accepting IS the scheduling step. There is no "apply". Auto-accept is an optional toggle at every tier.
- Candidate matching activates the moment jobs are posted; first requests arrive within a few hours; **matching stays live until the event starts** — it does NOT stop when employer registration closes (Scott's explicit correction).

**Structural consequences (decided AND implemented):** the events calendar has NO virtual/in-person filter; event detail pages are never labelled virtual or in-person; "Virtual" comes out of page titles; a "next-inperson" programmatic URL family must NEVER be created.

**Verified commercial facts** (full detail: `LIVE-SITE-SCOPE.md`, `HANDOFF.md` §3, `HANDOFF-4.md` §2):
- Tiers per event: Starter $495 (1 job, 20+ scheduled candidate interviews, 2 recruiter seats) · Growth $895 "Most Popular" (up to 3 jobs, 60+, up to 5 seats) · Pro $1,495 (up to 6 jobs, 100+, unlimited recruiters). The scheduled-interview count is a volume commitment, not a feature — it carries the most weight (Scott's strongest line).
- Full bundle ladders (mined from the live SvelteKit payload 24 Aug, in `employer-pricing.html`'s inline script — the authoritative record): Starter 5=$470 → 100=$297 (save $19,800); Growth 5=$850 → 100=$537 (save $35,800); Pro 5=$1,420 → 100=$897 (save $59,800). Hidden discount codes in the live payload: Non-profit $395, Small-business $795. Credits never expire, usable across any event type.
- Early registration: flat $100 off every tier (never a percentage), struck prices $395/$795/$1,395. **Threshold: 30 days, settled by Scott Aug 25** (§0.1); the live code's `minDays:31` is a developer fix.
- Event lifecycle: **eight states** per the Aug 25 empirical capture (§0.3) — the A–E five-state model in `HANDOFF.md` §3 / `LIVE-SITE-SCOPE.md` §2 is superseded for event-page work. A dormant `onNewYearsSale` flag implies a promo state, unconfirmed.
- Show rates: **all five types publish stats on the live site** (§0.2): Healthcare 91%/35/8 · Veterans 89%/35/7 · Diversity 87%/35/11 · Entry-Level 86%/73/19 · Technology 84%/53/11 — healthcare Scott-confirmed, the other four pending his confirmation. Platform totals: 4,000+ employers · 500,000+ interviews · 300+ cities · 3M+ candidates · 87% of employers return. The **20-mile fact** ("candidates are verified to be within approximately 20 miles of the event city") is the strongest owned in-person argument.
- Healthcare 2025 data, Scott-confirmed 25 Aug and published in his own article: **582 healthcare events, avg 35 scheduled interviews and 8 hires per employer per event** — real for HEALTHCARE ONLY. The old purge-on-sight rule for 35/7-8 still binds everywhere else (veterans/market figures like Portland 968/73/19 are per-event, never type-wide).

## 3. Technology / Architecture

- **Redesign sets (page-/vid-/af-/concept-):** no build step, no framework, no dependencies beyond Inter (rsms.me). Every page self-contained: `shared/base.css` + `shared/motion.js` (+ `shared/vignettes.css` where used) + its own `<style>`. Nav/footer duplicated per page by design (no templating layer; if one is ever introduced, extract the footer first — byte-identical within a set).
- **Live-site clone stream:** "**Edit the builder, never the output.**" `employer-home.html`, `employer-pricing.html`, `employer-faq.html`, `employer-event-detail.html`, `employer-home-mobile.html` are GENERATED by `build-employer-*.py` scripts from frozen captured DOM in `assets/live-capture/`. Every `sub()` asserts its match count and aborts loudly on zero matches. Build order matters: home builder BEFORE `build-event-detail.py` (event page imports the How-It-Works section by H2 text probe and the bento by `id="built-in-tools"`) and BEFORE `build-employer-home-mobile.py` (its source is the built desktop page). New markup in clone pages uses inline styles or scoped `<style>` — never bare Tailwind utilities (the live compiled CSS purges anything the live pages never used).
- **Video:** `build-video.py` (SCENES data → edge-tts synthesis → timeline from measured audio → assembly into `video-template.html` placeholders). Same edit-the-builder rule. See `HANDOFF-VIDEO.md`.
- **Publish/deploy — the ONLY push path:** github.com web UI in Scott's Chrome (claude-in-chrome Browser 2). **No git credentials, no gh, no SSH keys exist on this machine.** Private repo `scottjobagent/jobfairx-marketing` (everything incl. strategy docs); public preview repo `scottjobagent/jobfairx-marketing-preview` → GitHub Pages at https://scottjobagent.github.io/jobfairx-marketing-preview/ (site only, strategy docs NEVER uploaded, HTML comments stripped via `re.sub(r'<!--.*?-->\n?', ...)`). Stage files in the session scratchpad (file_upload refuses other paths; the scratchpad path is session-specific — update `~/Desktop/.claude/launch.json` first thing). Verify head SHA moved after every upload (clicks silently fail), then verify deployed bytes with a cache-buster (Pages caches ~600s; deploys can lag minutes).
- **Git:** local history and GitHub history are UNRELATED lineages. NEVER run `git checkout/restore/stash/reset/clean` here — uncommitted working-tree files are other streams' live work (~90 modified files is normal). Never `git add -A`. Never force-push. Read-only git is fine.
- **Verification tooling:** `tools/mcheck.py` (true-390 iframe overflow probe — a plain headless `--window-size=390` run LIES, Chrome clamps to 500px); `tools/capture.py` (screenshot harness with the load-bearing NEUTRALISE list); `capture-healthcare.py` (video-stream capture harness for the healthcare V3 prototype); PIL band-crop screenshot review; headless Chrome uses plain `--headless` (not `--headless=new`) on this machine.
- **Desktop is iCloud-synced** — deletions go to Recently Deleted; never bulk-delete; recover via Finder.

## 4. Repository Structure

```
jobfairx-marketing/
├── HANDOFF.md            # foundational: redesign, product model law, lessons §8
├── HANDOFF-2.md          # live-site clone stream (23–24 Aug) + seeker stream state
├── HANDOFF-3.md          # Fairs AI stream: concept 6, calendar, pricing (§0 two-session rules)
├── HANDOFF-4.md          # newest clone-stream state (25 Aug): mobile v1, pricing/FAQ clones
├── HANDOFF-VIDEO.md      # product video stream (build, script, roadmap)
├── AF-BRIEF.md           # AI Flow fan-out build brief (chrome contract, link map)
├── EMPLOYER-HOME-DEV-NOTES.md  # developer handoff for the signed-off homepage
├── COST-PER-HIRE-CLAIM.md      # researched cost claim, all variants + sources
├── LIVE-SITE-SCOPE.md    # live-site capture: lifecycle states, pricing, §6b model
├── CONTENT-SPEC.md / DESIGN-SYSTEM.md / PAGE-INVENTORY.md / RECOMMENDATION.md / VISUAL-AUDIT.md / README.md
├── index.html            # concept chooser (5 cards; concept 6 never added — known gap)
├── concept-{1,2,3,4,5,6}*.html + page-*.html (27) + vid-*.html (5) + af-*.html (19)
├── employer-home.html / employer-pricing.html / employer-faq.html /
│   employer-event-detail.html / employer-home-mobile.html      # BUILD OUTPUTS
├── build-employer-home.py / build-event-detail.py / build-employer-faq.py /
│   build-employer-home-mobile.py / build-employer-pricing.py   # THE editable sources
├── build-video.py / video-template.html / video-event-day-lobby.html / vo-draft/
├── capture-healthcare.py
├── shared/  (base.css ~390 lines, motion.js ~300, vignettes.css ~420)
├── assets/product/       # 14 unique sanitised 2× screenshots + *-hc.png video captures
├── assets/live-capture/  # frozen rendered-DOM captures — NEVER edit
├── assets/employer-home/, assets/event-detail/   # localized live assets (?v=N cache-busted)
├── assets/_reference-do-not-publish/   # unlicensed iStock comps — gitignored, never publish
└── tools/                # capture.py, mcheck.py, shoot.sh, downloaded prototype pages (*-v3*.html)
```

## 5. Current Pages

- **Redesign set (28):** `concept-3-hybrid.html` (the recommended original homepage), page-events, page-event-detail (5-state template, REVIEW-ONLY switcher), page-pricing, page-faq, page-contact, page-platform + 6 capability pages (candidate-pipeline is the reference), page-solutions + 5 type pages (healthcare is the reference), page-interview-locations, page-in-person-interviews, page-demo, page-security, page-resources, page-about, page-privacy-policy, page-terms, page-city-hub (template, 352 instances planned).
- **vid set (6):** concept-4-vid + vid-events/event-detail/pricing/faq/contact.
- **af set (20):** concept-5-aiflow + 19 af-* pages (full parallel walkthrough, deployed, a11y-fixed).
- **Fairs AI:** concept-6-fairs.html + the reworked page-events.html calendar + updated page-pricing.html.
- **Live-site clones:** employer-home (FINAL, signed off desktop + mobile v1), employer-pricing, employer-faq, employer-event-detail (captured, not yet updated — next target), employer-home-mobile. Note: `mobile-view.html` (390px phone-frame viewer) and `difference-options.html` (review scratch, pending deletion) exist on the deployed preview repo but NOT in this local root — HANDOFF-4 §5 records them byte-verified live.
- **Video:** video-event-day-lobby.html (durable copy of the built self-narrating video).
- **Two files are TEMPLATES, not pages:** page-event-detail.html and page-city-hub.html.

## 6. Current UX / IA

- **Clone-page nav (Scott's spec, matches live):** Upcoming Hiring Events · Pricing · FAQ · Contact Us · Sign In · Register for an Event. Sign In / Register are app destinations (`virtual.jobfairx.com/login` keeps its URL; the word "virtual" is allowed only there).
- **Fairs AI nav:** Upcoming Hiring Events · Features ⌄ · Solutions ⌄ · Pricing · FAQ + Sign In + Register. Contact Us removed from nav (footer only). Dropdown links deliberately `href="#"` ("We're just creating the nav"). Mobile fold at 1200px.
- **AI Flow nav:** mega-dropdowns with inline Phosphor fill icons (Features in accent blue, Solutions in the five type colours).
- **Footer on redesign sets = site index** (five columns, byte-identical within a set, self-links as `<span aria-current="page">`). Clone pages keep the live footer.
- **Calendar columns (Fairs AI):** Date · City · Type · Candidate matching · View Event Details. Matching column values: Live / Starts soon / Starts 30 days out; Save $100 as an amber chip under the city. "Closes tomorrow"/"Registration closed" are deliberately ABSENT from the calendar (Scott's ruling — they live on event detail).
- **Mobile:** Scott wants **dedicated mobile designs, not responsive collapse**, with mobile-purpose images ("Can't use the same images"). employer-home-mobile.html is v1 of that language: portrait 4:5 photography, visible step labels, full-width CTAs, mobile-specific product captures.

## 7. Current Design System

`DESIGN-SYSTEM.md` is the locked token layer (derived from a measured 17-site teardown — the numbers are evidence, not taste). Hard rules:

- Never pure white/black (canvas `#fbfaf8` light / `#0b0d12` dark; ink `#14161a` / `#f4f6fa`). Display weight 500, never 700 (vid uses 600, AI Flow 600 — deliberate deviations). Tracking ramp crosses zero (−0.042em display → +0.004em body; eyebrows are the only positive-tracking text).
- One depth mechanism per element: hairline+rim on dark, shadow on light, never both. No coloured bloom (capped ~15% alpha). Accent `#2f5cff` (deepened from live's stock Tailwind `#2563eb`).
- **HARD CUTS between dark/light sections** (Scott's explicit order; gradient `.seam` elements were deleted). **Nav is SOLID when stuck** — no backdrop-filter. **No 3D-tilted screenshots** (`--tilt: 0deg` kept for reversibility).
- Motion: entrances `cubic-bezier(.16,1,.3,1)`, hover `(.4,0,.2,1)`, split-clock reveal (opacity 150ms linear / transform 800ms), 60ms stagger, hero headline never animates in, no springs, full `prefers-reduced-motion`. Counters animate FROM the authored DOM value (Gem's live "0x" failure is the cautionary case).
- Screenshots: crop into the story region via `--z/--l/--t` translate() percentages (never `inset:0`, never shrink the frame); white shots on dark sit inset on a surface plate.
- Vignette system (`shared/vignettes.css`): beat-driven `[data-vignette][data-beats]`; **the final-frame rule** — no-JS and reduced-motion users rest on the COMPLETED story; two synced blocks at the bottom of the file define that frame; never a hybrid state. One moving element per viewport, IO-gated.
- Contrast floors: `#8b909b` banned for real text; `#6b6f8c` minimum on white; green text uses `--ok-ink #0e6e34` (`--ok #17994a` is swatch only); drawer text/CTA hard-coded (`#08090c` ground, `#96b0ff` CTA) because `--void` resolves light inside a light wrapper.
- Fairs AI palette tokens and AI Flow language rules live in `HANDOFF-3.md` §11.2 and `AF-BRIEF.md` respectively.

## 8. Brand Direction

Premium enterprise AI platform — peer-level with Linear, Stripe, Anthropic, Vercel; never "a 2020 recruiting site". Real product pixels everywhere (crops and DOM rebuilds, never mock UI, never stock photography — no licensed photos exist; AI Flow deliberately ships none rather than fake it). Honesty is a brand device: visible `{{PLACEHOLDER}}`s, "SOC 2 Type II — not yet certified" in plain words, empty logo slots until written confirmation per company. Green means state (success), never decoration; JobFairX blue is brand/CTA. Restraint: one motion focus per viewport, one overhang fragment per panel.

## 9. Marketing Strategy

- **Business goal of every page:** get an employer to register for a hiring event. Target reader: recruiter/TA lead deciding if an event is worth $495–$1,495, fluent in job boards, not in "matching".
- **The launch story** is interview-location choice (in person / video / phone); **the control story** is "candidates request, you accept." Format order in marketing: **in person → video → phone** (in-person is the market priority; phone real but deliberately downplayed — never in a hero). NOTE: the redesign sets predate this order and use video→phone→in-person — noted and deferred, not fixed.
- **Page strategy** (`PAGE-INVENTORY.md`): 26 hand-built pages in waves 10/11/5; template instances SHRINK to ~2,675 (net −1,198) — pruning beats expanding. Wave 1 closes all 98 dead links; Wave 3 (agreed, NOT started): ai-hiring-compliance, dpa, accessibility. Blocked: customer-stories (no written permission), platform/ai-matching (zero visual evidence of a matching UI).
- **SEO discipline:** never run the "Virtual" title-tag removal (3,520 pages) in the same pass as the city consolidation; kill 8 non-city slugs; fix the sugarland/sugar-land split; the 1,760 evergreen next-{type} pages are the SEO engine and multiply any event-page change.
- **Video strategy:** self-narrating HTML explainer of event day (Indeed check-in video remake) exists; production VO licensing path documented (edge-tts is draft-only; ElevenLabs Starter ~$6/mo commercial via hosted MCP).

## 10. Current Approved Messaging

**Vocabulary law (all streams):** SAY "in-person interviews", "set your interview location", "same event, your choice of room", "hiring events", "video" (not "virtual"); candidates "request", employers "accept", which "schedules". NEVER "in-person events", "virtual events", "event format", "apply/application/applicants" (exception: describing the job-boards' world in the Difference section — Scott-locked), "virtual hiring events/virtual job fairs". **No em dashes in site copy** (Scott: "do not use an m dash" — docs may, site must not). Testimonial quotes are people's words and are never edited.

Key approved copy anchors (verbatim sources in the stream docs):
- Clone homepage hero: "**Hire faster with in-person and video interviews**" (non-breaking hyphen); title "Hiring Event Platform for Employers | JobFairX".
- Scott's standard sub (calendar + pricing): "Register for a hiring event, post your jobs, and select in-person or video interviews. AI Candidate Matching starts immediately."
- Pricing H1: "Flexible Hiring Event Packages" (full at all widths; already live in production).
- Tier-card bullet: "In-person or video interviews"; includes-list item: "In-person, video, or phone interviews" — the mismatch is a documented INTENTIONAL decision, signed off.
- FAQ Q2 (new): "Where do interviews take place?" — "You choose. … It never changes the price."
- Difference section on employer-home: **live-verbatim by explicit decision** after a full implemented-then-reverted round trip (§26). Includes-lists on home and pricing stay identical at 8 items.
- The three testimonials (Target / Western Regional Medical Center / Tesla) — company + role only, no personal names, nothing beyond them.
- Calendar status pills Scott loves and which must survive any redesign prominently: "Matching live" / "Matching soon" / "Early registration" + Save $100 chip.
- The video's FINAL SCRIPT (6 sections) is locked and used verbatim — never paraphrase (`HANDOFF-VIDEO.md`).

## 11. Homepage Strategy

Two active generations:
1. **employer-home.html (live-clone, FINAL):** live page rebuilt with format messaging. Section order and all copy in §3 of `HANDOFF-2.md` / `EMPLOYER-HOME-DEV-NOTES.md` (the newest word — Scott signed off desktop AND mobile 25 Aug). How It Works: registration first; Event day step carries the Interview Settings panel visual; Review & confirm uses real product screenshots (`assets/product/review-confirm*.png`, desktop/mobile variants swapping at the `lg` breakpoint). Ships zero JS; the developer wiring list (hamburger, pricing stepper, feed-driven calendar mock) is in the dev notes.
2. **Concept homepages (reference):** concept-3-hybrid (recommended among 1–3; dark hero → light middle → dark close, "night is the promise, day is the proof, night is the decision"), concept-4-vid, concept-5-aiflow, concept-6-fairs. Scott has not picked a winner.

## 12. Event Calendar Strategy

`page-events.html` (Fairs AI stream): compact live-derived hero on a lavender wash, white card rows on `#f7f8fa`, City as its own column, "Hiring Event" stripped from row labels, the Candidate-matching column (one question, three values on one timeline), Save $100 as a chip not a pill, all-columns-flex width fix (two failed attempts documented), mobile cards below 820px, `var PAGE = 14`. Deep links `?type=` resolve INSIDE the owning IIFE via `selectByValue()` — a synthetic click silently does nothing. No virtual/in-person filter, ever. Calendar tail below the list is still the old hybrid dark design — flagged to Scott, not yet in scope.

## 13. Event Details Strategy

- **CURRENT STATE (supersedes the rest of this section where they conflict — §0.4):** `employer-event-detail-v2.html` is the built, deployed redesign (Austin healthcare, authored via `build-event-healthcare.py`). Three-act story: before the date your schedule fills → on the date you work a queue (full-width live-lobby capture) → the moment it ends the report is ready. Renders ONE true lifecycle state, no on-page toggles (Scott rejected them); the 8-state STATES object lives in the builder for the developer. It is the template for the other four types and the 1,760 city pages (parameterised via the `EV` dict).
- Live anatomy (19 sections, `LIVE-SITE-SCOPE.md` §3): countdown banner → event pill → type-specific H1 → CTAs → stock hero → live trust metrics ("Updated daily" — pre-registered counts are per-event dynamic; show rate + interview/hire averages are type-level constants, §0.2) → logo wall (rights unverified — do not reprint without confirmation) → video → steps → tools → testimonials → pricing (state-dependent) → bundles → FAQ → CTA → contact.
- Redesign template: page-event-detail.html renders five countdown states behind a REVIEW-ONLY switcher (keys 1–5, default A) that must be deleted before production. Same pattern on vid-/af-event-detail. Equal-size tier cards (Scott dislikes the lifted featured card).
- Clone: `employer-event-detail.html` (Dallas Technology event) is captured and built and is the declared NEXT work target of the clone stream; do not start before Scott directs scope. **Correction to HANDOFF-4 §8** (per the Aug 25 9-agent verification, recorded in memory `handoff-4-verification-corrections`): the event page does NOT contain the old ✕/✓ Difference table or a "This Isn't a Job Board" CTA band — that section exists only on employer-home.html. Scope the event-page work from the page as it actually is. Also: `build-event-detail.py` will hard-abort if run today — its three review-row anchors (lines ~280–282, `>Tamara Williams</b>` etc.) no longer exist in the built employer-home.html after the real-screenshot swap; rewrite or drop those `loc` calls before any run. Every other anchor it clones from home still matches.

## 14. Employer Application

The employer product itself (for accurate marketing claims; two prototype generations):
- **Public prototype** (screenshot source): scottjobagent.github.io/jobfairx-prototype/* — visual-v3, lobby-v3, setup-flow-v3, interview-screen-v3, edit-post-v3, account-billing, share-preview, plus the **Healthcare V3 set** (visual/lobby/interview-screen/setup-flow-v3-healthcare.html, also downloaded to `tools/`). The healthcare V3 set is the current best product reference and the video's capture source.
- **App nav:** Events · Interviews · Messages · Automations · Analytics (+ hidden Candidates tab — the only nav page not live; NEVER show it in marketing or video).
- Dashboard: one row per registered event; INTERVIEW LOCATION column; setup state; seat/job metering; candidates cell; live mode disables Edit/Share. Setup flow: 7-step wizard (job post → details → review → confirmation → interview settings → screening → review/submit); add-job mode re-skins steps 1–4. Interview settings: segmented Video/Phone/In-Person; external link is a sub-choice inside Video (validated URL); in-person requires full address + parking/arrival; slot duration 15/30/60; capacity; auto-accept.
- Prototype-only scaffolding (strip for production, documented in the healthcare files): A/L corner toggle, `?autom=` seeding, package dev toggle, `.pgt` hidden toggles, jax research modal, TEMPORARY hide-blocks (Candidates nav, developer-doc link).
- Rich behavioral detail (roomless flows, phone call panel, notes-beside-resume, reschedule format control, analytics rules, credits/registration) is documented in the healthcare V3 files' own WHY comments — they are the design record. The prototype still contains internal contradictions (dueling purchase-modal feature lists, seat-plan naming, demo-data inconsistencies) — see §25.

## 15. Candidate Application

Mostly out of this repo's scope. What matters for marketing: candidates register per city/date, are verified within ~20 miles, get prep materials and email+SMS reminders, request interviews at self-chosen slots, and **cannot reschedule** (seeker-side model). The seeker prototype is a separate Desktop project with its own handoff chain (`~/Desktop/HANDOFF-4.md` current) — read it end-to-end before touching that stream. Seeker vocabulary: "Job Fairs" (employer side says "hiring events").

## 16. Interview System

Event day runs as a queue in the lobby: tabs Waiting to interview / Interviewing / Interviewed / Not yet interviewed. Video events: Waiting splits into "Interview rooms" (Ready + Start interview) and "Waiting rooms"; rooms run in parallel up to package seats. Phone/in-person/external ("roomless") events: one longest-wait-first list, "Checked in" badge, call panel / mark-as-interviewed flows, notes carried from interview into evaluation. In-room: timer, mute/video, Notes · Resume · Chat panels; notes come back in the post-event report. Event end: tabs become Summary / Interviewed / Not interviewed; report is ready the moment the event ends. **The app does not track hires** — outcomes are recruiter Yes/Maybe/No only; never claim hire tracking, ROI, or time-to-hire in marketing.

## 17. Messaging & Automations

Direct candidate chat (bottom-right dock everywhere; Messages page with Inbox/Archived, All Events + All Jobs filters). **Five automation presets**: Message new candidates / Message scheduled candidates / Email declined candidates / Missed interview follow-up / Post-interview follow-up — On/Off per job or event, merge fields `{CANDIDATE_FIRSTNAME} {JOB_TITLE} {COMPANY} {RECRUITER_NAME} {INTERVIEW_TIME}`, optional external application link, "Request an automation". Marketing claims only what captures verify: presets send on their own; **no stage→trigger mapping is claimed anywhere** (not visible in any capture — deliberate).

## 18. AI Candidate Matching

AI matches posted job titles to registered candidates and promotes jobs directly to them; activates on posting; requests within a few hours; notification per request + 9:00 AM daily summary email. **No screenshot of a matching UI exists** — the ai-matching platform page stays unbuilt, and matching is drawn as an obvious labelled DIAGRAM (V2 vignette), never mocked chrome. Do not blur the mechanic into generic ATS language; no ATS/integration claims exist or may be invented.

## 19. Event Categories

Healthcare · Diversity · Veteran · Technology · Entry-Level. Product-canonical colours: Diversity orange `#e07b39`, Technology blue `#2f5cff`, Healthcare teal `#12897f`, Veterans red `#d1454b`, Entry-Level sky `#3aa0e6` (keep marketing and product in sync). A type is an audience, never a format. Per-type stats only where published (§2). The "Denver Engineering Event" neutralisation exists so screenshots never invent a sixth type.

## 20. Components

- `.anno` annotated-screenshot component (base.css + motion.js `initAnno`): numbered pins over real screenshots paired to caption keys; pins/crops are ONE calculation — recompute, never eyeball; anno figures sit on light sections; pins hide below 780px.
- `.panel`, `.frag` (max two per hero), `.crop` (translate() percentages of the image), `.video-ph` (5 instances, one component — production swap is inner markup only), `.shotgap` (honest capture gaps — never mock).
- Vignettes V1–V6 + static upgrades S1–S4 (`VISUAL-AUDIT.md` Part B–D): V1 Request→Accept→Scheduled is the signature.
- Fairs AI/AF chrome components per their briefs. Clone-page bento (`id="built-in-tools"`): zero-JS static showcase, authored once in the home builder, imported by the event builder.
- Video player components: scenes/callout rings/captions/chapters/scrub rail in `video-template.html`.

## 21. Important Files

**Read order for a new session (after this file):**
1. `HANDOFF-4.md` (newest clone-stream state) → 2. `HANDOFF-3.md` (**§0 two-session rules FIRST** — "the single largest risk in this project") → 3. `HANDOFF-2.md` → 4. `HANDOFF.md` (§2 product model + §3 verified facts are LAW; §8 lessons are pre-paid mistakes) → 5. `EMPLOYER-HOME-DEV-NOTES.md` → 6. `HANDOFF-VIDEO.md` (if touching the video) → 7. `AF-BRIEF.md` / `LIVE-SITE-SCOPE.md` / `DESIGN-SYSTEM.md` / `CONTENT-SPEC.md` / `PAGE-INVENTORY.md` / `VISUAL-AUDIT.md` / `COST-PER-HIRE-CLAIM.md` as the task requires.

**Never hand-edit:** employer-*.html build outputs, `assets/live-capture/*`, `video-event-day-lobby.html` (edit `build-video.py`). **Never publish:** strategy docs to the preview repo, `assets/_reference-do-not-publish/`, `interviews-pending.png` (byte-identical dup of interviews.png).

## 22. Completed Work

- Full 28-page redesign + design system + strategy docs (Aug 17); Wave V vignettes; concept-4 vid set; concept-5 AI Flow 19-page fan-out (built, adversarially verified, a11y-fixed, deployed, 24/24 URLs live).
- Fairs AI: concept-6 homepage (vFairs teardown-derived, JobFairX blue), calendar rework, pricing update — all pushed; nothing half-finished.
- Live-site clone stream: employer-home FINAL (desktop signed off + mobile v1 + view toggle), employer-pricing (exact clone + Scott's headline/sub; 125px pixel-diff, all anti-aliasing), employer-faq (virtual sweep + new Q2; 10 questions), event-detail captured/built, bento shipped to both pages, dev notes written.
- Cost-per-hire research (4-agent sourced sweep) and the Difference-section saga resolved (reverted to live-verbatim).
- Healthcare 35/8 restored on both healthcare pages with "2025 platform data" attribution.
- Product video: complete rebuild on the Healthcare V3 prototype — real captures (whole-page Interviewing tab, real photos in both interview windows from paid event-details images), locked verbatim script, no lateral pans, no long pauses, safe-zone build checks; published as an artifact and synced to the repo; HANDOFF-VIDEO.md written (the ~2:09 six-section build). A parallel session then extended it — see §23.

## 23. In-Progress Work

- **Video stream is LIVE in a parallel session** (as of Aug 25 ~15:40): it rebuilt the video from the six-section 2:09 cut documented in HANDOFF-VIDEO.md to a **4:12 seven-section** cut (an "Interviews" chapter added between Before the Event and Event Status; Before the Event expanded; VO chunks renamed `vo-draft/p*.mp3`), still en-US-AvaNeural, and synced `build-video.py`, `video-event-day-lobby.html`, and the artifact (same URL, version 1787697610-33b2). HANDOFF-VIDEO.md has NOT been updated for this rebuild — for video state, trust the repo's `build-video.py` + the deployed artifact over that doc's scene table/durations, and coordinate with that session before touching any video file.
- **Video voice pick:** Scott has 16 voice samples and has not chosen. On his pick: `vo-env/bin/python build-video.py en-US-<Name>Neural`, republish the SAME artifact URL (from a new session pass `url:` or it forks), sync repo copies. Until then the video stands at Ava. (The `vo-env` venv lived in a session scratchpad and is volatile — a new session recreates it: `python3 -m venv vo-env && vo-env/bin/pip install edge-tts pillow`; full recipe in `HANDOFF-VIDEO.md`.)
- **Clone-stream mobile iteration:** employer-home-mobile.html is explicitly v1; Scott iterates by screenshot; expect art direction.
- Nothing else is half-finished — every other stream closed its loop before handoff.

## 24. Outstanding Work

Per stream, decided but not started:
- **Clone stream:** Scott directed the event-page work Aug 25 evening and `employer-event-detail-v2.html` shipped (§0.4) — the "do not start event details" gate is history. Remaining: extend v2 to the other four types + city parameterisation (via the builder's `EV` dict), mobile designs for pricing/FAQ, dev-notes docs for pricing/FAQ/event-v2, the `minDays` 31→30 developer flag, and mobile iteration on employer-home-mobile v1.
- **Fairs AI stream:** resolve HANDOFF-3 §14 with Scott; bring page-pricing.html into the Fairs AI language (clicking Pricing from the white calendar header jumps into a dark page with a different nav + surviving "Book a demo"); decide the calendar's hybrid tail; add concept 6 to index.html.
- **Redesign set:** HANDOFF-2 roadmap #8–#15 (CTA verb ladder, headline polish with recorded replacements, sentence-case sweep, etc.); FAQ expansion was roadmap #7 (may have been executed via build-employer-faq.py — verify against the repo); Wave 3 trust pages; wave-close pass on page-platform.html (unlock the five stale "Coming soon" cards, delete stale footer comments); programmatic generation (city-hub ×352 etc.) designed, not generated.
- **Video:** production licensed VO swap (ElevenLabs path documented); upstream prototype data fixes then recapture; possible MP4 export.
- **Before ANY production ship:** delete review-only switchers/pills, AVIF/WebP + lazy loading (~70% saving), replace the five .video-ph placeholders, fill placeholders from verified data only, fix prototype PII/vocabulary upstream, clear or re-capture messages-thread.png (likely production candidate names, already live on the homepage).

## 25. Known Bugs / Issues

**Live-site correctness bugs (rewrite in place, don't redirect):** three resources articles factually wrong since the in-person launch (virtual-vs-in-person-hiring-event argues AGAINST the launched capability; virtual-hiring-events says "No Zoom, no external links, no downloads"; how-does-a-virtual-job-fair-work). `/employer/job-fairs/{state}` hard-500s. Hardcoded "Apr 22, 2026" testimonial date on every live event page. Live forms have zero `required` attributes. All live technology logos fabricated; healthcare wall unverified.

**Contradiction ledger** (format: Conflict → Evidence → Most recent → Recommended):
1. **30 vs 31 days — RESOLVED Aug 25** (§0.1): Scott ruled 30. Copy uses 30 everywhere; pages still saying 31 (the vid/af ports) need the sweep; the live code's `minDays:31` is a developer task. The residual work is applying the ruling consistently, not deciding it.
2. **Concept 5 vs concept 6 for the af- set** → AF-BRIEF builds on concept-5 chrome; concept-6 (Aug 24) is newer but is its own homepage → HANDOFF-3 is the authority → don't rebuild af- chrome from either without checking HANDOFF-3; Scott hasn't picked a winner.
3. **Purchase-modal feature lists (prototype)** → lobby sells jobs/interviews/seats; visual sells events-access/matching-tiers/support at identical prices → both current in the prototype → production must pick one; flag to Scott before any marketing claim relies on either.
4. **Seat-plan naming** → lobby says "Starter · N of 2 seats"; dashboard/setup say "Growth · N of 5"; live pricing says Starter = 2 seats, prototype Growth = 5; other tiers unknown → live pricing page wins for marketing; other tiers ship as [PLACEHOLDER].
5. **91% show rate vs 66% attendance in analytics.png** → both real (platform-wide vs one account/one range) → handled by the analytics honesty note; never print a platform average beside one account's dashboard.
6. **includes-list count** → event-detail clone lists 9 (with dashboard item), home/pricing list 8 → Scott's call was 8 on home+pricing → align event-detail when its update round comes.
7. **"84% average interview show rate"** on the Dallas event CTA vs "only three show rates exist" → 84% is live-site sourced (event CTA stat), provenance unstated → keep as live-verbatim on clones; never present as a type-wide stat.
8. **Format order** → clone stream binds in person → video → phone; the redesign sets predate this → deferred, fix only when Scott directs a pass over those sets.
9. **README's run instructions (port 8765) are stale** → 8765 is a foreign server that 404s → use the scratchpad server (8732/8790 patterns per stream docs).
10. **Prototype demo-data inconsistencies** (same candidate different jobs per view; timezone drift CT/PDT; duplicate Chicago dropdown entry; decorative vs computed tab counts; two rival mark-as-interviewed modals with different rosters; setup sidebar links to visual.html not the -healthcare file; hardcoded Aisha Rahman resume under any candidate name) → demo scaffolding, upstream in Scott's prototype → don't "fix" in marketing copies; flag upstream; a real build must pick one source of truth per count.
11. **Empty {{LOGO}} slots vs AI Flow "no logo walls"** → keep-every-placeholder won → Scott may prefer removal in AF language; unresolved.
12. **'429 pre-registered veterans'** renders as authored fact on event-detail pages but is feed-rendered in production, not placeholder-marked → open with Scott; fix both pages together.
13. **`build-event-detail.py` review-row anchors drifted** → the real-screenshot swap on employer-home removed the mock-table strings its lines ~280–282 probe for → most recent: Aug 25 verification → fix those three anchors before running the builder (see §13).
14. **HANDOFF-4 doc-precision errata** (Aug 25 verification; facts fine, mechanisms off): pricing headline is a span-unwrap not `<br>`; the live pricing payload (ladders/discount codes) was never saved to disk — the codes exist only as HANDOFF-4 prose and `employer-pricing.html`'s inline script; FAQ raw "virtual" count is 4 (4th is an invisible provenance comment; rendered = 3); FAQ answers are hardcoded in the builder's ANSWERS list (JSON-LD is provenance, not mechanism); employer-home's footer still says "Virtual Job Fair Calendar" (clone fidelity — home is FINAL; flag to Scott, don't edit); af-solutions-healthcare.html carries a stale "honest placeholders" comment on the now-real 35/8 tiles.

## 26. Rejected Ideas

(Full lists: HANDOFF.md §8.8/§2, HANDOFF-2 §6, HANDOFF-3 §13/§15, HANDOFF-4 §6/§7.5, RECOMMENDATION.md, VISUAL-AUDIT.md.) Highlights — rejected on evidence or by Scott's explicit call, do not relitigate without new data:

- "In-person events" as a concept (the central rejected model — rebuilt wrong twice even after correction).
- **The Difference-section saga (HANDOFF-4 §6):** expert critique → mockup options → cost-per-hire row iterations with superscript citations → row removed → ENTIRE section reverted to live-verbatim. Do not re-pitch. The seven-row table Scott liked is ON HOLD, not dead. "Hire rate", never "Conversion rate". No dollar figures in the table.
- Homepage fixes Scott explicitly DECLINED at final audit: trust-marquee cleanup, Tesla stat-tile framing, meta "book interviews", tier-bullet/includes phrasing mismatch, mixed-timezone screenshot, Starter/Pro pricing-card gaps. Declined = declined.
- Four separate interview-location pages · standalone job-postings page · blog · careers page · case-study pages · title×city programmatic (247,808 URLs) · more city×type pages · frosted nav · gradient seams · coloured bloom · 3D tilt · marquee/logo walls · count-up-to animation · lifted featured pricing card · "Book a demo" (killed everywhere on AI Flow; one survivor on page-pricing.html flagged) · Contact Us in the Fairs AI nav · "Status" as the calendar column name · closes/closed states on the calendar · side-by-side format mocks, format toggles, format badges, scheduling-modal format field (clone stream) · scroll-sync messaging section and tabs showcase (lost to the static bento) · em dashes in site copy · stock photography · ATS claims · fake maps · mocked matching UI · invented stats (35/8 ban outside healthcare stands).
- Video stream: mock UI on black; intro title card; candidates page on screen; lateral pans; long pauses; paraphrasing the locked script; Andrew and Emma voices (superseded by Ava, pending final pick).

## 27. Do Not Break

The invariants across streams (each stream doc has the full list — this is the union of the load-bearing ones):

1. Product model + vocabulary law (§2, §10) in every rendered sentence, alt text included.
2. Two-session rules (HANDOFF-3 §0): file ownership per stream; check the preview repo head via API before pushing; upload only files you changed; never a full tree.
3. No destructive git. No `git add -A`. No force-push. Uncommitted working tree = other streams' live work.
4. Edit builders, never outputs; keep every `sub()` loudly asserted; home builder before event/mobile builders; bump `CSS_V` on any CSS change.
5. Frozen captures (`assets/live-capture/`) untouched; re-capture deliberately and re-run the FULL NEUTRALISE list on any screenshot re-capture (regex gi; whole-clause for "application steps"; the Tamar→Robin pair stays dropped for lobby captures).
6. `{{PLACEHOLDER}}` discipline: never fill without a verified source; never drop one in a port; never decorate one.
7. `tools/mcheck.py` clean on every touched page (plain headless 390 runs lie); footer hash-identity per set; exactly one h1; `[hidden]` guard present; no interviews-pending.png; zero banned vocabulary in rendered text.
8. Design laws: hard cuts, solid stuck nav, no bloom/tilt/springs, display 500 (concept deviations only), counters FROM authored values, final-frame rule, one motion per viewport, contrast floors, `.crop` translate() rule, drawer hard-coded colors, `setTotal` clearTimeout on every path, SVG wires 120/120, `--s-7` token defined, deep links resolved inside the owning IIFE, setDrawer bind-all fix.
9. Clone-page specifics: live chrome wins (header/footer); signed-off content stays (Difference section live-verbatim, marquee, stat tiles 36/7 92/19 51/14, verbatim testimonials); includes-lists identical at 8; "virtual" hard guards (pricing exactly 2 occurrences, FAQ page 3); FA Pro CDN frozen at 5.10.0; og:image/canonical left as production; inline styles for new markup.
10. Video stream: locked script verbatim; never the candidates page; safe-zone checks stay in `check_scene`; same artifact URL on republish (`url:` param from a new session or it forks); healthcare V3 prototype is the capture source of truth.
11. Prototype JS contracts (if touching `tools/*-healthcare.html`): method layers monkey-patch exact base function names and DOM ids; table column order is load-bearing; BroadcastChannel `jobfairx-demo` contract; sessionStorage `jfxMethod`; URL params; `.pgt` demo override.
12. Legal: never draft policy text; diversity compliance blocks stay for counsel; no unverified logo/attendance claims; only the three approved testimonials; fictional demo names (Dana Whitfield et al.) are the PII FIX — never "re-fix" them.
13. Never claim hire tracking/ROI/time-to-hire. Platform totals attributed as totals earned by video events — never imply in-person volume.
14. Desktop is iCloud-synced — no bulk deletes. Don't kill other sessions' server processes; Scott's real Chrome is running.

## 28. Do Not Reintroduce

Compressed ban list (details in §26): in-person events framing · "apply" language · gradient seams · frosted/backdrop-filter nav · 3D tilt · coloured bloom · marquee logo walls · count-up-to · lifted pricing card · "Book a demo" · "Conversion rate" label · cost-per-hire homepage row (without Scott) · dollar figures in the Difference table · the reverted Difference redesign · per-method chip colors (prototype) · two-section waiting view for roomless events (prototype) · "Hired" pipeline stage · manual no-show button · corner-overlay or `left:100%` PLACEHOLDER chips · `.crop` inset:0 · bare Tailwind utilities in clone pages · regex spans over repeated markup · a next-inperson URL family · a sixth event type · mock UI for missing screens · intro title cards, lateral pans, or paraphrased narration in the video.

## 29. Design Principles

Premium = restraint measured against peers, not effects: tinted grounds, weight 500, hairline-or-shadow, hard cuts, one motion per viewport, real pixels only. Honesty is a design device (placeholders, shotgaps, "not yet certified"). The designed state is the only state — JS-dependent markup ships dead through static pipelines; native elements over JS. Failure must leave a truthful page (counters, final frames, no-JS rest states). Density serves the story (2+2 rows, not the app's 8+8). Mobile is a dedicated design. Recompute, never eyeball (pins, crops, coordinates).

## 30. Content Principles

Every sentence about events/locations gets checked against §2. Only verified facts; placeholders otherwise; quotes never edited; no invented numbers, and numbers verified against LIVE-SITE-SCOPE.md before entering any brief. Outcome-led headings; sentence case; no em dashes in site copy; bare format labels in headings vs prepositions in prose ("In person" heading, "interview in person" prose). Live-site copy is NOT product truth (its strings often don't exist in the app — check the app first). Render with JS before concluding anything is absent from a live page. Scott voice-dictates — interpret intent through transcription noise, write the lawful version, note it in one sentence.

## 31. Open Questions

Awaiting Scott (do not resolve unilaterally):
1. ~~30 vs 31 days~~ RESOLVED — 30 (§0.1). 2. Video voice pick (16 samples out). 3. Mobile v1 feedback. 4. ~~Event-details scope~~ v2 shipped (§0.4) — remaining scope is the other four types + city rollout. 5. Concept winner (six candidates). 6. page-pricing.html Fairs-AI-ification + surviving "Book a demo". 7. Calendar's hybrid dark tail. 8. {{LIVE_EVENT_FEED}} note visibility for the developer. 9. Empty {{LOGO}} slots in AF language. 10. Diversity FAQ "respond to" rewording (voice check). 11. FAQ interview-volume + cancellation/refund answers (a refund policy doesn't exist anywhere while $29,700 bundles sell "never expire" credits). 12. Interviewer seats for Starter/Pro beyond captured facts. 13. SOC 2/compliance status. 14. Per-type stats: are the veterans/diversity/entry-level/technology live figures (§0.2) as real as healthcare's Scott-confirmed 2025 data? 15. Logo-wall rights (veterans wall mixes real names with invented-looking ones); testimonial personal-name permissions. 16. onNewYearsSale sixth banner state; exact D→E cutoff hour. 17. In-person pricing parity (assumed same price per FAQ Q2 copy Scott approved; formal parity unconfirmed for bundles/discounts). 18. 15.6% hire-rate stat provenance. 19. Scott's live article's old Difference table (apply approved corrections when next touched). 20. 429-veterans placeholder marking. 21. delete difference-options.html? 22. Ahrefs + Search Console access for the SEO pass. 23. Seeker-side naming items (Events→Job Fairs etc.).

## 32. Recommended Next Steps

None unilaterally. The most likely Scott directions, by stream: video voice pick → rebuild/republish; mobile-design feedback → iterate v1; "move to event details" → clone-stream target (audit first, per HANDOFF-4 §15); Fairs AI → pricing-page language + §14 questions. When he picks one, read that stream's doc chain first (§21), confirm state against the repo, then work.

## 33. Full Project Context / Historical Decisions

Chronology: **Aug 17** — redesign built (28 pages, design system from a 17-site teardown, strategy docs, HANDOFF.md); platform + solutions pages verified against 14 sanitised product screenshots. **Aug 18–19** — Wave V vignettes; concept-4 vid; concept-5 AI Flow 19-page fan-out (11 build agents + adversarial verify — the fan-out model that worked twice); HANDOFF.md §14. **Aug 20** — af- set on disk. **Aug 23–24** — pivot: Scott chose cloning the live site page-by-page via Python builders over editing the redesign (HANDOFF-2); Fairs AI stream: concept-6 from a vFairs teardown, calendar rework, pricing update (HANDOFF-3); pricing clone captured all three bundle ladders + two discount codes (superseding HANDOFF-3's "never captured"). **Aug 24–25** — Difference saga and revert; cost-per-hire research; healthcare 35/8 confirmed and restored; FAQ clone; mobile v1; homepage signed off (HANDOFF-4, EMPLOYER-HOME-DEV-NOTES). **Aug 24–25 (this session)** — product video: Indeed remake → real screenshots → interview-location scene (video/in person/phone order) → Emma → locked verbatim script + 17-point brief → full rebase onto the Healthcare V3 prototype (hidden A/L toggles, headless repaint workarounds, photo compositing from paid event-details images) → overlap fixes hardened into build-time safe-zone checks → Ava, ~2:09 → HANDOFF-VIDEO.md → this master handoff.

The deepest pattern across all streams: **claims are downstream of captures.** Every marketing sentence traces to a screenshot, a live payload, or Scott's explicit confirmation — and when it can't, it ships as a visible placeholder. The second pattern: **lessons get institutionalized** — every expensive mistake became a build-time check, a banned technique, or a documented rule (HANDOFF.md §8, HANDOFF-2 §9, HANDOFF-3 §13, HANDOFF-4's incident notes). Read those before repeating one.

---

## When this handoff is used in a new chat

FIRST: read this file. Then inspect the relevant repository files and verify the current implementation against it. Then review the stream docs in the §21 order, plus any relevant assets, prototypes, or documentation.

DO NOT immediately start coding. First establish that you understand the project. Then provide a concise confirmation that you have:

- Read the handoff
- Reviewed the repository
- Understood the current state
- Understood the design system
- Understood the content strategy
- Understood completed and incomplete work
- Identified any conflicts or open questions

THEN STOP. Do NOT recommend a task. Do NOT start implementing anything. Do NOT assume what Scott wants to work on next.

Instead ask exactly:

**What would you like to work on first?**

Wait for the answer.
