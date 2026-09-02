# JobFairX Marketing — Session Handoff 3

**Written:** 25 Aug 2026, at the end of a long Claude Code session.
**Covers:** the AI Flow (`af-`) 19-page fan-out, a rejected "Kula" concept, the new
**"Fairs AI"** concept (`concept-6-fairs.html`), the rebuilt **calendar page**
(`page-events.html`), and a **pricing page** audit plus copy changes.

**⚠️ READ THIS FIRST: TWO CLAUDE SESSIONS SHARE THIS DIRECTORY.** See §0. Getting
this wrong can destroy another session's work.

**Companion docs, in reading order:**
`HANDOFF-3.md` (this file — the most recent state) → `HANDOFF-2.md` (the *other*
session's stream, 16–25 Aug) → `HANDOFF.md` (§1–14, the original 28-page build; its
§2 product model and §3 verified facts are still LAW) → `LIVE-SITE-SCOPE.md` →
`AF-BRIEF.md` → `DESIGN-SYSTEM.md` / `CONTENT-SPEC.md` / `PAGE-INVENTORY.md`.

---

## 0. THE TWO-SESSION PROBLEM — read before touching anything

`~/Desktop/jobfairx-marketing/` is worked on by **two Claude sessions at once**, and
both publish to the **same** GitHub repos.

| | This session (HANDOFF-3) | The other session (HANDOFF-2) |
|---|---|---|
| Owns | `concept-6-fairs.html`, `page-events.html`, `page-pricing.html`, the 19 `af-*.html`, `concept-5-aiflow.html`, `shared/*` | `employer-home.html`, `employer-event-detail.html`, `build-employer-home.py`, `build-event-detail.py`, `assets/employer-home/`, `assets/event-detail/`, `assets/live-capture/`, `fonts/` |
| Method | Direct HTML editing | **Python builders** that regenerate HTML from captured live DOM |
| Version control | Does **not** commit; edits sit uncommitted in the working tree | **Commits to local git** (`git log` shows their commits) |
| Publishes via | github.com web upload | github.com web upload |

**Consequences you must respect:**

1. **Never edit `employer-home.html` or `employer-event-detail.html` directly.** They
   are generated. Edit the builder, re-run it. Even then — that is the other
   session's stream; leave it alone unless Scott says otherwise.
2. **Never run `git checkout`, `git restore`, `git stash`, or `git reset` in this
   directory.** This session's work is *uncommitted*. Those commands would delete it.
   `git status` showing ~30 modified files is normal and expected, not a problem to
   "clean up."
3. **Before uploading, check what is already in the preview repo.** Both sessions push
   to `scottjobagent/jobfairx-marketing-preview`. Upload only the files you changed.
   Do not upload a full tree — you could overwrite a newer file from the other stream.
4. The preview repo currently holds **64 root files**, including both streams'
   outputs. Both `employer-*.html` and all six `concept-*.html` are live there.

---

## 1. Executive overview

**Purpose.** Redesign JobFairX's employer-facing marketing site
(`jobfairx.com/employer`) so it reads as a premium enterprise AI platform rather than
a 2020 recruiting site, and so it correctly markets the newly launched **in-person
interview location**.

**Business goal.** Employers buy per-event packages ($495 / $895 / $1,495) or bundles
(5–100 events, down to $297/event). The site's job is to get an employer to register
for a hiring event. Every page ends in that action.

**Target user.** A recruiter or talent-acquisition lead evaluating whether a JobFairX
hiring event is worth $495–$1,495. They arrive knowing job boards, not knowing what
"matching" or "interview location" means here.

**Current phase.** Concept selection. Six homepage concepts exist side by side.
Scott has not chosen a winner. Two of them have page sets built out behind them.

**Current milestone.** The **Fairs AI** concept (concept 6) plus its two supporting
pages — the calendar and pricing — are the active work. Scott is iterating on them
directly and intends to hand them to a developer.

**Product vision.** An employer joins a hiring event, posts jobs, and matched
candidates request interviews. Accepting a request *is* the scheduling step. The
employer independently chooses where their own interviews happen: JobFairX video,
phone, in person at their address, or their own link.

---

## 2. THE PRODUCT MODEL — this is law, and it is easy to get wrong

Reproduced from `HANDOFF.md` §2 because violating it has cost this project real time,
more than once.

**An event is a market moment.** "Dallas Healthcare Hiring Event, Sep 22, 11:00 AM –
3:00 PM CT." Every employer joins the *same* event. There are exactly **five event
types**: Healthcare, Diversity, Veteran, Technology, Entry-Level.

**Interview location is a per-employer setting, not an event property.** Each employer
independently chooses: **JobFairX video** ("JobFairX video call") · **Phone** ("You
call each candidate") · **In person** (their street address) · **Your own link**
("Microsoft Teams"). Two employers at the same event can interview completely
differently. The events dashboard has an INTERVIEW LOCATION column showing all four
side by side — `assets/product/dashboard-events.png` is the best proof asset owned.

**What launched** is the in-person *interview location*, NOT "in-person events."

### Vocabulary law

| ✅ Always | ❌ Never |
|---|---|
| in-person **interviews**, in-person or video interviews | in-person **events**, virtual events, "event format" |
| set your interview location | choose your event format |
| candidates **request** interviews | candidates **apply** |
| employers **accept**, which **schedules** | "application", "applicants" |
| hiring events | virtual hiring events, virtual job fairs |

**"Video," not "virtual."** Established this session. "Virtual" is the retired
event-level word; "video" is what the product itself says ("JobFairX video call").

**Scott uses the banned phrasing in conversation.** He has said "in person and virtual
job fairs" and then corrected himself in the same breath. Interpret intent, write the
lawful version, and say so in one sentence. He has never objected to this.

**Structural consequences:** the calendar has NO virtual/in-person filter (events carry
no format); event pages are never labelled virtual or in-person; a `next-inperson`
programmatic family must never be created.

---

## 3. Verified facts — invent nothing

All from `HANDOFF.md` §3 / `LIVE-SITE-SCOPE.md`, captured by rendering the live site
with JS (plain fetch misses client-rendered parts).

**Platform stats:** 4,000+ employers · 500,000+ interviews conducted · 300+ cities ·
3M+ registered candidates. These are platform totals earned by video events — never
imply in-person volume.

**Pricing:** Starter $495 / Growth $895 ("Most Popular") / Pro $1,495 per event.
Tiers: 1 / up to 3 / up to 6 jobs · 20+ / 60+ / 100+ scheduled candidate interviews ·
2 / up to 5 / unlimited recruiter seats. **The scheduled-interview count is a volume
commitment, not a feature** — it carries the most weight.

**Bundles:** 8-rung ladder. Starter: 5=$470ea → 10=$445 → 15=$420 → **25=$395 (Most
Popular)** → 40=$365 → 50=$345 → 75=$320 → 100=$297ea (save $19,800; max 40% off).
"Credits never expire" · "Use across any event type." **Growth and Pro ladders were
never captured** and ship as placeholders.

**Early registration:** flat **$100 off every tier**, never a percentage. Struck
prices $395 / $795 / $1,395. **Threshold: the live code says `minDays: 31`; our pages
say 30. UNRESOLVED — see §14.**

**Event lifecycle, five states** (event-detail page renders all five behind a
REVIEW-ONLY switcher, keys 1–5, default state A):

| State | Window | Banner (verbatim) |
|---|---|---|
| A | 31+ days | "Early registration pricing ends soon. Save $100 and lock in priority candidate matching." |
| B | 15–31 d | "Candidate matching activates soon." |
| C | ~3–15 d | "Candidate matching is live." |
| D | ~2 d | "Employer registration closes tomorrow. Reserve your spot now →" |
| E | ≤1 d | "Employer registration is closed for this event. Next {City} {Type} Hiring Event: {Date}." |

**Show rates — only three exist:** Healthcare 91% · Veterans 89% · Entry-Level 86%.
Diversity and Technology have **none**. Healthcare also: 582 events in 2025.
Platform-wide: 87% of employers return.

⚠️ **"35 interviews / 7 hires per employer" are PER-EVENT metrics from a veterans
event page** and swing 2–3× by market (Portland 968/73/19). They are NOT type-wide
averages. This invented statistic has resurfaced three times; it was purged again this
session.

**The 20-mile fact:** "candidates are verified to be within approximately 20 miles of
the event city." The strongest in-person argument owned.

**Customers — only three, one sentence each, company + role, no personal names:**
Target ("This was our second event and we interviewed over 90 candidates in one day"
— Senior Recruiter) · Western Regional Medical Center ("My team hired two LPNs, three
RNs, and two MAs at the hiring event" — Director of Talent Acquisition) · Tesla
("We've used JobFairX for three veterans events now…" — Recruiter).

**Contact:** info@jobfairx.com · (702) 269-0808 · JobFairX, LLC, 209 S Stephanie St.
STE B #144, Henderson, NV 89012 · Mon–Fri 5:00 AM–5:00 PM PST.

**Event type colours (product-canonical):** Diversity orange `#e07b39` · Technology
blue `#2f5cff` · Healthcare teal `#12897f` · Veterans red `#d1454b` · Entry-Level sky
`#3aa0e6`.

**No logo rights.** The live healthcare wall names CVS/Kaiser/Mayo with an unverified
"has attended" claim; **all ten live technology logos are fabricated**. We ship no
logo walls — only visibly empty `{{LOGO NN}}` slots with a note that they stay empty
until each company confirms in writing.

---

## 4. Repository, deploy, and preview

**Local canonical:** `/Users/scottl./Desktop/jobfairx-marketing/`

**Repos:**
- **Private** `github.com/scottjobagent/jobfairx-marketing` — everything, including
  strategy docs. For the developer.
- **Public preview** `github.com/scottjobagent/jobfairx-marketing-preview` — site only,
  HTML comments stripped, docs excluded. Live at
  **https://scottjobagent.github.io/jobfairx-marketing-preview/**

**The only push path is the github.com web UI in Scott's Chrome.** There are no git
credentials on this machine, no `gh`, no SSH keys. Procedure that works:

1. Stage files somewhere the session can read (the scratchpad).
2. Navigate to `https://github.com/<repo>/upload/main` (add `/<dir>` for a subfolder;
   the URL creates the directory).
3. `find` the file input **fresh on each page load** — refs go stale.
4. Fill the commit summary, then click **Commit changes**. A `find`-ref click sometimes
   does not submit; take a screenshot and click by coordinate if the page does not
   navigate away.
5. **Verify by fetching the deployed bytes**, not by assuming. GitHub Pages takes
   ~30–70s; a check immediately after commit can return the stale file and read as a
   failure. Poll with an until-loop and a cache-buster query string.

**Preview stripping:** HTML comments are removed for the public repo
(`re.sub(r'<!--.*?-->\n?', '', src, flags=re.S)`). Strategy docs are never uploaded
there.

**Local preview server:** `python3 -m http.server 8790` from the repo root. Motion
needs HTTP; `file://` renders but sits still. **Port 8765 is occupied by another
process** and 8788 went stale mid-session — use 8790 or verify before sharing a link.

**Scott's link preference:** he cannot click `localhost` links in his client (they do
not linkify) and has to copy-paste them. **Always give the `https://` preview URL**,
and open pages directly in his Chrome when possible.

---

## 5. What exists — complete file inventory

### 5.1 Homepage concepts (6)

| File | Concept | Language | Page set behind it |
|---|---|---|---|
| `concept-1-dark.html` | Cinematic dark | Pre-live-data scaffolding | none |
| `concept-2-light.html` | Technical-editorial | Pre-live-data scaffolding | none |
| `concept-3-hybrid.html` | **Night into day (recommended)** | Dark hero → light proof → dark close | the 27 `page-*.html` |
| `concept-4-vid.html` | Daylight platform (vidcruiter) | Wash gradient, violet cards | 5 `vid-*.html` |
| `concept-5-aiflow.html` | Calm editorial (wisq + careerflow) | Cream/navy, mega-dropdowns | 19 `af-*.html` |
| `concept-6-fairs.html` | **Fairs AI (vFairs) — ACTIVE** | White/grey, JobFairX blue | `page-events.html`, `page-pricing.html` |

`index.html` is the chooser. **It still shows five cards — concept 6 was never added.**

### 5.2 The `af-` set (19 pages, AI Flow language)

`af-events` · `af-event-detail` · `af-pricing` · `af-faq` · `af-contact` ·
`af-platform` + `af-platform-{events-dashboard, candidate-pipeline,
interview-scheduling, event-day, messaging-automations, analytics}` ·
`af-in-person-interviews` · `af-solutions` + `af-solutions-{healthcare, diversity,
veteran, technology, entry-level}`.

### 5.3 The original set (27 `page-*.html`, hybrid language)

events, event-detail (template, 5 states), pricing, faq, contact, platform + 6
capability pages, solutions + 5 type pages, interview-locations,
in-person-interviews, demo, security, resources, about, privacy-policy, terms,
city-hub (template).

### 5.4 Shared

- `shared/base.css` (389 lines) — tokens + primitives. **Read first.**
- `shared/vignettes.css` (420 lines) — animated product vignettes + the no-JS /
  reduced-motion final-frame contract.
- `shared/motion.js` (367 lines) — reveal, parallax, nav, tabs, journey, counters,
  anno, vignettes.
- `assets/product/*.png` — 15 files, 14 usable. **Never use `interviews-pending.png`**
  (byte-identical duplicate of `interviews.png`).
- `tools/mcheck.py` — **true-390 overflow probe.** `tools/capture.py` — screenshot
  harness with a mandatory text-neutralisation list. `tools/shoot.sh`.

### 5.5 The other session's files — do not touch

`employer-home.html`, `employer-event-detail.html`, `build-employer-home.py`,
`build-event-detail.py`, `assets/employer-home/`, `assets/event-detail/`,
`assets/live-capture/`, `fonts/`.

---

## 6. CURRENT WORK IN PROGRESS — resume here

**Nothing is half-finished.** Every change made this session is complete, verified and
pushed. Scott ended the session by asking for this handoff, not by interrupting work.

**The active thread** is the Fairs AI concept and its two supporting pages. Scott is
iterating on them screenshot-by-screenshot and intends to hand them to a developer.
His last three instructions were: audit the pricing page and add the in-person/video
option (done), mock the changes before building (done), and build them (done and
pushed).

**Three things were flagged to Scott and are awaiting his answer** (§14). He has been
asked about the 30-vs-31-day question **three times** and has not answered. Do not
change it unilaterally.

**The most likely next task**, based on what was flagged at the end: bringing
`page-pricing.html` into the Fairs AI language. It currently wears the **old dark
hybrid nav with Contact Us in it**, so clicking "Pricing" from the calendar page jumps
the viewer from a white Fairs AI header into a dark page with a different nav. It also
still has a **"Book a demo"** button, which Scott killed everywhere on the AI Flow set.
Both were reported; neither was changed, because pricing was not in the stated scope.

---

## 7. `concept-6-fairs.html` — the Fairs AI homepage

**Reference:** `vfairs.com/event-management-platform/virtual-job-fair/`, torn down by
four agents at 1440×1057 with CDP and pixel sampling.

### 7.1 What the teardown found (do not re-derive)

- **Nav:** 80px, flat `#FFFFFF`, **no border and no shadow** (verified: y=79 white,
  y=80 hero). Sticky at `scrollY ≥ 80`, and the stuck state settles at **opacity .9**,
  not 1. Container `max-width: 1238px` + `5vw` padding.
- **Hero:** 613.47px. Base `#FFF7F5` under a **raster PNG** (`bg-img-min.png`,
  1920×658, indexed) at `background-size: cover` — a cool grey-lavender bloom anchored
  top-left plus a warm peach/pink **double** radial on the right (core at 86%/83% of
  the artwork). At 1440 the right 350px of that artwork is clipped away.
- **Hero art:** a **Lottie** (910×512, 60fps, 603 frames) of **six embedded PNGs**.
  Zero vector shapes — every card, chip, avatar and connector is baked pixels.
- **Trust band:** `#F1F1F1`, 60px padding, centred 24px/500 heading, Gartner + G2
  badges left, 4×3 logo grid right under a colour-kill filter chain.
- **Chip row:** 7 outlined pills, `1px #606970`, radius 8, shadow
  `0 1px 2px rgba(0,0,0,.05)`. Hover fills `rgba(249,102,52,.15)` with the border
  tinted **over** the fill.
- **Feature blocks:** copy column 600px, media board 616×429. The board is a **Lottie
  stack**, not CSS: white solid → a 55px-cell grid raster at 47% opacity with accent
  dots at every **second** intersection → **two drifting radial glows** (32% layer
  opacity over 0.694 peak ≈ 0.222 effective) → the product artwork. **~17MB of Lottie
  for that one band.** Block 3 alone swaps the grid for a salmon rounded panel.
- **Bullets:** FontAwesome ticks `#F96634`, 18px, 23px indent. **Arrow links:** a 7×7
  box with two 3px borders rotated 45°.
- **Testimonials:** nested double panel, same fill `#ECF0F4`, outer radius 24 / inner 16.
- **CTA band:** 1200×243 plate inset 120px, radius 12, `#FEF0EB` under a raster orange
  gradient carrying two lighter rounded "elbow" ribbons.
- **FAQ:** rows `#F1F5F8`, radius 12, 1100×70, 20px gaps, chevron 16px from the right.

### 7.2 Decisions taken (documented in the file's header comment)

1. **Palette is JobFairX blue** (Scott's explicit call). Their orange→pink gradient
   maps to blue→cyan. Their neutral grounds (`#F1F1F1`, `#F1F5F8`, `#ECF0F4`) are kept
   because those *are* the design; only the chroma changed.
2. **The hero wash is rebuilt in CSS** — three radial-gradients on the measured
   geometry, not an 86KB raster.
3. **The hero art is rebuilt in DOM** (Scott: "good call") — a real product screenshot
   plus sharp DOM cards, so it stays crisp and every string in it is verifiable.
4. **The feature board is rebuilt in CSS** — white base, a 39.37px grid with accent
   dots at alternate intersections, two drifting glows at ~22% effective alpha. **This
   is the layer most likely to be missed**; it is why those blocks read as designed.
5. **No booths, no 2D/3D environments, no multilingual event sites, no booth payments.**
   vFairs sells multi-employer *hosting*; our employers *join* events.
6. **No Gartner/G2 badges, no customer logo wall, no language selector, no site
   search.** The trust band keeps its composition: verified stats where the badges sit,
   empty `{{LOGO}}` slots where the wall goes.
7. **Type is Inter, not TT Norms Pro.** Their h1 is 48px/56px in a face that *is* the
   bold (weight 400 declared); their 21px eyebrow renders as faux bold because only a
   400 face loads. Type here is fluid; theirs is fixed.

### 7.3 Structure

Nav → hero (copy left, layered DOM composition right) → trust band → section head +
chip row → 5 alternating feature blocks (matching, pipeline, scheduling, locations,
event day/reporting) → testimonials → CTA band → FAQ (5 questions) → dark footer.

### 7.4 The header (ported to the calendar page)

Scott asked for the **AI Flow header structure in the Fairs AI chrome**. Nav reads:
**Upcoming Hiring Events · Features ⌄ · Solutions ⌄ · Pricing · FAQ**, then Sign In and
Register for an Event. **Contact Us was removed from the nav** on both pages (it stays
in the footer).

- **Features panel:** 720px, 2 columns, 7 items — Events dashboard, Candidate pipeline,
  Interview scheduling, Event day, Messaging & automations, Analytics & reporting,
  In-person interviews (with a "New" tag) — plus an "All features →" row.
- **Solutions panel:** 560px, 5 items in the five product-canonical colours, plus
  "All solutions →".
- **Icons** are Phosphor **fill** glyphs (MIT), inlined, fetched originally from
  `unpkg.com/@phosphor-icons/core@2.1.1/assets/fill/`.
- **Behaviour:** click toggles, hover opens for mouse users with a 160ms close delay,
  Escape closes and returns focus to the button, outside-click closes, `focusout`
  closes when tabbing past the last item.
- **All dropdown links are `href="#"`** — Scott: "No need to have them point anywhere
  yet. We're just creating the nav."
- Below **1200px** the whole row folds into the drawer (raised from 1040px because two
  dropdown buttons made the labels wrap).

---

## 8. `page-events.html` — the calendar page (most-worked file)

1,459 lines. This page was transformed from the hybrid original into the Fairs AI
language across several rounds of Scott's feedback.

### 8.1 What was removed

The **announce bar**, the **old dark hybrid nav and drawer**, and the entire **dark
hero** (eyebrow, "2026 hiring events", intro line, the NEW Interview location card, and
the bullet strip). Scott: "I want to remove the section… We don't need it."

### 8.2 What replaced it

The **Fairs AI header** (minus Contact Us, with `aria-current="page"` on Upcoming
Hiring Events), then a **compact hero copied from the live calendar page**
(`jobfairx.com/employer/hiring-event-calendar`):

- Eyebrow: **2026 Hiring Events**
- H1: **Interview-Ready Candidates Matched to Your Jobs**
- Sub (Scott's final wording): **"Register for a hiring event, post your jobs, and
  select in-person or video interviews. AI Candidate Matching starts immediately."**

The hero sits on a soft lavender-blue wash (`.cal-hero__wash`, two radial gradients).

### 8.3 The calendar itself

- Ground is **`#f7f8fa`**, matching the live page — the calendar no longer sits on white.
- Rows are **compact white cards**, radius 12, `1px #e6e8ec`, 10px apart, shadow only on
  hover. Scott chose cards over ruled rows after being given the trade-off.
- Columns: **Date · City · Type · Candidate matching**, then a **View Event Details**
  button.
- **City is its own column** and the words "Hiring Event" were stripped from every row
  label. Rationale given to Scott and accepted: every row on the page is a hiring event,
  so repeating it 14 times pushes the differentiators right and makes the column
  unscannable.

### 8.4 The Candidate matching column — the most-discussed decision

It was originally called **Status** and mixed two different clocks: a matching state
("Matching live") and a price ("Early registration"). That is why no header fit.

**Resolution:** the column asks one question and carries three values on one timeline:

| Value | Window | Style |
|---|---|---|
| **Live** | under ~15 days | green `#e7f5ec` / `#146c43`, pulsing dot |
| **Starts soon** | 15–30 days | accent blue tint / `#1f45d6` |
| **Starts 30 days out** | 31+ days | neutral `#f0efec` / `#5f5e5a` |

The discount left the column and became an amber **Save $100** chip under the city.
**It was previously printed twice on those rows** — as a chip *and* as a status pill.
The duplicate pill was deleted.

**Scott's ruling on the two remaining lifecycle states:** "I don't wanna put
registration closed on the calendar... Candidate matching stays live until the event
starts so we don't need to make these updates... they'll see that when they click on
the event details, and we show them the next event." **Closes tomorrow and Registration
closed are deliberately absent from the calendar.** They belong on the event detail
page. This also corrected a wrong assumption: matching does **not** stop when
registration closes.

### 8.5 Column widths — two failed attempts before the fix

1. Original: `132px 1fr 158px 178px 148px`. City was the only flexible column, so all
   slack pooled between City and Type while Type/matching/button clustered right.
2. First fix: capped City at 300px and put the slack in a spacer *before* the button.
   This only **moved** the hole; Scott caught it from a screenshot.
3. **Current fix:** every data column flexes —
   `minmax(96px,.7fr) minmax(150px,1.3fr) minmax(126px,1fr) minmax(140px,1.05fr) 168px`.
   Measured at 1900px: 152 / 282 / 217 / 228px with even 20px gutters. The button stays
   **fixed at 168px** — a button that grows with the window looks broken. Ratios are
   weighted, not equal: City is widest ("Manchester, NH" is the longest string), Date
   narrowest (fixed-length).

### 8.6 Mobile (≤820px) — rebuilt as cards

The old mobile stack was genuinely broken: the **View Event Details button rendered on
top of the Live pill**, and the event type stacked *above* the city.

Now each row is a card in scan order: date small on top → city as the headline → the
Save $100 chip on its own line → type and matching pill sharing a line → **full-width
button**. Below 380px the two pills stop sharing a line. The tap target went from a
~100px button to the full card width.

### 8.7 JS that must never regress

City search (150ms debounce), the custom type listbox with five colour dots and full
keyboard support, `?type=healthcare|diversity|veteran|technology|entry-level` deep
links resolved **inside the owning IIFE** via `selectByValue()` (a synthetic click does
not work), Load More, the `[hidden]{display:none!important}` guard, and the empty
state. `var PAGE` was raised **8 → 14** because all six early-registration rows sat
behind Load More, making the Save $100 state invisible on load.

### 8.8 Placeholder still on the page

`{{LIVE_EVENT_FEED}}` above the table: "sample rows built from the real market list and
the five real event types. Dallas · Aug 25 and Pearland · Sep 22 are verified against
the live site; every other date is feed-rendered in production, not a sourced fact."
**Scott was asked twice whether the developer should see this. He has not answered.**

---

## 9. `page-pricing.html` — audited and updated

1,243 lines. Still in the **hybrid** language (dark nav, dark sections).

### 9.1 The audit

The **live** pricing page (`jobfairx.com/employer/hiring-event-pricing`) mentions
interview location **nowhere** — not in the headline, not in the three cards, not in
its eight "All Packages Include" items. Its title is still "Virtual Hiring Event
Pricing." Our page already covered it in four places, but the **includes list was
missing it** — the one place a buyer comparing against a competitor would look.

### 9.2 The four changes made (Scott approved a mockup first)

1. **Headline** → **"Flexible Hiring Event Packages"** (Scott chose option B; he
   explicitly rejected the old "20, 60 or 100+ scheduled interviews.").
2. **Sub** → "Register for a hiring event, post your jobs, and select in-person or
   video interviews. AI Candidate Matching starts immediately." The old sub opened
   "That's what a package is," which pointed back at the deleted headline, so this was
   forced, not optional.
3. **Card bullet** on all three tiers: "All four interview locations" → **"In-person or
   video interviews"**. Scott rejected the longer "— your choice" version.
4. **Includes list** gained a 9th item in **position four**, the only item with a
   second line: **"In-person or video interviews" / "Set your interview location per
   event. It never changes the price."** The grid moved from 4 columns to **3** so nine
   items read 3×3 instead of leaving an orphan.
5. The redundant hero trust chip "All four interview locations included" was **removed**
   (the badge directly above says the same thing better).

### 9.3 ⚠️ SCOTT DISLIKES EM DASHES

"do not use an m dash." Avoid `—` in all site copy from now on. Use a period or a
comma. (This document uses them; the *site copy* must not.)

---

## 10. The `af-` set — 19 pages, built and verified this session

Built by 11 agents on disjoint page groups, each cloning `concept-5-aiflow.html`'s
chrome verbatim and porting content from its `vid-*` or `page-*` source.

**Verification:** deterministic sweeps (one h1, `[hidden]` guard, zero banned
vocabulary in rendered text, link map, footer hash-identity, no
`interviews-pending.png`) plus `tools/mcheck.py` at true-390 → **20/20 ok**. Then four
adversarial reviewers returned **41 findings: 3 high, 19 medium, 19 low**. One was
disproved; the rest were fixed.

**Fixes applied centrally to all 20 pages:**
- The event-type listbox held focus with `outline:none` and a 1.12:1 active tint — no
  perceivable focus indicator (WCAG 2.4.7 Level A).
- **No `<main>` landmark and no skip link anywhere** (WCAG 2.4.1). Both added.
- Mega-dropdowns did not close on `focusout`.
- The drawer CTA was 3.88:1 on `#08090c`; now `#96b0ff` at 9.4:1.
- `shared/vignettes.css`: `#8b909b` (3.20:1) → `#6b6f8c`; the amber chip 3.78:1 →
  `#8d5512`; the queue vignette's final frame left a ~140px layout hole.
- The `PLACEHOLDER` review chip was an absolute corner overlay printing on top of live
  body copy. It is now an **inline badge**. An intermediate version used `left:100%`
  and **broke the 390px viewport on 14 pages** — do not reintroduce either failure.

**Source-page bugs fixed while in there:** the invented "35 interviews and 8 hires" in
`page-solutions-healthcare.html`; "the highest of the five" show rates (only three
exist) in `page-solutions-veteran.html`; a veterans-wide 35/7 average in
`vid-event-detail.html`; and a missing `--s-7: 28px` token in `shared/base.css` that
was silently zeroing `.af-card` padding on the homepage and every clone.

**"Book a demo" was killed across all 20 AI Flow pages** (hero, closing CTAs, footer
row) on Scott's instruction: "We don't want that anywhere."

---

## 11. Design system

### 11.1 Shared foundation (`shared/base.css`)

- **Never pure white or black.** Canvas `#fbfaf8` light / `#0b0d12` dark; ink `#14161a`
  / `#f4f6fa`.
- **Display weight 500, never 700** (concept 4 and 6 deviate to 600/700 deliberately).
- **Tracking is a ramp that crosses zero:** −0.042em at display → **+0.004em at body**.
  Negative tracking below 18px was an early mistake, corrected system-wide.
- **One depth mechanism per element:** hairline + rim-light on dark, shadow on light,
  never both. **No coloured bloom** (cut from 42% to 15–16% alpha after research showed
  peers use none).
- **HARD CUTS between light/dark sections.** Scott ordered this explicitly. The
  gradient `.seam` elements were deleted. Do not reintroduce.
- **Nav is SOLID when stuck — no backdrop-filter.**
- **No 3D-tilted screenshots.** `--tilt` exists defaulting to 0deg for reversibility.
- **Screenshots crop into the story region**, never shrink the whole frame. `--z` zoom,
  `--l`/`--t` percentage offsets of the image via `translate()`, `--zm`/`--lm`/`--tm`
  for mobile art-direction.
- Spacing scale: `--s-1` 4px … `--s-7` 28px … `--s-40` 160px.
- Motion: entrances `cubic-bezier(.16,1,.3,1)`, hover `(.4,0,.2,1)`, reveal = opacity
  150ms linear + transform 800ms, stagger 60ms via `--i`, hero headline never animates
  in, no springs, static logo walls, full `prefers-reduced-motion` support.

### 11.2 Fairs AI palette (`concept-6-fairs.html`, `page-events.html` header)

```
--f-white  #ffffff      --f-grey   #f1f1f1   (trust band)
--f-panel  #f1f5f8      (FAQ rows)
--f-quote  #ecf0f4      (testimonial cards)
--f-hero   #f5f8ff      (their #FFF7F5, swung blue)
--f-ink    #101216      --f-ink-2  #606970   (their exact nav/body grey)
--f-ink-3  #8b929a      --f-line   #e0e0e0
--f-blue   #2f5cff      --f-blue-deep #1f45d6   --f-cyan #2ba0ff
--f-grad   linear-gradient(to right, #2f5cff 0%, #2ba0ff 100%)
```

Container `.f-row`: `max-width: 1238px`, `padding-inline: 5vw`, 80px flat at ≥1600.

### 11.3 The final-frame contract (`shared/vignettes.css`)

Authored markup is beat 0 and must be a **complete, truthful screen**. With JS absent,
blocked, or reduced motion, the page rests on the **completed** story — never beat 0
with props revealed, and never a hybrid (a "Requested" card beside a "candidate
notified" note is a contradiction, not a state). Two synced blocks at the bottom of
the file define that frame; keep both in sync with any new stateful primitive.

---

## 12. Verification routine — run this on every change

1. **`python3 tools/mcheck.py <files>`** — the true-390 probe. Headless Chrome clamps
   `--window-size` to a 500px minimum, so a `--window-size=390` run certifies a 500px
   layout and lies. `mcheck.py` wraps each page in a real 390px iframe.
2. **Render and LOOK.** Screenshot at 1440, and at the width the change affects. Crop
   bands with PIL and actually read them. Several bugs this session were invisible
   until a crop was inspected.
3. **Probe behaviour, don't assume it.** Drive the page in a headless iframe harness
   and report state through `document.title`: filters, deep links, dropdowns, search.
4. **Vocabulary sweep** on rendered text — strip comments, scripts and styles, unescape
   entities, include `alt` and `aria-label`.
5. **Chrome fidelity** — the af- set has a differ that checks announce/nav/drawer/IIFE
   against `concept-5-aiflow.html`.
6. **Verify the deployed bytes** after pushing.

---

## 13. Lessons learned this session

1. **Both reference sites' signature effects were baked assets, not CSS.** Kula's
   gradient is a 15-second MP4; vFairs' wash is a raster PNG and its hero art is a
   Lottie of six flattened PNGs. **Always determine whether the thing you are copying
   is even reproducible** before promising it.
2. **A find-and-replace over rows silently skipped six of fourteen.** The early-
   registration rows had an extra `<i class="ev__chip">` inside the name cell, so the
   pattern did not match. They were all behind Load More, so the render looked clean.
   **Count what you changed and compare to what exists.**
3. **Fixing "too much whitespace" by capping one column just moves the hole.** Slack has
   to be shared across every flexible column, or it pools somewhere new.
4. **`box-sizing: border-box` ate a 10px bezel** and made a "390px" mobile preview
   render at 370. Close enough to look right, wrong enough to hide a breakpoint bug.
5. **Media queries key off viewport width.** A CSS-narrowed wrapper renders the desktop
   layout and lies; a real iframe is the only honest mobile preview.
6. **A column can only be scanned if every cell answers the same question.** Mixing a
   product state and a price in one column is what made it unnameable.
7. **The invented "35 interviews / 8 hires" statistic has now resurfaced three times.**
   Check §3 before any number enters a page.
8. **GitHub Pages returns stale bytes for ~30–70s.** A verification immediately after
   commit reads as failure. Poll.

---

## 14. Open questions for Scott

1. **30 or 31 days for the early-registration window.** Our pages say 30 in three
   places; the live site's code says `minDays: 31`. **Asked three times, unanswered.**
2. **The `{{LIVE_EVENT_FEED}}` note on the calendar** — should the developer see it, or
   should it come out? Asked twice, unanswered.
3. **`page-pricing.html` still wears the old hybrid nav** (with Contact Us) and still
   has a **"Book a demo"** button. Flagged, not changed.
4. **The calendar page is still hybrid below the event list** — the dark
   interview-location section, dark CTA and dark footer. Flagged, not changed.
5. **Empty `{{LOGO NN}}` slots** on the veteran, diversity, entry-level and healthcare
   pages: keep, or drop entirely in the AF language?
6. **A diversity FAQ question was reworded** from "Do candidates apply to our postings
   first?" to "…respond to…" because "apply" is banned. Same claim; his call on phrasing.
7. Older, still open from `HANDOFF.md` §9: SOC 2 / compliance status · per-type stats
   for diversity and technology · logo-wall rights · `onNewYearsSale` sixth banner
   state · exact D→E cutoff hour · testimonial personal names · in-person pricing parity.

---

## 15. Remaining roadmap

**Immediate**
1. Answer §14.1–14.4 with Scott, then act on them.
2. Bring `page-pricing.html` into the Fairs AI language (header, grounds, type) so the
   three-page walkthrough is coherent.
3. Decide the fate of the calendar's hybrid tail.
4. Add concept 6 to `index.html` (the chooser still shows five).

**Then**
5. If Fairs AI wins, fan out the remaining pages the way the af- set was built.
6. Resolve the 30-vs-31-day question across every page that states it.
7. Pre-production: delete the REVIEW ONLY state switcher from event-detail pages,
   convert PNGs to AVIF/WebP with `loading="lazy"`, replace the five `.video-ph`
   placeholders, fill placeholders from verified data only, and get the prototype's
   PII/vocabulary fixed upstream.

**Never (rejected on evidence — do not relitigate without new data)**
Four separate interview-location pages · a standalone job-postings page (Scott: it is
part of the package) · a blog · careers · case-study pages (no permissions) ·
title×city programmatic (247,808 URLs) · frosted nav · gradient seams · coloured bloom
· 3D tilt · marquee logo walls.

---

## 16. Risks

- **Two sessions, one directory.** §0. The single largest risk in this project.
- **Uncommitted work.** This session's changes live only in the working tree. Any
  destructive git command loses them.
- **PII upstream.** The public prototype still shows what look like real candidate
  names. Marketing copies are clean; the source is not.
- **Legal.** Never draft policy text. The refund-policy gap is flagged visibly in
  Terms. The diversity page must never imply selection by protected characteristics.
- **Licensing.** `assets/_reference-do-not-publish/` holds unlicensed iStock comps.
- **Public exposure.** The preview repo is world-readable, including pricing and the
  "not yet certified" security honesty. Scott chose this knowingly.
- **Fragile invariants** worth checking after any bulk edit: footer hash-identity
  across a set · exactly one h1 per page · zero 390px overflow · no
  `interviews-pending.png` · vocabulary sweep · the `[hidden]` guard.

---

## 17. How Scott works

- Short bursts, often voice-dictated. **Expect transcription noise** — "road treatment"
  meant "row treatment", "take it for datum" meant "take it verbatim", "the toogle"
  meant the toggle. Interpret intent.
- He says "green light" when he means go, and asks for confirmation before big work.
  **When he asks you to confirm understanding, confirm and stop — do not start.**
- He wants to be **shown**, not told. Mock things up in chat before building. He
  responds to visuals and picks quickly.
- He asks "what do you recommend?" and expects a real answer with reasoning, not
  options without a verdict.
- He gives corrections by screenshot. Look at what he sends before responding.
- **He dislikes em dashes in copy.**
- He wants clickable `https://` links, not localhost.

---

## Instructions for the Next Claude Code Session

You are continuing a project that was paused only because the previous Claude Code
conversation reached its context limit.

Before making any changes:

1. Read this entire handoff from beginning to end. **§0 first** — two sessions share
   this directory, and a careless git command would destroy uncommitted work.
2. Review the complete codebase.
3. Review every file referenced in this handoff.
4. Verify your understanding against the current implementation.
5. Reconstruct the project's architecture, UX philosophy, design system, coding
   standards, and implementation strategy.

Once you have completed your review:

- Confirm that you fully understand the project.
- Provide a concise summary of your understanding.
- Identify exactly where the previous Claude stopped working.
- Do not write any code yet.
- Do not redesign, refactor, or make implementation suggestions unless you discover a
  genuine blocker.

Instead, stop and ask:

"I've finished reviewing the handoff and the codebase, and I'm fully caught up on the
project. What would you like to work on first?"

Wait for Scott's response before taking any further action.
