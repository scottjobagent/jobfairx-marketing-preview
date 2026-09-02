# Indeed product-video reference — "Adding Users and Setting Access Levels"

**Source:** YouTube `vLxxWX4-oSI`, embedded on
https://www.indeed.com/help/employers/articles/206589143
Title: *Indeed Employer Account Access: Add, Edit & Control Team Permissions*
Runtime 2:24 (144s) · 1280×720 · Indeed for Business channel, unlisted, ~983 views.

**Local copy (gitignored, never publish — Indeed's copyrighted material):**
`assets/_reference-do-not-publish/indeed-users-video/indeed-users-permissions.mp4`
plus `frames/t001–t048.png` — one full-resolution frame every 3 seconds.

**How this was analysed:** watched frame by frame (browser playback plus the
extracted frames), colours sampled from actual pixels with PIL. Not from the
transcript. To re-watch or extract more frames, see the toolkit note at the
bottom.

This is the second Indeed video studied for the JobFairX explainer — the first
was the check-in tool overview that the event-day lobby video is modelled on.
This one is the better reference for *form-and-permission* flows.

---

## 1. The six screen types

The whole video is built from six repeating layouts. Nothing else appears.

| # | Screen | When | Construction |
|---|---|---|---|
| 1 | **Brand card** | 0–5s | Flat navy; a large tone-on-tone lighter-blue organic wave behind the white lowercase wordmark. Depth from a flat shape, not a gradient. |
| 2 | **Title card** | 5–10s | Flat navy, white two-line title, left-aligned, nothing else on screen. |
| 3 | **Numbered agenda** | 10–16s | Darker-navy rounded banner across the top, then numbered rows building in one at a time. |
| 4 | **Step banner + app** | 16–41s, 70–88s, 112–130s | The numbered pill pins to the top of the navy field; a Mac-chrome browser window sits below it and bleeds off the bottom edge. |
| 5 | **Isolated modal** | 41–70s, 88–112s | The dialog alone, floating on flat navy. All surrounding page chrome gone. |
| 6 | **Recap + end card** | 130–144s | The agenda layout returns with all three items, then a disclaimer over a faded watermark, then a text-only CTA card. |

### Measured geometry (at 1280×720)

**Agenda / step-banner component** — the same component in both places:
- Header banner: 836 × 84, radius ~8, inset 221px from left
- Number circle: 104px diameter, solid white, navy numeral
- Label pill: 670 × 68, radius ~10, **transparent fill with a 2px white stroke**
- The circle **overlaps the pill's left edge** — it is not adjacent to it. This
  overlap is the detail that makes the component read as designed rather than
  as two stacked boxes.
- Vertical rhythm between agenda items: 140px

**Isolated modal (screen 5):**
- Modal 527 × 482 — only **41% of the frame width**, floating in open navy
- Radius ~6, soft shadow, near-white surface
- Segmented control inside: active tab is a dark navy pill, inactive is white
- The primary button sits in its **disabled** state (`#97b6e8`) until the email
  field is filled, then goes solid blue — the state change is part of the story
- Cancel is a ghost text button; fine-print legal text sits below the buttons

**Step banner + app (screen 4):**
- Browser window 1070px wide, navy margins ~105px left and right
- Window top at y≈193, **bleeding off the bottom of the frame** — never a
  fully-contained floating card
- Full Mac chrome retained: traffic lights, tab, URL bar showing `indeed.com`

**End card:** two large flat circles at different blues, one bottom-left and one
top-right, both running off-frame; left-aligned white text at x=248; the URL
bolded inline. No button, no logo.

---

## 2. Colour scheme (sampled from the frames, not guessed)

| Role | Hex |
|---|---|
| Primary ground (title, agenda, modal isolation) | `#0f2a58` / `#0b2a5d` |
| Agenda banner strip (darker) | `#001a3e` |
| End-card ground | `#062e6c` |
| Decorative blobs / circles | `#0a357d` → `#2761ae` |
| Surfaces (modal, app) | `#fdfdfd` |
| Disabled primary button | `#97b6e8` |
| Destructive action | red — **used exactly once**, on "Yes, remove" |

That is the entire palette: one navy family at four or five values, white, one
blue for action, and red held in reserve for the single destructive step. The
decorative shapes are always the same blue 10–30% lighter, flat-filled, never
gradients.

---

## 3. Motion grammar

- **Sequential list build.** Agenda items appear one at a time, ~1.5–2s apart,
  paced to the narration. Nothing appears before it is spoken about.
- **Pin and zoom.** The step banner holds position while the screenshot beneath
  it scales from framed card to bleeding off the edge. This is the only camera
  move in the video.
- **No lateral pans anywhere.** Transitions are cuts and scale-ups only — the
  same rule already locked for the JobFairX video.
- **Real cursor, real app.** The actual pointer travels, clicks and types. There
  are no highlight rings, spotlights or callout arrows at any point. They even
  leave the app's real grey loading skeleton on screen mid-transition, which
  reads as authenticity rather than as a mistake.
- **State changes carry the beat.** The disabled→enabled button, the tab flip
  from "Currently used" to "All options", checkboxes ticking — the UI's own
  state transitions are the animation.
- **Bookend symmetry.** The agenda screen at 10s returns at 130s as the recap,
  the same layout with all items present.

---

## 4. What is worth taking for JobFairX

1. **Modal isolation — the strongest idea here.** When a step happens inside a
   dialog, cut to the dialog alone on the brand ground. Our video currently
   solves every beat with whole-page crops plus callout rings; for the
   form-heavy beats (Interview Settings, the reschedule modal, the Yes/No/Maybe
   evaluation) isolating the dialog would remove all page noise and let the
   viewer read the form. It fits our existing single-accent colour law and the
   no-pan rule without changing either.
2. **One component doing double duty.** Their numbered circle+pill is the
   agenda, the step banner, and the recap. Reusing one component across all
   three roles is what makes a 2-minute video feel systematic.
3. **Red reserved for the destructive step only.** We already treat green as
   success-only; the same discipline on red is free consistency.
4. **Letting the product's own state changes be the animation** rather than
   adding motion on top — cheaper to build and more honest.

**What not to take:**
- The brand card and title card opening. Scott cut our intro title card
  deliberately; do not reintroduce it.
- The 41%-width modal floating in a large empty field. Their story is sparse
  enough to carry it; ours is denser and our frames are already committed to
  whole-page views. Isolate the modal, but crop tighter than they do.
- Their agenda screen as-is. Ours uses chapters on the scrub rail, which does
  the same job without spending 6 seconds of runtime.

---

## 5. Re-watching this or any other video

The toolkit lives at `~/.venvs/watch/` (outside this repo):

```bash
~/.venvs/watch/bin/yt-dlp-live -f "bv*[height<=720][ext=mp4]/b[ext=mp4]/b" -o out.mp4 <url>
FF=$(~/.venvs/watch/bin/python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FF" -i out.mp4 -vf "fps=1/3" frames/t%03d.png
```

Use `yt-dlp-live` (the official standalone binary), **not** the pip-installed
`yt-dlp` in the same venv — system Python is 3.9, so pip resolves to a version
too old for current YouTube. Pillow is installed in that venv for pixel
sampling. Full notes in the `video-watching-capability` memory entry.
