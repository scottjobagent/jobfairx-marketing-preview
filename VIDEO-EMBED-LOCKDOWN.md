# Lock every video embed on jobfairx.com (Indeed behavior)

**Goal (Scott, 25 Aug):** on every video across the site, clicking the YouTube
logo, channel avatar, video title, or "Watch on YouTube" must do nothing — no
new window, no navigating away. Expanding to full screen must work everywhere.

Shareable version for the developer:
https://claude.ai/code/artifact/1f963133-2800-430e-826a-dcec873f793f

## Three changes

1. `sandbox="allow-scripts allow-same-origin"` on every YouTube iframe.
   This is what kills the click-through.
2. `allowfullscreen` **in the server-rendered HTML** wherever it's missing —
   the employer hero and any JS-injected lightbox embed.
3. Drop `autoplay=1&mute=1` from the hero URL so the video plays with sound
   when the visitor starts it. Read the autoplay section first.

## Where the videos are

Scanned the full sitemap (3,906 URLs, every page family). Three video
locations, all under `/employer`. The 2,113 job-seeker pages have none.

| Page | Pages | Video | Needs |
|---|---|---|---|
| `/employer` (hero) | 1 | QuRalPnpPLA | sandbox **+ allowfullscreen** |
| `/employer/demo` | 1 | rMg30AReS-Q | sandbox |
| `/employer/job-fairs/{state}/{city}/next-{type}` | 1,760 | QuRalPnpPLA | sandbox (one template) |

## Why the hero won't go fullscreen

The served HTML for `#hero-video` has **no** `allowfullscreen` and no
`fullscreen` in its `allow` list. Client-side script adds both after hydration,
so DevTools shows them and it looks correct. But a frame's permissions are
resolved when it loads — setting `allowfullscreen` on an already-loaded iframe
does not retroactively grant it, so the button stays inert. Put the attribute
in the initial markup.

Served today:

```html
<iframe id="hero-video" class="aspect-video w-full"
        src="https://www.youtube.com/embed/QuRalPnpPLA?autoplay=1&mute=1&playsinline=1&rel=0"
        title="JobFairX product overview" frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; web-share"
        referrerpolicy="strict-origin-when-cross-origin"></iframe>
```

Replace with:

```html
<iframe id="hero-video" class="aspect-video w-full"
        src="https://www.youtube.com/embed/QuRalPnpPLA?playsinline=1&rel=0"
        title="JobFairX product overview" frameborder="0"
        sandbox="allow-scripts allow-same-origin"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; fullscreen"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen></iframe>
```

`autoplay=1&mute=1` comes off so the video waits for the visitor and then
plays with sound. Also drop whatever script patches `allowfullscreen` on
after load.

## Autoplay: it can't play with sound

**Browsers block unmuted autoplay. This is not a YouTube limitation.** Chrome,
Safari, and Firefox all refuse to start a video with sound before the visitor
interacts with the page. Removing `mute=1` while keeping `autoplay=1` does NOT
give you a video that plays out loud — the browser blocks the play and the
visitor gets a dead, paused player. No parameter, header, or account setting
overrides this.

So the choice is muted autoplay vs. **click-to-play with sound**, and
click-to-play wins: the click is itself the gesture that unlocks audio, so the
visitor hears the video from the first frame instead of joining it partway
through on mute. Today's muted autoplay means people notice the video already
running, having missed the opening, and many never realize there's audio.

Two ways:

- **Ship now** — drop the autoplay parameters. The player renders paused with
  its own play button; clicking plays with sound. One-line change.
- **Upgrade** — poster frame + custom play button, swapping the iframe in on
  click with `autoplay=1` and no mute. Same sound behavior, but you control
  the thumbnail and the page loads lighter. This is what the event-page
  prototype already does for its video modal.

Either way keep `autoplay` in the `allow` list — that's what lets the
click-to-play version start once the visitor has clicked.

## Why the sandbox works

`sandbox` switches the frame to deny-by-default and re-grants only what's
listed. The lockdown is what's deliberately absent.

- `allow-scripts` — granted, so the player runs: playback, controls, captions.
- `allow-same-origin` — granted, so YouTube keeps its own cookies and storage
  and doesn't error. That's *YouTube's* origin, not ours; it grants the frame
  nothing on jobfairx.com.
- `allow-popups` — **withheld**. This is the one that matters. The logo,
  avatar, title, "Watch on YouTube", share button, and end-screen cards all
  open via `target="_blank"` / `window.open()`, which the sandbox refuses.
- `allow-top-navigation` — withheld, so the frame can't redirect the page.

`allowfullscreen` is a separate attribute the sandbox does not gate — adding
the sandbox will not take expand away from pages where it already works.

## Not a YouTube setting

No account-side switch disables the branding links; they're built into the
player. The only embed control in Studio is *Allow embedding* on/off, and
turning it off breaks the video everywhere. Three false leads:

- `modestbranding=1` — deprecated Aug 2023, no effect.
- `fs=0` — hides the fullscreen button, the opposite of the goal.
- A transparent div over the player — also swallows play, scrub, volume,
  and fullscreen.

## Verify

On `/employer`, `/employer/demo`, and one event page: logo click dead, title
and avatar dead, fullscreen expands, playback/scrub/volume/captions still
work. On `/employer` also confirm the hero no longer starts on its own and
that pressing play gives sound from the first frame. Then **view source** — `allowfullscreen` must be in the served HTML, not
only in the inspector.

## Applied locally

All local embeds now carry the lock:

- `build-employer-home.py`, `employer-home.html`, `employer-home-mobile.html`
- `employer-event-detail.html`
- `employer-event-detail-v2.html` (inline + JS modal; modal also gained
  `allowfullscreen`, which it was missing)
- `build-event-healthcare.py` (inline + JS modal, same)

Left untouched: `assets/live-capture/event-detail-live-dom.html` — that's a
raw capture of the live site and should keep recording the live state.
