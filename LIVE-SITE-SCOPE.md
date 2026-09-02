# Live Site Scope — jobfairx.com/employer

Captured 17 Aug 2026. Everything below is **verbatim from the live site**.

> **Method note.** The countdown banners are rendered client-side, so plain fetching
> misses them entirely. They were captured by rendering each page in headless Chrome
> with JS enabled. Anyone auditing this later needs to do the same or they'll conclude
> the banners don't exist.

---

## 1. Site map — bigger than the four pages we discussed

| Page | URL |
|---|---|
| Employer home | `/employer` |
| Upcoming hiring events | `/employer/hiring-event-calendar` |
| Healthcare-only calendar | `/employer/healthcare-hiring-event-calendar` |
| Event detail (×1,760) | `/employer/job-fairs/<state>/<city>/<id>` |
| Evergreen "next event" (×1,760) | `/employer/job-fairs/<state>/<city>/next-<type>` |
| Pricing | `/employer/hiring-event-pricing` |
| **Event bundles** | `/employer/hiring-event-bundles` |
| FAQ | `/employer/hiring-event-faq` |
| Contact | `/employer/contact` |
| **Host an event** | `/employer/host-an-event` |
| ~~Job postings~~ *(out of scope — bundled into the event packages)* | `/employer/job-postings` |
| ~~Job posting pricing / bundles~~ *(out of scope)* | `/employer/job-posting-pricing`, `/employer/job-posting-bundles` |
| Nonprofit | `/employer/nonprofit` |
| Demo | `/employer/demo` |
| About | `/employer/about-us` |
| Resources hub (11+ articles) | `/employer/resources/...` |

**Worth flagging:**

1. ~~A second product line.~~ **Resolved:** job postings are *part of the hiring-event
   package* — they are the "Promote 1 / up to 3 / up to 6 jobs" line on each tier. No
   standalone page is needed.
2. **1,760 evergreen `next-<type>` landing pages** — 352 cities × 5 event types. This is
   the SEO engine. Each renders a full event page for whatever the next event in that
   city/type is. Any event-page redesign multiplies across all 1,760.
3. `/employer/resources/virtual-vs-in-person-hiring-event` **already exists** — there's
   in-person content on the site, just not in the product messaging.

---

## 2. The event lifecycle — five states, not three

This is the core finding. The event detail page changes its banner, its pricing and its
CTA based on how far out the event is.

### State A — 31+ days out → early registration discount

Verified on Pearland, TX Veterans, 22 Sep 2026 (36 days out).

- **Banner (amber/cream bar, full width above nav):**
  > "Early registration pricing ends soon. Save $100 and lock in priority candidate matching. **Register Now →**"
- **Pricing cards show a struck original and a discounted price:**

  | Tier | Was | Now | Badge |
  |---|---|---|---|
  | Starter | ~~$495~~ | **$395** | "Save $100 — Early Registration· Ends August 22" |
  | Growth | ~~$895~~ | **$795** | same |
  | Pro | ~~$1,495~~ | **$1,395** | same |

- **CTA:** "Reserve My Spot →"
- The cutoff date shown ("Ends August 22") is **exactly 31 days before the event** —
  see "The threshold is 31 days, not 30" below.

### State B — 15 to 31 days out → matching activates soon

- **Banner:**
  > "Candidate matching activates soon. Reserve your spot to meet interview-ready candidates →"
- Pricing at full rate, no discount badge.

### State C — roughly 3 to 15 days → matching live

- **Banner:**
  > "Candidate matching is live. Reserve your spot to meet interview-ready candidates →"
- Pricing at full rate.

### State D — registration closed *(this one wasn't on your list)*

- **Banner:**
  > "Employer registration is closed for this event. Next [City] [Type] Hiring Event: [Date]. **View Details →**"
- Every pricing CTA becomes a disabled **"Registration Closed"**.
- The banner deep-links to the next event in that city and type.

### State E — registration closing soon *(a fifth state; I initially missed this)*

Between State C and State D there is a closing-soon window:

- **Banner (2 days out, verified on Omaha):**
  > "Employer registration closes tomorrow. Reserve your spot now →"
- Sibling variants in the same component: **"Employer registration closes in [N] days."**
  and **"Employer registration closes today."**
- Still purchasable — `Reserve My Spot` ×5, `Registration Closed` ×0.

**The cutoff is between 1 and 2 days out**, verified the same day:

| Event | Date | Days out | Banner | State |
|---|---|---|---|---|
| Dallas, TX Healthcare | 25 Aug | 8 | "Candidate matching is live…" | C |
| Omaha, NE Healthcare | 19 Aug | 2 | "Employer registration closes tomorrow…" | **E — open** |
| Syracuse, NY Veterans | 18 Aug | 1 | "Employer registration is closed…" | **D — closed** |

> **I got this wrong first time and it's worth recording why.** I originally reported
> that Omaha, Manchester and Cincinnati had *no banner*, and concluded State C simply
> stops ~3 days out. It doesn't — those pages carry the **closing-soon** banner, and my
> keyword list didn't include "registration closes", so I read absence into my own blind
> spot. Separately, a scope agent concluded none of these banners exist at all, because
> it read raw HTML instead of executing JS. Two different methods, two different false
> negatives, both pointing the same way. **Always render the page, and never conclude
> "not present" from a keyword list you wrote before you knew the answer.**

### The threshold is 31 days, not 30

Every event page carries a server payload:

```js
earlyRegistration: { minDays: 31, discount: 100, eligible: true|false, deadline: '<Month Day>' }
```

The deadline is always **event date minus exactly 31 days**, verified on 6 of 6 events
(Sep 22 → "Ends August 22"; Sep 23 → "Ends August 23"; Sep 30 → "Ends August 30" ×2;
Oct 27 → "Ends September 26" ×2). The discount is a **flat $100 on every tier**, never
expressed as a percentage — the effective rates would be an uneven 20.2% / 11.2% / 6.7%,
which is presumably why.

---

## 3. Event detail page — anatomy

Section order, consistent across all events:

1. Countdown banner (one of the five states above)
2. Nav
3. Event pill — `Pearland, TX · Virtual Veterans Hiring Event` / `September 22, 2026 · 11:00 AM – 3:00 PM CDT`
4. Type-specific H1 + subhead
5. CTA pair — `Reserve My Spot →` and `See How It Works` (play icon → video)
6. Hero photo (stock imagery, type-matched)
7. **Live trust metrics** — e.g. `429 Pre-Registered Veterans` *(carries an "Updated daily" chip)*, `35 Avg. Interviews / Employer`, `7 Avg. Hires / Employer`. **These are per-event and change by market** — Portland showed 968 / 73 / 19, McAllen 728 / 73 / 19.
8. Type-specific logo wall — the veterans event shows Lockheed Martin, Booz Allen, Patriot Defense, Atlas Freight, FedTech, Shield Logistics, VetHire
9. "See How JobFairX Works" video walkthrough
10. "Hiring Events Built Around Interviews" — 3 steps
11. "Built-in Tools" — messaging, scheduling, interview tracking
12. Testimonials — **type-specific**, different from the homepage set
13. Pricing packages (state-dependent)
14. Bundle cross-sell
15. Past companies
16. FAQ
17. Final CTA
18. Contact form
19. Footer

**Per-type copy varies:** Veterans → "Hire Mission-Ready Veterans"; Entry-Level → "Hire
Emerging New Talent"; Technology → "…scaled their engineering teams"; Healthcare →
"…scaled their healthcare teams"; Diversity → "…building diverse teams".

---

## 4. Pricing — two axes

**Per event:** Starter $495 · Growth $895 (Most Popular) · Pro $1,495

| | Starter | Growth | Pro |
|---|---|---|---|
| Jobs | Promote 1 job | Up to 3 jobs | Up to 6 jobs |
| Interviews | 20+ scheduled | 60+ scheduled | 100+ scheduled |
| Seats | 2 recruiter seats | Up to 5 | Unlimited recruiters |

**Bundles** (`/employer/hiring-event-bundles`) — an 8-step ladder, priced per tier via a
Starter/Growth/Pro tab switcher. Starter ladder:

| Events | Per event | Total | Save |
|---|---|---|---|
| 5 | $470 | $2,350 | $125 |
| 10 | $445 | $4,450 | $500 |
| 15 | $420 | $6,300 | $1,125 |
| **25** | **$395** | **$9,875** | **$2,500** ← Most Popular |
| 40 | $365 | $14,600 | $5,200 |
| 50 | $345 | $17,250 | $7,500 |
| 75 | $320 | $24,000 | $13,125 |
| 100 | $297 | $29,700 | $19,800 |

Trust chips: **"Credits never expire"** and **"Use across any event type"**.
Max saving is 40% at 100 events.

**"All Packages Include" — 8 bullets** (verbatim): AI matching and job promotion ·
resumes and contact info for every matched candidate · unlimited interviews before,
during and after · auto-accept or review each request · employer dashboard with
dispositions, notes, analytics · post-event report with downloadable data ·
follow-up interviews and messaging after the event · dedicated human support.

---

## 5. FAQ — 9 questions

Two answers contain facts we should be using far more prominently:

- **Q3 — "Are candidates local?"** → *"candidates are verified to be within
  approximately 20 miles of the event city."* **This is the single strongest argument
  for in-person events and it's buried in an FAQ.** Your candidates are already local.
- **Q5 — matching timing** → *"candidate matching activates immediately and you will
  start receiving interview requests within a few hours."*
- Q7 ties interview volume to plan: Starter ~20, Growth ~60, Pro 100+.

---

## 6. Contact page

- info@jobfairx.com · **(702) 269-0808** · JobFairX, LLC, 209 S Stephanie St. STE B #144,
  Henderson, Nevada 89012 · **Mon–Fri, 5:00 AM – 5:00 PM PST**
- Form: 8 required fields + optional message. Dropdowns for Company Size, Job Title,
  Subject.
- **Accessibility defect:** the `required` attribute appears **0 times** on the page —
  required status is conveyed only by a `*` in the label text. Screen readers and native
  validation get nothing. Worth fixing in the rebuild.
- The whole contact block is duplicated in the DOM for desktop/mobile rather than
  responsive — doubles the maintenance and confuses assistive tech.

---

## 6b. ⚠️ The interview-location model — read this before writing any copy

This was initially got wrong, and the error is easy to repeat.

**In-person is NOT an event type. There is no such thing as an "in-person event."**

An event is a market-and-audience moment — *Dallas Healthcare Hiring Event, Apr 22,
11:00 AM – 3:00 PM CT*. Every employer joins that same event. What each employer sets
independently is **where their own interviews happen** — the product calls this the
**INTERVIEW LOCATION**, and it is a column on the events dashboard:

| Interview location | What the dashboard shows |
|---|---|
| JobFairX video | "JobFairX video call" |
| Phone | "You call each candidate" |
| In person | "2200 Ross Ave, Suite 400 · Dallas, TX" |
| Your own link | "Microsoft Teams" |

Two employers at the same Dallas Healthcare event can interview completely differently.
One runs JobFairX video, another has candidates come to their office.

**What actually launched** is the in-person *interview location* option — not in-person
events, not employer-hosted physical job fairs.

| ✅ Say | ❌ Never say |
|---|---|
| in-person **interviews** | in-person **events** |
| set your **interview location** | choose your **event format** |
| same event, your choice of room | host your own in-person event |
| four interview locations | four event types *(the five event types are Healthcare / Diversity / Veteran / Technology / Entry-Level — a different axis entirely)* |

Consequences for the rebuild:
- The events calendar must **not** have a virtual/in-person filter. Events don't carry a format.
- The event detail page must **not** be labelled as an in-person or virtual event.
  It shows the event, and explains that you pick your interview location on registering.
- FAQ answers about "our virtual hiring events" become "our hiring events", with the
  location choice explained separately.

---

## 7. Virtual-only language that must change

| Where | Current string |
|---|---|
| Event pill, every event | "Virtual Veterans Hiring Event" |
| Every page title | "Virtual Hiring Event" |
| Calendar H2 | "Virtual Hiring Events" |
| FAQ Q1 | "conduct interviews directly inside the JobFairX video interview platform, **no Zoom**…" |
| FAQ hero | "Everything you need to know about our **virtual** hiring events." |
| Contact subcopy | "Have questions about our **virtual** hiring events?" |
| Event subheads | "…in a structured **virtual** hiring event." |
| Resources | 5 of 11 article slugs are virtual-specific |

---

## 7b. Additional mechanics captured

**Pricing page** — the three cards are selectable (`role="button"`). The selected card
reveals a **quantity stepper**; its selectable counts are the union of `[1,2,3,4]` and
every bundle size for that tier → `1,2,3,4,5,10,15,25,40,50,75,100`. A live **Total**
row and a "You save $X" pill update with it, and the CTA pluralises to
"Reserve My Spots" at 2+. Below the grid: *"Looking for larger bundles or custom volume?"*
→ See all bundles.

**"What Employers Experience"** — 87% employers who return · 91% (interview show rate),
attributed *"Based on 2025 platform data"*.

**Per-event show rates vary by type:** Healthcare 91% · Veterans 89% · Entry-Level 86%.

**Every event page carries a server data blob** — e.g. Omaha
`{brand:'Healthcare', registeredCandidates:893, companiesRegistered:18, scheduledInterviews:462}`.
There is also a global `onNewYearsSale:false` promo flag, currently off — so a
seasonal-sale banner state exists in the codebase beyond the four above.

**Calendar mechanics** — city search with autocomplete (150ms debounce, max 5
suggestions), a custom type dropdown with colour dots (All Types / Diversity / Veterans /
Healthcare / Entry Level / Technology), a desktop 4-column grid row per event
(`Date · City · Event Type`), a separate mobile stacked row, an empty state
("No events found" / "Try adjusting your search or filter criteria.") and
"Load More Events". Intro copy: *"Find a hiring event, register, and post your jobs.
Candidate matching starts immediately."*

**Job postings — the second product line.** H1 *"Hire the Right Person For Your Job"*.
A **30-day job posting**, sold in quantities (1 / 3 / 5 … up to 200), separate purchase
from events. Includes AI candidate matching, automated screening/messaging/scheduling,
candidate messaging, automatic reminders, unlimited interviews per candidate.
Prices render client-side and were **not** captured — see open question 7.

---

## 8. Open questions

1. **Is the early-registration discount flat $100 across all three tiers?** It is on the
   event I verified ($495→$395, $895→$795, $1,495→$1,395). Confirm it isn't percentage-based elsewhere.
2. **Do in-person events use the same four countdown states and the same discount?**
3. **Does the bundle ladder apply to in-person events too** — "use across any event type"
   currently means the five *audience* types, not format.
4. ~~Is `job-postings` in scope?~~ **Answered: no.** Job postings are part of the
   hiring-event package — that is the "Promote 1 / up to 3 / up to 6 jobs" line on each
   tier. No separate page; `page-job-postings.html` deleted.
5. **Are the per-event trust metrics live-queried?** They carry an "Updated daily" chip.
   The rebuild should keep them dynamic rather than hard-coding.
6. ~~What is the exact registration cutoff?~~ **Answered:** it sits between 1 and 2 days
   before the event. Confirm the exact hour it flips.
7. ~~Job posting prices~~ **Moot** — no standalone job-postings page.
8. **`onNewYearsSale`** — a seasonal-sale flag in the code, currently off. That's a
   *sixth* banner state. What does it show when on, and does it stack with early
   registration?
9. **Is the 31-day threshold intentional?** You described it as "thirty days out"; the
   code says `minDays: 31`. Harmless either way, but the copy should match whichever
   is right.

---

## 9. Implementation details worth keeping

**Events API:** `GET /api/employers/job-fairs?country=US` — **1,200 events**, 100 per
page. Params: `country`, `candidateTypes`, `searchText`, `page`, `from`, `until`.
"Load More Events" only renders when `eventCount > 75`.

**Event-type colours** (use these so marketing and product agree):

| Type | Colour |
|---|---|
| Diversity | orange |
| Technology | blue |
| Healthcare | teal |
| Veterans | red |
| Entry-Level | sky |

**Row title differs by breakpoint:** desktop `"Western Region, US Virtual Hiring Event"`,
mobile drops the word Virtual → `"Western Region, US Hiring Event"`. Given the
interview-location model, **"Virtual" should come out of the event title entirely** —
the event isn't virtual, the interviews might be.

**Dates:** desktop `Sep 3, 2026`; mobile `Thu, September 3`. Every event carries a
`formattedTime` (e.g. `11:00 AM PDT`) and a UTC `startDate` the page never renders.
