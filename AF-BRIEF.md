# BUILD BRIEF — AI Flow page set (concept 5 walkthrough)

Scott approved concept 5 ("AI Flow") and wants EVERY landing page built in its
language: all feature pages, all solutions pages, pricing, FAQ, contact, and
the upcoming-events page (whose status pills — Matching live / Matching soon /
Early registration + save-$100 chip — he singled out and loves; they must
survive the redesign prominently). You build the page(s) named in your prompt.

## Read first, in order

1. `/Users/scottl./Desktop/jobfairx-marketing/concept-5-aiflow.html` — THE
   chrome and design language. Copy verbatim: the `.aiflow` palette block,
   announce bar, the full nav with BOTH mega-dropdowns (icons included — they
   are inline Phosphor fill glyphs; bright accent blue for Features, the five
   type colours for Solutions), the drawer, `.af-head`/`.af-btn` grammar, the
   gradient `.af-cta` close, and the light `.foot-af` footer. Change only:
   `<title>`, meta description, the `aria-current`/`is-current` marker, and
   the footer self-link.
2. Your SOURCE page (named in your prompt) — you PORT its content, data,
   behaviour and placeholders. Do not invent; do not drop placeholders.
3. `HANDOFF.md` §2 (vocabulary law), §3 (verified facts), §4 (design rules),
   §11–12 (lessons: green only for genuine completion states; `#8b909b` fails
   AA for real text — use `--muted-af #6a7086` on white, `--muted-cream
   #5f6580` on cream; no layout-property animations; `--void` resolves light
   inside light wrappers — the drawer hard-codes `#08090c`; `[hidden]` guard
   required; descendant selectors in card components bite — prefer `>`).
4. `shared/vignettes.css` header — the beat/vignette contract, if you use one.

## The AI Flow language (non-negotiable)

- Warm near-white canvas `--canvas-af`, cream panels `--cream`, navy ink
  `--navy`; display weight 600; centered `.af-head` section grammar: mono
  eyebrow → huge centered headline → ≤2 calm lines → at most one navy pill.
- ONE enormous rounded panel (24px radius, soft double shadow) per section —
  big images, easy reading. Screenshots live inside white plates in cream
  panels or edge-to-edge in `.af-stage`-style panels.
- Primary CTA = navy pill; secondary = cream pill; JobFairX blue = links,
  accents, wordmark. Green ONLY where the product shows a genuinely complete
  state ("Matching live" qualifies; use `--ok-ink #0e6e34` for green TEXT).
- Serif (Georgia stack) ONLY if your page has an editorial-resources moment.
- Hard cuts between grounds; navy band sections for punctuation; the grainy
  gradient CTA closes every page before the light footer.
- Motion: `data-reveal` entrances + at most ONE living element per screenful;
  no springs; transform/opacity only; complete truthful frame with JS off and
  under reduced motion (the shared final-frame blocks handle vignettes — do
  not put `data-reveal` on a page's last element; do not add `vg-fade` to a
  container that wraps real content).
- PRICING CARDS ARE EQUAL SIZE (Scott explicitly dislikes the lifted featured
  card): three identical cards, "Most Popular" as a small tag on Growth, same
  dimensions, same layout.

## Copy/data law

Vocabulary: candidates **request**, employers **accept**, accepting
**schedules**; never apply/application/applicants; never "in-person event(s)",
"event format", "virtual event"; interview location is a per-employer setting.
Every number/name/quote/address traces to your source page, HANDOFF §3 or
LIVE-SITE-SCOPE.md. Customers = company + role only. Fictional demo names only
from the approved set. Keep every `{{PLACEHOLDER}}` + `data-placeholder`. No
stock photography, no awards, no logo walls. Screenshots only from
`assets/product/` (never `interviews-pending.png`).

## Link map (the af- set)

Home = `concept-5-aiflow.html`. Nav/footer/dropdowns point at the af- set:
`af-events.html`, `af-event-detail.html`, `af-pricing.html`, `af-faq.html`,
`af-contact.html`, `af-platform.html` (All features target),
`af-platform-events-dashboard.html`, `af-platform-candidate-pipeline.html`,
`af-platform-interview-scheduling.html`, `af-platform-event-day.html`,
`af-platform-messaging-automations.html`, `af-platform-analytics.html`,
`af-in-person-interviews.html`, `af-solutions.html`,
`af-solutions-healthcare.html`, `af-solutions-diversity.html`,
`af-solutions-veteran.html`, `af-solutions-technology.html`,
`af-solutions-entry-level.html`. Links with no af- page (interview-locations,
about, resources, demo, security, legal) keep their `page-*.html` targets.
Sign In / Register stay `href="#"`. IMPORTANT: your page's chrome must use
this af- link map even though today's concept-5-aiflow.html still points some
links at page-*; the orchestrator repoints the homepage in the same wave.

## Self-QA before you finish — REQUIRED

1. `python3 tools/mcheck.py <yourfile>` → `ok` (real-390 iframe probe; plain
   --window-size lies).
2. Full-page 1440px headless screenshot + one with motion.js stripped + one
   with --force-prefers-reduced-motion; LOOK at all three (PIL band crops),
   fix, re-shoot. Check no floating/overlay element covers content its own
   alt/caption narrates, and no crop leaves a clipped app-sidebar sliver.
3. Exactly one h1; footer identical to the chrome reference except the
   self-link; zero banned vocabulary in rendered text; placeholders intact;
   `[hidden]` guard present; delete any temp files you created in the repo.
Report: what you built, every deviation + reason, QA results, screenshot paths.
