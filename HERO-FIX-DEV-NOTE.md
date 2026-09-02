# Employer page header — hero size fix

**Written:** 31 Aug 2026
**Preview:** `employer-hero-fix-preview.html` (built by `build-hero-fix.py`)
**Captures:** `assets/live-capture/hero-fix-aug31/` — server-rendered HTML of all five live URLs plus the production stylesheet `app.bb701d17.css`, fetched 31 Aug 2026.

---

## 1. The problem, measured

The employer home page headline is **52px** on desktop. Five inner pages are **30px**. Everything else on the employer site already has a real hero size.

Read from the compiled stylesheet, not inferred from class names:

```css
/* no media query - applies at every width */
.text-3xl { font-size: 1.875rem; line-height: 2.25rem }

/* home page only */
@media (min-width: 1024px) {
  .lg\:text-\[52px\] { font-size: 52px }
}
```

Below 1024px every page is 30px and they match. At 1024px the home page steps up and these five don't move — they were never given a desktop size, so they inherit a body-copy heading token and stop there.

A second, independent effect makes three of them look physically recessed: the hero is `bg-white` with a 900×450 `bg-blue-600/10 blur-[140px]` halo pinned to top-centre, and the next section switches to `bg-slate-50`. Bright pool in the middle, grey gutters either side, hard edge underneath — an inset panel.

| Page | Headline | Halo | slate-50 immediately below |
|---|---|---|---|
| `/employer` (home) | 52px | off-centre, top-right | no |
| `hiring-event-calendar` | 30px | top-centre | **yes**, y=362 |
| `healthcare-hiring-event-calendar` | 30px | top-centre | **yes** |
| `hiring-event-faq` | 30px | top-centre | **yes**, y=250 |
| `hiring-event-pricing` | 30px | top-centre | no (first band 1,941px down) |
| `contact` | 30px | top-centre | no |

Pricing and Contact only ever had the size problem. The other three have both.

---

## 2. Scope — exactly five pages

All 26 core employer URLs in `sitemap.xml` were swept for the class string `text-3xl font-medium lg:font-semibold`. Five carry it:

- `/employer/hiring-event-calendar`
- `/employer/healthcare-hiring-event-calendar`
- `/employer/hiring-event-pricing`
- `/employer/hiring-event-faq`
- `/employer/contact`

**Not affected** — these already have their own hero sizes and need no change:
`host-an-event` 46px extrabold · `job-postings` 52px · `about-us` 52px · `resources` 48px · `job-posting-pricing` 60px · `hiring-event-bundles` 44px · `nonprofit` 30px (different component, document-style header) · `demo` · `job-posting-bundles` · the 1,760 programmatic `/employer/job-fairs/*` pages.

The same class string on all five suggests one shared page-header component. **If it is one component, this is a single-file change.** Please confirm which.

---

## 3. The change

### 3.1 Headline — all five

```
- text-3xl font-medium lg:font-semibold
+ text-3xl lg:text-[44px] font-medium lg:font-semibold lg:leading-[1.05] lg:tracking-[-0.03em]
```

`text-3xl` is kept so **mobile renders byte-identically to today**. The new step is desktop-only. 44px rather than 52px so the home page keeps the top of the hierarchy.

Full class strings as they appear now:

| Page | Element | Current class |
|---|---|---|
| calendar | `h2` ×2 (`hidden lg:block` + `lg:hidden`) | `… lg:mb-4 max-w-3xl mx-auto text-3xl font-medium lg:font-semibold` |
| healthcare | `h1` | `text-slate-900 lg:mb-4 max-w-3xl mx-auto text-3xl font-medium lg:font-semibold` |
| pricing | `h1` | `text-slate-900 mb-4 flex gap-1.5 max-w-3xl justify-center mx-auto text-3xl font-medium lg:font-semibold` |
| faq | `h1` | `text-slate-900 mb-4 max-w-3xl mx-auto text-3xl font-medium lg:font-semibold` |
| contact | `h1` | `text-slate-900 mb-4 max-w-3xl mx-auto text-3xl font-medium lg:font-semibold` |

### 3.2 Eyebrow — calendar, healthcare, pricing

```
- text-[12px] font-bold lg:text-center text-[#2563eb] uppercase tracking-[0.14em] mb-2 lg:mb-4
+ text-[12px] lg:text-[14px] font-bold lg:text-center text-[#2563eb] uppercase tracking-[0.14em] mb-2 lg:mb-4
```

Matches the home page's 14px. FAQ and Contact have no eyebrow.

### 3.3 Halo — all five

```
- absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[450px] bg-blue-600/10 blur-[140px] rounded-full pointer-events-none hidden lg:block
+ absolute -top-[140px] right-[4%]        w-[780px] h-[430px] bg-blue-600/10 blur-[150px] rounded-full pointer-events-none hidden lg:block
```

The symmetric top-centre placement is what creates the vignette. The home page anchors its decorations right; this matches.

### 3.4 Hero background — calendar, healthcare, faq only

```
- bg-white relative overflow-hidden
+ bg-gradient-to-b from-white to-slate-50 relative overflow-hidden
```

Removes the hard edge where the hero meets the `bg-slate-50` band. **Pricing and Contact keep `bg-white`** — nothing grey sits beneath them.

---

## 4. Tailwind must generate four new utilities

These are not in `app.bb701d17.css` because nothing currently uses them. They appear once the class strings are in the components — no config change needed, but worth confirming the content globs cover these files:

- `lg:leading-[1.05]`
- `lg:tracking-[-0.03em]`
- `lg:text-[14px]`
- `to-slate-50`

(`lg:text-[44px]`, `from-white` and `bg-gradient-to-b` already exist.)

The preview ships a shim block supplying these; it is preview-only and must not be copied into production.

---

## 5. Three separate bugs found while measuring

Unrelated to the visual change, all worth fixing in the same pass.

1. **`<h1>` is on the eyebrow, not the headline, on two pages.**
   - `/employer` — the `h1` is the 14px eyebrow "THE HIRING EVENT PLATFORM FOR EMPLOYERS"; the real headline is a plain `<div>`.
   - `/employer/hiring-event-calendar` — the `h1` is the 12px eyebrow "2026 Hiring events"; the headline is an `<h2>`.
   Pricing, FAQ, Contact and healthcare-calendar are correct. Search engines are reading the eyebrows as the page titles on the two most important employer pages.

2. **The calendar page has no `<h1>` at all on mobile.** That eyebrow `h1` carries `hidden lg:block`, so below 1024px it is not rendered, and the mobile headline is an `lg:hidden <h2>`.

3. **`/employer/faq` returns 404.** The real path is `/employer/hiring-event-faq`. Worth a redirect plus a grep for anything still pointing at the short URL.

---

## 6. Verifying

`build-hero-fix.py` asserts a match count on every replacement and aborts on drift, so re-running it against fresh captures is a cheap way to confirm the live markup still matches what this note describes.

```bash
python3 build-hero-fix.py
```

24 edits should apply, all count 1 or 2. Any `ABORT` means the live markup moved and this note needs re-checking before the change lands.

---

## 7. Explicitly not in this change

No copy edits. No CTA added to the inner heroes — Calendar and FAQ currently have no button above the fold at all, which is worth a separate conversation. No left-alignment. Those are design decisions, not defect fixes.
