# Landing Page Audit — how many pages do we need?

Audited 17 Aug 2026 across six parallel workstreams (product features, solutions,
competitive IA, programmatic SEO, trust/company, content), then reconciled.

---

## The answer

| | Count |
|---|---|
| **Hand-built pages** | **26** — phased 10 / 11 / 5 |
| **Templates to design** | **16** — 4 existing reskinned + 12 new. *This is the real workload number.* |
| Template-generated instances | ~2,675 — **down from 3,873 today** |
| Total hand-authored surface after Wave 3 | ~44 (26 new + 6 built + 12 live articles) |

**The SEO layer should shrink, not grow — a net −1,198 pages.** That is the audit's most
counter-intuitive conclusion and the evidence behind it is strong (below).

Benchmark: Radancy 76 pages · Ashby ~40 core · Premier Virtual 29. We land in range and
under Ashby's discipline line.

---

## Verified findings

I checked the claims that carried the most weight rather than taking them on trust.

| Claim | Result |
|---|---|
| 98 dead `href="#"` links across the 6 built pages | ✅ **Exactly 98** (17 home / 25 events / 11 event-detail / 15 pricing / 15 FAQ / 15 contact) |
| We have 15 product screenshots | ❌ **14.** `interviews.png` and `interviews-pending.png` are byte-identical (md5 `8422e5f2…`). The Pending (18) tab was never captured. |
| `/employer/job-fairs/{state}` is broken | ✅ **Hard 500.** `/employer/job-fairs/texas` errors. |
| There is no employer city hub | ✅ `/employer/job-fairs/texas/dallas` **301s** to `hiring-event-calendar/?searchText=Dallas%2C%20TX` — a filtered list, not a page. **1,760 city×type pages point up at nothing.** |
| A `next-inperson` page family exists | ✅ **500s — and must stay that way.** It would manufacture a sixth pseudo event type and contradict the interview-location model. |

---

## Wave 1 — Coherence (10 pages + 3 rewrites) · P0

**Test: zero dead links anywhere.** There are 98 today; this wave closes every one.

`/employer/demo` · `/employer/platform` (hub) · `/employer/interview-locations` ·
`/employer/in-person-interviews` · `/employer/platform/candidate-pipeline` ·
`/employer/security` · `/employer/privacy-policy` · `/employer/terms-and-conditions` ·
`/employer/resources` (index) · `/employer/about-us`

**Build the annotated-screenshot component FIRST.** Six capability pages and both
interview-location pages depend on it, and a 3200×2000 dashboard shot is illegible at
page width without numbered pins. It's a component, not a page, and it blocks the wave.

**Three live articles are factually wrong the day in-person launched** — correctness
bugs, not content projects. Rewrite in place, do not redirect:
`virtual-vs-in-person-hiring-event` (our highest-intent in-person URL, currently arguing
*against* the thing we just shipped), `virtual-hiring-events` (the pillar — "No Zoom, no
external links, no downloads"), `how-does-a-virtual-job-fair-work`.

**Nav must change in this wave or the plan orphans itself.** Current: Upcoming Hiring
Events · Pricing · FAQ · Contact. Target: **Platform · Solutions · Events · Pricing ·
Resources** — five items, the benchmark median across nine competitors.

## Wave 2 — Traffic (11 hand-built + 7 template-filled + 357 generated) · P1

Five capability pages (`events-dashboard`, `interview-scheduling`, `event-day`,
`analytics`, `messaging-and-automations`), five solution pages (one per event type,
healthcare hand-built as the reference), plus `/employer/job-fairs/{state}/{city}` ×352
and `/job-fairs-near-me/{type}` ×5.

**The cheapest win in the entire audit isn't a page.** All ten live resources articles
CTA to the events calendar. Zero link to pricing. Zero link to bundles. Re-pointing
`high-volume-hiring` at `/employer/hiring-event-bundles` is a one-line change.

## Wave 3 — Enterprise close (3 shippable, 2 blocked) · P2

`/employer/ai-hiring-compliance` · `/employer/dpa` · `/employer/accessibility`.
These don't lose deals loudly, they stall them silently. **9 of 9 benchmarked
competitors have a security page** — more universal than a pricing page — and we
dead-link ours today.

Blocked: `/employer/customer-stories` (no written permission from Target or Tesla) and
`/employer/platform/ai-matching` (**no visual evidence AI matching has a UI at all**).

---

## Do not build

The audit was asked to be ruthless. The strongest calls:

- **Four separate interview-location pages.** Phone, video and your-own-link have no
  independent search demand, all four would share the one screenshot, and splitting them
  invites exactly the "in-person events" misreading we just corrected. **One page.**
- **More city×type pages.** Dallas Healthcare and Omaha Healthcare are **95.8% identical**
  — and so are Dallas (pop 1.3M) and Abbeville, Alabama (pop ~2,600). The instinct is to
  expand the SEO engine; the data says prune it to ~900 per audience.
- **Title × city pages.** 704 titles × 352 cities = **247,808 URLs** — the classic
  programmatic death spiral, repeating a 95.8%-duplicate failure at 140× scale.
- **A blog.** 12 articles already live at `/employer/resources`. A second content system
  splits authority against itself. Point the dead footer "Blog" link there.
- **Careers.** No openings exist. Deleting the link is the honest fix; an empty careers
  page is worse than none.
- **Three case-study pages.** Three customers, one sentence each, no sign-off. Build the
  index only.
- Also cut: company-size pages, persona pages, integrations, glossary, webinar library,
  press page, status page, help centre, a standalone job-postings page, a second
  cost-per-hire calculator.

---

## Gaps that block work — get these before building

1. **No in-person interview screenshots exist.** All 14 shots show the *setting*, never a
   room. The flagship launch page has no hero asset.
2. **A data defect sits in the exact crop the in-person page wants.**
   `dashboard-events.png` shows *"Atlanta Diversity Event"* with the interview address
   *"2200 Ross Ave, Suite 400 · Dallas, TX"*. An Atlanta event with a Dallas address —
   we cannot ship that as the hero of the launch.
3. **Metric contradiction that someone will screenshot.** `analytics.png` shows
   **"Attendance rate 66%"** against a marketing claim of **91% show rate** "based on
   2025 platform data". Both are on our own property.
4. **Likely production PII in shipped assets.** `messages.png` / `messages-thread.png`
   appear to contain six real candidate names, an employer, and a recruiter's first name.
   `messages-thread.png` **is already live on the homepage.**
5. **Fabricated logo walls on 2 of 5 type pages**, and unverified "has attended"
   attendance claims naming CVS, Kaiser Permanente, HCA, Mayo Clinic, Cleveland Clinic,
   JPMorgan Chase on the other four.
6. **No refund or cancellation policy exists anywhere** — while selling 100-event bundles
   at $29,700 with credits advertised as "never expire".
7. Unconfirmed: in-person pricing parity, SOC 2 status, per-type stats for 4 of 5 types.

---

## Programmatic hygiene — cheap, do it in the same pass

- Kill 8 non-city slugs (`united-states/national`, `western/eastern/central-region`,
  `inland-empire`, `orange-county`).
- Fix the slug split: `texas/sugarland` on event pages vs `texas/sugar-land` on near-me —
  it splits link equity between two URLs for one city.
- Remove the stale hardcoded testimonial date "Apr 22, 2026" rendering on **every**
  employer event page.
- Add meta robots. Today all 3,906 sitemap URLs *plus* ~12,068 unlisted `/{id}` pages are
  indexable by default.

> **Sequencing constraint that cuts across every wave:** never ship the "Virtual"
> title-tag rewrite across 3,520 pages in the same pass as the city consolidation. Two
> simultaneous site-wide changes make the traffic data uninterpretable and you lose the
> ability to tell which one worked.
