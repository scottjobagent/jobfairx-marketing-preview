# JobFairX Marketing — Session Handoff 4

**Written:** 25 Aug 2026, at ~80% context in a long Claude Code session.
**Covers:** the **employer live-page clone stream** — the exact clones of the live
pricing and FAQ pages with Scott's updates, a full round-trip redesign-and-revert
of the homepage "Difference" section, the cost-per-hire research program, the
prototype-screenshot pipeline for the Review & Confirm visual, the homepage final
audit and sign-off, and the new **dedicated mobile design** of the homepage.

**⚠️ READ FIRST: TWO CLAUDE SESSIONS SHARE THIS DIRECTORY.** HANDOFF-3.md §0 is
still law. Getting it wrong destroys another session's uncommitted work.

**Companion docs, reading order:** this file → `HANDOFF-3.md` (the Fairs AI
stream: concept 6, calendar, af- set — NOT touched this session; its §0 shared-
directory rules and §14 open questions still stand) → `HANDOFF-2.md` (the
original employer-clone stream this session took over and extended) →
`HANDOFF.md` (§2 product model and §3 verified facts are LAW) →
`EMPLOYER-HOME-DEV-NOTES.md` (developer handoff for the homepage, written this
session) → `COST-PER-HIRE-CLAIM.md` (research substantiation, written this
session) → `LIVE-SITE-SCOPE.md` / `DESIGN-SYSTEM.md` / `CONTENT-SPEC.md`.

---

## 0. The two-session problem — unchanged, plus what this session did about it

`~/Desktop/jobfairx-marketing/` is worked by multiple Claude sessions publishing
to the same repos. Rules that saved us repeatedly this session:

1. **Never run `git checkout` / `restore` / `stash` / `reset` / `clean` here.**
   This stream's work is uncommitted in the working tree (~90 modified files is
   normal). The parallel session commits locally; origin is far behind. Read-only
   git commands are fine.
2. **The only push path is the github.com web UI in Scott's Chrome** (no git
   credentials, no gh, no SSH on this machine). Full procedure in §12.
3. **Upload only the files you changed.** Both streams publish to
   `scottjobagent/jobfairx-marketing-preview` (public, GitHub Pages at
   https://scottjobagent.github.io/jobfairx-marketing-preview/).
4. **Cross-stream edits happened this session at Scott's explicit direction**:
   this session appended clearly-marked sections (8c–8f) to the other stream's
   `build-employer-home.py`. The assertion contract made this safe — the other
   session's builder evolved mid-day underneath us and everything still composed,
   because every `sub()` aborts loudly on anchor drift. Keep that discipline.
5. HTML comments are stripped for every preview upload:
   `re.sub(r'<!--.*?-->\n?', '', src, flags=re.S)`. Strategy docs never go to the
   public repo.

---

## 1. Executive overview

**Purpose.** Update jobfairx.com's employer-facing marketing pages to market the
newly launched in-person interview location (and phone), remove the retired
"virtual" identity, and hand the developer pixel-exact prototypes of every page.

**Method of this stream (different from the Fairs AI stream):** capture the LIVE
page (server HTML or rendered DOM), rebuild it byte-faithfully through a Python
builder whose every replacement asserts its match count, then apply Scott's
updates as further builder steps. "Edit the builder, never the output."

**Business goal.** Employers buy flat-rate event packages ($495/$895/$1,495) or
bundles. Every page drives to event registration.

**Current phase.** Homepage: FINAL (desktop signed off, mobile design v1
delivered, developer notes written). Pricing and FAQ clones: final with Scott's
updates. Next page: **event details** (`employer-event-detail.html`).

**How Scott works (unchanged, HANDOFF-3 §17, all reconfirmed this session):**
voice-dictated bursts with transcription noise ("higher rate" = "hire rate",
"hiring bank" = "hiring event", "q l n d has that little s underline" =
LinkedIn's superscript footnote); wants to be SHOWN (mock in chat before
building — he picks fast from rendered images); asks "what do you recommend?"
and expects a verdict; corrects by screenshot; **when he asks you to confirm
understanding, confirm and STOP**; hates em dashes in site copy; needs
clickable https:// links (never localhost).

---

## 2. Product model & verified facts — the law, plus this session's additions

Everything in HANDOFF.md §2 (event = market moment; five event types; interview
location is a per-employer setting: in person / JobFairX video / phone / own
link; candidates REQUEST, employers ACCEPT, accepting IS scheduling; auto-accept
is an optional toggle) and §3 (stats, pricing, show rates, three customers,
20-mile fact) remains binding. **New verified facts captured this session:**

- **All three bundle ladders**, from the live pricing page's SvelteKit payload
  (per-event price by count / total savings):
  - Starter (job-fair-starter-N, base $495): 5=$470, 10=$445, 15=$420, 25=$395,
    40=$365, 50=$345, 75=$320, 100=$297 (save $19,800)
  - Growth/exhibitor (job-fair-exhibitor-N, base $895): 5=$850, 10=$805,
    15=$760, 25=$715, 40=$655, 50=$620, 75=$575, 100=$537 (save $35,800)
  - Pro/sponsor (job-fair-sponsor-N, base $1,495): 5=$1,420, 10=$1,345,
    15=$1,270, 25=$1,195, 40=$1,095, 50=$1,045, 75=$970, 100=$897 (save $59,800)
- **Hidden discount codes** in the payload: Non-profit $395, Small-business $795.
- **Stepper/cart mechanics** (verified against live code + clicks): valid event
  counts are 1–4 plus the bundle rungs; selecting a tier resets count to 1; at a
  bundle count the card's header price becomes the bundle per-event rate; cart
  URL is `bundle=<id>` at bundle counts else `pkg=<pkgId>&qty=N`, plus
  `skipEvent=1&returnTo=<path>#pricing`; Reserve on an unselected card fires
  that card's pkg at qty=1.
- **HEALTHCARE 35/8 IS NOW REAL: 582 healthcare events in 2025, employers
  averaged 35 scheduled interviews and 8 hires per event — confirmed by Scott
  (25 Aug chat) and published as "JobFairX 2025 Platform Data" in his own
  article** (jobfairx.com/employer/resources/cost-per-hire, byline Scott
  Lobenberg, July 2026). The old purge-on-sight rule for "35/7-8" is superseded
  FOR HEALTHCARE ONLY. It now lives on the metrics tiles of
  `page-solutions-healthcare.html` and `af-solutions-healthcare.html`
  (attribution "2025 platform data"; the explanatory note under the tiles was
  rewritten to match). Veterans/market figures (Portland 73/19, McAllen 728/73/19
  etc.) remain per-event and must never be presented as type-wide.
- **Scott's hire-rate stat:** JobFairX "more than 15.6%" vs job boards
  "2 to 3%"; he named it "Hire rate" (not "Conversion rate"). Currently NOT on
  any page (the section that carried it was reverted). Available for future use.
- **The live site drifted from HANDOFF-3's audit:** the live pricing page's H1
  is already "Flexible Hiring Event Packages" (Scott's approved headline shipped
  to production); its title tag, includes list, and CTA had not caught up.
  Always re-capture before trusting an old capture.

**Vocabulary law refinements exercised this session:** "applicants"/"apply" are
allowed when describing the JOB BOARDS' world (the Difference section's left
column and lead paragraph — deliberate rhetorical exception, now Scott-locked);
testimonial quotes are people's words and are never edited; `virtual.jobfairx.com`
Sign In URLs keep the word (login domain); everything else follows the ban.

---

## 3. What exists — this stream's files

### 3.1 Pages (repo root, all deployed on the preview repo)

| File | What it is | Builder |
|---|---|---|
| `employer-home.html` | Live homepage clone + Scott's updates; FINAL | `build-employer-home.py` (other stream's file; sections 8c–8f are this session's) |
| `employer-home-mobile.html` | **Dedicated mobile design** of the homepage (v1) | `build-employer-home-mobile.py` (this session; runs AFTER the desktop builder, transforms its output) |
| `employer-pricing.html` | Exact live pricing-page clone + updates | `build-employer-pricing.py` (this session) |
| `employer-faq.html` | Exact live FAQ clone + updates + dev-note pill | `build-employer-faq.py` (this session) |
| `employer-event-detail.html` | Dallas Technology event clone (other stream) — **next work target**, untouched this session | `build-event-detail.py` (other stream) |
| `mobile-view.html` | Phone-frame viewer (390px iframe + page switcher); defaults to the mobile design | hand-written, staged copy in session scratchpad |
| `difference-options.html` | 3-option Difference mockup page — review scratch, **deletable on Scott's word** | one-off |

### 3.2 Captures (assets/live-capture/ — additive files only, dir belongs to the other stream)

- `pricing-live-dom.html` — SSR of /employer/hiring-event-pricing, 24 Aug,
  scripts stripped (SSR had no modulepreloads/iframes; capture = curl + strip 2
  script blocks).
- `faq-live-dom.html` — SSR of /employer/hiring-event-faq, 24 Aug, scripts
  stripped. NOTE: the FAQ accordion's ANSWERS are not in the SSR DOM — they
  hydrate client-side; the builder injects them from the page's FAQ JSON-LD.
- (existing: `employer-live-dom.html`, `event-detail-live-dom.html` + css/img.)

### 3.3 Product screenshots added (assets/product/)

- `review-confirm.png` (1648×1218 px = 824×609 css @2x) and
  `review-confirm-mobile.png` (1168×1302 = 584×651 css @2x) — ONE unified
  application window captured from the event-lobby prototype: "Candidates
  awaiting your response (2)" with Accept/Decline/Reschedule + hairline divider
  + "Upcoming interviews (2)" (retitled from "Candidates with upcoming
  interviews"; its location column hidden). Referenced with `?v=2`. Recipe §11.

### 3.4 Mobile image variants (assets/employer-home/)

- `healthcare-m.jpg`, `diversity-m.jpg`, `veteran-m.jpg`, `tech-m.jpg`,
  `entry-level-m.jpg` — 780×975 (4:5) PIL center-crops (biased upward to keep
  faces) of the five event-type photos, JPEG q86, used only by the mobile page.

### 3.5 Docs written this session

- `EMPLOYER-HOME-DEV-NOTES.md` — the homepage developer handoff. Leads with
  Scott's chrome ruling (see §7). Hand this to the developer.
- `COST-PER-HIRE-CLAIM.md` — the full cost-per-hire research: article-aligned
  claim, Appcast backup framing, sources with URLs, attack-surface answers,
  status "NOT currently on the site".
- `HANDOFF-4.md` — this file.

---

## 4. The builders — file-by-file

All follow the same contract: read a capture (or a built page), apply `sub()`
replacements that ABORT unless the match count is exact, log every step, write
the output. Provenance comment at the top of every output (stripped for the
public preview).

### 4.1 `build-employer-pricing.py` (355 lines-ish, this session)

SRC `assets/live-capture/pricing-live-dom.html` → OUT `employer-pricing.html`.
1. De-frameworkise (data-svelte-h ×29 dynamic, sveltekit body attr, HTML_TAG
   markers). 2. Localise (app.css/page.css → `assets/employer-home/*.css?v=2` —
   the pricing page uses the SAME two stylesheets as the homepage; favicon was
   RELATIVE `../favicon.png` in SSR, unlike the rendered-DOM captures; logo ×2).
3. Scott's updates: headline "Flexible Hiring Event Packages" full at all
   widths (live hides "Flexible" on mobile — he chose one headline everywhere;
   implemented via `<br>` + `style="max-width:24ch"`); his standard sub
   ("Register for a hiring event, post your jobs, and select in-person or video
   interviews. AI Candidate Matching starts immediately."); "In-person or video
   interviews" bullet inserted on all three tier cards between the
   scheduled-interviews and seats bullets; includes list kept at 8 by replacing
   the dashboard item with "In-person, video, or phone interviews"; full
   virtual sweep (title/og/twitter ×3, descriptions ×3, CTA "hired through our
   hiring events", footer "Hiring Event Platform" and "Job Fair Calendar") with
   a HARD GUARD asserting exactly 2 "virtual" remain (the login URLs).
4. Reinstates the page's client behavior with a dependency-free inline script
   using the live payload data verbatim (tiers, all bundle ladders, steps
   ladder, class toggles matching live: selected card = `border-blue-500` +
   glow + check circle + stepper block; disabled stepper button classes; cart
   URL construction). Verified byte-for-byte behavior parity against the live
   stepper. Mobile drawer open/close included.

### 4.2 `build-employer-faq.py` (this session)

SRC `faq-live-dom.html` → OUT `employer-faq.html`.
1. De-frameworkise; localise (same shared assets). 2. Virtual sweep: titles ×3,
   descriptions ×3, intro line, Q1 question ("virtual job fairs"→"hiring
   events"), Q2 question likewise, footer ×2; guard == 2. 3. Injects ALL answer
   panels (the SSR ships only question buttons): answers taken from the live
   page's FAQ JSON-LD, panel markup copied from the hydrated live page
   (`px-5 lg:px-6 pb-4 lg:pb-5` + `text-sm text-slate-600`), `hidden` attr;
   Q1's answer rewritten to cover in-person/video/phone ("…interview candidates
   in person at your address, on JobFairX video, or by phone. Video interviews
   run directly inside JobFairX, no Zoom, no downloads, no external software
   required."); Q7's answer keeps its "View packages" link. 4. NEW question 2
   "Where do interviews take place?" ("You choose. When you set up your jobs,
   you select your interview location: in person at your address, on JobFairX
   video with nothing to install, or by phone. It never changes the price.") —
   10 questions total. 5. A floating **"Dev note: what changed"** pill
   (bottom-right, id dev-note, labeled "Prototype note, remove before
   production") — Scott asked for it, then asked it be reworded to ONE
   remove-the-word-virtual instruction instead of quoting each old phrase (the
   whole deployed page contains "virtual" exactly 3×: 2 login URLs + that one
   instruction). 6. Inline script: accordion (items toggle independently; open
   state = `border-blue-200 bg-blue-50/40 shadow-sm` + chevron `rotate-180`),
   drawer, dev-note toggle.
Open item: Q6 (candidate prep "platform tutorials") optional rewording was
offered and not taken.

### 4.3 `build-employer-home.py` (other stream's file; this session's sections)

The other session owns steps 1–8b (they evolved it mid-day: step-1 keeps the
live calendar visual, Interview Settings panel moved to Event day, messaging
section removed, card format bullets, all-packages format item). This session
appended, at Scott's direction:
- **8c** — now just a comment: the Difference section is UNTOUCHED, matching
  the live site verbatim, after a full redesign round-trip Scott reverted
  (history in §6 and COST-PER-HIRE-CLAIM.md).
- **8d** — Review & confirm visual → the unified prototype screenshot
  (`<div id="jfx-rev">` anchor — NOTE the id comes BEFORE class, a
  `<div class="w-full max-w-[560px]` search misses it; balanced-div walk;
  swaps in the two `<img>`s, desktop `hidden lg:block` / mobile `lg:hidden`,
  `?v=2` cache-busters, long descriptive alts).
- **8e** — All Packages Include 9 → 8: removes the dashboard item by
  DETERMINISTIC string bounds (span text → rfind item-div open → find
  `</div>`). ⚠️ The first attempt used a lazy regex
  (`<svg[^>]*>.*?</svg>\s*<span…`) whose `.*?` spanned five items and silently
  deleted them — caught by the post-build item count. Never use unanchored lazy
  regex spans over repeated sibling markup; walk bounds instead.
- **8f** — the review-only **Desktop | Mobile view toggle** pill (fixed
  bottom-left, id view-toggle, title "Prototype view toggle, remove before
  production"); Mobile links to `mobile-view.html?page=employer-home-mobile.html`.

### 4.4 `build-employer-home-mobile.py` (this session)

SRC = the BUILT `employer-home.html` (⚠️ run the desktop builder FIRST) → OUT
`employer-home-mobile.html`. Scott: "I don't want a responsive page. I want
actual mobile design… images fit for mobile. Can't use the same images."
v1 transformations: title suffix "(Mobile design)"; the four How-It-Works step
eyebrows made visible on the phone (`hidden lg:inline-block…` → `inline-block…`,
count 4 — desktop hides them below lg); the five event-type photos swap to the
4:5 `-m.jpg` crops with frames changed from `aspect-[3/2]` to
`style="aspect-ratio:4/5"` (count 5); the view toggle flips to the Mobile
state linking back to `employer-home.html`; provenance comment. The
review-confirm image already swaps to its mobile capture below lg; the calendar
mock, Interview Settings, and analytics visuals are DOM and fold natively.
**This is v1 — Scott iterates by screenshot; expect more art direction.**

---

## 5. Deployed state (preview repo, all verified byte-exact after push)

- https://scottjobagent.github.io/jobfairx-marketing-preview/employer-home.html
  (FINAL desktop + toggle pill)
- …/employer-home-mobile.html (mobile design v1)
- …/mobile-view.html (phone-frame viewer, defaults to the mobile design;
  switcher: Home mobile / Home desktop / Pricing / FAQ / Event detail)
- …/employer-pricing.html · …/employer-faq.html (final with updates)
- …/employer-event-detail.html (other stream's, untouched)
- …/difference-options.html (review scratch, pending deletion)
- assets/product/review-confirm*.png · assets/employer-home/*-m.jpg

---

## 6. The Difference section saga — full history (do not relitigate)

Scott asked for an expert critique of the homepage "This Isn't a Job Board.
It's a Day of Interviews" section. A 4-lens panel (conversion copy, UI,
product-truth, competitive research) returned unanimous keep-but-fix. Three
mockups were rendered with the page's real CSS (`difference-options.html`):
A tightened ✕/✓ scorecard, B honest scorecard with a concession row, C
cost-model comparison (prose cells, no icon war). **Scott picked C**, then
iterated: bullet heading "Interview in person, video, or phone" (he cut "your
way"); NO dollar figures in the table; a conversion row using his 15.6%-vs-2-3%
numbers; then a researched cost-per-hire row (three versions: Appcast $851
ad-spend framing → article-aligned "$5,475 US average, and climbing¹" vs
"Under $200 in event spend on our 2025 healthcare events²" with
**LinkedIn-style superscript citations** (his idea, from a screenshot; dotted
sup marks with title tooltips jumping to a numbered #cph-sources line linking
his article)) → he removed the cost row entirely ("let's leave the cost per
hire off") → renamed "Conversion rate" to **"Hire rate"** → and finally
**reverted the ENTIRE section to the live site's version** ("update it back to
what the live site has"). A seven-row expansion he liked in a mock is ON HOLD
(roster: What you pay for / What you review / Who screens / Candidate intent
"Low-intent applicants" / Hire rate / Scheduling "Accept a request and it's
booked" / Where interviews happen "In person, video, or phone. You choose").
**Current state: live-verbatim. Do not re-pitch. Do not "fix" "Interviews
auto-scheduled" or "Passive applicants" on this page — he knows and chose
them.** All researched variants preserved in COST-PER-HIRE-CLAIM.md.

Research findings worth keeping (all sourced in the claim doc): SHRM's famous
"$4,700 average" is a right-skewed 2022 mean (median $1,244; 2025 median
$1,200 non-exec; $5,475 "2025 average" circulates via secondary sources only);
Appcast measured advertising cost per hire $851 (2024, "rose sharply" 2025);
job-board apply-to-hire ≈0.5–0.6% channel-specific (Jobvite 184 apps/hire,
CareerPlug 180) vs ~2.4% blended; **no credible third-party events-vs-boards
comparison exists — the stats circulating on Google trace back to jobfairx.com's
own resource pages** (circular-citation risk); Scott's article embeds the OLD
✕/✓ table (with "Interviews auto-scheduled" etc.) — when the developer next
touches the article, apply the same row corrections Scott approved wherever he
wants them.

---

## 7. Scott's decision ledger (this session — binding)

1. Exact clones first, updates after, as explicit builder steps. Clone = keep
   even "wrong" live copy (titles, "virtual events" CTA) until he directs.
2. Pricing headline/sub pair, card bullet, includes swap, virtual sweeps: done
   as specified above; includes lists on home and pricing MUST stay identical
   (8 items, dashboard item removed on both — his call both times).
3. "Hire rate," not "Conversion rate," if the stat ever returns.
4. FAQ: new Q2, rewritten Q1 answer, dev-note pill with the single
   remove-virtual instruction.
5. **Homepage FINAL with these explicit keep-as-is sign-offs:** the ~40-company
   trust marquee ("don't worry, the developer's got it"); the results-card stat
   tiles (36/7, 92/19, 51/14) even though the Tesla tile's framing conflicts
   with its own quote; the meta descriptions' "book interviews" phrasing; the
   tier-card "In-person or video interviews" bullet vs the includes' phone
   phrasing (documented intentional); the mixed-timezone review-confirm
   screenshot; the Starter/Pro empty-gap pricing cards. Declined = declined.
6. **Header and footer belong to the live site.** Production keeps the CURRENT
   live chrome, desktop and mobile; the prototype only supplies the content
   between. All prototype chrome quirks (mobile footer's hidden column labels)
   are capture artifacts to ignore. This is the lead item of
   EMPLOYER-HOME-DEV-NOTES.md.
7. **Mobile = a dedicated design, not responsive collapse**, with
   mobile-purpose images. The developer gets BOTH views via the toggle.
8. The 35/8 healthcare stats are real platform data (see §2).
9. Review & Confirm visual: one unified app window, 2 awaiting + 2 upcoming,
   blue Accept drawing the eye, calendar-visual footprint (~4:3), real
   prototype pixels only.

---

## 8. Current work in progress — exactly where this stopped

**Nothing is half-finished.** The last completed acts: mobile design v1 +
toggle + viewer deployed and verified; links delivered to Scott; memory and
docs updated. Scott's stated sequence: **iterate the mobile design → then the
event details page** (`employer-event-detail.html`).

**The most likely next message is mobile-design feedback (screenshots) or "move
to event details."** For event details, know: it's the OTHER stream's build
(`build-event-detail.py`, reads its own capture AND clones sections from the
built employer-home.html — the HOW/MSG spans; check those anchors still match
before running it); it still contains the old ✕/✓ Difference table and a CTA
band anchored on "This Isn&rsquo;t a Job Board"; its testimonial headshots were
replaced by initials circles; its FAQ is native details. Expect Scott to want:
the same clone-fidelity audit, virtual sweep, format updates, maybe the same
unified-screenshot treatment, and a mobile design. Do NOT start it before he
directs scope.

---

## 9. UX / UI / marketing decisions (with the why)

- **Screenshot strategy:** marketing visuals are REAL product pixels, captured
  from the prototype and surgically curated in ITS OWN DOM (trim rows, merge
  cards, retitle, hide columns) before screenshotting — never redrawn
  illustrations. Why: authenticity survives demos; Scott's brief demanded
  "looks exactly like JobFairX."
- **Density serves the story:** the unified Review & Confirm window shows 2+2
  rows, not the app's 8+8 — "a carefully curated product screenshot," request →
  review → scheduled readable in 3–5 seconds.
- **Capture width = legibility lever:** capture at the narrowest viewport where
  the UI still fits (880px desktop / 640px mobile with columns hidden), so text
  stays near-native when displayed at 560px. The original complaint ("text too
  small, too much whitespace") came from scaling an 824px table to 61% in a
  fixed-height card.
- **Mobile design language (v1):** portrait 4:5 photography (faces large),
  visible step labels to carry the narrative, full-width CTAs, mobile-specific
  product captures. Phone-first, not shrunken desktop.
- **Messaging arc (site-wide):** away from "virtual" entirely; interview
  location choice (in person / video / phone) is the launch story; "candidates
  request, you accept" is the control story; hero deliberately says "in-person
  and video" (phone appears from the Event-day step onward — documented
  four-mention scheme in the home builder).
- **Citations pattern:** LinkedIn-style dotted superscripts + numbered source
  line (built, currently unused — pattern preserved in COST-PER-HIRE-CLAIM.md).
- **Review-only chrome pattern:** floating dark pills, bottom corners, always
  labeled "remove before production" (FAQ dev-note bottom-right; view toggle
  bottom-left).

---

## 10. Verification routine (unchanged core + additions)

1. `python3 tools/mcheck.py <files>` — true-390 overflow probe (iframe trick;
   headless clamps window width to 500).
2. Render and LOOK: headless screenshot, PIL-crop bands, actually read them.
3. Probe behavior in an iframe harness reporting via `document.title`.
4. **Pixel-diff against the live page for clones**: headless-render live
   (scripts off = SSR) and the clone at identical size, `ImageChops.difference`
   (the pricing clone: 125 of 6,336,000 px differed, all font AA).
5. Verify DEPLOYED BYTES after push: poll with cache-buster
   (`?cb=$RANDOM`) until `cmp` says byte-identical. 404s for ~2–5 polls are
   normal; one deploy took ~4 minutes (queued Pages build) — check
   api.github.com/repos/.../commits to confirm the commit landed before
   suspecting the upload.

---

## 11. Capture recipes (hard-won, reuse verbatim)

**Live-page capture:** `curl -A <chrome UA>` the page; if SSR carries the full
content (pricing, FAQ did), strip `<script>…</script>` blocks and save to
`assets/live-capture/` — cleaner than rendered-DOM capture (no modulepreloads,
no announcer). Bundle/config data lives in the SvelteKit bootstrap's `data:`
payload — mine it before stripping (that's where the ladders came from).

**Lobby prototype screenshots** (source of review-confirm images):
- Source: https://scottjobagent.github.io/jobfairx-prototype/lobby-v3-healthcare.html?method=video
  — self-contained single file (~447KB, only Google Fonts external). curl it,
  serve from a local http.server, inject a harness before `</body>`.
- **Use the DEFAULT pre-event state.** The bottom-left A/L dev toggle
  (`button.dev-toggle-btn`): **L switches to the live-event state, which
  EMPTIES "Candidates awaiting your response"** — Scott's dictated "click the
  L" contradicted his own target screenshot; the screenshot wins.
- Harness features built (session scratchpad `lobby-cap.html`, pattern worth
  reimplementing): visible-only heading matcher; row trimming with heading
  count rewrite; `unify=1` merges the two `.live-panel-section` cards into one
  window with a hairline divider (color read from the table th border), retitles
  section 2 "Upcoming interviews", hides its location column, tightens
  `.collapsible-body` padding; `hidecols=Name|Name` hides listed th columns in
  all tables (mobile: hide "Desired job|Desired location" so
  Accept/Decline/Reschedule fit at 640); `.dev-toggle-btn` parent hidden;
  **capture.py's NEUTRALISE list applied MINUS the ["Tamar","Robin"] pairs**
  (that rule mangles "Tamara Williams" — the fictional name marketing already
  uses — into "Robina Williams"; David Chen→David Okafor stays).
- Shoot `--force-device-scale-factor=2`, crop to the reported section box.

**Headless Chrome quirks:** it can hang AFTER "bytes written" (Google updater
noise) — run with a filename poll loop and `pkill -f <unique user-data-dir
tag>` (never a broad pattern; Scott's real Chrome is running); `--headless=new`
failed on this machine, use plain `--headless --no-sandbox`; min window width
500 (use the mcheck iframe for narrower); `cd` into the scratchpad INSIDE the
same command as the `cat > harness` or the file lands in the wrong dir (bit us
once — grey iframe screenshot = iframe src not found).

---

## 12. Push procedure (works every time)

1. Stage in the session scratchpad `stage/` dir: comment-stripped page copies;
   images copied as-is. (`file_upload` can only read session-shared dirs — NOT
   `~/Desktop`; staging is mandatory.)
2. Chrome MCP: new tab → `github.com/scottjobagent/jobfairx-marketing-preview/upload/main`
   (append `/assets/product` or `/assets/employer-home` for subdirs — separate
   commits per directory).
3. `find` the file input fresh → `file_upload` (multi-file OK) → `find` commit
   summary → `form_input` → scroll down → **click "Commit changes" BY
   COORDINATE** (the ref-click silently fails to submit about half the time;
   screenshot first, click the green button, wait, confirm the tab navigated to
   the repo root).
4. Poll deployed bytes (§10.5). Close your tabs.

---

## 13. Ops notes

- **Port 8790**: an earlier session's `python3 -m http.server` still serves the
  repo from disk — reuse it (it reads per-request, so fresh builds are live).
  8766 (in `~/Desktop/.claude/launch.json`, "marketing") is held by a DEAD-cwd
  server that 404s everything; 8733 is another session's. Don't kill others'
  processes.
- Temporary capture servers: `python3 -m http.server 8795` in the scratchpad,
  `pkill -f "http.server 8795"` when done.
- The other session was ACTIVE in this directory during this session (its
  builder gained steps mid-day). Re-run `git status`/read builders before
  assuming state.
- Desktop is iCloud-synced; deletions go to Recently Deleted (never bulk-delete).

---

## 14. Work log (chronological)

1. Read HANDOFF-3; 8-agent read-only verification of it against the codebase
   (all claims confirmed).
2. Pricing clone: capture, builder, behavior parity probe, 125-px pixel diff,
   deploy. Bundle ladders + discounts mined from payload.
3. Pricing updates: headline/sub → card bullets → includes swap → virtual sweep
   (each its own commit, each verified deployed).
4. FAQ audit (11 virtual spots + interview-location gaps) → clone with answers
   injected + new Q2 + accordion + dev-note pill → pill reworded.
5. Difference critique panel → 3 mockups → option C shipped → cost-row
   iterations (research program: 4-agent sourced sweep; article read) → row
   removed → Hire rate rename → FULL REVERT to live. Healthcare 35/8 restored
   to both solutions pages.
6. All Packages Include 9→8 on home (regex incident + deterministic fix).
7. Final home audit (4 agents: claims/links/visual/consistency) → Scott's
   sign-offs → EMPLOYER-HOME-DEV-NOTES.md.
8. Review & Confirm visual: stacked v1 → Scott's unified-window brief → v2
   (2+2, one window) deployed.
9. Mobile: viewer page → Scott's "actual mobile design" brief (confirmed) →
   `-m.jpg` crops, mobile builder, toggle (8f), viewer default flip; all
   deployed and byte-verified.
10. This handoff.

---

## 15. Remaining roadmap

**Immediate**
1. **Mobile design iteration** — Scott reviews v1 in the viewer; expect
   screenshot-driven tweaks (typography scale, section spacing, possibly more
   image art direction).
2. **Event details page** (`employer-event-detail.html`) — await Scott's scope;
   likely: audit, virtual sweep, format updates, unified-screenshot treatment,
   mobile design, dev notes. Mind the cross-stream builder rules.
3. Delete `difference-options.html` from the preview repo when Scott says so.

**Then**
4. Pricing/FAQ mobile designs (the viewer already lists both pages).
5. Dev-notes docs for pricing and FAQ (mirroring the homepage's).
6. The Fairs AI stream's HANDOFF-3 §14 open questions remain with that stream
   (30-vs-31 days, {{LIVE_EVENT_FEED}} note, page-pricing hybrid nav, calendar
   hybrid tail, {{LOGO}} slots) — untouched here, don't lose them.

**Never / on-hold (do not relitigate without Scott)**
Cost-per-hire row (preserved in the claim doc) · seven-row Difference table
(roster in §6) · any Difference-section change · marquee/stat-tile/meta
"fixes" he declined · footer/header changes (live chrome wins).

---

## 16. Risks

- **Two sessions, one directory** — still the top risk; the other session
  edits `build-employer-home.py` too. The assertion contract is the safety net;
  keep every new step loudly asserted and clearly attributed.
- **Uncommitted work** — this stream's output exists only in the working tree
  and on the preview repo.
- **Live-site drift** — production changes under us (it did this session).
  Re-capture before reusing old captures for new claims.
- **Lazy regex over repeated markup** — see §4.3/8e incident.
- **GitHub Pages lag** — up to minutes; never conclude failure without checking
  the commits API.
- **Public preview** — world-readable; pricing, dev notes pills, and toggles
  are visible by Scott's choice; strategy docs must never be uploaded there.
- **FA Pro CDN** — domain-licensed, frozen v5.10.0; flagged to the developer.

---

## 17. Open questions

1. Mobile design v1: what does Scott want changed? (Awaiting his review.)
2. Event details page: scope and order of updates.
3. `difference-options.html`: delete now or keep for reference?
4. FAQ Q6 optional rewording (offered, unanswered).
5. The 15.6% hire-rate stat: source/derivation if it ever goes on a page with a
   citation (he confirmed the label, not the provenance).
6. Scott's article's embedded old ✕/✓ table: when/how the developer updates it.
7. HANDOFF-3 §14 items (other stream).

---

## Instructions for the Next Claude Code Session

You are continuing a project that was paused only because the previous Claude Code
conversation reached its context limit.

Before making any changes:

1. Read this entire handoff from beginning to end.
2. Review the complete codebase.
3. Review every file referenced in this handoff.
4. Verify your understanding against the current implementation.
5. Reconstruct the project's architecture, design system, UX philosophy,
   marketing strategy, coding standards, and implementation approach.

Once you have completed your review:

- Confirm that you fully understand the project.
- Provide a concise summary of your understanding.
- Explain exactly where the previous Claude stopped working.
- Do not write any code yet.
- Do not make design changes yet.
- Do not make recommendations yet.

Instead, stop and ask me exactly this:

"I've finished reviewing the handoff and the codebase, and I'm fully caught up on
the project. What would you like to work on first?"

Wait for my response before taking any further action.
