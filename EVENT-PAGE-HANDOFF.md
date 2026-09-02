# Event details page — current handoff

**Written:** 2 Sep 2026. **Supersedes** `CLAUDE_HANDOFF.md` (25 Aug) *for the event
details page only*. Everything else in that master doc still stands — read it for
the design system, the vocabulary laws and the other streams.

New session on any machine: read this, then say what you're working on. Don't
start editing until Scott names the file.

---

## 1. Where things are

Everything is published to the preview site. Nothing here needs a particular
machine.

    https://scottjobagent.github.io/jobfairx-marketing-preview/<file>

| Page | What it is | Status |
|---|---|---|
| `event-details-by-brand.html` | **The working page.** Five live event types behind a brand toggle. | Approved, current baseline |
| `event-details-by-brand-cards.html` | Working page + the four-box demo section at Indeed's sizes, Review-outcomes removed | **Newest. Awaiting Scott's verdict** |
| `event-details-by-brand-layout.html` | The ten layout-audit fixes on one stylesheet | Built, not ruled on |
| `event-details-dev-notes.html` | Developer package (also `EVENT-DETAILS-DEV-NOTES.md`) | Live, needs updating if the cards ship |
| `event-cards-size-markup.html` | Indeed's card dimensions vs our 1180 grid | Decided: Indeed sizes won |
| `event-chapters-markup.html` | Demo with clickable video chapters | Rejected in favour of cards |
| `event-reshuffle-markup.html` | Demo video-only + How It Works rebuilt | Rejected |
| `event-howitworks-markup.html`, `event-walkthrough-markup.html` | Earlier section mocks | Superseded |

**Builders are in this repo too.** Every page is generated — never hand-edit the
HTML. `build-<name>.py` builds `<name>.html`. Each one asserts its match counts
and aborts rather than silently mis-editing.

Build order that matters:

    build-event-details-by-brand.py     -> the working page (reads captures/_by-brand-deployed.html)
    build-event-details-cards.py        -> the cards page (reads the working page)
    build-event-details-layout.py       -> the layout page (reads the working page)
    build-event-details-dev-notes.py    -> the developer package (reads the by-brand builder)

The mock builders read shared strings out of `build-event-details-by-brand.py` at
build time, so they cannot drift from what was approved.

---

## 2. The page as it stands (cards version)

    hero -> stats + logos -> FOUR BOXES -> Choose your interview format
         -> Results -> Pricing -> Past Companies -> FAQ -> close -> contact

**Four boxes** — eyebrow "Hiring Event Demo", heading "Manage your hiring event
from start to finish.", white background, Indeed's measured geometry:
content 1314, cards **306 x 464**, gap 30, image **2:1 full-bleed**, 56px to the
title, title 28/35, body 16/24, padding 32.

| # | Card | Links to | Have it? |
|---|---|---|---|
| 1 | Manage your hiring event | YouTube `cDvxtuvm7mA`, 2:40 | yes |
| 2 | Add interviewers | tutorial library, **0:41** | yes |
| 3 | Interview settings | help-centre article | video is *planned, not made* |
| 4 | Event performance | help-centre article | video is *planned, not made* |

Card 1's image is per-brand (`brand-<slug>.jpg`); cards 2-4 use product
captures (`card-interviewers.jpg`, `card-settings.jpg`, `card-report.jpg`).

**Choose your interview format** — Video / In person / Phone, card colours from
the calendar's event-type palette, sub names the event's city per panel.

---

## 3. Decisions that are settled — do not reopen

- **Built-in Tools** section: removed. Also already removed from the employer home page.
- **How It Works** ("Hiring Events Built Around Interviews", three beats): removed.
  Two of its three beats repeated the demo.
- **Review interview outcomes**: removed 2 Sep. Card 4 covers the post-event report.
- **Demo runtime**: no `2:40` anywhere — not in the eyebrow, not on the poster.
- **Card order** in the format section: Video, In person, Phone. No links on those cards.
- **Video chapters** and the **reshuffle**: both mocked, both rejected.
- Indeed's `/employers/hiring-events` **redirects to `/onboarding`** and that page
  has zero sales CTAs. It is their real Hiring Events page, and it works because
  their reader is already an Indeed customer. Ours is a conversion page. Don't
  copy their post-purchase vocabulary.

---

## 4. Traps that have already cost time

- **`box-sizing` is `content-box` on this site.** `max-width` applies to the
  content box, so a container renders ~40px wider than its stated max-width.
  Pin `box-sizing:border-box` on anything where the number matters. This is why
  the cards first came out 316 instead of 306, and why the format section is
  really 1244 wide, not 1180.
- **Never `loading="lazy"` inside the brand panels.** Four of five panels parse
  hidden and Chrome never re-evaluates them, so the image renders empty.
- An `<img>` with its own intrinsic ratio will stretch a fixed-ratio frame.
  Take it out of flow (`position:absolute;inset:0`) or the frame is ignored.
- `app.css` is a **compiled** Tailwind build with no runtime. New classes do
  nothing. Everything new ships as scoped `.jfx-*` CSS.
- The captured DOM uses `../../../../` relative asset paths — absolutise them.
- **Live-site bug:** the post-event report mock is dated to a different stale
  event on every type (Apr 22 2026 Healthcare, Nov 13 **2025** Technology,
  Mar 11 Diversity, Feb 12 Veterans, May 6 Entry-Level). Told to the developer.

---

## 5. Open, waiting on Scott

1. **Does the cards page ship?** If yes, the dev notes need rebuilding — Change 1
   becomes the four boxes instead of the navy band.
2. **Do the layout-audit fixes ship?** Built, measured, never ruled on.
3. **Two videos to make:** "Change Interview Settings" and "Review Post-Event
   Results" — both already on the tutorial library's planned list. They'd turn
   cards 3 and 4 from articles into videos.
4. **Thumbnails** for all four cards. Proposed treatment: framed app screenshot
   on brand navy `#00245B`, one short label — the V3 video treatment.
5. **Voice licence.** The tutorial library still prints "en-US-AvaNeural (draft,
   not licensed for commercial use)". Scott says he has commercial rights;
   confirm that note is stale before any clip goes on jobfairx.com.
6. **Help-centre URLs.** The help centre is on claude.ai artifact links today.
   The developer needs real jobfairx.com URLs.
7. **Day of event tips** section: recommended against. Indeed's version is two
   parts damage control ("Troubleshooting Device Issues"), which advertises a
   problem on a page where someone is deciding whether to buy.

---

## 6. Assets made in this stream

`walkthrough-poster.jpg` (1052x586, frame at 1:50 of the demo) ·
`brand-healthcare|technology|diversity|veteran|entry-level.jpg` (800x400, 2:1) ·
`card-interviewers.jpg`, `card-settings.jpg`, `card-report.jpg` (crops of
`assets/product/*`)

---

## 7. How to deploy

The preview site is this repo's `main` branch via GitHub Pages. Upload through
the GitHub web UI, then **verify the deployed bytes match the local file** before
telling anyone it is live — a commit occasionally does not land:

    L=$(shasum -a 256 <file> | cut -d' ' -f1)
    curl -s "https://scottjobagent.github.io/jobfairx-marketing-preview/<file>?cb=1" | shasum -a 256
