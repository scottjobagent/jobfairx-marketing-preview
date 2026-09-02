# HANDOFF-VIDEO.md — JobFairX Hiring-Event Product Video

**Complete project transfer. Written 2026-08-24 (late), at the moment the conversation hit
its context limit. The next session continues exactly here with zero rediscovery.**

This is the handoff for the **product-video stream** of the JobFairX marketing work. It is a
sibling of `HANDOFF.md` / `HANDOFF-2.md` / `HANDOFF-3.md` (marketing-site streams — separate
work, do not confuse). Persistent memory files also exist under
`~/.claude/projects/-Users-scottl--Desktop/memory/` (see `event-day-lobby-explainer.md`),
but THIS document is the authoritative, self-contained record.

---

## 1. Executive Overview

- **Project purpose:** An enterprise-grade product demo video for JobFairX — the employer
  experience of running a hiring event: the event-day lobby, choosing how to interview
  (video / in person / phone), the interview workflow, and turning conversations into hires.
- **Origin:** Scott asked for a JobFairX equivalent of Indeed's help-center video
  *"Indeed's Check-In Tool – Setup and Usage"* (YouTube `n2a4yKFaHhc`, 2:34, unlisted,
  embedded at indeed.com/help/employers/articles/check-in-tool-overview). Its full
  transcript was captured early in the project and its structure (access → candidate table
  → check-in → statuses → metrics → recap) shaped the first cut. The video has since
  evolved far past that reference under Scott's direction.
- **What the deliverable IS:** a self-narrating HTML "video" — a 16:9 player that plays
  scenes (real product screenshots with timed highlight rings and effects), synced captions,
  an embedded per-scene voiceover track, chapters, and a scrub bar. It is published as a
  Claude artifact and doubles as (a) the review/approval vehicle and (b) the base for a
  screen-recorded MP4 later.
- **Business context:** JobFairX runs hiring events for employers. Employers register for an
  event, pick how they interview (video on the JobFairX platform / in person / phone), and on
  event day work a lobby of candidates. Target audience of the video: first-time employers.
- **Current phase:** Content-complete on the Healthcare V3 prototype with real two-person
  interview visuals. Scott is actively reviewing round by round. **The immediate open item
  is his voice choice** (16 samples were just sent — see §4).

### Canonical links & paths
- **Artifact (the video, stable URL across every republish):**
  `https://claude.ai/code/artifact/dd475d54-f6ca-434d-a6e9-fe8138a33db0`
- **Durable output:** `Desktop/jobfairx-marketing/video-event-day-lobby.html`
- **Build system (synced copies in `Desktop/jobfairx-marketing/`):**
  `build-video.py`, `video-template.html`, `capture-healthcare.py`
- **VO clips + cue sheet:** `Desktop/jobfairx-marketing/vo-draft/` (`s*.mp3`, `timing.json`)
- **Screenshots:** `Desktop/jobfairx-marketing/assets/product/*-hc.png` (current set)
- **Prototype (SOURCE OF TRUTH):**
  `https://scottjobagent.github.io/jobfairx-prototype/visual-v3-healthcare.html`
- The working copies this conversation actually edited live in the session scratchpad
  (`/private/tmp/claude-501/-Users-scottl--Desktop/<session>/scratchpad/`) — **volatile**.
  Everything important was synced to `jobfairx-marketing/`; treat the repo copies as truth.
  A Python venv with `edge-tts` and `Pillow` was at `scratchpad/vo-env/` — a new session
  must recreate it: `python3 -m venv vo-env && vo-env/bin/pip install edge-tts pillow`.

---

## 2. THE FINAL SCRIPT — LOCKED, VERBATIM, NEVER PARAPHRASE

Scott delivered this as the source of truth with an explicit instruction: *use exactly as
written; do not add, remove, or paraphrase words.* Chunk splits (for captions/timing) are
allowed; word changes are not. The built narration was verified verbatim programmatically.

**Section 1 — The Lobby**
1.1 This is the event-day lobby — your entire hiring event, live and organized in one place.
1.2 You can see your candidates, manage interviews, and keep your hiring event moving.

**Section 2 — Choose How You Interview**
2.1 When you register for an event, you choose how you want to interview candidates: video, in person, or phone.
2.2 For video interviews, interviews take place on the JobFairX platform. For in-person interviews, candidates receive the location and instructions they need for their interview.
2.3 And for phone interviews, you call the candidate at their scheduled interview time.

**Section 3 — Interviews**
3.0 When a candidate logs in for their interview, they appear in the Waiting Room. This lets you know the candidate is online and ready for their interview.
3.1 When the candidate joins their scheduled interview, they move from the Waiting Room into an Interview Room.
3.2 When the interviewer joins, the interview begins in the Interview Room. At the same time, the interview moves from the Waiting to Interview tab to the Interviewing tab, making it easy to see which interviews are currently in progress.
3.3 When the interview ends, the interviewer is asked whether the candidate is a good fit for the role. They can select Yes, No, or Maybe.
3.4 The interview then moves to the Interviewed tab, and the interviewer is returned to the Waiting to Interview tab, where they can start their next scheduled interview.

**Section 4 — Event Status**
4.0 The four tabs show the state of your event — waiting to interview, interviewing, interviewed, and not yet interviewed.
4.1 The counts update automatically throughout the day. Interviewed gives you a running total of completed interviews.

**Section 5 — Conducting Video Interviews**
5.1 Select Start Interview to open a JobFairX video room. There's nothing for the candidate to download or install.
5.2 The interviewer controls the conversation, with no time limit on the interview. When the interview is complete, simply select End.
5.3 Notes taken during the interview and how you rated the candidate are available after the event.

**Section 6 — Recap**
6.0 That's a hiring event on JobFairX. Open the lobby, meet candidates, run your interviews, and turn conversations into hires.

Scott also delivered a 17-point enterprise production brief with the script. Its standing
requirements: every line's visual must make the line understandable on its own; no dead air;
no over-animation; one idea highlighted at a time; minimal text overlays (short uppercase
section labels only); visuals never ahead of or behind narration; the recap ends on the
strongest visual plus a brief brand card; QA by watching the whole output, not just scenes.

---

## 3. Current Video — exact state (2:09, voice Ava, 10 scenes / 6 chapters)

Scene list as built in `build-video.py` (`SCENES`). All frames are REAL screenshots from the
Healthcare V3 prototype. `crop=(W, ox, oy)` is a 16:9 window in the image's natural pixels;
every scene is ONE steady view (≤3% centered push-in via `ZOOM = 0.97`; `zoom=False` =
static; negative `ox` = pillarboxed contain-fit). Rings = `callouts=(x,y,w,h, capIdx, +delay-s)`.

| id | Chapter | Image | Framing | What happens |
|---|---|---|---|---|
| s1 | The Lobby | `lobby-tables-hc.png` | (3200,0,0) | Cold open, full lobby, no rings. Label THE LOBBY. |
| s2 | Choose How You Interview | `dashboard-events-hc.png` | (2100,700,530) | Rings sweep the Interview-location column top-to-bottom: Video → In person → Phone (matches narration order). Label chip fully covers the EVENT DETAILS header (deliberate full-cover). |
| s3a | Interviews | `lobby-tables-hc.png` | (3200,0,485) | WAITING ROOM label. Rings: Waiting-rooms header → status pills (Entering interview room / Awaiting available interviewer) → Interview-rooms header. |
| s3b | Interviews | `lobby-interviewing-hc.png` | (3200,0,0), zoom=False | INTERVIEWING label. WHOLE page per Scott — nothing clipped. Rings: "Interviews in progress (3)" header (100,764,650,90) → active Interviewing tab (1050,586,330,108) → Interviewer column incl. header (2350,876,340,450). |
| s3c | Interviews | `room-recmodal-hc.png` | (3556,−178,0), zoom=False | CANDIDATE FIT label (top-right), caption on TOP. The REAL prompt "Would you recommend moving forward with James Cooper?" over the dimmed live call; ring on Yes/Maybe/No toggle (1120,790,650,110). |
| s3d | Interviews | `lobby-interviewed-hc.png` | (3200,0,150) | INTERVIEWED label. Rings: Interviewed tab (1820,588,320,110) → Feedback column of Yes/No/Maybe pills (1765,975,320,630) → back to Waiting-to-interview tab (240,588,420,110). |
| s4 | Event Status | `lobby-tables-hc.png` | (3200,0,150) | Rings: whole tab strip (60,574,3020,124) → a "+1" pill rises at (2085,465) on "counts update automatically" → Interviewed tab (1820,588,300,110). |
| s5a | Conducting Video Interviews | `lobby-tables-hc.png` | (1700,1440,660) | Close-up; ring on **James Cooper's** Start Interview button (2690,1108,392,92) — row 2, chosen for candidate continuity with the room. |
| s5b | Conducting Video Interviews | `room-late-hc.png` | (3556,−178,0), zoom=False | Caption on TOP, label top-right. Two people on camera. Rings: call controls (1395,1838,450,160) → End incl. its label (1700,1840,130,155) → Notes only (2780,1865,130,130). |
| s6 | Recap | `lobby-tables-hc.png` | (3200,0,0) | Holds the lobby; runtime end card: "JobFairX / Turn conversations into hires." + Replay. |

VO chunking (captions) differs slightly from the section numbering: long script sentences
were split at sentence/comma boundaries into caption-sized chunks WITHOUT changing words
(e.g. 2.2 → two chunks; 3.2 → two chunks). The exact chunk lists are in `SCENES[*]['vo']`.

**Voice:** currently `en-US-AvaNeural` (Scott picked Ava over Emma; Emma over Andrew before
that). **A full 16-voice sample set was just sent and Scott has not yet chosen** — that is
the live open loop. Rebuild with any voice: `vo-env/bin/python build-video.py en-US-<Voice>Neural`.

**Timing model:** scenes are packed from measured audio: `LEAD = 0.4` s from scene cut to
first word; `GAP = 0.5` s from last word to next cut → ~0.9 s between scenes everywhere
(Scott: "long pauses are errors"; the build prints a pause audit; max observed 0.93 s).

---

## 4. Current Work in Progress (CRITICAL — where we stopped)

**The very last action:** Scott asked to hear all voice options again. Sixteen samples
(all US edge-tts neural voices, each reading final-script line 1.1) were generated to
`scratchpad/voices2/` and sent to him as files: Ava (current), AvaMultilingual, Aria, Emma,
EmmaMultilingual, Jenny, Michelle, Andrew, AndrewMultilingual, Brian, BrianMultilingual,
Christopher, Eric, Guy, Roger, Steffan.

**Next expected message from Scott: a voice name.** On receiving it:
1. `vo-env/bin/python build-video.py en-US-<Name>Neural` (from a scratchpad containing the
   build files + `vo/` dir + venv; or run in `jobfairx-marketing/` — the script's paths are
   absolute for assets, relative for `video-template.html`, `vo/`, and its output).
2. Verify the build log shows no `!!` warnings and pauses ≤ ~0.95 s.
3. Republish the artifact **to the same URL** (publish the same file path from the owning
   conversation, or pass `url:` from a new one — never publish without `url` from a new
   session or it forks a second artifact).
4. `cp` the html to `jobfairx-marketing/video-event-day-lobby.html`, refresh `vo-draft/`.

There is no other in-flight edit. The video itself is content-complete pending Scott's
next review pass.

---

## 5. Architecture — how the whole thing works

There is no app framework, no routing, no state library. The system is three files plus
assets, deliberately shaped like Scott's existing marketing "builder" pattern
(`build-employer-home.py` etc. — Python builders that regenerate HTML):

```
jobfairx-marketing/
  build-video.py            # THE build: scenes data + VO synthesis + timeline + assembly
  video-template.html       # player shell with %%PLACEHOLDERS%%
  capture-healthcare.py     # screenshot capture harness for the Healthcare V3 prototype
  video-event-day-lobby.html# the built video (durable copy of the artifact)
  vo-draft/                 # per-scene VO mp3s + timing.json cue sheet
  assets/product/*-hc.png   # current captures (see §7)
  tools/capture.py          # Scott's original harness — NEUTRALISE list lives here (load-bearing)
  tools/*-v3-healthcare.html# downloaded prototype pages (re-download if stale)
```

### 5.1 build-video.py (the heart — read top to bottom before touching anything)
Pipeline per run:
1. **SCENES** list: per scene — id, title (chapter), label (on-screen chip), optional
   `labelPos='tr'`, `capTop=True`, img key, crop, optional `zoom=False`, callouts, `fx`
   (image-coord effect HTML with `__D__` delay placeholder), `ov` (design-coord overlay
   HTML), onscreen (script-section prose), `vo` (caption chunks — final script verbatim).
2. **Synthesis:** per scene, chunks joined with a space → one `edge_tts.Communicate(text,
   VOICE, boundary='WordBoundary')` stream → mp3 + word-boundary offsets. **Alignment
   assert:** count of word events must equal count of alphanumeric-containing tokens; the
   per-chunk caption offset = offset of its first word. (edge-tts 7.2.8: word boundaries
   ONLY arrive with the `boundary` kwarg; default is SentenceBoundary.)
3. **Timeline:** scene start = running cursor; VO anchor = start + LEAD; next cursor =
   anchor + measured audio + GAP. `CAPS` = [absolute-time, text] pairs; `VOTRACK.clips` =
   {t, end, base64 mp3 data URI}. DUR = last audio end + 3 s.
4. **check_scene** (build-time QA — do not remove): crop-in-bounds per image
   (`IMG_DIMS` via PIL), every ring inside the zoomed end-crop, **caption-zone rule**
   (ring bottom in design px must be ≤445 for bottom-caption scenes; ≥100 from top for
   `capTop` scenes), **label-chip rule** (no ring with design y<62 AND x<230 on labeled
   scenes). Violations print `!!` in the build log.
5. **Assembly:** emits scene sections (pan div sized per-image via inline style, bg class,
   callouts with computed `--d`, fx/ov with `__D__` replaced, label chip), per-scene
   `@keyframes` (from-crop → zoomed-crop, linear, duration = scene length), image CSS
   classes (base64; **files >1 MB are re-encoded JPEG q86** to keep the page ~4 MB), VO
   clip JS, `SCENES_JSON` (id/start/title/capTop), `CAPS_JSON`, `ONSCREEN_JSON`, duration
   labels. Writes the final HTML + `vo/timing.json`.

Transform math: design surface is 960×540; a crop `(W,ox,oy)` renders as
`transform: scale(960/W) translate(-ox px, -oy px)` on a plane holding the image at natural
size. Callout/fx coordinates are in image-natural pixels and therefore stable.

### 5.2 video-template.html (player shell)
- Theme-aware page (light/dark token system per `DESIGN-SYSTEM.md`; player chrome is
  committed dark; Inter via Google Fonts with cv01/ss03; accent #2f5cff family).
- **Player engine** (vanilla JS, IIFE): rAF clock with **dt clamped to 0.1 s** (hidden-tab
  gaps must not leap the clock); `activate()` toggles `.on` per scene — display:none→flex
  restarts that scene's CSS animations (this is the animation clock; **seeking into
  mid-scene restarts scene animations from zero — correct only in linear playback; a
  known, accepted artifact**); captions = last CAPS entry ≤ t; caption bar position
  toggles via `capTop` (`.caps.top{top:64px}` — 64, not 16, so it clears the label chips).
- **Voiceover:** `VOTRACK` clips follow the shared clock: `voFind(t)` picks the clip,
  drift >0.4 s snaps `audio.currentTime`, pause/play/seek/mute all routed through
  `voUpdate()`. Debug state is exposed on `#player[data-vo]` ("on|idx|playing|ct") because
  browser-pane JS runs in an isolated world (see §10). Speaker toggle button in controls.
- **Chapters:** rail ticks + chips deduplicate consecutive scenes sharing a title, so ten
  scenes render as six sections.
- **Section labels:** `.slabel` chip top-left (or `.tr` top-right), over a
  `.shot.has-label::before` top gradient scrim (72px) so chips never sit on raw UI.
- **Effects CSS:** `.co` ring pulse (4.6 s, `--d` delay); `.fx-plus` (+1 pill, 64px font —
  image-coord elements scale by ~0.3 so sizes are ~3× design intent); `.fx-flow` and
  `.fx-under` exist but are currently unused (see Lessons); `.fit-scrim/.fit-card` exist
  but unused since the real modal capture replaced the reconstruction.
- Poster (lobby bg + play disc + duration chip), end card ("JobFairX / Turn conversations
  into hires." + Replay), keyboard (space/k, ←/→ 5 s, Home), pointer-capture rail seek
  wrapped in try/catch, `prefers-reduced-motion` handling, script section below the player
  auto-built from SCENES (timecodes, On screen, Voiceover), production-notes list.

### 5.3 capture-healthcare.py (screenshot harness)
Downloads nothing itself — expects prototype pages already in `tools/` (curl them from
`scottjobagent.github.io/jobfairx-prototype/<page>` if missing). For each shot: injects a
script into the local page copy, renders headless Chrome
(`--force-device-scale-factor=2 --window-size=1600,1000` → 3200×2000; `tall=True` shots
use 1600×1250 → 3200×2500), `--virtual-time-budget` drives fake time (863000 ms ≈ a 14:23
call timer). The injection, in order: dismiss the JobAgentX survey modal
(`jaxModalDismiss()` — **AI agents must NEVER appear in JobFairX demos**, standing rule);
set dashboard/lobby Live mode via the prototype's own `setDevMode`/`setLobbyMode` (the
bottom-left A/L corner toggles Scott pointed out; **the `?mode=live` URL param does NOT
work on the healthcare lobby**); click "Start interviewing" (`goOnline`) so status reads
Available and the banner clears; click a lobby tab (visible-filtered `.tab` match) then
**rebuild the tab strip's DOM** (headless repaint bug: class changes alone leave stale
active-tab styling — dump-DOM proved classes correct while pixels were wrong); run
per-shot `evalJs`; hide `.dev-toggle-corner/#lobbyDevToggle`; run the **NEUTRALISE** text
replacements imported from `tools/capture.py` (real-company names → Northwind, PII-looking
names → fictional, banned vocabulary fixes — **always reuse this list; it is load-bearing**
per HANDOFF.md §7); optional scroll.

Room-shot specifics (`room-late-hc`, `room-recmodal-hc`): URL query
`?candidate=James%20Cooper` (sets the name chip and the recommend-modal name); unmute
click; **photo compositing** — `tech.d1d87547.jpg` (paid, from the live event-detail page)
into `.iv-video-main`, `recruiter.63204f89.jpg` into `.iv-pip` (NOT `.iv-floating-self`,
a stray hidden tile that must be display:none'd), single restyled "You" chip, and the
"Start Video" center label text-swapped to "Stop Video" so controls agree with cameras-on.
The recmodal shot additionally opens `#recModal` via its `.open` class (the page's own path).

---

## 6. Chronological record of the whole project (what, why, files)

1. **Indeed research.** Fetched the help article; found the YouTube embed; captured the
   full transcript by replaying the player's tokened `timedtext` request (bare requests
   return empty 200 — needs the `pot` token; grab the URL from the network log). Key frames
   screenshotted for structure. Why: mirror their beats before adapting.
2. **V1 (mock-UI, 2:36, 9 scenes).** Animated hand-built lobby/dashboard/room mocks styled
   from `DESIGN-SYSTEM.md`; scenes as 960×540 surfaces; captions; chapters. Adapted
   Indeed's QR scene into "check-in happens on its own." Bugs fixed en route: quirks-mode
   table color inheritance (meta charset + explicit colors), rAF hidden-tab clock leap
   (dt clamp), nth-child animation mis-indexing, a `var VO` name collision (renamed VOTRACK).
3. **Voiceover pipeline.** edge-tts chosen after testing (`say` voices poor; only Samantha
   installed). Word boundaries via `boundary='WordBoundary'`. Captions retimed from word
   offsets. Per-scene clips embedded as data URIs; clock-synced playback with drift snap.
   **Licensing research (agent fleet):** edge-tts output is NOT licensed for commercial
   use — draft only. Production paths: **ElevenLabs hosted MCP**
   (`claude mcp add --transport http elevenlabs https://api.elevenlabs.io/v1/mcp` then
   `/mcp` OAuth in an interactive session; free tier is contractually non-commercial;
   Starter ~$6/mo ≈ 30 min TTS with commercial license), **Azure AI Speech F0** (500K
   chars/mo free, licensed, same voice family), **OpenAI TTS** (~$0.05/take). No TTS
   connector exists in the claude.ai registry (searched).
4. **Scott review #1:** real screenshots, full-frame ("size of the screen, not this black
   background with this little image"), cut the ~11 s title card, never show the candidates
   page (only nav page not live), lobby is the best subject. Rebuilt on the 14 existing
   `assets/product` captures; added "Pick where interviews happen" scene (his new
   in-person feature; order video → in person → phone; **the in-person address goes to the
   candidate with their scheduled interview and is NEVER posted on the event**).
5. **Scott review #2:** voice → **Emma**; **no lateral pans** ("it's all in one view — you
   don't slide over") → every scene one steady view, subtle centered push-in only, room =
   static contain; **pauses are errors** → GAP/LEAD tightened to ~0.9 s (from 2.4 s; 2:47→2:25).
6. **Transcript-editing session.** Scott edited lines one at a time (video untouched during
   it). Ended with him delivering the FINAL SCRIPT (§2) + production brief.
7. **Final-script rebuild (2:05).** New 10-scene structure; section labels; tab-slide
   underline fx with native-underline masking; +1 pill; flow line; a reconstructed fit
   dialog; caption-on-top for room scenes; chapter dedupe. Cut the Interviews-page scene
   (not in the script). Verified narration verbatim programmatically. 11-agent frame-audit
   workflow found 8 real blockers (ring misalignments, caption collisions, s3b/s3d
   near-identical, candidate-continuity break) — all fixed; person-level tracking dropped
   in favor of section-level to avoid continuity contradictions.
8. **"Go capture the upgrades."** Traced captures to the public prototype + Scott's
   `tools/capture.py`. Captured the real Interviewing tab, Interviewed tab (feedback
   pills!), the REAL recommend modal (`recModal.open`; auto-named), and a late-timer room
   (virtual-time budget). Replaced the reconstruction and the slide effects with real-screen
   cuts.
9. **HEALTHCARE V3 REBASE (Scott: wrong prototype used).**
   `visual-v3-healthcare.html` declared source of truth. Explored every area/state per his
   brief (dashboard A/L, lobby A/L, all tabs, room, modal, setup flow, in-person lobby
   variant). Re-captured all six video screens; re-measured every crop and ring; per-image
   dimensions support added (`IMG_DIMS`, tall 3200×2500 lobby captures). New prototype
   facts: dashboard L mode shows "This event is live"; the location column reads
   Video/In person/Phone top-to-bottom (matches narration order — fixed an old ring-hop
   polish issue); lobby Active mode = pre-event Accept/Decline/Reschedule requests view;
   lobby Live starts status **Away** with a "Ready to start interviewing?" banner.
   10-agent audit + fixes.
10. **Overlap round (Scott's screenshots):** label chip covering a table header; caption
    covering ringed content. → top scrim behind labels; **permanent build-time safe-zone
    checks** (caption zone + chip zone, §5.1); s2 reframed to (2100,700,530) with the chip
    full-covering EVENT DETAILS; two more latent violations the check caught were fixed.
11. **Live-interview round (Scott's screenshots + directive):** Interviewing tab must show
    the WHOLE page (→ (3200,0,0) zoom=False); the interview scenes must show **two real
    people talking** using the paid images from the live event-detail page → photo
    compositing (§5.3), candidate set to James Cooper for photo/name/continuity coherence
    (s5a's ring moved to James's row), top captions moved below the chip band, big captures
    JPEG-re-encoded at embed time.
12. **Voice sampling (current).** Andrew → Emma → **Ava** (current). All 16 US voices just
    re-sampled on the final opening line and sent. Awaiting choice.

---

## 7. Asset inventory (assets/product/, current *-hc set)

| File | Size/dims | Contents | Used by |
|---|---|---|---|
| `dashboard-events-hc.png` | 3200×2000 | Events dashboard, LIVE mode, survey dismissed. Dallas (Video·live) / Omaha (In person, Greenleaf Center Omaha addr) / Chicago (Phone). | s2 |
| `lobby-tables-hc.png` | 3200×2500 (tall) | Full live lobby, status Available: header, countdown, 4 tabs (6/3/11/14), Interview rooms (Sarah Mitchell RN / James Cooper / Sofia Martinez — Ready + Start interview) and Waiting rooms (Derek Washington Entering interview room / Marcus Johnson + Priya Patel Awaiting available interviewer). | s1, s3a, s4, s5a, s6 |
| `lobby-interviewing-hc.png` | 3200×2000 | Interviewing tab active: Interviews in progress (3) with interviewer names (Emily Okafor/Maria Lopez/David Park — Okafor is the NEUTRALISE rename of Chen), durations, Rejoin/End. | s3b |
| `lobby-interviewed-hc.png` | 3200×2500 (tall) | Interviewed tab active: 11 candidates with Yes/No/Maybe feedback pills, interviewer, Notes. | s3d |
| `room-late-hc.png` | 3200×2000, ~3.9 MB | Live call: candidate photo full-frame (tech.jpg), recruiter photo in self-view, single "You" chip, timer ~14:23, controls Mute/Stop Video/End, tools Notes/Resume/Chat. candidate=James Cooper. | s5b |
| `room-recmodal-hc.png` | 3200×2000, ~2.7 MB | Same call, dimmed, with the real "Would you recommend moving forward with James Cooper? (Optional)" modal: Yes/Maybe/No toggle, notes field, Done. | s3c |

Older sets still present (`lobby-live.png`, `interviews.png`, `lobby-interviewing.png`
non-hc, etc.) are from the WRONG prototypes — never use them again. Also **never use**
`assets/_reference-do-not-publish/candidate-preview.png` (unlicensed iStock comps —
explicit HANDOFF.md rule). Licensed people photos: `assets/event-detail/tech.d1d87547.jpg`
and `assets/live-capture/img/recruiter.63204f89.jpg` (both ship on jobfairx.com — paid).

---

## 8. Design decisions & philosophy (keep consistent)

- **The product is the hero.** Real screenshots only; effects are restrained rings, one
  idea at a time; no lateral pans (the app is one screen — cuts, not slides); ≤3% push-in.
- **Design system:** everything derives from `jobfairx-marketing/DESIGN-SYSTEM.md`
  (Inter + cv01/ss03; accent #2f5cff/#4a72ff; light canvas #fbfaf8 / dark #0b0d12 token
  pairs; low radii; one depth mechanism per surface). Player chrome committed dark;
  captions dark pills; ring blue with white halo.
- **Copy rules (Scott's standing marketing rules):** outcome headings; no em dashes in
  headings; the locked script is beyond editing entirely.
- **Safe zones are law:** caption zone (design y>445 bottom / y<100 top-caption) and
  label-chip zone (y<62 ∧ x<230) must stay ring-free — enforced in `check_scene`; a chip
  may fully cover one small element (never half-cover text).
- **Pacing:** ~0.9 s between scenes; anything ≥1.2 s prints as LONG in the pause audit.
- **Honesty:** never fabricate UI; the one sanctioned manipulation class is the
  NEUTRALISE-style text/data cleanup + the photo compositing Scott explicitly authorized
  with paid assets. Flag data defects upstream instead of painting over them.

---

## 9. QA methodology (proven; reuse it)

1. **Build-time numeric checks** (in `build-video.py`): word-count alignment assert;
   crop bounds; ring-in-crop; caption/chip safe zones; pause audit vs `vo/timing.json`;
   narration verbatim diff against the final script (done via a one-off script — worth
   re-running after any VO change).
2. **PIL end-frame renders:** render each scene's tightest (zoom-end) framing at 960×540
   with rings/fx drawn, straight from the source PNGs (no browser needed). This caught
   edge clips and misalignments the browser pass missed. For overlay questions, composite
   simulated chip/scrim/caption rectangles too.
3. **Agent audit fleets (Workflow tool):** ~10 parallel reviewers, one per scene frame +
   optionally a cross-scene story reviewer; strict "only what you can SEE" prompts with a
   marker legend. Two such fleets each surfaced real blockers. **Interpretation caveat:**
   the PIL renders do NOT composite runtime elements (captions, label chips, end card,
   fit-dialog) — fleets will report them "missing"; that's noise, verified separately in
   the browser.
4. **Browser verification:** the in-app pane; chapter chips + arrow-key seeks run the
   render pipeline synchronously (works even when rAF is frozen); `#player[data-vo]`
   exposes audio state across JS worlds. See §10 for the pane's many traps.

---

## 10. Environment quirks & lessons learned (expensive ones)

- **Browser pane:** hides whenever Scott switches panels → rAF freezes (clock stops),
  screenshots time out or return stale/black compositor frames. `javascript_exec` runs in
  an ISOLATED world (page globals & constructor patches don't cross — hence `data-vo`).
  Muted media in background tabs gets power-paused (test audio at volume 0.02 instead).
  Local server: `.claude/launch.json` config `lobby-video` (port 8471, serves the scratchpad;
  other sessions own `marketing-verify` 8733, `marketing` 8766, `demo-v2` 8529 — don't touch).
  The claude.ai artifact URL can't be opened in the pane (not signed in).
- **Headless Chrome capture:** `--virtual-time-budget` fast-forwards timers (used for the
  14:23 call timer); bare YouTube-style fetches of guarded endpoints return empty; class
  changes without layout change can PAINT STALE under virtual time (the tab-strip rebuild
  fix); `?query` params work on `file://` URLs; images referenced relatively from the temp
  file resolve against `tools/`.
- **edge-tts:** 7.2.8 needs `boundary='WordBoundary'`; the CLI `--write-media` works for
  quick samples; output is a draft voice ONLY (licensing, §6.3).
- **Artifact:** same file path → same URL. From a NEW session pass `url:` explicitly or
  you fork a second artifact. Page budget 16 MB — the JPEG re-encode keeps us ~4 MB.
- **Dead ends / rejected:** fake tab-underline slide fx (misrepresents; masked native
  underline — all removed once real tab captures existed); flow-line connector (crossed
  glyphs — sequential rings won); person-level ring tracking (continuity contradictions);
  reconstructed fit dialog (replaced by the real modal); lateral pans (Scott veto);
  scrolling captures for tall pages (page too short to scroll — tall viewport instead);
  `?mode=live` on the healthcare lobby (doesn't work — use setLobbyMode).
- **The volatile-tmp lesson** (from the wider project): anything that matters gets copied
  into `jobfairx-marketing/` immediately.

---

## 11. Known issues & upstream prototype data defects (Scott's fix list — flag, don't paint over)

Visible in freeze-frames; all live in the PUBLIC prototype's demo data, so the durable fix
is upstream, then re-run `capture-healthcare.py` + `build-video.py`:
1. Event header says **CT** while every interview row says **PDT**.
2. Non-healthcare roles at the Dallas event (Software Engineer, Data Analyst, Customer
   Service Rep, Sales Rep) alongside RN/Medical Assistant.
3. Two candidates share the identical 11:00–11:30 slot.
4. Upcoming events sort Apr → Jul → May (not chronological).
5. The real toggle order is **Yes | Maybe | No** while the locked script says "Yes, No, or
   Maybe" (align one or the other someday; not misleading, just out of sync).
6. Recommend-modal typography: gray name + bold black "?" reads slightly detached.
7. James Cooper's role differs across tabs (Medical Assistant / Sales Representative).
8. The room's bottom-left chip said "Demo (You)" with a contradictory mic state (now hidden
   under the composited photo, but it's still in the prototype).

Video-side accepted imperfections: seek-into-scene restarts that scene's animations
(correct in linear playback); s5b rings sit within ~5 px of the frame bottom (the real
control bar is at the screen bottom); caption bars cover non-narrated bottom rows (standard).

---

## 12. Remaining roadmap (priority order)

1. **Voice choice** (WIP, §4) — rebuild + republish on Scott's pick.
2. **Scott's next review pass** — expect screenshot-driven notes; the fix loop is:
   adjust `SCENES` / captures → rebuild → PIL-verify changed frames → republish same URL.
3. **Production voiceover** — swap the draft voice for a licensed one (ElevenLabs MCP
   Starter $6 / Azure F0 / OpenAI; §6.3). The build is backend-agnostic: replace `synth()`
   and keep word-timing (Azure & ElevenLabs both provide timestamps) or fall back to
   sentence-proportional caption timing.
4. **Upstream data fixes** (§11) then one recapture+rebuild cycle.
5. **MP4 export** when Scott wants a real file: screen-record the artifact playing with
   voice on (macOS Screenshot app), or lay `vo-draft/s*.mp3` over a recording using
   `timing.json`; the video also drops into the `.video-ph` placeholder on the `vid-*`
   marketing concept pages.
6. **Possible upgrades noted but not requested:** a real capture of the interview-type
   picker in registration (setup-flow shows only the job-location field); the after-event
   Summary screen (`lobby-v3-healthcare.html?mode=event-ended`) if the script ever grows a
   post-event beat.

## 13. Open questions
- Which voice? (the only live blocker)
- Ship the draft-voice artifact to stakeholders, or wait for the licensed VO first?
- Will Scott fix the prototype data (§11) before the video is called final?
- Does he eventually want the MP4, and hosted where (site `.video-ph`, YouTube like
  Indeed's, both)?

---

## Instructions for the Next Claude Code Session

You are continuing a project that was paused only because the previous Claude Code conversation reached its context limit.
Before making any changes:

1. Read this entire handoff from beginning to end.
2. Review the complete codebase.
3. Review every file referenced in this handoff.
4. Verify your understanding against the current implementation.
5. Reconstruct the project's architecture, design system, UX philosophy, marketing strategy, coding standards, and implementation approach.

Once you have completed your review:

* Confirm that you fully understand the project.
* Provide a concise summary of your understanding.
* Explain exactly where the previous Claude stopped working.
* Do not write any code yet.
* Do not make design changes yet.
* Do not make recommendations yet.

Instead, stop and ask me exactly this:
"I've finished reviewing the handoff and the codebase, and I'm fully caught up on the project. What would you like to work on first?"
Wait for my response before taking any further action.
