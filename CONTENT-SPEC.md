# JobFairX Employer Homepage — Content Spec

Shared across all three concepts. The concepts differ in **visual language**, not in
what they say or which product surface they show. That is deliberate: it makes the
three genuinely comparable, and it means the winning concept already has its copy.

---

## Non-negotiable vocabulary

The product has a specific, unusual mechanic. The copy must not blur it into
generic ATS language, because the mechanic *is* the differentiator.

| Say this | Never say this |
|---|---|
| Candidates **request** interviews | Candidates apply / submit applications |
| You **accept** a request → it **schedules** the interview | You review applications |
| **Hiring event** | Job fair booth, career fair |
| **Interview formats**: JobFairX video, phone, in person, your own link | Virtual booth, chat room |
| **Matched** candidates | Resume database, sourcing pool |

The single sentence the homepage exists to land:

> **Candidates come to you already matched, already interested, and already asking
> for an interview — you just say yes.**

That is the inversion. Everything else is support.

---

## Section-by-section

### 1. Navigation
Sticky, shrinks on scroll. Left: wordmark. Center: Platform · Solutions · How it works ·
Pricing · Resources. Right: `Sign in` (ghost) + `Book a demo` (primary).

Mobile: wordmark + hamburger → full-screen overlay panel.

### 2. Hero — full viewport

- **Eyebrow:** `AI-matched hiring events`
- **H1:** `Hiring events that fill themselves.`
- **Sub:** `JobFairX matches qualified candidates to your open roles, and they request
  the interview. Accept, and it's on your calendar. Run it by video, phone, or in person.`
- **Primary CTA:** `Book a demo` · **Secondary CTA:** `See how it works` (scrolls, does not leave)
- **Trust line under CTAs:** `No job board noise · No resume mining · You only meet people who asked to meet you`
- **Product visual:** the live event lobby (`lobby-live.png`) as the anchor plane, with two
  extracted fragments floating in front at different parallax rates:
  - a **candidate request card** (Accept / Decline / Reschedule)
  - an **interview format chip cluster** (Video · Phone · In person)

### 3. Social proof strip
Logo wall, grayscale at 55% opacity → full opacity on hover. Above it, one quiet line:
`Hiring teams running events on JobFairX`.

> ⚠️ **Placeholder.** Real customer logos are not in this file. The concepts ship with
> neutral wordmark placeholders that are obviously placeholders. Do not publish with these.

Stat bar beneath — **all four numbers are placeholders pending real data**:
`{{X}} interviews scheduled · {{X}} avg. requests per event · {{X}}% show rate · {{X}} days to first hire`

### 4. The inversion (why we're different) — the emotional core
Split layout. Left: the old way as a short, dry list. Right: the JobFairX way.
Product visual: `candidates.png` cropped tight to the Requested rows.

- **H2:** `You've been doing the chasing. Stop.`
- Old way: post a job → wait → sift 400 resumes → chase for a callback → half ghost you.
- New way: register for an event → post roles → AI matches → **they** request → you accept.

### 5. Four ways to interview — visual, not textual
Four-panel interactive row. Each panel: icon, format name, one line, and a
cropped product fragment showing that format's badge in the real UI.

| Format | Line |
|---|---|
| **JobFairX video** | Built-in video room. Nothing to install, for you or the candidate. |
| **Phone** | You call each candidate at the scheduled time. Numbers are in the dashboard. |
| **In person** | Share an address. Candidates see it on their confirmation. |
| **Your own link** | Zoom, Teams, Meet — paste your link and we schedule around it. |

Source screenshot: `dashboard-events.png` INTERVIEW LOCATION column already shows
Video / Phone / In person side by side. `interviews.png` shows all formats mixed in one
schedule. This is the strongest proof we have and it is real, not mocked.

### 6. How it works — the 7-step journey
Sticky-scroll narrative: the step list pins while the product visual swaps beside it.
On mobile it degrades to a vertical timeline with the visual under each step.

1. **Register for an event** — or host your own branded one. → `setup-flow.png`
2. **Post your open jobs** — title, location, format. → `edit-post.png`
3. **AI matches qualified candidates** — against your roles, not keywords. → `candidates.png`
4. **Candidates request interviews** — they come to you. → `candidates.png` (Requested crop)
5. **You accept** — one click schedules it. → `candidates.png` (Accept button crop)
6. **Interview your way** — video, phone, in person, your link. → `lobby-live.png`
7. **Keep hiring after the event** — messaging and automations stay on. → `automations.png`

### 7. AI candidate matching — deeper dive + video placeholder
- **H2:** `Matching that understands the role, not just the keywords.`
- Video placeholder: **"AI Candidate Matching"** (16:9, elegant, obviously intentional)
- Supporting product visual: `candidate-preview.png` (the resume view)

### 8. Platform capabilities — feature grid
Six cards, each with a real cropped product visual, not an icon:
Dashboard & events · Candidate pipeline · Interview scheduling · Messaging ·
Automations · Analytics & reporting

Screenshots: `dashboard-events` · `candidates` · `interviews` · `messages-thread` ·
`automations` · `analytics`

### 9. "See JobFairX in Action" — primary video section
Large 16:9 placeholder, centered, ambient glow. Chapter chips underneath that will
become video timestamps: `Overview` `Setting up an event` `Matching` `Interview day` `Reporting`

### 10. Customer results
Three result cards + one featured story with a **video placeholder** ("Employer success story").

> ⚠️ **Placeholder.** No real customer names, quotes, or metrics exist in the source
> material. Every figure and quote in this section is `{{PLACEHOLDER}}` and styled to
> read as unfinished. Do not publish until real, approved customer data replaces them.

### 11. Pricing preview
Three tiers referencing the real package names visible in the product
(**Starter / Growth / Pro** — from the setup flow's package toggle and
"Starter · 1 of 2 interviewer seats used" in the lobby).

Show what scales: interviewer seats, jobs per event, events. **Prices are `{{PLACEHOLDER}}`** —
actual figures are not in the source material. CTA: `Talk to sales`.

### 12. Final CTA
Full-bleed, cinematic. `Your next hire is already looking for you.`
Primary `Book a demo` · secondary `Browse upcoming events`.

### 13. Footer
Oversized wordmark, four link columns (Platform · Solutions · Company · Legal),
region/social row. Trust badges: SOC 2 / EEOC / data handling — **placeholders**,
pending confirmation of what JobFairX actually holds.

---

## Video placeholder inventory

| ID | Section | Ratio |
|---|---|---|
| `video-overview` | Hero secondary / §9 | 16:9 |
| `video-walkthrough` | §9 chapter: Setting up an event | 16:9 |
| `video-matching` | §7 AI Candidate Matching | 16:9 |
| `video-story` | §10 Customer results | 16:9 |
| `video-action` | §9 "See JobFairX in Action" | 16:9 |

All five are one component (`.video-ph`) with a poster slot, a play affordance, a
duration chip, and a caption. Swapping in production = replacing the inner markup with
`<video>` or an embed. Nothing else changes.

---

## Update — real data sourced from jobfairx.com/employer

Concept 3 no longer runs on placeholders. Everything below is now live in
`concept-3-hybrid.html`, taken verbatim from the production employer page:

| Data | Value |
|---|---|
| Platform totals | 4,000+ employers · 500,000+ interviews conducted · 300+ cities · 3M+ registered candidates |
| Pricing | Starter **$495** · Growth **$895** · Pro **$1,495**, per event |
| Volume commitment | 20+ / 60+ / 100+ scheduled candidate interviews — promoted to the emphasised line on each tier, because it is a commitment rather than a feature |
| Event types | Healthcare · Diversity · Veteran · Technology · Entry-level |
| Markets | 300+ cities; Dallas, Nashville, Boston, Norfolk, Miami, Denver, Seattle, Chicago, Austin, New York named |
| Customers | Target · Tesla · Western Regional Medical Center, each with its own outcome |

**In-person is the launch story.** It was added to the product after the live
marketing site was written — which is why jobfairx.com still says "Virtual Hiring
Event Platform" and rules out alternatives. The announcement bar, a hero badge, a
dedicated `#inperson` section and a `New` marker on the format tab all carry it.
Retire that framing in ~6 months; an evergreen announcement bar is kept commented
out directly beneath the live one, and the section still reads correctly with the
tag removed.

**Stats stay attributed as platform totals.** They were earned by virtual events.
Nothing on the page claims in-person volume.

**Still placeholders (4):** `{{SOC 2}}`, `{{EEOC}}`, `{{Data handling}}`,
`{{Compliance}}` — footer trust badges. Not verifiable from any source available,
so not invented.

---

## Honest-placeholder rule

Anything not grounded in the source material is rendered as a visible placeholder,
never as invented fact. That covers: customer logos, customer names, quotes, all
statistics, all prices, compliance badges, and press mentions. They are marked
`{{LIKE_THIS}}` in the markup and carry a `data-placeholder` attribute so they can be
found and swapped in one pass.
