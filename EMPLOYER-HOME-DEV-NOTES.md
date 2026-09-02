# employer-home.html — developer notes

Final as of 25 Aug 2026. Scott signed off on desktop and mobile. This page is a
prototype for the content update to jobfairx.com/employer; it is not a redesign
of the site chrome.

## Header and footer: use the LIVE site's current design

Scott's instruction, verbatim intent: the header and footer are already done on
the live site. Keep the header and footer exactly as they exist on
jobfairx.com/employer today, desktop and mobile, and apply only the page
content between them from this prototype. Any header/footer differences you
spot in the prototype (including the mobile footer's hidden column labels) are
artifacts of the 23 Aug capture. Do not port them; the live chrome wins.

## What changed vs the live page (the actual update)

Rebuild diffs are all encoded in `build-employer-home.py` (read its section
comments top to bottom; every step asserts against the captured DOM). Highlights:
- Title/meta/og/twitter: "Virtual" removed ("Hiring Event Platform for
  Employers"); hero headline "Hire faster with in-person and video interviews";
  hero supporting copy updated.
- How It Works: step order and copy per Scott (registration first); Event day
  step is "Interview in person, video, or phone" with the Interview Settings
  panel visual; Review & confirm step uses real product screenshots
  (`assets/product/review-confirm.png` desktop, `review-confirm-mobile.png`
  under lg, both referenced with `?v=2`).
- Pricing card bullets, All Packages Include reduced to 8 items (dashboard item
  removed; list now matches the pricing page word for word).
- Final CTA and footer-link copy edits ("Hiring Event Platform").

## Deliberate, signed-off content (do not "fix")

- The Difference section is live-verbatim by Scott's explicit decision,
  including "Interviews auto-scheduled", "Passive applicants", "Post and pray",
  and the red X marks.
- The Trusted By marquee logos: Scott confirms the developer already has this
  handled; ship per the live site.
- The results cards' stat tiles (36/7, 92/19, 51/14) stay as-is per Scott.
- Meta descriptions' "book interviews" phrasing stays as-is per Scott.
- Testimonial quotes are verbatim and never edited.
- Interview-format phrasing varies on purpose: hero says "in-person and video"
  (phone deliberately not in the hero), the Event day step and All Packages
  Include say "in-person, video, or phone", tier cards say "In-person or video
  interviews". Documented decisions, not inconsistencies.

## Wiring the developer must do

- Mobile hamburger: drawer never opens in the prototype; wire per live site.
- The page now ships exactly ONE inline script, seven lines, at the end of the
  body. Its only job is the reschedule tutorial: on click it swaps the poster
  for a `<video controls autoplay>`. Everything else on the page is still static.
- The three "Reserve My Spot" buttons and the Growth card's Events stepper are
  inert; production behavior should match the live pricing page's component
  (bundle rungs 1-4 then 5/10/15/25/40/50/75/100; cart URL uses bundle=<id> at
  bundle counts, else pkg+qty).
- Dead anchors: "See how it works" in the Review & confirm step is href="#";
  the four "View Event Details" rows in the step-1 calendar mock are mock
  content. The calendar mock's events/dates are illustrative (late Aug 2026)
  and should be rendered from the real event feed in production.
- Analytics, JSON-LD, and tracking scripts were stripped at capture; production
  keeps the live site's own.

## Assets and build

- Never edit employer-home.html by hand. Edit `build-employer-home.py`, rerun.
  Source of truth: `assets/live-capture/employer-live-dom.html` (23 Aug 2026).
- Local stylesheets: `assets/employer-home/app.css` and `page.css` with `?v=2`
  cache-busters (bump CSS_V in the builder on any CSS change).
- Product screenshots: `assets/product/review-confirm.png` (824x609 css @2x)
  and `review-confirm-mobile.png` (584x651 css @2x); the two <img> swap at the
  lg breakpoint. Regeneration recipe is documented in the session notes if the
  lobby UI changes.
- Font Awesome Pro 5.10.0 loads from pro.fontawesome.com with an SRI hash (as
  live). FA Pro is domain-licensed; if the production domain ever changes,
  self-host it.
- og:image still points at https://jobfairx.com/images/og-image.png; canonical
  is https://jobfairx.com/employer. Both correct for production.


## Reschedule and follow-ups section (added 26 Aug, Scott-approved)

Sits between How It Works and Hiring Event Results. It replaces the live site's
scroll-pinned "Built-in Tools / Candidate Messaging and Interview Scheduling"
block, which was removed from this page on 24 Aug.

- Built by `build-employer-home.py` section **8g**. Edit the builder, never the
  output.
- Layout: two columns. Copy and a three-point checklist left, the employer
  tutorial right. Scott picked this from three rendered options.
- **Headline must not contain a `<br>`.** An explicit break creates a phantom
  line box and the heading renders on three lines at every size down to 32px.
  Left to wrap naturally at `lg:text-[40px]` it breaks after "and", which is the
  break Scott marked up. Verified by counting client rects.
- There is no supporting paragraph by design; Scott cut it because the three
  points say the same thing.
- **Background is brand navy, `bg-brand-dark` (#00245b)** — the only dark band
  in the body of the page. Chosen 26 Aug from a three-way comparison. The
  reason is structural: from this section down the page was white, white,
  white, white (Reschedule, Hiring Teams, Pricing, closing CTA), so the
  alternation flatlined for the whole bottom half. A slate-50 tint was tried
  and rejected because How It Works directly above is also slate-50, which
  erased the boundary above while fixing the one below. No border is needed;
  the tone does the separating.
- On the dark band: eyebrow `text-blue-400`, headline `text-white`, item
  titles `text-white`, item copy `text-slate-300`, check chips `bg-blue-500`
  with a white tick. All five are already compiled in app.css.

### The video

- Poster `developer-tutorial-reschedule/thumbnail.jpg` (2560x1440), file
  `developer-tutorial-reschedule/jobfairx-01-reschedule-candidate-1080p.mp4`
  (3.3 MB, 1920x1080, 1:04, captions burned in). Both already live in the
  preview repo; the page references them by relative path.
- The play button, progress bar and "1:04" are a designed still, not a real
  player. Clicking swaps in a native `<video controls autoplay>`.
- **To move to YouTube:** upload per
  `developer-tutorial-reschedule/index.html` (that page carries the title,
  description, transcript and the do-not-upload-captions rule), then replace the
  `<video>` string in section 8g's `TUT_SCRIPT` with the iframe embed. One line.
  Do not add a caption track: the captions are burned into the picture.

## Hero copy (changed 26 Aug)

Headline and subcopy are set by section **8h**, from Scott's marked-up
screenshot, verbatim:

- "Meet interview-ready candidates at hiring events built to hire."
- "Post the roles you need to fill, meet candidates matched to your openings,
  and interview them in person, by video, or by phone."

Line breaks are `hidden lg:block`, so the phone wraps naturally. Note this
changes the interview-format ladder documented below: the hero previously said
"in-person and video" and held phone back until the Event day step. Scott's copy
names all three in the hero.

## Hero video: unauthenticated fetches lie about it

The hero embed (`QuRalPnpPLA`) **plays correctly in a real browser** — verified
26 Aug on the deployed preview. But do not trust automated checks on it:

- `youtube.com/oembed` returns **403**
- the watch page fetched without cookies contains `UNPLAYABLE` and
  `LOGIN_REQUIRED` and an empty title
- a headless render with no cookies shows "This video is private"

That pattern is consistent with an unlisted video plus YouTube's consent wall
for anonymous requests, not with a broken embed. The embed URL itself returns
200 and the poster, title and Watch-on-YouTube button all render for a signed-in
user. Same note as the existing "Error 153 only in offline rendering" quirk
below: check this one in a browser, never in a script.

## Verification

- `python3 tools/mcheck.py employer-home.html` must stay clean (true-390
  overflow probe).
- YouTube hero embed (QuRalPnpPLA) verified playing on the deployed preview;
  an "Error 153" appears only in offline/file:// rendering.
