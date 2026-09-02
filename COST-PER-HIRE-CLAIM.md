# Cost-per-hire claim — documentation

**STATUS (25 Aug 2026): NOT currently on the site.** Scott reviewed the shipped
row twice and made the final call to leave cost per hire off the homepage table
("let's leave the cost per hire off"). This doc preserves the researched claim,
both framings, and the citation pattern for whenever a cost claim returns.

**Claim shipped on `employer-home.html`, "The Difference" table (25 Aug 2026,
article-aligned version):**

> Cost per hire — Traditional job board: "$5,475 US average, and climbing¹" ·
> JobFairX: "Under $200 in event spend on our 2025 healthcare events²"
> Sources line (anchored #cph-sources, superscripts jump to it, hover shows the
> source via title — LinkedIn-style citation marks, Scott's request):
> "1. SHRM 2025 Benchmarking Report, US average cost per hire, non-executive.
> 2. JobFairX 2025 platform data: 582 healthcare events, average 8 hires per
> employer per event. Details in our cost-per-hire guide." (links to
> /employer/resources/cost-per-hire)

## Why these numbers

The claim mirrors Scott's own published article,
**jobfairx.com/employer/resources/cost-per-hire** (byline Scott Lobenberg,
July 21 2026), on his instruction (25 Aug chat). The site tells one story:
homepage row → article → pricing page.

1. **$5,475** — US average cost per hire, non-executive, attributed by the
   article to SHRM's 2025 Benchmarking Report. Caveat: SHRM's public 2025 data
   brief publishes MEDIANS ($1,200 non-executive); the $5,475 average
   circulates via secondary sources citing the gated full report (Pin 2026).
   Plausible (2022: mean $4,683 vs median $1,244, a ~3.8x ratio), but not
   verified against SHRM primary. The homepage row therefore says "US average"
   and lets the numbered source line carry the attribution, same as the article.
2. **Under $200 per hire** — from the article's own math: top tier $1,495 flat
   ÷ 8 average hires per event ≈ $187, "before staff time." The 8-hires
   average: **582 healthcare hiring events in 2025, employers averaged 35
   scheduled interviews and 8 hires per event — confirmed by Scott as real
   platform data (25 Aug 2026 chat)**, published in the article as "JobFairX
   2025 Platform Data."

## Status change on the 35/8 stat — read this

The internal handoffs (HANDOFF.md §3, HANDOFF-3.md §13.7) treated
"35 interviews / 7-8 hires" as an unverified per-event figure and record it
being purged from marketing copy three times. **As of 25 Aug 2026 that ruling
is superseded for HEALTHCARE specifically:** Scott confirmed 35 interviews /
8 hires per employer per event is the real 2025 platform average across the
582 healthcare events. It is now restored as canon on:
- `page-solutions-healthcare.html` (metrics tiles: 35 and 8, "2025 platform data")
- `af-solutions-healthcare.html` (same tiles)
(The stat also appeared in the Difference table's source note while the cost
row was live; that note left the page with the row.)
Veterans/market-level figures (e.g. Portland 73/19) remain per-event numbers
and must still never be presented as type-wide.

## Appendix: the Appcast framing (researched 25 Aug, kept as backup)

An earlier version of the row used Appcast's measured job-board advertising
cost per hire — **$851, 2024 US data** (Appcast 2025 Recruitment Marketing
Benchmark Report; 2026 report says it "rose sharply" in 2025). Cross-check by
funnel arithmetic: ~$20 median cost per application × 40-42 applications per
hire (blended) = $780-$850; at job-board-specific conversion (Jobvite 2017:
184 apps/hire; CareerPlug 2024: 180) it rises to $3,500-$3,700. This is the
same-category (ad-spend-only) comparison and is the most defensible framing if
the SHRM-average version is ever challenged; swap back by reverting the row in
`build-employer-home.py` §8c.

## Attack surface, answered

- "$5,475 includes recruiter time; $200 doesn't." True; the row says "in event
  spend" and the article says "before staff time." Same category on our side,
  clearly labeled. If challenged hard, fall back to the Appcast framing
  (ad spend vs ad spend).
- "8 hires is cherry-picked healthcare." The row says "healthcare events"
  explicitly; healthcare is also the most expensive benchmark category
  ($9,000-$12,000 in the article), which is the fair comparison for the buyer
  the row targets.
- "Where does 15.6% conversion come from?" Separate row, Scott-supplied,
  definition still pending — do not conflate with this claim.

## Maintenance

- Keep the homepage row, the article, and the pricing page telling the same
  story; if the article's numbers change, change the row in
  `build-employer-home.py` §8c and this doc together.
- Re-verify the SHRM figure when the 2026 full report becomes accessible.
- The article still contains the OLD comparison table ("Interviews
  auto-scheduled", "Post and pray", "Passive applicants") — when the developer
  next touches it, apply the same row corrections as the homepage redesign.
- Researched 25 Aug 2026 (4-agent sourced sweep; SHRM 2022/2025 and Jobvite
  2017 primary PDFs fetched; Appcast via PR releases; article read same day).
