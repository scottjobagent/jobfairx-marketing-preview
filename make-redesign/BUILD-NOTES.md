# Build notes for Brandon: employer marketing pages, Waves 1 to 3 (9 Oct 2026)

These are design references, not production code. Open `index.html` first: it carries the inventory, the per-page change list and the flags. Each preview is a standalone HTML file with the CSS inline and shared assets in `assets/`.

## What the files are

| File | Roadmap row | What it shows |
|---|---|---|
| `employers-hub.html` | S-005, Wave 1, modify | The employer home, restyled. Live: `/employer`. |
| `employers-pricing.html` | S-006, Wave 1, create | Pricing on its own page. Live today: `/employer/hiring-event-pricing`. |
| `employers-host-a-hiring-event.html` | S-007, Wave 1, create | Human-written page skeleton; amber boxes are writer sections. |
| `employers-virtual-hiring-events.html` | S-008, Wave 1, create | Video-interview feature page. Copy says "video", the URL is Michael's. |
| `hire-city.html` | H-rows, Waves 1 to 3, create | Programmatic employer city page (Workstream C spec). Houston example values. |
| `hire-city-vertical.html` | V-rows, Waves 2 and 3, create | Same template narrowed to one vertical. No spec yet; do not build from it. |
| `employers-vertical-healthcare.html` | S-009 to S-015, Waves 2 and 3 | Vertical landing template, shown on healthcare. |
| `employers-guide-template.html` | S-016 to S-032, ST-001 to ST-010 | Editorial shell for comparisons, guides and state guides. |

## Design system (matches the Tampa Technology redesign where it overlaps)

- Font: Inter only, loaded from Google Fonts in the previews; the live site self-hosts it.
- Container: max-width 1280px, 32px sides from 1024px, 24px below. Sections 90px top and bottom (48px under 768px, 72px between).
- Type: H1 52px / 600 / line-height 1 / -0.03em (30px, 500 under 1024px). H2 36px / 600 / -0.02em (26px under 1024px). Eyebrow 14px bold capitals, .12em tracking, brand blue (12px on phones). Body 16px, lead 19px (17px on phones).
- Colours: brand blue `#0044B3` for primary buttons on light backgrounds, eyebrows, links and the gradient tiles (with `#2563EB` as the gradient end and supporting UI blue only). Navy `#00245B` for the hero gradient (to `#001640`), dark bands and footer. Light grey `#F8FAFC` alternate sections with 1px `#E2E8F0` lines. Ink `#0F172A`, `#334155`, `#475569`, `#64748B`. On navy: `#FFFFFF`, `#C9D6EA`, `#93C5FD`.
- Buttons: 48px pills, 600 weight, 15px. Primary on light = brand blue fill. Primary on navy = white fill with brand-blue text. Secondary = 1px `#CBD5E1` border on light, 45% white border on navy.
- Cards: white, 1px `#E2E8F0`, 16px radius, 28px padding. One depth mechanism (hairline), shadows only on product screenshots and the hero panel.
- Gradient icon tiles: 48px, 12px radius, 135deg `#0044B3` to `#2563EB`, white 22px stroke icon.
- Motion (Scott lifted the August no-motion rule for the employer site on 9 Oct): sections, cards and steps fade up 18px over 0.6s as they enter the viewport, with a 90ms stagger inside grids (IntersectionObserver; everything is visible without JavaScript). The hub's logo strip is a 48s linear marquee that pauses on hover. Hover colour changes and a 3px arrow nudge on links. `prefers-reduced-motion: reduce` disables all of it and shows the logo strip as a static wrapped row.

## The Interview settings panel (hero component)

A CSS mock of the product's event setup, in the product's own words:

- "How do you want to interview candidates? *" with "This applies to every interview scheduled for this event." Segmented control: Video, In-Person, Phone. Each option shows its own note: JobFairX video call (no software, secure link on confirmation); Interview address (candidates see it on their confirmation and reminders); You call each candidate (number on the confirmed interview, call at the start time).
- "Interview time slot duration" with "Choose how often candidates can schedule an interview." Options 15 minutes and 30 minutes. Hint: 15 suits screening, 30 suits full interviews. Never present 15 minutes as more interviews; interviews per slot is a separate control.
- "Do you want panel interviews for all interviews?" switch, with the line from the product's edit page. The switch is disabled, with the note "Panel interviews are available on video interviews on JobFairX.", whenever In-Person or Phone is selected. Panel interviews are video on JobFairX only.
- The preview's 30-line script wires the segmented controls and the switch. A `#fmt=person` or `#fmt=phone` hash preselects a format for review; drop that hook in production.

## Links and forms

- Header and footer are the live site's links (calendar, pricing, FAQ, contact, sign-in, bundles, resources, about, job-seeker links, privacy, terms). Keep the live chrome.
- Every CTA points at a working live URL: the calendar for registration, the live pricing page, the live contact page, and the calendar `?filter=` views for event types. New pages are designed under the live singular stem `/employer/...` (Michael's sheet writes `/employers/...`; Scott treats that as a typo, Michael to confirm, see flag 1 in `index.html`). Those new URLs appear only in each preview's review bar, canonical and the guide template's related links.
- The `/hire/{city}` enquiry form has the six Workstream C fields plus "Which positions are you looking to fill?", city and state prefilled from the page. It posts nowhere yet; the spec's endpoint does not exist.
- The amber dashed boxes are placeholders for writer copy or data gates and never ship.

## Data rules on `/hire/{city}` (from Workstream C)

Heading and reach line show the candidate count only at 250 or more registered candidates in the metro, and the employer half only at 3 or more employers on the next event; below either floor the number is dropped, never shown as zero. Proof shows three local logos only with permission, else three national logos not labelled as local. Price is always "From $495 for a single event. No subscription." Event rows come from the live feed.

## Not done here

No pages for the job-seeker city templates (S-001, S-002, S-004, A-rows), no repair of the existing employer event pages (S-003), no changes to registration or scheduling behaviour, no deployment.
