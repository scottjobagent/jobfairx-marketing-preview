# Seeker home page — developer notes

**Built:** 30 Aug 2026 · **Output:** `seeker-home.html` · **Source of truth:** `build-seeker-home.py`
**Clone of:** `https://jobfairx.com/` (the job seeker home page — note the root is the SEEKER page; `/employer` is the employer one)

**Edit the builder, never the output.** `seeker-home.html` is generated. Every substitution asserts
its match count and the build aborts on drift, so a change to the live page fails loudly instead of
silently shipping stale copy. 47 assertions pass today.

---

## What this page is

Chrome is cloned byte-identical from the live capture: `<head>`, nav, footer, the city link farm and
the mobile search block. The body argument is **authored**, because the live one teaches a product
model that no longer exists.

The employer home page was used as the **design** reference only — layout, section rhythm, the
alternating image/text rows, the component vocabulary. None of its messaging carries over; a
recruiter deciding to spend $495 and a job seeker deciding to spend an afternoon are different
readers. All content comes from the shipped seeker application.

## The SEO contract, enforced by the build

Asserted **frozen**: `<title>`, canonical, `og:title`, `twitter:title`, `og:image`, `fo-verify`, the
GA4 id, `alt="Customer Logos"` (×2), the single `<h1>`, and all 349 live city-farm hrefs.

**Changed, deliberately:**

| Surface | Why |
|---|---|
| `<h1>` → `Skip the Applications.` / `Get a Confirmed Interview Time.` | Measured: the old H1 contained "job fair" zero times and no city token, so it carried no query language. "Get Invited to Interview" also reversed the mechanic — candidates request, employers accept. |
| meta + og + twitter description | The live string said "Attend" (implies a venue), "top employers" (unsourced), "get hired" (an outcome nobody can promise). Descriptions are a click-through surface, not a ranking one. |
| `<p>` → `<h2>` on *Companies That Hire on JobFairX* and *Job Fairs Near Me* | Strings byte-identical; both already read as headings. |
| Florida / New York duplicate state `<h2>`s → `<p>` | Column-split artifacts. Zero hrefs touched. |

**Added, nothing removed:** FAQPage JSON-LD with four Q&A (the page had none); server-rendered FAQ
answers (today the live page serves four questions and **no answers at all**); the three Wisconsin
city links, which de-orphan three sitemap pages; a second link to `/job-fairs-near-me`, which
receives exactly one inbound link from this page today; real start times on the event cards, from a
payload field the live page already fetches and discards.

**Event card hrefs repointed** from the dated `/job-fairs/{state}/{city}/{id}` to the evergreen
`/job-fairs/{state}/{city}/next-{type}` each of those URLs already canonicalises to. The dated URLs
are not in the sitemap, so five of the domain root's links were being spent on redirect-equivalents.

## Two live-site defects this page fixes

1. **No background.** Neither `<html>` nor `<body>` paints one on jobfairx.com — both compute to
   `rgba(0,0,0,0)` and there is no `color-scheme` meta. A browser in dark mode therefore renders the
   whole seeker site dark-on-dark. Fixed here with `html{background:#fff;color-scheme:light}`.
   **Apply this to the live site.**
2. **The city farm is `hidden lg:block`.** All 349 links are in the served HTML at every width, but
   invisible below the large breakpoint, so a phone user's entire browse surface is one search box.
   Un-hidden here; no href, anchor string or node was removed, so nothing changes for a crawler.

## Build rules that bite

- **New markup must not use bare Tailwind utilities.** The live CSS is purged. `bg-green-50` and
  `bg-purple-50` were tried for the Healthcare and Entry-Level chips and rendered unstyled; the live
  site uses **teal** for Healthcare and **sky** for Entry-Level, and those classes do survive.
  Everything else authored here lives in one scoped `<style id="sk-style">` with `.sk-*` classes.
- **Mobile must be probed with `tools/mcheck.py`.** A plain headless `--window-size=390` run is a
  lie — Chrome clamps to 500px. `mcheck` loads the page in a true 390px iframe. Current result: ok.
- The builder also guards: zero occurrences of "virtual" outside the permitted `virtual.jobfairx.com`
  host, zero banned copy strings, zero motion classes, zero em dashes in any heading, exactly one
  `<h1>`, and exactly 352 city links.

## Outstanding

- **Six product screenshots are pending** and render as visible placeholders. Nothing is faked — mock
  UI is banned and the seeker app has zero marketing captures today. The capture pass needs a
  neutralisation list first: the prototype carries a real employer brand and named recruiters, and
  candidates never see recruiter names.
- **Two shots are blocked outright**, not merely pending: any crop of the in-person dashboard card
  would publish the literal strings `[PLACEHOLDER — arrival instructions]` and `[PLACEHOLDER — parking]`.
  Those need real values from Scott.
- **Escalated, deliberately not shipped:** the platform stat tiles (4,000+ / 500K+ / 300+). They are
  live on `/job-fairs-near-me`, but inside its *For Employers* block, so moving them into a seeker
  section is a new claim in a new context — and platform totals must be attributed as video-event
  totals, never implying in-person volume.
- **The matching-status chip is held.** The field carries only `live` and `soon` across the estate;
  `early` never appears and its sibling `earlySavings` is employer pricing leaking onto a seeker
  page. Rendering `live` as "Matching open" would be an unverified product claim on the domain root.
- **`VirtualLocation` / `OnlineEventAttendanceMode`** survive in Event JSON-LD across roughly 5,270
  seeker pages. Wrong about the product; the SEO upside of replacing it is unproven, because Google's
  Event documentation describes neither the current markup nor the obvious replacement. Stage on one
  small family and measure. Not part of this page.
