# JobFairX Employer Homepage — Concepts & Recommendation

Three homepage concepts, built as working pages rather than static mockups, because
motion was named as a defining characteristic and motion doesn't survive a flat comparison.

Open `index.html` to compare them side by side.

---

## What the research actually said

I studied juicebox.ai and stability.ai in depth, plus Linear, Vercel, Stripe, Anthropic,
OpenAI, Cursor, Clay, ElevenLabs, Notion, Attio, Vanta, Ramp, Deel, Ashby, Greenhouse,
Superhuman, Gem and Paradox — at token level, pulling real hex values, type scales, shadow
stacks and easing curves.

Five findings reshaped the work, and three of them contradict assumptions in the brief.
Flagging them plainly rather than quietly designing around them:

### 1. Nobody perspective-tilts product screenshots any more

**Not one** of the seventeen reference sites tilts a screenshot in 3D. The research called it
"the strongest 2019-template tell remaining." The brief asks for floating 3D cards, perspective
movement and stacked glass panels.

I kept the *intent* — depth, dimensionality, layered UI — and dropped the *skew*. Depth now
comes from real z-layers moving at different parallax rates, tinted multi-layer shadows, rim
lighting and ambient glow. **This is reversible in one line:** every concept reads
`--tilt: 0deg`. Set it to `8deg` and you get the literal version from the brief.

### 2. juicebox's hero has no parallax, no scroll motion, and no product screenshot

I walked its layer tree: two static paint layers. The depth you're responding to is a *density
vignette* — a halftone dot field that's saturated at the edges and dissolves to nothing in the
middle, so the headline sits in an optical clearing. Nothing moves.

Concept 2 reproduces that technique honestly. Concepts 1 and 3 add motion, because your product
*does* have a dashboard worth showing and an events business benefits from showing it.

### 3. stability.ai has no scroll-driven motion either

Zero `scroll-timeline`, zero `position: sticky`, no GSAP. Every dark/light seam is static. The
sophistication is entirely in colour and in masked bleeds — a four-percentage-point gradient
edge is all that separates two treatments. Concept 3's seams use exactly that: a tall gradient
blend so neither side has a visible edge.

### 4. Hero headline weight is never 700

Linear ships a custom 510. Stripe sets *all* display type at 300. Cursor 400, Clay 500. All
three concepts use **500**, with line-height 0.98 and −0.042em tracking. This one choice does
more for "premium" than any effect.

### 5. Never animate a statistic *toward* its value

Gem is currently shipping a live homepage that reads "0x Boost recruiter efficiency" because
its count-up never fires. Our counters read the final value out of the DOM and animate *from* a
lower number to it, so a failed script still shows the real figure.

---

## The three concepts

### Concept 1 — Dark / Cinematic
One continuous night; no theme change anywhere. Depth is ambient light and glass.

- Asymmetric hero: copy holds a 520px column, the product plane bleeds past the right edge
- Three drifting aura blobs on a fixed layer, transform-animated so they stay on the compositor
- Glass cards with `backdrop-filter`, rim-lit panels, Linear's corner-anchored radial glow
- Journey as six numbered full-bleed bands, alternating sides

**Strongest at:** looking like an AI company. **Weakest at:** a white, data-dense dashboard
fights a black page all the way down — every screenshot needs a plate, and the eye tires.

### Concept 2 — Light / Technical-editorial
The page as a printed document. Deliberately no shadow, no glass, no glow, no `backdrop-filter`.

- 16px inset page frame with hairline rules instead of alternating background fills
- Bracketed section ordinals `[01] [02] [03]`, figure captions under every screenshot
- Tracking opposition: negative on the sans, positive on the uppercase mono
- Per-format accent + tint pairs, one hue per interview format
- Hero is a dot field with a burned-through clearing — no screenshot, juicebox's actual technique
- 4px radii throughout, flat dark buttons with mono labels

**Strongest at:** trust, legibility, and making dense product screenshots look natural — a white
dashboard on warm paper needs no special handling at all. **Weakest at:** it reads *technical
publication*, not *AI platform*. Less immediately impressive in a first-three-seconds sense.

### Concept 3 — Hybrid / Night into day ← **recommended**
Dark hero, daylight middle, dark close. The theme change carries the narrative: night is the
promise, day is the proof, night is the decision.

- Cinematic hero with the live event lobby as an anchor plane and two floating UI fragments
- Fragments are **rebuilt in DOM**, not cropped from a PNG — razor sharp, animatable, and it
  sidesteps the "white screenshot punched into a black page" problem entirely
- Nav inverts automatically to whichever themed section sits under it
- Sticky-scroll seven-step journey: the steps scroll while the product visual stays pinned
- Tabbed interview formats, each tab swapping to a real product view of that format

---

## Recommendation: build Concept 3

Three reasons, specific to selling hiring events to employers.

**1. Your product is white, and most of your page is product.**
This is the deciding factor. You have fifteen real screenshots of a light, data-dense recruiting
dashboard, and the brief rightly asks to weave them through the whole page. On a fully dark
page every one of them needs a plate, a scrim and a rim light to avoid reading as a hole punched
in the design — that's a tax paid on every section. Concept 3 pays it once, in the hero, where
the drama is worth it, then switches to daylight for the eight sections that are mostly product
and mostly explanation. The screenshots stop fighting the page and start carrying it.

**2. The theme change does narrative work, not decorative work.**
The dark→light→dark structure isn't a style choice, it maps onto the argument: a cinematic
promise, a well-lit proof, a confident close. That's also the thing you liked about stability.ai,
and it's the one structural idea the other two concepts can't offer.

**3. It hedges the risk in both directions.**
Concept 1 risks looking like an AI company that might not be a real product. Concept 2 risks
looking like a real product that isn't an AI company. Concept 3 opens with the first impression
and then spends eight sections earning the second.

The honest counter-argument: Concept 3 is the most complex to build and maintain — two palettes,
a theme-aware nav, and seams that need care at every breakpoint. If speed to launch matters more
than first-impression drama, **Concept 2 is the safer build** and will hold up better as the site
grows to twenty pages. If you want one page to look extraordinary and are willing to spend on it,
Concept 3.

---

## Refinements applied after the deep-dive landed

The last research pass finished after the first build and produced four corrections,
all now applied to the shared system:

- **Coloured glow pulled back.** Peer sites get depth from hairlines, rim light and
  occlusion — "there is no bloom on any of them." The accent bloom behind the hero
  panels dropped from 42% to 15% alpha, so the 0.5px rim and 1px ring carry the edge.
- **Tracking ramp now crosses zero.** Body and small text moved from −0.005em to
  **+0.004/+0.006em**. Negative tracking at 14–16px is the most common reason a good
  type system still reads cramped.
- **Scroll reveal split onto two clocks** — opacity 150ms linear against transform
  800ms expo, matching Stripe. The fast fade removes the laggy feeling.
- **Grain added to the dark grounds.** A 256px inline-SVG `feTurbulence` tile at
  `mix-blend-mode: overlay`, with a lighter Safari value. Zero network cost, and it
  stops the large flat fills from banding.

**One open question I did not decide for you:** the two research passes contradicted
each other on frosted-glass navs. One found `blur(12–16px)` to be the current norm;
the other found juicebox, Anthropic and Vercel all ship solid bars and called frosted
chrome "the dated tell." Concepts 1 and 3 currently blur; Concept 2 is solid. It's a
two-line change either way — flag which you prefer.

---

## Before this goes to build

**Everything below is a placeholder and must not ship as-is.** Each carries a
`data-placeholder` attribute and renders with a visible orange tag:

| Item | Status |
|---|---|
| Customer logos (6) | Invented. Need real, approved logos. |
| All four statistics | Invented. Need real figures + a source for each. |
| Three customer quotes | Invented. Need name, full title, company, approval. |
| All prices | Invented. Package *names* (Starter/Growth/Pro) are real — taken from the product. |
| Compliance badges | Invented. Need confirmation of what JobFairX actually holds. |
| Announcement bar date/city | Needs the real next event. |
| Five video slots | Elegant placeholders, ready to swap for embeds. |

**Two things I changed in the screenshots, deliberately:**

- The prototype uses **Tesla** as the demo account name and **Baylor Scott & White Health** as a
  demo employer. On a marketing homepage those read as customer claims, so I replaced both with
  a fictional "Northwind Health" at capture time.
- `candidate-preview.html` turned out to be an internal iStock comp sheet — unlicensed preview
  images with "Buy on iStock" links, not product UI. It's excluded from the publishable assets
  and quarantined in `assets/_reference-do-not-publish/`. **Do not use those photos anywhere.**

**Performance, before launch:** the fifteen screenshots are 2× retina PNGs, 80–370KB each.
Convert to AVIF with WebP fallback and add `loading="lazy" decoding="async"` below the fold —
expect roughly 70% off. Nothing else on these pages is heavy: no libraries, no build step, no
web fonts beyond Inter, all motion is transform/opacity on the compositor.

---

## What's in this folder

```
index.html              compare the three concepts
concept-1-dark.html     Concept 1
concept-2-light.html    Concept 2
concept-3-hybrid.html   Concept 3  ← recommended
shared/base.css         design tokens + primitives, shared by all three
shared/motion.js        scroll reveal, parallax, tabs, sticky journey, counters
assets/product/         15 clean 2× screenshots captured from the live prototypes
assets/_reference-do-not-publish/   unlicensed stock comps — excluded on purpose
DESIGN-SYSTEM.md        tokens, type scale, depth, motion, screenshot rules
CONTENT-SPEC.md         section-by-section copy and the product-visual map
RECOMMENDATION.md       this file
```

Concepts share `base.css` and `motion.js` deliberately: the design system is the deliverable,
and three pages proving the same tokens flex into three different languages is stronger evidence
than three one-off pages.
