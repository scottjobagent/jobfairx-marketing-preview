# JobFairX Marketing — Design System v1

Derived from a token-level teardown of Linear, Stripe, Vercel, Anthropic, Cursor, Clay,
ElevenLabs, Notion, Attio, Vanta, Ramp, Deel, Ashby, Greenhouse, Superhuman, Gem and
Paradox. Values below are real, measured numbers from those systems, adapted — not
invented round numbers.

---

## 0. The five rules that separate premium from template

These came out of the research as near-universal, and every one of them is cheap to obey.

1. **Never pure white, never pure black.** Every reference canvas is tinted
   (`#faf9f5`, `#f7f7f4`, `#fafafa`) and every ink is a warm or cool near-black
   (`#141413`, `#26251e`, `#171717`). Pure `#fff`/`#000` is the fastest template tell.
2. **Hero weight is never 700.** Linear ships a custom 510. Stripe sets *all* display
   type at 300. Cursor 400, Clay 500. We use **500**.
3. **Tracking is a ramp that crosses zero.** Negative on display
   (-0.03em to -0.045em), but slightly **positive at 14–16px** (+0.004 to +0.01em).
   Cursor runs +0.01em @14px → -0.03em @72px; Retool ships +0.0126em on body.
   Negative tracking on small text is the most common way a good type system
   still reads cramped. Display line-height stays sub-1.1.
4. **Pick one depth mechanism per system** — hairline border *or* drop shadow, never
   both on the same element. Linear/Cursor/Vercel are hairline-only; Notion/Stripe are
   shadow-only. **Depth never comes from coloured glow.** Linear's hero carries no
   box-shadow at all — only a 2px ring and a 0.5px white border, with the cast shadow
   shipped as pre-rendered images. Cursor uses two neutral shadow layers plus a 1px
   white rim. There is no bloom on any peer site; ours is kept to a faint brand tint
   at 15% alpha so the hairline and rim do the actual work.
5. **Render final stat values in HTML and animate *from* them.** Gem currently ships a
   live homepage reading "0x Boost recruiter efficiency" because its count-up never
   fires. Never animate *to* a number.

---

## ⚠️ One place this system deliberately departs from the brief

The brief asks for *floating 3D cards, perspective movement, stacked glass panels,
3D-tilted product screenshots.*

The research finding was unusually blunt and unanimous:

> **Not one** of the seventeen reference sites tilts a product screenshot in 3D
> perspective. It is "the strongest 2019-template tell remaining."

So this system splits the intent from the execution. We keep **depth** and drop **skew**:

| Brief asks for | What we ship | Why |
|---|---|---|
| Floating 3D cards | Real UI fragments on separate z-planes with independent parallax rates | Reads as depth, not as a skewed JPEG |
| Perspective movement | Mouse/scroll **translation** of layers, ≤14px, plus ≤1.2° rotation | Parallax reads premium; skew reads dated |
| Stacked glass panels | Hairline-framed panels with ambient glow behind, offset in z | Linear's approach, cheapest to execute well |
| Layered screenshots | Anchor plane + 2 extracted fragments in front | Same silhouette, none of the cheapness |

**This is a recommendation, not a lock.** A single CSS custom property
(`--tilt: 0deg`) controls it. Set it to `8deg` and you get the brief's literal version
across all three concepts. Say the word.

---

## 1. Typography

**Face:** Inter Variable, with `font-feature-settings: 'cv01' 1, 'ss03' 1` enabled
globally — this is Linear's exact configuration and the correct substitute for a
licensed display face. Mono: `ui-monospace, 'SF Mono', monospace` for eyebrows/data.

```css
:root {
  --font-sans: 'Inter var', Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: ui-monospace, 'SF Mono', SFMono-Regular, Menlo, monospace;
}
html { font-feature-settings: 'cv01' 1, 'ss03' 1; }
```

### Scale

| Token | clamp() | Weight | LH | Tracking |
|---|---|---|---|---|
| `--t-display` | `clamp(2.75rem, 1.4rem + 5.6vw, 5rem)` | 500 | 0.98 | -0.042em |
| `--t-h1` | `clamp(2.25rem, 1.3rem + 4vw, 3.75rem)` | 500 | 1.02 | -0.038em |
| `--t-h2` | `clamp(1.875rem, 1.2rem + 2.8vw, 3rem)` | 500 | 1.06 | -0.032em |
| `--t-h3` | `clamp(1.375rem, 1.05rem + 1.4vw, 1.875rem)` | 550 | 1.15 | -0.022em |
| `--t-lead` | `clamp(1.0625rem, 1rem + 0.5vw, 1.25rem)` | 400 | 1.5 | -0.01em |
| `--t-body` | `1rem` | 400 | 1.6 | -0.005em |
| `--t-sm` | `0.875rem` | 400 | 1.55 | 0 |
| `--t-eyebrow` | `0.75rem` | 600 | 1.3 | **+0.09em** |

Eyebrows are the **only** place tracking goes positive. Uppercase, 11–13px, weight 600.

---

## 2. Color

### Dark palette (Concept 1, hybrid hero, footer)

```css
--d-void:      #08090c;   /* deepest ground */
--d-canvas:    #0b0d12;   /* section background */
--d-surface-1: #12151c;   /* card */
--d-surface-2: #191d26;   /* raised card */
--d-hairline:  rgba(255,255,255,0.09);
--d-hairline-strong: rgba(255,255,255,0.16);
--d-ink:       #f4f6fa;
--d-ink-2:     #a8b0be;   /* secondary */
--d-ink-3:     #6b7383;   /* tertiary */
```

### Light palette (Concept 2, hybrid mid-page)

```css
--l-canvas:    #fbfaf8;   /* warm off-white, never #fff */
--l-surface:   #ffffff;   /* cards only, on the tinted canvas */
--l-sunken:    #f3f1ed;
--l-hairline:  #e6e3dd;
--l-ink:       #14161a;   /* cool near-black */
--l-ink-2:     #565b66;
--l-ink-3:     #8b909b;
```

### Accent

JobFairX blue is retained but **deepened and desaturated** — the current `#2563eb` is a
stock Tailwind blue and reads generic. One accent, used only for primary CTA, focus
rings, link emphasis and the brand mark, per Linear's discipline.

```css
--accent:       #2f5cff;
--accent-hover: #4a72ff;
--accent-press: #1f45d6;
--accent-ink:   #ffffff;
--accent-glow:  rgba(47,92,255,0.35);
```

Supporting hues appear **only** on the interview-format chips, mapped to the real badge
colors already in the product so the marketing site and the app agree:

```css
--fmt-video:    #b06d1f;  /* amber, matches in-app Video badge */
--fmt-phone:    #b06d1f;
--fmt-inperson: #b06d1f;
--fmt-external: #4b5563;
```

---

## 3. Spacing

4px base, matching Anthropic/Linear/Vercel.

```css
--s-1:4px; --s-2:8px;  --s-3:12px; --s-4:16px; --s-5:20px; --s-6:24px;
--s-8:32px; --s-10:40px; --s-12:48px; --s-16:64px; --s-20:80px;
--s-24:96px; --s-32:128px; --s-40:160px;
```

- **Container:** `max-width: 1200px`, gutters 24px mobile / 32px desktop.
  A narrow variant at `760px` for editorial passages.
- **Section rhythm:** `96px` desktop, `56px` mobile. Hero gets `160px` bottom.
- **Card padding tiered by weight** (this is why premium pages feel composed):
  feature 24px · pricing 28px · testimonial 32px · CTA banner 48px.

---

## 4. Radius

Low. High radius reads consumer, not enterprise.

```css
--r-xs:4px; --r-sm:6px; --r-md:8px;    /* buttons */
--r-lg:12px;                            /* cards */
--r-xl:16px;                            /* screenshot frames */
--r-2xl:24px;                           /* large panels */
--r-pill:999px;                         /* badges + marketing CTAs only */
```

---

## 5. Depth — one mechanism per surface

**Dark sections → hairline + glow. Light sections → shadow.** Never both.

```css
/* light-mode elevation ladder */
--sh-sm: 0 1px 2px rgba(20,22,26,.05), 0 1px 1px rgba(20,22,26,.04);
--sh-md: 0 2px 4px rgba(20,22,26,.04), 0 8px 16px -4px rgba(20,22,26,.07);
--sh-lg: 0 4px 8px rgba(20,22,26,.04), 0 16px 32px -8px rgba(20,22,26,.10);
--sh-panel: 0 24px 48px -8px rgba(20,22,26,.18), 0 2px 6px rgba(20,22,26,.06);
--sh-float: 0 12px 28px -6px rgba(20,22,26,.16), 0 2px 4px rgba(20,22,26,.06);

/* dark-mode: ambient glow replaces shadow entirely */
--glow-accent: 0 0 0 1px var(--d-hairline), 0 30px 80px -20px var(--accent-glow);
```

---

## 6. Motion

```css
--e-out:   cubic-bezier(0.16, 1, 0.3, 1);    /* entrances */
--e-inout: cubic-bezier(0.4, 0, 0.2, 1);     /* hover / state */
--t-micro: 120ms;   /* hover, press */
--t-fast:  200ms;   /* chips, tabs */
--t-base:  320ms;   /* card reveal */
--t-slow:  520ms;   /* section reveal */
```

**Rules**
- Scroll reveal runs opacity and transform on **different clocks**: `opacity 150ms
  linear` against `transform 800ms` on the expo curve. Stripe does exactly this — the
  fast fade is what stops a long entrance from feeling laggy. Stagger **60ms** per item.
- **Never animate the hero headline on load.** Linear, Vercel, Anthropic and Cursor all
  paint it immediately. Animating it delays the one thing the visitor came for.
- Button press = `scale(0.975)` over 100ms. No color darkening.
- Zero bounce, zero overshoot. Not one reference site uses spring easing.
- Parallax via `transform` only, lerp factor `0.08`, driven by one shared `rAF` loop.
- **Open question — frosted nav.** The research split on this. One pass found
  `backdrop-filter: blur(12–16px)` to be the 2026 sticky-header norm (24px is where
  low-end Android drops frames). A second pass found the opposite: juicebox has zero
  occurrences in a 342KB stylesheet, Anthropic zero, and Vercel's header is solid
  black — calling frosted chrome "the dated tell." Concepts 1 and 3 currently ship
  `blur(14px)`; Concept 2 ships a solid bar. **Worth deciding deliberately** — swapping
  to solid is a two-line change in each concept.
- Logo wall is **static**. Marquee now reads downmarket.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important; animation-iteration-count: 1 !important;
    transition-duration: .01ms !important; scroll-behavior: auto !important;
  }
  [data-parallax] { transform: none !important; }
}
```

---

## 7. Components

### Buttons
14px / weight 500 / `--r-md` / height 44px (40px compact).
- **Primary** — accent fill, white ink, no shadow in dark sections, `--sh-sm` in light.
- **Secondary** — transparent, 1px hairline, ink text.
- **Ghost** — text + a 1px underline that grows from left on hover (`--t-micro`).

### Cards
`--r-lg`, hairline in dark / `--sh-md` in light. Hover: `translateY(-2px)` +
one step up the shadow/hairline ladder over `--t-fast`.

### Product panel (`.panel`)
The workhorse. `--r-xl`, 1px hairline, `--sh-panel` in light sections, ambient glow in
dark. Contains a screenshot cropped via `object-position`, never squashed.

### Floating fragment (`.frag`)
An extracted UI region — a candidate request row, a format chip cluster, a KPI tile.
Own shadow, own parallax rate, `--r-lg`. Two per hero maximum.

### Video placeholder (`.video-ph`)
16:9, `--r-xl`, hairline, centered play glyph in a 64px accent-tinted disc, duration
chip top-right, caption below. Swapping in production replaces the inner markup only.

### Inputs
44px tall, `--r-md`, 1px hairline, focus = 2px accent ring at 40% + hairline→accent.

---

## 8. Screenshot handling

Our screenshots are a dense, white, data-heavy recruiting dashboard. Four techniques
make that look premium, in order of payoff:

1. **Crop, don't shrink.** Never show the whole 1600×1000 frame. Crop to the one region
   that carries the story — the INTERVIEW LOCATION column, the Accept button, the KPI
   row. Use a fixed-ratio wrapper with `overflow:hidden` and `object-position`.
2. **Bleed off the edge.** Let the panel run past the container on one side. It implies
   the product continues beyond the viewport.
3. **On dark sections, inset on a plate.** A white screenshot on near-black looks
   broken. Sit it on a `--d-surface-1` plate with 12px padding and a hairline, so the
   white reads as *a screen* rather than *a hole*.
4. **Mask the far edge.** `mask-image: linear-gradient(to bottom, #000 70%, transparent)`
   where a panel runs into the next section.

**Production note:** these PNGs are 2× retina, 80–370KB each. Before launch, convert to
AVIF with WebP fallback and add `loading="lazy" decoding="async"` on everything below
the fold. Expect ~70% size reduction.

---

## 9. Accessibility

- Contrast: body ≥ 4.5:1, large display ≥ 3:1. `--l-ink-3` and `--d-ink-3` are for
  non-essential meta only — never body copy.
- Focus visible on every interactive element; never `outline: none` without a replacement.
- Format-chip meaning never carried by color alone — always icon + label.
- Section landmarks, one `<h1>`, ordered heading levels.
- All motion respects `prefers-reduced-motion`.
- Video placeholders carry real captions, not just an icon.
