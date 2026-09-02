# JobFairX Employer Marketing Site — Session Handoff

Written 17 Aug 2026 at the end of a full working session. This is the institutional
memory of the project. The next Claude session should treat it as the source of truth
for every decision recorded here, and verify against the codebase before changing
anything.

Companion docs (read in this order after this file):
`LIVE-SITE-SCOPE.md` → `CONTENT-SPEC.md` → `DESIGN-SYSTEM.md` → `PAGE-INVENTORY.md` →
`RECOMMENDATION.md` → `README.md`. This handoff does not duplicate their content; it
tells you what they are, what happened, and why.

---

## 1. Project overview

**Purpose.** Redesign JobFairX's employer-facing marketing website (jobfairx.com/employer)
so it reads as a premium enterprise AI platform — peer-level with Linear, Stripe,
Anthropic, Vercel — instead of a 2020 recruiting site. Scott's original brief demanded:
three homepage concepts (dark / light / hybrid), real product screenshots woven through
the story, video placeholders, the hiring journey made scannable, and a reusable design
system. The brief expanded during the session into a full site rebuild.

**Who.** Scott (scott@jobfairx.com), founder. GitHub account: `scottjobagent`.
Communicates in short bursts, often by voice dictation (expect transcription noise —
one message was a stray football broadcast; he confirmed it was a mistake). Gives
"green light" style approvals. Wants to be shown, not asked — but expects real
questions when a decision is genuinely his.

**Status at handoff.** 28 pages built, verified, and published:

- **Local canonical:** `/Users/scottl./Desktop/jobfairx-marketing/` — served with
  `python3 -m http.server 8765` (motion needs HTTP; file:// renders but sits still).
- **Private repo (developer handoff):** `github.com/scottjobagent/jobfairx-marketing` —
  everything, including strategy docs. 3 commits, uploaded via github.com web UI in
  Scott's Chrome (no git credentials exist on this machine — no gh, no SSH keys, no
  keychain entry; web upload is currently the only push path).
- **Public preview (client-viewable):**
  `github.com/scottjobagent/jobfairx-marketing-preview` → live at
  **https://scottjobagent.github.io/jobfairx-marketing-preview/** (verified 200).
  Contains the site ONLY: strategy docs excluded, all internal HTML comments stripped
  before upload. Scott explicitly chose a public link over adding the developer as a
  collaborator.

**Phases completed:** research (8-agent teardown of premium sites) → 3 homepage
concepts → hybrid chosen and rebuilt on live-site data → 5 inner pages → landing-page
audit (26 hand-built / 16 templates verdict) → Wave 1 (10 pages, closes all dead
links) → Wave 2 (12 pages) → site-wide footer → GitHub publication.

**Next phase (agreed, not started):** Wave 3 — enterprise-close pages, plus the
programmatic templates. See §9.

---

## 2. The product model — the most important thing in this document

Getting this wrong was the session's biggest error and it WILL recur if you're not
careful, because the live site's own copy teaches the wrong model.

**An event is a market moment** — "Dallas Healthcare Hiring Event, Sep 22, 11:00 AM –
3:00 PM CT". Every employer joins the *same* event. There are exactly **five event
types** (audiences): Healthcare, Diversity, Veteran, Technology, Entry-Level.

**Interview location is a per-employer setting, not an event property.** Each employer
independently chooses where *their own* interviews happen: **JobFairX video** ("JobFairX
video call") · **Phone** ("You call each candidate") · **In person** (their street
address) · **Your own link** ("Microsoft Teams" etc.). Two employers at the same event
can interview completely differently. The product's events dashboard literally has an
INTERVIEW LOCATION column showing all four side by side — that screenshot
(`assets/product/dashboard-events.png`) is the single best proof asset owned.

**What just launched** (the reason the marketing site is being rebuilt now) is the
**in-person interview location** — NOT "in-person events". Scott corrected this
mid-session: "It's not their own event. They're still joining a Dallas healthcare
event... They could just set where they want their interviews to go."

Vocabulary law (violations were found and purged several times):
- ✅ "in-person interviews", "set your interview location", "same event, your choice of room"
- ❌ "in-person events", "event format", "host your own in-person event", "virtual event"
- ✅ Candidates **request** interviews; employers **accept**, which **schedules**
- ❌ "apply", "application", "applicants" (the live prototype's own demo copy says
  "application steps" — it was patched in the screenshot capture layer)

Structural consequences already enforced: the events calendar has NO virtual/in-person
filter (events don't carry a format); the event detail page is never labelled virtual
or in-person; "Virtual" was dropped from page titles; a `next-inperson` programmatic
family must never be created (it 500s today; keep it that way).

**The purchase mechanic:** employer registers for an event → posts jobs (jobs are
INSIDE the event package — "Promote 1 / up to 3 / up to 6 jobs" — there is NO separate
job-postings product; Scott killed that page explicitly) → AI matching activates →
candidates request interviews from the employer's availability → accepting schedules →
event day runs as a queue in the lobby → post-event report is ready the moment the
event ends.

---

## 3. Verified facts (use these; invent nothing)

All captured from the live site, most by rendering JS in headless Chrome (plain fetch
misses the client-rendered parts). Full verbatim capture in `LIVE-SITE-SCOPE.md`.

**Platform stats:** 4,000+ employers · 500,000+ interviews conducted · 300+ cities ·
3M+ registered candidates. Attributed as platform totals (earned by virtual events —
never imply in-person volume).

**Pricing:** Starter $495 / Growth $895 ("Most Popular") / Pro $1,495 per event.
Tiers: 1/3/6 jobs · 20+/60+/100+ scheduled candidate interviews · 2/5/unlimited
recruiter seats. The scheduled-interview count is a volume commitment, not a feature —
it gets the emphasis everywhere (Scott's strongest line).

**Bundles:** 8-rung ladder, Starter: 5=$470ea → 100=$297ea (save $125 → $19,800),
max 40% off. "Credits never expire" · "Use across any event type". 25-events rung is
"Most Popular".

**Event lifecycle — FIVE countdown states** (the event-detail page renders all five;
switcher control bottom-right, keys 1–5, marked REVIEW ONLY — must be deleted before
production):

| State | Window | Banner (verbatim) | Pricing |
|---|---|---|---|
| A | 31+ days | "Early registration pricing ends soon. Save $100 and lock in priority candidate matching." | struck: $395/$795/$1,395, badge "Save $100 — Early Registration · Ends {Month Day}" |
| B | 15–31 d | "Candidate matching activates soon." | full |
| C | ~3–15 d | "Candidate matching is live." | full |
| D | ~2 d | "Employer registration closes tomorrow. Reserve your spot now →" | full, still purchasable |
| E | ≤1 d | "Employer registration is closed for this event. Next {City} {Type} Hiring Event: {Date}. View Details →" | CTAs disabled "Registration Closed" |

The threshold is **exactly 31 days** — server payload `earlyRegistration:{minDays:31,
discount:100}`, deadline always event-date-minus-31, verified 6/6. Discount is a flat
$100 on every tier, never a percentage. D→E cutoff verified between 1 and 2 days out
(Omaha 2d open, Syracuse 1d closed). There is also a dormant `onNewYearsSale` flag —
a sixth banner state exists in their codebase, unconfirmed with Scott.

**Show rates (only three exist):** Healthcare 91% · Veterans 89% · Entry-Level 86%.
Diversity and Technology have NO published stats. Healthcare also has: 582 events in
2025. Platform-wide: 87% of employers return. ⚠️ "35 interviews / 7 hires per
employer" are PER-EVENT metrics from a *veterans* event page and swing 2–3× by market
(Portland 968/73/19) — they are NOT type-wide averages and were removed from the
healthcare page after a reviewer caught them.

**The 20-mile fact:** "candidates are verified to be within approximately 20 miles of
the event city" — the strongest in-person argument owned; was buried in FAQ Q3, now a
headline moment on the FAQ and in-person pages.

**Customers (only three, one sentence each, company+role attribution, no names, no
written permission):** Target ("This was our second event and we interviewed over 90
candidates in one day" — Senior Recruiter) · Western Regional Medical Center ("My team
hired two LPNs, three RNs, and two MAs at the hiring event" — Director of Talent
Acquisition) · Tesla ("We've used JobFairX for three veterans events now..." —
Recruiter). Scott approved using these. Nothing beyond them.

**Contact:** info@jobfairx.com · (702) 269-0808 · JobFairX, LLC, 209 S Stephanie St.
STE B #144, Henderson, NV 89012 · Mon–Fri 5:00 AM–5:00 PM PST.

**Events API:** `GET /api/employers/job-fairs?country=US` — 1,200 events, 100/page.
Type colours (product-canonical): Diversity orange · Technology blue · Healthcare teal ·
Veterans red · Entry-Level sky.

**Two Terms documents exist:** `/employer/terms-and-conditions` (2,152 words — the one
ported) and `/terms-and-conditions` (3,927 words, job-seeker). Do not confuse them; a
0%-overlap scare came from diffing against the wrong one.

---

## 4. Design system — the decisions and their reasons

Full tokens in `DESIGN-SYSTEM.md` and `shared/base.css`. The load-bearing rules,
each research-derived (17-site teardown incl. computed-style extraction):

1. **Never pure white/black.** Canvas `#fbfaf8` light / `#0b0d12` dark; ink `#14161a`
   / `#f4f6fa`.
2. **Display weight 500, never 700.** Line-height sub-1.1 on display.
3. **Tracking is a ramp that crosses zero:** −0.042em at display → **+0.004em at body**.
   Negative tracking below 18px was an early mistake, corrected system-wide.
4. **One depth mechanism per element:** hairline + rim-light on dark; shadow on light;
   never both. **No coloured bloom** — accent glow was cut from 42% to 15–16% alpha
   after research showed zero peer sites use bloom (Linear's hero has no box-shadow at
   all). Grain overlay (inline feTurbulence, mix-blend overlay, Safari-reduced) is the
   anti-flatness device.
5. **HARD CUTS between dark/light sections.** Scott explicitly ordered this
   ("have hard lines from the dark to the light instead of the fading"); it also
   matches stability.ai (all 16 boundaries, dividers disabled). The gradient `.seam`
   elements were deleted. Do not reintroduce.
6. **Nav is SOLID when stuck — no backdrop-filter.** Two reasons: frosted glass over a
   hard theme cut shows the seam sliding through it, and the stronger research pass
   found juicebox (0 occurrences in 342KB CSS), Anthropic, and Vercel all ship solid.
7. **No 3D-tilted screenshots.** `--tilt` exists in base.css defaulting to 0deg for
   reversibility, but research was unanimous that perspective-skewed UI is "the
   strongest 2019-template tell". Depth = layered parallax translation only (≤ ~26px,
   lerp 0.08, single rAF loop).
8. **Screenshots:** crop into the story region, never shrink the whole frame. The
   `.crop` primitive's `--l/--t` are percentages OF THE IMAGE via `transform:
   translate()` (an earlier `inset:0` version over-constrained and stretched — do not
   regress). White screenshots on dark sit inset on a surface plate. Hero "floating
   fragments" are rebuilt in DOM, not cropped PNG, so they stay sharp and animate.
9. **Motion:** entrances `cubic-bezier(.16,1,.3,1)`; hover `(.4,0,.2,1)`; reveal =
   opacity 150ms linear + transform 800ms (Stripe's split-clock trick); stagger 60ms;
   hero headline NEVER animates in; no springs/bounce; static logo walls (marquee reads
   downmarket); count-up animates FROM the authored value with a hard settle-timeout so
   a stalled rAF can't freeze a fake number (Gem ships "0x" live because of this);
   full prefers-reduced-motion support.
10. **Nav content (Scott's explicit spec, matches live site):** Upcoming Hiring Events
    · Pricing · FAQ · Contact Us · Sign In · Register for an Event. Sign In / Register
    are `href="#"` on purpose — app destinations, not to be built. The audit's
    suggested Platform/Solutions/Events/Pricing/Resources nav was NOT adopted; footer
    carries the full map instead.
11. **Footer = site index.** Five columns (Platform ×7 · Solutions ×6 · Events ×4 ·
    Company ×5 · Legal ×4), byte-identical markup across all 28 pages (verified by
    hash), self-links render as `<span aria-current="page">` not anchors, Pricing/FAQ
    deliberately duplicated with nav (Scott approved), template pages
    (event-detail, city-hub) deliberately excluded. Grid stacks 6→3→2→1 at
    1100/700/420px.
12. **Honest placeholders.** Anything unverified ships as visible `{{PLACEHOLDER}}`
    with a `data-placeholder` attribute (one-pass findable via
    `grep -rn "data-placeholder" *.html`). This is a feature, not debt: the security
    page says "SOC 2 Type II — not yet certified" in plain words because honesty beats
    vagueness in procurement. Never fill a placeholder without a verified source.
13. **Legal pages PORT, never draft.** Privacy ported at 81% shingle-overlap, employer
    Terms at ~71%. An invented sentence there is a legal representation. Terms carries
    a deliberately visible placeholder for the missing refund/cancellation policy
    (none exists anywhere while $29,700 bundles sell with "credits never expire").
14. **The `.anno` annotated-screenshot component** (base.css bottom + motion.js
    `initAnno`) is the workhorse of capability pages: numbered pins over the real
    screenshot paired to a caption key by `data-anno`; hover/focus/tap all work;
    pins get `aria-describedby`. Build order matters — it blocked six pages.

---

## 5. Architecture

```
/Users/scottl./Desktop/jobfairx-marketing/
  index.html                    concept chooser (3 homepage candidates)
  concept-3-hybrid.html         THE homepage (approved); concept-1-dark / concept-2-light kept for reference
  page-*.html                   27 pages (see below)
  shared/base.css               all tokens + primitives (~390 lines). Read first.
  shared/motion.js              reveal, parallax, nav, tabs, journey, counters, anno (~300 lines)
  assets/product/*.png          14 UNIQUE screenshots, 2× retina, sanitised
  assets/_reference-do-not-publish/   unlicensed iStock comps — gitignored, NEVER publish
  tools/capture.py              screenshot harness (see §7) — copied from session scratchpad
  tools/shoot.sh                deterministic page renderer (paths need adjusting)
  tools/mcheck.py               390px horizontal-overflow probe
  *.md                          docs + this handoff
```

Pages: events, event-detail (5-state), pricing, faq, contact ·
platform + 6 capability pages (events-dashboard, candidate-pipeline ⭐reference,
interview-scheduling, event-day, messaging-automations, analytics) ·
solutions + 5 type pages (healthcare ⭐reference, diversity, veteran, technology,
entry-level) · interview-locations, in-person-interviews (the launch page) ·
demo, security, resources, about, privacy-policy, terms · city-hub (template).

**Patterns:** No build step, no framework, no dependencies beyond Inter from rsms.me.
Every page self-contained: links the two shared files + its own `<style>`. Nav/footer
duplicated per page BY DESIGN (no templating layer yet — if one is introduced, extract
the footer first, it's byte-identical everywhere). Theming via `data-theme="dark|light"`
wrapper divs; all primitives read the four scoped custom properties. Two files are
TEMPLATES, not pages: `page-event-detail.html` (1 of ~1,200 events; 5-state switcher
is review-only) and `page-city-hub.html` (Dallas worked example; every dynamic field
marked `<!-- {{VAR}} -->`; 352 instances planned).

**Interactive JS worth knowing:** events page has working city search + custom type
dropdown + deep links (`?type=healthcare|diversity|veteran|technology|entry-level`,
vocabulary-mapped to internal values `entry`/`veterans` via `selectByValue()` — a
synthetic click does NOT work, and the handler must live INSIDE the IIFE); pricing has
a quantity stepper computing bundle totals from the real ladder; FAQ has an accessible
accordion + sticky category rail (mobile chip-strip needs `min-width:0` on grid item
AND scroller — this exact bug caused 231px overflow once); demo/contact forms have
real `required`/`aria-*`/validation (the live site has ZERO required attributes — a
defect we fixed, don't regress).

---

## 6. GitHub state

- **Private** `scottjobagent/jobfairx-marketing`: full project. Note: the LOCAL git
  history (one commit, made before push was possible) is UNRELATED to the GitHub
  history (created via web upload). Developer must clone from GitHub; local folder is
  ahead in content only via later web uploads being identical. If reconciling, fetch
  and reset local to origin/main — do not force-push local over it.
- **Public** `scottjobagent/jobfairx-marketing-preview`: site only, comments stripped,
  docs excluded, Pages enabled (main / root). Live and verified:
  https://scottjobagent.github.io/jobfairx-marketing-preview/
- `.gitignore` excludes `_reference-do-not-publish/` and `interviews-pending.png`
  (byte-identical dup of interviews.png, md5 8422e5f2… — the Pending tab was never
  captured; never use this file, never treat it as a 15th screenshot).
- Web-upload procedure that works: `/upload/main/<dir>` URL creates the directory;
  `find` the file input fresh each page (refs go stale); files must be staged in the
  session-readable scratchpad; commit button sometimes needs a coordinate click after
  `scroll_to`. Verify file COUNT after upload — a hand-transcribed list silently
  dropped `page-solutions.html` once (caught by 37≠38).

---

## 7. The screenshot capture harness (tools/capture.py)

Screenshots come from Scott's prototype at
`scottjobagent.github.io/jobfairx-prototype/*` (visual-v3, lobby-v3, setup-flow-v3,
interview-screen-v3, edit-post-v3, account-billing, share-preview). The harness
downloads the pages, injects JS, renders in headless Chrome at 2× (3200×2000), and:

- kills the prototype dev toolbar (label-heuristic) and inline demo toggles;
- clicks through nav/state ("Active#2" = 2nd exact match — toggle groups reuse labels);
- **neutralises text** via case-insensitive DOM replacement. This list is load-bearing:
  - Real companies used as demo data → "Northwind Health" (was Tesla, Baylor Scott &
    White — would read as customer claims);
  - The Atlanta event's Dallas address → real Atlanta address (data defect in the
    exact crop the in-person page uses as hero);
  - "Denver **Engineering** Event" → "Denver **Technology** Event" (Engineering is not
    one of the five types; a screenshot must not invent a sixth);
  - Likely-production PII → fictional names (Dana Whitfield, Amara Osei, Rosa Delgado,
    Ken Mbeki, Nina Farrow, Theo Blackwood, Robin). ⚠️ These fictional names have
    tripped a reviewer as "PII" — they are the FIX, not the problem;
  - "application steps" → interview-request language (whole-clause replacement — a
    fragment swap once produced "please ensure you have sent you an interview request").

**If any screenshot is re-captured, the full neutralisation list must run.** And the
root problem remains upstream: the PII-looking names and banned vocabulary are in
Scott's PUBLIC prototype itself — flag to Scott, only the marketing copies are clean.

---

## 8. Lessons learned (expensive ones — do not repeat)

1. **The interview-location inversion.** Built "in-person events" into copy and briefs
   before Scott corrected the model. Even after correction, a Wave-2 agent wrote
   "Location belongs to the interview, never to the event" (wrong again, opposite
   direction) — adversarial review caught it. Any sentence about events/locations
   should be checked against §2.
2. **Absence-of-evidence failures, twice, same shape.** A scope agent declared the
   countdown banners nonexistent (it fetched raw HTML; they're client-rendered). I
   then declared state C "stops ~3 days out" (my keyword list lacked "registration
   closes"). Rules: ALWAYS render with JS before concluding "not present"; never
   conclude absence from a keyword list written before knowing the answer; sample
   across the full range.
3. **I propagated an invented statistic through my own brief** ("35 interviews / 8
   hires" as healthcare-wide — actually per-event veterans metrics, and 7 not 8).
   The audit asserted it, I passed it into a build brief unverified, the reviewer
   caught it in output. Verify audit numbers against LIVE-SITE-SCOPE before they
   enter any brief.
4. **Case-sensitive text replacement shipped lowercase "zarreyah"** in a published
   screenshot while replacing "Zarreyah". Neutralisation is now regex `gi`.
5. **Reviewer false positives are real:** flagged my fictional replacement names as
   PII; flagged `<img>` inside CSS comments as missing alt; flagged commented warnings
   as banned vocabulary. Verify findings (md5, context, comment-stripping) before
   acting — but note the same reviewers also caught genuine highs, so run them anyway.
6. **JS scope bug pattern:** the events deep-link handler silently did nothing when
   placed outside the IIFE that owns `typeSelect`. Symptom: no error, no effect.
7. **grep -c counts lines not visible copy.** Strip comments/scripts/styles and
   unescape entities before auditing rendered text (`$`/`%` audits produced noise
   until then).
8. **Rejected on evidence** (don't relitigate without new data): 4 separate
   interview-location pages (one page; splitting re-manufactures the events
   misreading) · standalone job-postings page (Scott: part of the package) · blog
   (12 articles exist; second system splits authority) · careers (no openings) ·
   case-study pages (no permissions) · title×city programmatic (247,808 URLs,
   95.8%-duplicate death spiral) · MORE city×type pages (audit says prune 1,760→~900) ·
   frosted nav, gradient seams, coloured bloom, 3D tilt, marquee walls, count-up-to.

---

## 9. Work remaining

**Wave 3 (agreed next):** `/employer/ai-hiring-compliance`, `/employer/dpa`,
`/employer/accessibility` (trust template exists on page-security). BLOCKED:
customer-stories (needs written permission from Target/Tesla), platform/ai-matching
(zero visual evidence AI matching has a UI — needs a product screenshot or it stays
unbuilt).

**Programmatic (designed, not generated):** city-hub ×352 from the template; T6 state
hubs ×46 (`/employer/job-fairs/{state}` currently hard-500s live); T7 near-me-by-type
×5; T8 hire-a-role ~120 curated (gated on city tiering). Hygiene pass on the live
site: kill 8 non-city slugs, fix `sugarland`/`sugar-land` split, remove the hardcoded
"Apr 22, 2026" testimonial date on every event page, stage the "Virtual" title-tag
removal across 3,520 pages — NEVER in the same pass as the city consolidation (two
simultaneous site-wide changes make traffic data uninterpretable).

**Live-site correctness bugs (rewrite in place, don't redirect):** three articles are
factually wrong since in-person launched — `virtual-vs-in-person-hiring-event` (the
highest-intent in-person URL argues AGAINST the launched capability),
`virtual-hiring-events` ("No Zoom, no external links, no downloads"),
`how-does-a-virtual-job-fair-work`. Cheapest win anywhere: all ten resources articles
CTA to the calendar; none link pricing or bundles — repoint high-volume-hiring at
bundles.

**Open questions for Scott (asked, unanswered):** in-person pricing parity (same
tiers? same $100 early discount? — the in-person page carries a placeholder, do NOT
assume parity) · SOC 2 / compliance status (footer `{{Compliance}}` + security page
placeholders) · `onNewYearsSale` sixth banner state · per-type stats for
diversity/technology/veteran/entry-level · logo-wall rights (live healthcare wall
names CVS/Kaiser/Mayo/etc. with an unverified "has attended" claim; ALL TEN live
technology logos are fabricated — technology page ships with no wall at all, on
purpose) · testimonial personal names (titles carry credibility; currently
company+role only) · exact D→E cutoff hour · 31 vs 30 days ("thirty days out" per
Scott, `minDays:31` per code — copy currently follows the code).

**Before production:** delete the REVIEW ONLY state switcher from page-event-detail ·
convert PNGs to AVIF/WebP + `loading="lazy"` below the fold (~70% saving) · replace the
5 video placeholders (`.video-ph`) with real embeds · fill placeholders from verified
data only · get the prototype's PII/vocabulary fixed upstream.

**Untracked locally:** tools/, HANDOFF.md, and all post-push edits (footer, Wave 2
fixes) exist locally and in neither repo yet — the private repo is 3 commits behind
the local folder. Next session should sync it.

---

## 10. Risks

- **PII:** the public prototype (jobfairx-prototype) still shows what look like real
  candidate names + a recruiter's name. Marketing copies are clean; the source is not.
- **Legal:** never draft policy text; the refund-policy gap is flagged visibly in
  Terms; the diversity page must never imply selection by protected characteristics
  and carries a `{{legal review required}}` block where compliance claims would sit.
- **Licensing:** `_reference-do-not-publish/` contains unlicensed iStock comps.
- **Public exposure:** the preview repo makes the rendered site (incl. "not yet
  certified" security honesty and full pricing) world-readable. Scott chose this
  knowingly. The strategy docs remain private — keep it that way.
- **Fragile invariants worth a check after any bulk edit:** footer hash-identical
  across 28 pages · exactly one h1 per page · zero 390px overflow (tools/mcheck.py) ·
  zero unintentional `href="#"` (intentional set: Sign In, Register, `{{Compliance}}`)
  · no `interviews-pending.png` usage · vocabulary sweep from §2.

---

## 11. Wave V — product-visual & motion upgrade (17–18 Aug 2026)

Scott approved the VISUAL-AUDIT.md plan in full (AI-matching shown as a labelled
diagram; living video posters; one-moving-element-per-viewport budget). Built,
adversarially verified twice (11 checker agents total), all findings fixed.

**New files:** `shared/vignettes.css` (~420 lines — read its header comments; it
documents its own contracts) and `initVignettes`/`initAnnoIntro` in motion.js.
`VISUAL-AUDIT.md` is the spec. All 28 pages upgraded.

**The beat contract (short):** `[data-vignette][data-beats]` containers get
cumulative `vg-b1..N` classes on an in-view timeline; authored markup is beat 0;
`[data-at="N"]` props appear at beat N (hidden only under `.js`). **The final
frame rule:** no-JS and reduced-motion users rest on the COMPLETED story — two
synced blocks at the bottom of vignettes.css define that frame; keep both in
sync with any new stateful primitive, and never leave a hybrid (a "Requested"
card beside a "candidate notified" note was a caught bug, not a state).

**Hard-won specifics (do not relearn):**
- `pathLength=100` + `preserveAspectRatio=none` leaves ~1px wire slivers in
  Chrome at dash 100/100 — vignettes.css ships 120/120 overshoot.
- **Headless Chrome clamps windows to 500px wide** — a `--window-size=390`
  probe certifies a 500px layout. tools/mcheck.py now wraps pages in a real
  390px iframe; never trust a plain-window mobile probe.
- Ring/pin coordinates over crops are DERIVED (formula in the scratchpad
  BUILD-BRIEF, worked examples in the two reference pages) — never eyeballed.
- The pricing total crossfade must clearTimeout on EVERY path of setTotal —
  the early-return race put a stale $990 on screen and into aria-live once.
- Overhang cards must clear both narrated screenshot cells AND figcaptions;
  events-dashboard + in-person hero placements were each corrected once.
- V6 (messaging) deliberately claims NO stage→preset trigger mapping (not
  visible in any capture); its three preset names are the screenshot's ON rows.
- Analytics' anno figure has NO vg-intro on purpose (it hosts the V5 vignette;
  two motion systems on one figure broke the budget). page-events.html has no
  vignettes.css link on purpose (uses none of it).
- Fictional-name set + verbatim location strings: the allowed lists live in the
  BUILD-BRIEF (scratchpad) and §7's neutralisation list — same law.

**Accepted deviations:** V2 diagrams run 2 beats with always-visible nodes
(the brief's 3-beat template contradicted the truthful-authored-state contract);
diversity page got S-treatments only; resources untouched (no card imagery).

**Open:** pricing bundle-ladder clips ~23px at true 390 (PRE-existing, task
chip spawned); real video embeds replace the five `.video-ph` posters
wholesale; both repos are now many commits behind the local folder — sync via
Scott's web-upload path (§6).

---

## 12. Concept 4 "vid" + its walkthrough (18 Aug 2026)

Scott asked for a FOURTH homepage concept after reviewing vidcruiter.com, then
for the click-through built out. Both are done. The other three concepts and
the 28 original pages are UNTOUCHED — this is a parallel set for review, not a
replacement. If vid is chosen, migrating the remaining pages is a separate job.

**Files:** `concept-4-vid.html` (homepage) + `vid-events.html`,
`vid-event-detail.html`, `vid-pricing.html`, `vid-faq.html`,
`vid-contact.html`. `index.html` is now a 4-up chooser. The vid nav/footer
point at the vid set; everything else still points at `page-*.html`.

**What the reference actually taught us** (measured, not eyeballed): their hero
"exploded composition" is a single flat PNG — it never moves and softens on
retina; ours is DOM over a real screenshot. Their motion lives in exactly three
places, the best being a diagram where labelled chips travel wires between two
anchors (`wire-travel` 6.4s, with `source-emit`/`hub-receive` ring pulses).
Tokens: wash `#E8F9F4 → #D3EBFD → #F0EEFE`, navy `#181454`, green `#179B48`,
violet cards `#5B21B6 → #4C1D95 → #3730A3`, Lato 700.

**Decisions Scott made (do not silently revisit):**
1. GREEN is a success accent ONLY; JobFairX blue stays brand/CTA.
2. The travelling-chip diagram carries OUR mechanic (matched candidates
   requesting interviews, one accepted) — NEVER an ATS/integration claim; we
   have no evidence of ATS integrations.
3. Display weight 600 on the vid concept only (500 everywhere else).
4. No stock photography — the iStock comps stay unlicensed and unpublished.
5. Event-detail ships all five countdown states behind the review-only
   switcher, defaulting to state A (early registration).

**Expensive lessons from this wave — read before editing any vid page:**
- **Green is per-ROW, not per-feature.** A first pass put "Setup complete" on
  the Atlanta Diversity Event card; that row carries a red "Setup" chip and a
  "Complete setup" button in the source screenshot (only Dallas Healthcare and
  Denver Technology are complete). The page would have contradicted a
  screenshot displayed further down it. Check the pixels before painting green.
- **`--void` resolves LIGHT inside a `data-theme="light"` wrapper.** The mobile
  drawer rendered near-white text on cream (~1.04:1) on all six vid pages. The
  drawer now hard-codes `#08090c`.
- **A port can silently drop a utility rule.** `vid-events.html` lost
  `[hidden]{display:none!important}`, so calendar filtering did nothing while
  the counter claimed otherwise. All vid pages now carry the guard.
- **`#8b909b` fails WCAG AA (3.2:1) for real text.** Use `#6b6f8c` on white.
  Green TEXT needs `--ok-ink #0e6e34`; `--ok #17994a` is swatch/rule only.
- Contrast on tinted grounds is a separate problem: `#6b6f8c` is only AA on
  white, landing 3.99–4.25:1 on the wash and lavender. Unresolved.
- Descendant selectors bit twice in one file (`.wire__anchor b` broke the
  wordmark onto three lines; `.wire__anchor span` painted the green payoff
  grey). Prefer `>` in card/anchor components.

**Known open items (not defects introduced here):**
- Footer column headings are 4.08:1 on the dark ground — a shared-token issue
  affecting ALL 28 pages; fix at `--ink-3` in base.css in one pass.
- "429 pre-registered veterans" on event-detail is feed-rendered in production
  but is NOT placeholder-marked, on the vid page OR the original
  `page-event-detail.html`. Decide and fix both together.
- The FAQ accordion animates `grid-template-rows` — the only layout-property
  animation in the set. Accepted as the house accordion technique for now.
- `page-event-detail.html` FAQ says "30 or more days"; the vid port says 31 to
  match `minDays:31`. HANDOFF §9's 30-vs-31 question is still open with Scott.

---

## 13. Concept 5 "AI Flow" + THE PAUSED FAN-OUT (18 Aug 2026, evening)

This session ended mid-flight at a deliberate stop Scott ordered. Read this
section, then AF-BRIEF.md, before anything else — the very next action is
already specced and awaiting only his green light.

### What happened this session, in order

1. **Vid walkthrough verified, fixed, published.** The five vid-* pages (§12)
   went through 3-agent adversarial verification; all findings fixed (notable:
   a dropped `[hidden]` rule silently disabled the events-page filtering; the
   mobile drawer painted light-on-light because `--void` resolves LIGHT inside
   a light wrapper — hard-coded `#08090c` now; `#8b909b` fails AA as text).
   Both repos updated and the live preview verified:
   scottjobagent.github.io/jobfairx-marketing-preview/ (chooser → all
   concepts; vid walkthrough fully clickable).
2. **Concept 5 "AI FLOW" built and verified** — `concept-5-aiflow.html`,
   added to the chooser. References: **wisq.com** for the layout grammar
   (calm editorial: cream/navy, huge centered statements, one enormous
   rounded panel per section, navy punctuation bands, grainy gradient CTA,
   editorial serif resources block) and **careerflow.ai** for the navigation
   (Features + Solutions mega-dropdowns: icon + bold name + one-line
   description + "New" tag + "All …" footer link). Scott: "take the
   navigation quality from career flow, but the rest from [wisq]".
   Six concept decisions are documented in the file's header comment — navy
   primary CTAs (differs from vid on purpose), no photography (we own none —
   the wisq look leans on it; the gap stays honest), no awards/logo walls,
   EQUAL-SIZE pricing cards (Scott explicitly dislikes the lifted featured
   card), serif scoped to the editorial block (masthead + card titles), the
   three "Needs update" articles never promoted.
3. **Nav icons upgraded on Scott's order**: he wants Careerflow's bright
   icons. Their files are Phosphor (MIT) fill glyphs recoloured #1570EF.
   Ours now: inline Phosphor FILL paths (fetched from
   unpkg.com/@phosphor-icons/core@2.1.1/assets/fill/) at 32px, no tile box —
   Features in brand blue var(--accent), Solutions in the five
   product-canonical type colours. If more icons are needed, fetch more fill
   variants from that same package.
4. **Concept-5 verification: 24 findings, all addressed.** The two HIGHs:
   the hero "Book a demo" was a dead `#`; and **motion.js only ever bound the
   FIRST [data-nav-toggle], so the drawer's × close button has been dead on
   every page since the original build** — fixed centrally in
   shared/motion.js (setDrawer + bind-all). Other fixes: veteran dropdown
   line had invented "transitioning service members" (reworded to the page's
   own claim); alt-text truth (request card gained the verbatim
   "Apr 22 · 10:00 AM CT" row); dashboard crops no longer slice the
   Complete-setup column; focusin stops the auto-tabs; closed drawer is
   visibility-hidden (no ghost tab stops); dropdown hover keeps AA; token
   bridge maps base tokens onto the .aiflow palette; index.html retitled
   Five, footnote rescoped (it falsely called ALL data "invented
   scaffolding" — concepts 3-5 carry verified data), 5-card auto-fit grid.
5. **index chooser** now: dark / light / hybrid (Recommended) / vid (New) /
   AI Flow (New).

### ⏸ THE STOP POINT — resume exactly here

Scott (verbatim intent): build out EVERY landing page for AI Flow — all the
feature pages, solutions for healthcare/veteran/diversity (+ technology,
entry-level, hub), pricing, FAQ, and the upcoming-events page, whose status
pills he loves ("Matching live", "Matching soon", "Early registration" +
save-$100 chip) and which must survive the redesign prominently. Then:
"Before you do the fan out, after you complete your finding list, stop, and
then I'll give you the green light to go." The findings list was delivered.
**The fan-out is NOT launched. Wait for Scott's green light, then go.**

The plan, ready to execute:
- **AF-BRIEF.md (repo root)** is the complete build brief for agents: chrome
  contract (clone concept-5-aiflow.html verbatim: palette, nav with both
  icon dropdowns, drawer, af-head/af-btn grammar, gradient CTA, light
  footer), the af- link map, copy/data law, self-QA requirements.
- **19 pages**: af-events (port vid-events content/JS — keep the status
  pills front and centre), af-event-detail (port vid-event-detail, all five
  countdown states, default A), af-pricing (port vid/page-pricing data +
  fixed setTotal stepper; EQUAL cards), af-faq, af-contact,
  af-platform.html + af-platform-{events-dashboard, candidate-pipeline,
  interview-scheduling, event-day, messaging-automations, analytics} (port
  the hybrid capability pages' content), af-in-person-interviews,
  af-solutions.html + af-solutions-{healthcare, diversity, veteran,
  technology, entry-level}.
- Orchestration that worked twice: ~8 build agents on disjoint page groups
  (workflow), then 3-4 verify agents (data truth+vocab / visual QA at
  1440+1100+true-390 in all three motion states / design law+a11y+code),
  then fix, then re-check. Also repoint concept-5-aiflow.html's nav,
  dropdowns and footer to the af- set in the same wave (today some links
  still target page-*.html).

### Not yet uploaded (repos are behind by exactly this list)

`concept-5-aiflow.html` (new), `index.html`, `shared/motion.js` (drawer
fix — benefits every page), `HANDOFF.md`, `AF-BRIEF.md` (new). Public
preview gets the comment-stripped versions of the html; docs stay private.
After the fan-out, the af- set joins the upload.

### Open items (unchanged priority, do not lose)

- Pricing bundle-ladder 390px clip: a task chip was spawned and Scott
  started it in a separate session — verify whether page-pricing.html got
  the .ladder__scroll fix before re-uploading that page.
- Footer heading contrast on the dark ground (4.08:1) — one-pass fix at
  --ink-3 across all 28 original pages.
- "429 pre-registered veterans" on both event-detail pages renders as fact
  but is feed-rendered in production — decide marking with Scott.
- The closed-drawer ghost-tab-stop fix (visibility) exists on concept-5's
  chrome only; hybrid/vid page sets still carry focusable links in their
  closed drawers — fold into the next pass over those sets.
- HANDOFF §9's older open questions (SOC 2, per-type stats, logo rights,
  30-vs-31 copy, onNewYearsSale) remain with Scott.

---

## 14. The AI Flow fan-out — BUILT (19 Aug 2026)

Scott gave the green light ("Green light to continue, and don't stop till you're
done"), and the fan-out specced in §13 + AF-BRIEF.md is built, verified and
uploaded. This section replaces §13's "⏸ THE STOP POINT" as the current state:
that stop no longer exists.

### What was built

**The chrome was repointed first.** `concept-5-aiflow.html`'s nav, both icon
mega-dropdowns, drawer and footer now target the af- set; the only remaining
`page-*` links are the seven deliberate ones (demo, about, resources,
interview-locations, privacy, terms, security). Every builder cloned that one
canonical chrome, so the 19 pages agree with each other by construction.

**All 19 af- pages exist** (`af-events`, `af-event-detail`, `af-pricing`,
`af-faq`, `af-contact`, `af-platform` + the six capability pages,
`af-in-person-interviews`, `af-solutions` + the five type pages). Built by 11
agents on disjoint groups, each porting content/data/behaviour from its vid- or
page- source and re-expressing it in the AF language (cream/navy, centered
`.af-head` grammar, one enormous rounded panel per section, navy punctuation
bands, grainy gradient CTA, light footer).

Specifics worth not relearning:
- **af-events** keeps the status pills Scott singled out — "Matching live"
  (green `#0e6e34`, the one genuinely live state), "Matching soon" (accent
  blue), "Early registration" (cream/navy) + the amber save-$100 chip — front
  and centre in the Status column. Full calendar JS ported: city search, type
  dropdown with the five canonical colour dots, `?type=` deep links resolved
  INSIDE the owning IIFE via `selectByValue()`. No virtual/in-person filter.
- **af-event-detail** ships all five countdown states behind the review-only
  switcher, defaulting to A. Equal-size tier cards.
- **af-pricing** was ported from `vid-pricing.html` specifically, because that
  file carries the `.ladder__scroll` fix (page-pricing.html still lacks it).
  Equal cards, "Most Popular" as a tag on Growth, stepper `setTotal` clears its
  timeout on every path.
- Placeholders were carried, not filled: the in-person pricing-parity flag, the
  Growth/Pro bundle ladders (never captured), diversity's `{{legal review
  required}}` blocks, per-type stats that do not exist, and every unfilled logo
  slot.

### Fixes made during the wave (beyond the new pages)

1. **`shared/base.css` gained `--s-7:28px`.** The chrome's `.af-card` padded
   with `var(--s-7)`, a token the spacing scale never defined (it jumps 24→32),
   so those cards rendered with zero padding on the homepage and every clone.
   One additive line fixes all of them.
2. **`page-solutions-healthcare.html`: removed "employers average 35 interviews
   and 8 hires."** This is the invented statistic §8.3 records — it had survived
   in the FAQ answer of the source page. The af- port never carried it.
3. **`page-solutions-veteran.html` + `af-solutions-veteran.html`: "the highest
   of the five" → "the highest of the three rates we publish."** Only three show
   rates exist; diversity and technology cannot be ranked below 91%.
4. **`vid-event-detail.html` + `af-event-detail.html`:** the FAQ sentence
   presenting 35 interviews / 7 hires as a veterans-wide average was rescoped to
   this event's own updated-daily figures — the exact type-wide-average error
   §8.3 warns about, inherited from the vid source.
5. **`af-solutions-healthcare.html`: the six `{{LOGO 01–06}}` slots and
   `{{Written confirmation per company}}` were restored** (in AF styling) after
   the port dropped them. Keep-every-placeholder is a hard rule, and the sibling
   type pages all kept theirs.

### Verification, and the second fix pass

Deterministic sweeps (script in the session scratchpad, re-runnable): 19/19
pages one h1, `[hidden]` guard present, zero banned vocabulary in rendered text
(comments/scripts/styles stripped, entities unescaped, alt text included), every
internal link resolving, footers hash-identical to the chrome modulo the
self-link swap, no `interviews-pending.png`. `tools/mcheck.py` (true-390 iframe
probe): **20/20 ok**, chrome included. A chrome-fidelity differ confirms all 19
pages still match concept-5's announce/nav/drawer/IIFE after every edit.

Four adversarial reviewers (data truth + vocabulary · visual QA at
1440/1100/true-390 in three motion states, split over two agents · design law +
a11y + code) returned **41 findings: 3 high, 19 medium, 19 low**. One was
disproved on inspection; the rest were fixed.

**Applied centrally, to all 20 pages:**
- The event-type listbox held focus with `outline:none` and a 1.12:1 active-row
  tint — no perceivable focus indicator (WCAG 2.4.7 Level A). Real outline plus
  an inset accent bar now.
- No `<main>` landmark and no skip link anywhere in the set (WCAG 2.4.1): both
  added; the skip link is the first body child, `<main id="content">` wraps
  everything between drawer and footer.
- Mega-dropdowns did not close on `focusout` — tabbing past the last panel item
  left the panel open behind the next nav item.
- The drawer's "Register for an Event" CTA was `--accent` on `#08090c` (3.88:1);
  now `#96b0ff` (9.4:1).
- `shared/vignettes.css`: rebuilt-fragment labels `#8b909b` (3.20:1 — the colour
  §12 records as unusable for text) → `#6b6f8c`; the amber product chip 3.78:1 →
  `#8d5512`; the queue vignette's no-JS/reduced-motion final frame kept the
  departed chip's layout box, leaving a ~140px hole — now `display:none`.
- The `PLACEHOLDER` review chip was an absolute corner overlay printing on top of
  live body copy. It is now an INLINE badge. (An intermediate version pushed it
  outside the box with `left:100%` and broke the 390px viewport on 14 pages —
  the probe caught it. Do not reintroduce either failure mode.)

**Applied per page (6 agents, each required to prove its fix by re-render):**
the af-faq location figure was re-derived from the source pixels so all four
rows *and* all four location lines are inside the frame (its caption had been
promising a fourth row the crop cut off; mobile switched to the 7/10 rail
because four legible rows do not fit 4/3 at 352px); af-pricing now renders three
identical cards in every selection state (measured 371×720 each — the stepper
region is reserved, not conjured, so nothing grows when selection moves) and
announces once per quantity change instead of twice; af-event-detail's Growth
CTA no longer carries a filled navy button while its peers carry cream ones;
overhang cards on events-dashboard, interview-scheduling, event-day,
messaging-automations, healthcare and entry-level were moved off the content
their own alt text and captions narrate; annotation pins that sat on the words
they label were recomputed; a dozen crops that ended mid-word or mid-glyph were
re-derived; af-solutions-veteran's h1 → h3 heading skip was closed.

One reviewer finding was rejected with evidence: the healthcare pin-3 "drift" at
1100px does not occur.

### Uploaded

Both repos are current as of this wave. Private `scottjobagent/jobfairx-marketing`
received all 57 HTML files, the 9 docs, `shared/` and — for the first time —
`tools/`. Public `scottjobagent/jobfairx-marketing-preview` received the 57
comment-stripped HTML files and `shared/`; docs and tools stay private. Live and
verified page-by-page (24/24 URLs 200, deployed bytes spot-checked for the
`--s-7` token, the AA colours, the `<main>` landmark and comment stripping):
**https://scottjobagent.github.io/jobfairx-marketing-preview/**

### Known-accepted, do not re-flag

- Fictional demo names (Dana Whitfield, Amara Osei, Rosa Delgado, …) are the PII
  **fix**, not PII (§7, §8.5).
- Text inside screenshot PIXELS ("Manage applicants", green "Setup complete",
  Denver "1 of 2 jobs") is an upstream capture problem; authored alt text
  deliberately does not narrate it.
- The three motion-state renders being byte-identical is the authored-frame ==
  final-frame contract working. Headless Chrome ignores
  `--force-prefers-reduced-motion` (see `tools/shoot.sh`) — verify reduced motion
  by reading the vignettes.css final-frame blocks, not by diffing screenshots.
- "The type is an audience, never a format." asserts the vocabulary law; it is
  not the banned phrase "event format".
- Announce anchors were normalised on purpose: pages with a real `id="location"`
  keep `#location`; analytics and messaging point at
  `af-in-person-interviews.html`; that page points at `#how`; af-contact points
  at `concept-5-aiflow.html#location`.

### Open with Scott (unchanged, plus two new)

Still open from §9/§13: SOC 2 / compliance status · per-type stats for
diversity, technology, veteran, entry-level · logo-wall rights · `onNewYearsSale`
· exact D→E cutoff hour · 30-vs-31 days (copy follows the code, 31) · the "429
pre-registered veterans" marking · in-person pricing parity.

New from this wave:
- **Empty `{{LOGO NN}}` slots vs. the AF "no logo walls" rule.** Veteran,
  diversity, entry-level and now healthcare ship six visibly empty slots. The
  keep-every-placeholder rule won over the no-walls rule; Scott may prefer the
  slots removed entirely in the AF language.
- **A diversity FAQ question was reworded** from "Do candidates apply to our
  postings first?" to "Do candidates respond to our postings first?" (id
  `q-apply` → `q-request`) because "apply" is banned in rendered text. The claim
  is unchanged; the recruiter-voice phrasing is Scott's call.

### Migration status

The af- set is a complete parallel walkthrough, exactly as the vid set is. The
original 28 pages and the vid set are untouched except for the four source-bug
fixes listed above. If Scott picks AI Flow, the remaining originals (demo,
about, resources, security, interview-locations, city-hub, legal) still need
porting — that is the next job, and it is not started.

---

## Instructions for the Next Claude

You are continuing an existing project that was paused only because the
previous chat reached its context limit.

Before making any changes:

1. Read this entire handoff — §14 last, most carefully; it holds the current
   state. (§13's "⏸ STOP POINT" is historical: that fan-out is built.)
2. Review the complete codebase: `shared/base.css`, `shared/vignettes.css`,
   `shared/motion.js`, then `concept-5-aiflow.html` (the active chrome),
   `concept-3-hybrid.html` and `page-platform-candidate-pipeline.html`
   (reference implementations), `AF-BRIEF.md`, and skim
   `LIVE-SITE-SCOPE.md` §2/§6b.
3. Review every file referenced in this handoff before trusting a claim
   about it.
4. Reconstruct the architecture, design system, UX philosophy, coding
   standards and prior decisions — §2 (product model) and §3 (verified
   facts) are law; §8/§11/§12/§13 lessons are pre-paid mistakes.
5. Identify exactly where the previous Claude stopped: the AI Flow page-set
   fan-out (AF-BRIEF.md, §13) is BUILT and uploaded — see §14. What is not
   started is porting the remaining original pages (demo, about, resources,
   security, interview-locations, city-hub, legal) into the AF language, which
   only matters if Scott picks AI Flow.

Once you have finished reviewing everything:

- Confirm that you fully understand the project.
- Summarize your understanding.
- Explain exactly where development left off and how you plan to continue.
- Do not make any code changes yet.

Then ask:

"I've finished reviewing the handoff and the codebase, and I'm fully caught
up on the Employer Marketing Website project. I understand exactly where
development paused and I'm ready to continue from that point. What would you
like to work on next?"

Wait for Scott's response before taking any further action.
