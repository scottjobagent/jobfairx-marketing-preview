"""Mock-up: the Hiring Event Demo with the five steps as VIDEO CHAPTERS.

Same navy band, same poster, same five steps as the approved working page. The
difference: each step is a button that jumps the video to the moment it shows.
First click swaps the poster for the embed at that timestamp; later clicks seek
the running player. Timestamps come from watching the 2:40 frame by frame.

"Add interviewers" is not in the demo video. Rather than hide that, the mock
shows the honest treatment: it is still a chapter, but it opens the dedicated
0:45 tutorial in a new tab and is labelled "separate video".

Shared strings (poster, video id, steps, band CSS) are read out of
build-event-details-by-brand.py at build time so this cannot drift from the
approved page. Chrome is lifted from the captured live event page.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', 'healthcare.html')
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
OUT = os.path.join(MKT, 'event-chapters-markup.html')
BASE = 'https://jobfairx.com'
INTERVIEWERS_CLIP = 'https://claude.ai/code/artifact/1f6bfb21-9776-41cf-988c-cd3b7c15cc05'

# ------------------------------------- shared pieces from the working page ---
bb = open(BRAND_BUILDER, encoding='utf-8').read()
ns = {'re': re}
exec(bb[bb.index('CARDS = ['):bb.index('# ----------------------------------------- retire the Built-in Tools bento ---')], ns)
for k in ('VIDEO_ID', 'POSTER', 'WALK_STEPS', 'WALK_CSS'):
    if k not in ns:
        raise SystemExit('builder no longer defines %s' % k)
VIDEO_ID, POSTER, STEPS, WALK_CSS = ns['VIDEO_ID'], ns['POSTER'], ns['WALK_STEPS'], ns['WALK_CSS']
if STEPS != ['Choose your interview format', 'Add interviewers', 'Manage interview requests',
             'Manage the event-day lobby', 'Conduct interviews']:
    raise SystemExit('the five steps changed; re-time the chapters: %r' % (STEPS,))

# seconds into the 2:40, from the frame-by-frame watch; None = not in this video
TIMES = [8, None, 32, 104, 120]


# ---------------------------------------------------------------- helpers ---
def close_of(text, start, tag='div'):
    pat = re.compile(r'</?%s\b' % tag)
    depth, i = 0, start
    while True:
        m = pat.search(text, i)
        if not m:
            raise SystemExit('unbalanced <%s>' % tag)
        depth += -1 if text[m.start():m.start() + 2 + len(tag)] == '</' + tag else 1
        i = m.end()
        if depth == 0:
            return text.index('>', i) + 1


def absolutise(t):
    t = re.sub(r'(href|src)="(?:\.\./)+', r'\1="%s/' % BASE, t)
    t = re.sub(r'(href|src)="/(?!/)', r'\1="%s/' % BASE, t)
    return t


def strip_runtime(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<link[^>]*modulepreload[^>]*>', '', t)
    t = re.sub(r'\sdata-svelte-h="[^"]*"', '', t)
    return t


def mmss(s):
    return '%d:%02d' % (s // 60, s % 60)


src = open(SRC, encoding='utf-8').read()
head = strip_runtime(re.search(r'<head\b[^>]*>(.*?)</head>', src, re.S).group(1))
head = absolutise(re.sub(r'<title>.*?</title>|<link rel="canonical"[^>]*>', '', head, flags=re.S))
hs = src.index('<header')
hdr = absolutise(strip_runtime(src[hs:close_of(src, hs, 'header')]))
fs = src.index('<footer')
ftr = absolutise(strip_runtime(src[fs:close_of(src, fs, 'footer')]))

# ------------------------------------------------------------- the section ---
rows = []
for i, (title, t) in enumerate(zip(STEPS, TIMES)):
    n = i + 1
    if t is None:
        rows.append('<li><a class="jfx-ch jfx-ch-alt" href="%s" target="_blank" rel="noopener">'
                    '<span class="jfx-ch-n">%d</span><span class="jfx-ch-t">%s'
                    '<span class="jfx-ch-sub">Separate video</span></span>'
                    '<span class="jfx-ch-tm">0:45</span></a></li>' % (INTERVIEWERS_CLIP, n, title))
    else:
        rows.append('<li><button type="button" class="jfx-ch" data-t="%d">'
                    '<span class="jfx-ch-n">%d</span><span class="jfx-ch-t">%s</span>'
                    '<span class="jfx-ch-tm">%s</span></button></li>' % (t, n, title, mmss(t)))

SECTION = ('<section class="jfx-wk"><div class="jfx-wk-in"><div class="jfx-wk-text">'
           '<p class="jfx-wk-eyeb">Hiring Event Demo</p>'
           '<h2 class="jfx-wk-h">Manage your hiring event from start to finish.</h2>'
           '<ol class="jfx-chs">%s</ol>'
           '<p class="jfx-ch-hint">Select a step to jump to it in the video.</p>'
           '</div><div class="jfx-wk-media">'
           '<button type="button" class="jfx-wk-poster" data-yt="%s" aria-label="Play the hiring event demo">'
           '<img src="%s" width="1052" height="586" alt="The JobFairX event-day lobby, with interview rooms ready to start">'
           '<span class="jfx-wk-scrim"></span><span class="jfx-wk-btn">'
           '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
           '</span></button></div></div></section>' % (''.join(rows), VIDEO_ID, POSTER))

CHAPTER_CSS = '''
 .jfx-chs{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
 .jfx-ch{display:grid;grid-template-columns:32px minmax(0,1fr) auto;gap:14px;align-items:center;width:100%;
   text-align:left;background:transparent;border:1px solid transparent;border-radius:10px;padding:8px 10px 8px 8px;
   color:#fff;font:inherit;cursor:pointer;text-decoration:none;transition:background .15s ease,border-color .15s ease}
 .jfx-ch:hover{background:rgba(255,255,255,.06);border-color:rgba(159,198,255,.28)}
 .jfx-ch:focus-visible{outline:2px solid #8fbbff;outline-offset:2px}
 .jfx-ch.is-on{background:rgba(37,99,235,.30);border-color:rgba(159,198,255,.5)}
 .jfx-ch-n{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;
   font-size:13.5px;font-weight:600;color:#9fc6ff;background:rgba(255,255,255,.06);border:1px solid rgba(159,198,255,.4);
   font-variant-numeric:tabular-nums}
 .jfx-ch.is-on .jfx-ch-n{background:#2563eb;border-color:#2563eb;color:#fff}
 .jfx-ch-t{font-size:17px;font-weight:500;line-height:1.3}
 @media (min-width:1024px){.jfx-ch-t{font-size:18px}}
 .jfx-ch-sub{display:block;font-size:12px;font-weight:400;color:#9fb2cf;margin-top:2px}
 .jfx-ch-tm{font-size:12.5px;font-weight:600;font-variant-numeric:tabular-nums;color:#cfe0ff;
   background:rgba(255,255,255,.08);border:1px solid rgba(159,198,255,.28);border-radius:999px;padding:3px 9px;white-space:nowrap}
 .jfx-ch-alt .jfx-ch-tm::after{content:" \\2197";font-weight:400}
 .jfx-ch-hint{margin:14px 0 0 8px;font-size:12.5px;color:#9fb2cf}
 .jfx-wk-frame{width:100%;aspect-ratio:16/9;border:0;border-radius:14px;display:block}
'''

SCRIPT = '''<script>
(function () {
  var media = document.querySelector('.jfx-wk-media');
  var poster = media.querySelector('.jfx-wk-poster');
  var frame = null;
  function load(sec) {
    frame = document.createElement('iframe');
    frame.className = 'jfx-wk-frame';
    frame.src = 'https://www.youtube.com/embed/%s?rel=0&autoplay=1&enablejsapi=1&start=' + sec;
    frame.title = 'How to Run Your Hiring Event';
    frame.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
    frame.allowFullscreen = true;
    poster.replaceWith(frame);
  }
  function cmd(func, args) {
    frame.contentWindow.postMessage(JSON.stringify({event: 'command', func: func, args: args || []}), '*');
  }
  function seek(sec) {
    if (!frame) { load(sec); return; }
    cmd('seekTo', [sec, true]); cmd('playVideo');
  }
  function mark(el) {
    document.querySelectorAll('.jfx-ch').forEach(function (x) { x.classList.toggle('is-on', x === el); });
  }
  poster.addEventListener('click', function () { load(0); mark(null); });
  document.querySelectorAll('.jfx-ch[data-t]').forEach(function (b) {
    b.addEventListener('click', function () { seek(+b.getAttribute('data-t')); mark(b); });
  });
})();
</script>''' % VIDEO_ID

NOTE = ('<div class="jfx-note"><span class="jfx-note-k">Demo with chapters</span><span class="jfx-note-b">'
        'Same band, same five steps. Each step now jumps the video to the moment it shows &mdash; first click '
        'loads the player there, later clicks seek it. <b>Add interviewers</b> is not in the 2:40, so it opens '
        'the dedicated 0:45 tutorial instead and says so. Timestamps are from the frame-by-frame watch.</span></div>')

STYLE = ('<style>' + WALK_CSS + CHAPTER_CSS + '''
 .jfx-note{max-width:1180px;margin:0 auto;padding:14px 18px;display:flex;gap:14px;align-items:flex-start;
   background:#0b1220;color:#dbeafe;font-size:13.5px;line-height:1.5}
 .jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;color:#9fc6ff;flex:none;padding-top:2px;width:170px}
 .jfx-note-b b{color:#fff;font-weight:600}
 @media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
 .jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;padding:9px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .jfx-bar b{color:#fff;font-weight:600}.jfx-bar span{color:#93a4bd}
</style>''')

BAR = ('<div class="jfx-bar"><b>Event page &middot; demo with video chapters</b>'
       '<span>Houston Healthcare &middot; mock-up only &middot; click any step</span></div>')

html = ('<!DOCTYPE html><html lang="en"><head>%s<title>Demo with chapters | JobFairX</title>%s</head>'
        '<body class="bg-white">%s%s%s%s%s%s</body></html>' % (head, STYLE, BAR, hdr, NOTE, SECTION, ftr, SCRIPT))
open(OUT, 'w', encoding='utf-8').write(html)

checks = [
    ('five chapters', html.count('class="jfx-ch"') + html.count('class="jfx-ch jfx-ch-alt"') == 5),
    ('four timed, one separate', html.count('data-t="') == 4 and html.count('jfx-ch-alt') >= 1),
    ('timestamps rendered', all(mmss(t) in html for t in TIMES if t is not None)),
    ('separate video is labelled and links out', 'Separate video' in html and INTERVIEWERS_CLIP in html),
    ('poster loads embed on click, no eager iframe', not re.search(r'<iframe[^>]*youtube', html) and 'enablejsapi=1' in html),
    ('seek uses the player api, not a reload', "cmd('seekTo'" in html),
    ('no runtime capsule', 'jfx-wk-dur' not in html and 'jfx-wk-time' not in html),
    ('poster referenced', POSTER in html),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
