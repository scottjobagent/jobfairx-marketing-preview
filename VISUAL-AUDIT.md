# Visual Audit — Product Imagery & Motion Upgrade Plan

Written 17 Aug 2026. Scope per Scott's brief: **visuals only**. No layout, nav,
typography, color, section, or messaging changes. This document audits every product
visual on the 28-page site against the presentation standard set by
vfairs.com/event-management-platform/virtual-job-fair, and specifies upgrades that
stay inside our locked design system (HANDOFF §4) and vocabulary law (§2).

---

## Part A — What vFairs actually does (evidence, not impressions)

Method: rendered the page in the browser, then downloaded and decompiled all eight of
their product visuals. Findings are from the actual animation source files, not
eyeballing.

**A1. There is not a single raw screenshot on the page.** Every product visual is a
Lottie animation (~860×600, 12-second loop, 24–25fps) composed from 7–21 cropped UI
fragments, each a separate animated layer. Their "screenshots" are *rebuilt
compositions* — which is why they never read as screenshots.

**A2. The composition grammar** (recurring across all eight):

1. **Empty app chrome as a stage.** A blank product frame (nav bar + empty canvas)
   sits there first; content fragments fade in *inside it*, staggered, as if the app
   is coming to life.
2. **Entity storytelling.** The AI-matching visual is a candidate card + a recruiter
   card + a labeled "AI Job Match" pill + an animated connector line + an "81% Match"
   badge that pops between them. The mechanic is legible before you read a word.
3. **Simulated interaction.** A cursor layer *clicks* a row; the click opens a
   profile panel. The animation demonstrates the workflow, not just the screen.
4. **Narrative payoff.** A success toast ("Your application has been sent to…")
   lands as the final beat.
5. **Floating KPI chips.** Stat cards (Total Registrations · 201) hover *over* a
   table crop with their own shadows; toggles flip; bar-chart rows grow.
6. **Backdrops.** A faint 1920×1080 grid-with-accent-dots sheet under every
   composition, plus a soft accent radial bloom (879×879) behind the focal card.
7. **Flat-on, always.** Zero perspective tilt anywhere. Depth is entirely layering +
   soft shadow + overlap. (This independently confirms our no-3D-tilt rule.)

**A3. The motion grammar** (from keyframe data):

- Staggered opacity fades: each fragment fades in over ~0.7s, ~0.33s apart —
  *narrative* pacing, slower than UI-entrance pacing.
- Sequential build over ~5–8s, hold, loop.
- One scale-pop accent per composition (a badge), and in the hero one bounce-physics
  drop (spring expressions in the file).
- Hero layers enter in strict story order: stage → card → pill → connector → match
  badge → interview window. 0s → 5.4s.

**A4. What we do NOT adopt** (conflicts with locked, research-derived decisions):

| vFairs habit | Our rule | Our translation |
|---|---|---|
| Bounce/spring physics | No springs, no bounce (§4.9) | Scale 0.98→1 on `--e-out`; the pop reads without the wobble |
| Saturated accent bloom behind cards | Bloom capped ~15–16% alpha (§4.4) | Keep our existing glow discipline |
| Lottie runtime (~300KB JS + MB-scale JSON) | No dependencies, no build step (§5) | CSS keyframes + our existing rAF/IO patterns in motion.js; SVG stroke animation for connectors |
| Illustrated stock humans in UI | Real product only | Real crops + DOM-rebuilt fragments (the hero already does this) |
| 12s always-running loops everywhere | Motion supports, never distracts | Loops gated by IntersectionObserver, paused offscreen, `prefers-reduced-motion` lands on the final frame |

**The one-sentence diagnosis:** our site's *static* craft (shadow ladders, rim
lights, crops, annotated pins) is already at or above their level — but outside the
homepage hero, every product visual we ship is a **static crop in a panel**, while
every visual they ship is **alive**. The gap is motion and narrative, not polish.

---

## Part B — The JobFairX vignette system (build once, deploy everywhere)

The homepage hero already invented our answer: real screenshot as anchor plane +
razor-sharp DOM-rebuilt fragments (`.frag`) floating over it, with one deliberate
"alive" element (the Accept sheen). The upgrade path for the whole site is to
promote that technique into a small reusable library — six animated vignettes and
four static composition upgrades. All DOM+CSS+~150 lines added to motion.js; no new
dependencies.

### The six vignettes

**V1 — Request → Accept → Scheduled** (the signature; our "81% Match" equivalent)
A rebuilt interview-request card (fictional-name set from the capture harness:
Dana Whitfield, Amara Osei…). Beat 1: request card fades in ("Requested · today").
Beat 2: a focus ring lands on Accept; the button depresses. Beat 3: the state chip
flips to Scheduled with the time; a confirmation line appears under it ("Candidate
notified"). Hold, fade, loop (~10s). The entire product thesis — *accepting is the
scheduling step* — demonstrated in three beats with zero words read.
*Where:* candidate-pipeline hero flow strip, homepage "inversion" section,
interview-scheduling proof.

**V2 — AI matching, drawn as a diagram (not fake UI).** We have zero screenshots of
matching UI (HANDOFF §9 blocker) and we will not mock one. But vFairs' strongest
visual is entity storytelling, which doesn't need product UI at all: job card
("Registered Nurse · Dallas") left, three candidate fragments right, SVG connector
lines *drawing* (stroke-dashoffset) toward the job, a "Matched" chip landing on each
as its line completes — staggered. Styled in our tokens as an obvious *diagram*
(hairlines, mono labels), never chrome that could be mistaken for the app.
*Where:* platform overview "matching" section, solutions type pages (retinted per
audience), homepage step 03. *This also un-blocks the visual half of the
ai-matching story without violating the no-evidence rule.*

**V3 — Interview location selector.** The four options as rebuilt rows (JobFairX
video / Phone / In person / Your own link — the homepage `.frag--formats` card,
promoted to a vignette). A focus ring moves to "In person"; a street-address line
expands under it; beat 2 shows a candidate-confirmation fragment carrying that
address. Directly animates the launch message: *same event, your choice of room.*
*Where:* in-person-interviews hero, interview-locations page, homepage formats
section.

**V4 — Live event day / the queue.** Stage = `lobby-live.png` crop. Overlaid
DOM chips: a "waiting" candidate chip slides into the "in interview" room slot; a
session timer ticks; the queue count decrements. One motion at a time, slow.
*Where:* event-day capability page, event-detail "what event day looks like".

**V5 — Analytics that assemble.** Real `analytics.png` crop as the plane; two
rebuilt KPI chips float over it (per-event verified figures only, or `{{PLACEHOLDER}}`)
and count up on entry using the existing `data-count` machinery; one rebuilt bar row
grows to width. The count-up settle-guard already in motion.js applies as-is.
*Where:* analytics capability page, solutions pages' stat moments, post-event-report
sections.

**V6 — Messaging & automations timeline.** A vertical event timeline (registered →
matched → requested → reminder → post-event) where message bubbles fade in beside
each stage as a playhead line descends. Rebuilt from `messages.png` / `automations.png`
content, neutralized names only.
*Where:* messaging-automations capability page; a 2-beat variant for the
"reminders send on their own" line on the homepage.

### The four static upgrades (every page benefits, zero motion budget)

**S1 — Fragment-over-panel becomes the default proof composition.** Any `.proof__vis`
that today is a bare `.panel > .crop` gains one small overhanging DOM fragment
(a request card, a state chip, a location row) hanging 20–40% outside the panel edge,
`--sh-float` shadow, 2–6px parallax. One fragment, not three — restraint is the brand.

**S2 — Stage-build reveal for `.anno` centrepieces.** The annotated screenshot is our
best device; give it an entrance sequence: panel reveals first, then pins pop in
staggered (scale .6→1, 60ms apart, after a 300ms beat), then the key rows light once
each in order as a 1.5s "attract" pass, then settle to hover-driven. Screen-reader
and reduced-motion users get the current static behavior.

**S3 — Backdrop atmosphere for light sections.** Dark sections have glow + grid +
grain; light `--void` sections are flat fills. Add the light-theme twin of the hero
grid: 72px hairline grid at ~3% ink, radial-masked to fade at edges, behind
centrepiece figures only (not text columns). Direct translation of vFairs' grid+dot
sheet into our tokens.

**S4 — Living video placeholders.** The five `.video-ph` blocks are empty grey wells
today. Put a real screenshot crop behind each play button with an ultra-slow scale
drift (1.0→1.04 over 30s, alternating), dimmed 40%, grain on top. Reads as a paused
film, not a missing asset. Reduced-motion: static frame.

### Motion constitution for all of the above

- Entrances `--e-out`, hovers `--e-inout`; **no springs** — vignette pops are
  scale .98→1.
- Vignette internal pacing ~2.5s per beat, 8–12s loop, ≤3 beats; only ONE vignette
  playing per viewport (IntersectionObserver gates start; pause offscreen).
- Split-clock rule applies inside vignettes: opacity fast/linear, transform long/expo.
- Every loop's final state == a complete, truthful screen; `prefers-reduced-motion`
  and script-failure both land there (same reveal-default philosophy as base.css).
- Nothing in a vignette invents data: verified facts or the fictional-name set;
  anything else ships as `{{PLACEHOLDER}}`.
- Vocabulary law applies to rebuilt UI text: request/accept/schedule, never
  apply/application (vFairs' own copy says "application" — theirs, not ours).

---

## Part C — Section-by-section audit

Grouped by template family; every visual on all 28 pages is covered by one of these
entries.

### C1. Homepage (concept-3-hybrid.html)

| # | Section | Today | Verdict & upgrade |
|---|---|---|---|
| 1 | Hero stage + 2 frags | Best visual on the site. Static frags, parallax, Accept sheen. | **Keep composition; add the narrative.** Run V1 inside `.frag--request`: after 2s, focus ring → Accept press → "Scheduled ✓ Candidate notified" chip; hold 4s; reset. The sheen already primes exactly this. Consider a third micro-frag (tiny "91% show rate" stat chip, top-left, deep parallax) only if it doesn't crowd 980px. |
| 2 | Logo/proof row + stat band | Text-only proof items; count-up works. | Fine as is (names > grey logos until real logo files land — HANDOFF open question). Atmosphere: S3 grid behind the band. |
| 3 | In-person launch (`#inperson`) | Static dashboard-events crop — strongest proof asset, presented flat. | **S1 + V3 hybrid:** keep the INTERVIEW LOCATION column crop as anchor; overhang a rebuilt "In person — 2200 Ross Ave…" row fragment that swaps its location value every 4s (video call → your address → Microsoft Teams), proving "four side by side" without the reader parsing the table. |
| 4 | Event types ×5 | Icon cards, hover lift. | Adequate. Optional: 400ms accent tick on icon at reveal. Low priority. |
| 5 | The inversion (compare lists + candidates.png wide crop) | Copy carries it; crop is static. | **V1's home.** Replace the static wide crop's dead weight: same crop, but the Requested-row region gets the focus-ring → Accept → state-flip overlay, positioned like anno pins. The "old way" column could de-saturate as the "JobFairX way" column reveals — one subtle beat, not a show. |
| 6 | Interview formats tabs | Four panes, static crops, pane swap is display:none toggle. | Add a 200ms crossfade+4px slide on pane switch (motion.js initTabs). In-person pane: V3 lite — address line draws on after pane opens. |
| 7 | Journey (7 steps, sticky visual) | Already our second-best pattern; shots crossfade. | Per-step overlay fragments: step 4 (requests) shows the request-card frag; step 5 the Accept ring; step 7 a report KPI chip counting. Reuses V1/V5 pieces at 30% scale. |
| 8 | Capability grid ×6 crops | Static thumbnails. | Hover: crop `--z` eases +6% (zoom-into-story, not lift). 150ms. Cheap, page-wide payoff. |
| 9 | Stats / results / pricing | Typographic; tier cards. | No image work needed. Featured tier gets S3 backdrop. |
| 10 | 3 video placeholders | Empty grey wells. | **S4.** Posters: lobby-live (how it works), interview-screen (event day), dashboard-events (locations). |

### C2. Capability pages ×6 (candidate-pipeline is reference)

Slot-by-slot, applies to all six with the page-matched vignette:

- **`.cap-hero` flow strip** — today three static text beats. Make the strip the
  vignette stage: the three `<li>`s light in sequence with a moving hairline
  underline (2.5s/beat, loop), and the page's vignette plays its 3 beats in sync in
  a right-hand mini-stage where width allows. Per page: pipeline→V1, scheduling→V1
  (calendar-landing variant), events-dashboard→V3, event-day→V4, analytics→V5,
  messaging→V6.
- **`.anno` centrepiece** — S2 stage-build + attract pass. The pin/caption pairing
  is already better than anything vFairs has; motion makes it discoverable.
- **`.proof` figures** — S1 fragment-over-panel on every static one. The band crop
  in pipeline's "one click accepts" proof gets the V1 focus-ring overlay on the real
  Accept button pixels (coordinates derived the same way as anno pins — recompute,
  never eyeball, per the reference page's own warning).
- **`.shotgap` placeholders** (auto-accept setting; interviews-Pending tab) — stay
  honest gaps. But upgrade presentation: keep the dashed frame, add the S3 grid
  behind and a mono caption; a *diagram* (V2-style, clearly not UI) may sit inside
  the gap where the mechanic allows (auto-accept: two rebuilt toggle states side by
  side, labeled "illustration — capture pending").
- **`.ctaband` facts** — count-up already there; add a 1px accent rule that draws
  across the facts column on entry (600ms).

### C3. Solutions hub + 5 type pages

- Hero: type-tinted glow already present. Add S3 grid; V2 (matching diagram) with
  audience-specific job titles from verified live copy (e.g., "Registered Nurse" on
  healthcare) as the hero-adjacent visual where the template has a stage slot.
- Show-rate stats (91/89/86 where they exist): V5 treatment — chip pops then counts.
  Diversity/Technology have NO published stats (HANDOFF §3): no invented chips, no
  vignette numbers; those pages lean on V2 + S1 instead.
- Testimonial `.credit` lines: keep quiet, no cards, no motion (deliberate).
- Technology page has no logo wall on purpose — do not let a vignette imply one.

### C4. In-person-interviews + interview-locations

The launch pages; highest visual stakes.
- in-person hero: **V3 full version** as the hero visual, anchored on the
  dashboard-events crop (Atlanta-address-corrected asset). The 20-mile fact gets a
  micro-visual: a rebuilt map-pin chip + "verified ≤ ~20 miles" mono label — a chip,
  not a map (no map data exists; a fake map is an invented artifact).
- interview-locations: the four-way comparison is the page. Rebuild the four
  dashboard rows as DOM (S1 style), each row's location value cycling through its
  verbatim dashboard string. Static crops remain as proof-of-real below.
- Pricing parity placeholder stays visible — no vignette may imply verified pricing.

### C5. Events + event-detail

- Events calendar: functional UI, not imagery — leave the table alone. Row hover:
  2px translate + type-color left rule (their product-canonical colors). The empty
  state could take a miniature S3 grid.
- Event-detail: the five-state banner switcher is REVIEW-ONLY tooling — exclude from
  any motion work. The countdown/pricing states must never animate in a way that
  implies a state it isn't in. Trust-metric chips ("Updated daily") get count-up
  only, values stay server-truth per HANDOFF. Video placeholder → S4.

### C6. Pricing

- Tier cards + stepper are interaction, already good. Two additions: the bundle
  total recomputation gets a 150ms number crossfade (no slot-machine), and the
  "scheduled interviews" line — Scott's strongest line — gets one accent underline
  draw on reveal, all three tiers staggered.

### C7. Demo, contact, FAQ

- Demo: the form is the product here. One S1 composition beside it: request-card
  frag + "20+ / 60+ / 100+" chip. FAQ 20-mile headline moment: the V3 map-pin chip.
  Contact: no product visuals; leave.

### C8. About, security, resources, legal

- About: single anno figure — S2 only.
- Security: placeholder honesty is the design; S3 backdrop, nothing else. Never
  decorate "{{SOC 2 — not yet certified}}".
- Resources: article cards get the capability-grid hover (C1#8). Legal: no motion.
- city-hub template: inherits C1#3 + C5 patterns; anything animated must come from
  template variables, not hardcoded Dallas examples.

---

## Part D — Implementation notes (for the build pass, when approved)

1. **Architecture:** one new `shared/vignettes.css` (keyframes + fragment styles) and
   ~150 lines in motion.js (`initVignettes`: IO-gated timeline stepper — an array of
   [delay, className] beats per vignette, driven by one rAF clock, settle-guarded
   like initCounters). No per-page JS beyond data-attributes:
   `data-vignette="request-accept"` etc.
2. **Fragments are DOM, not images** — same reason as the hero: sharp at retina,
   theme-aware, animatable, and they sidestep white-hole-on-dark entirely.
3. **Perf:** transform/opacity only; one playing vignette per viewport;
   `content-visibility` untouched; zero new network requests.
4. **A11y:** vignettes are `aria-hidden` decorative *duplicates* of adjacent real
   copy; reduced-motion lands on final beat; no information exists only mid-animation.
5. **Screenshot hygiene:** any new crops re-run the full neutralization list
   (HANDOFF §7); no new captures needed for V1–V6 as specced.
6. **Invariant checks after the build pass:** footer hashes, one-h1, 390px overflow
   (mcheck.py), vocabulary sweep, placeholder grep — per HANDOFF §10.
7. **Suggested order:** V1 + S1 + S2 (80% of perceived lift) → V3 (launch pages) →
   S3/S4 → V5/V6/V4 → C1 micro-polish. Each step ships independently.

## Part E — Open items for Scott

- V2 shows *diagrammatic* AI matching (clearly not app UI). Comfortable with that
  on solutions/platform pages while the real matching UI has no screenshot?
- S4 needs nothing new, but real video embeds would beat living posters — any ETA on
  the five videos changes S4's priority.
- vFairs animates *everything*; we deliberately won't. If you want one more
  "alive" moment than specced, say where, and we'll trade something out — the budget
  is one motion focus per viewport, non-negotiable, or we become the thing the
  teardown rejected.
