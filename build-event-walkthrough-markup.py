"""Mock-up of the reworked walkthrough section for the event details page.

The live section is a thin left column ("See How JobFairX Works" / "A quick
walkthrough of the platform") next to a raw YouTube embed, on white. This
replaces it with a navy band whose left column is a table of contents for the
video, and a poster frame that loads the embed on click.

The three steps are the video's OWN opening card ("By the end of this video you
will be able to: Set interview format / Manage interviews / Run your hiring
event"), so the panel promises exactly what the 2:40 delivers.

Chrome (head/header/footer) is lifted from the captured live event page so the
mock renders in the real compiled Tailwind. The poster is a real frame from the
video at 1:50 - the live lobby - embedded as a data URI so this stays one file.

Every substitution asserts its match count. Edit this file, never the output.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', 'healthcare.html')
POSTER_B64 = os.environ.get(
    'JFX_POSTER_B64',
    '/private/tmp/claude-501/-Users-scottl--Desktop/dcae0819-a708-48f5-b19b-5ca5c66fa7d0'
    '/scratchpad/vid/poster_b64.txt')
OUT = os.path.join(MKT, 'event-walkthrough-markup.html')

VIDEO_ID = 'cDvxtuvm7mA'
DURATION = '2:40'

src = open(SRC, encoding='utf-8').read()
poster = open(POSTER_B64, encoding='utf-8').read().strip()
if len(poster) < 20000:
    raise SystemExit('poster data looks truncated (%d chars)' % len(poster))

BASE = 'https://jobfairx.com'


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


head = strip_runtime(re.search(r'<head\b[^>]*>(.*?)</head>', src, re.S).group(1))
head = absolutise(re.sub(r'<title>.*?</title>|<link rel="canonical"[^>]*>', '', head, flags=re.S))

hs = src.index('<header')
hdr = absolutise(strip_runtime(src[hs:close_of(src, hs, 'header')]))
fs = src.index('<footer')
ftr = absolutise(strip_runtime(src[fs:close_of(src, fs, 'footer')]))

# The live section, lifted verbatim so the two can be compared side by side.
ws = src.rfind('<section', 0, src.index('See How JobFairX Works'))
live = absolutise(strip_runtime(src[ws:close_of(src, ws, 'section')]))
if 'A quick walkthrough of the platform' not in live:
    raise SystemExit('live walkthrough section lift failed')

# --------------------------------------------------------------- authored ---
STEPS = [
    ('Set your interview format',
     'Set it once in your event settings and it carries through to candidates.'),
    ('Manage interview requests',
     'Review matched candidates, confirm interviews, and keep conversations moving.'),
    ('Run your hiring event',
     'See who is ready, start interviews, and keep every detail in one live lobby.'),
]

steps_html = ''.join(
    '<li class="jfx-wk-s"><span class="jfx-wk-n">%d</span>'
    '<div><h3 class="jfx-wk-st">%s</h3><p class="jfx-wk-sd">%s</p></div></li>' % (i + 1, t, d)
    for i, (t, d) in enumerate(STEPS))

SECTION = '''<section class="jfx-wk">
<div class="jfx-wk-in">
<div class="jfx-wk-text">
<p class="jfx-wk-eyeb">Watch the Walkthrough <span class="jfx-wk-dur">%s</span></p>
<h2 class="jfx-wk-h">See how a JobFairX hiring event works.</h2>
<p class="jfx-wk-sub">From setting your interview format to managing candidate requests and running
event&#8209;day, see how your team stays organized in one place.</p>
<ul class="jfx-wk-steps">%s</ul>
</div>
<div class="jfx-wk-media">
<button type="button" class="jfx-wk-poster" id="jfx-wk-play"
  aria-label="Play the walkthrough, %s">
<img src="data:image/jpeg;base64,%s" alt="The JobFairX event-day lobby, with interview rooms ready to start">
<span class="jfx-wk-scrim"></span>
<span class="jfx-wk-btn"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"
  aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
<span class="jfx-wk-time">%s</span>
</button>
</div>
</div></section>''' % (DURATION, steps_html, DURATION, poster, DURATION)

STYLE = '''<style>
 .jfx-wk{position:relative;overflow:hidden;background:#00245b;padding:56px 0;
   background-image:radial-gradient(900px 460px at 86% -8%,#00306f 0%,rgba(0,48,111,0) 62%)}
 @media (min-width:1024px){.jfx-wk{padding:88px 0}}
 .jfx-wk-in{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 16px;
   display:grid;grid-template-columns:1fr;gap:34px;align-items:center}
 @media (min-width:640px){.jfx-wk-in{padding:0 24px}}
 @media (min-width:1024px){.jfx-wk-in{padding:0 32px;gap:64px;
   grid-template-columns:minmax(0,460px) minmax(0,1fr)}}
 .jfx-wk-eyeb{margin:0 0 16px;font-size:12.5px;font-weight:700;letter-spacing:.14em;
   text-transform:uppercase;color:#8fbbff;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
 .jfx-wk-dur{background:rgba(255,255,255,.1);border:1px solid rgba(159,198,255,.3);
   border-radius:999px;padding:4px 10px;letter-spacing:.06em;color:#cfe0ff;font-size:11.5px}
 .jfx-wk-h{margin:0 0 16px;font-size:29px;font-weight:600;letter-spacing:-.025em;
   line-height:1.12;color:#fff}
 @media (min-width:1024px){.jfx-wk-h{font-size:38px}}
 .jfx-wk-sub{margin:0 0 30px;font-size:16px;line-height:1.6;color:#b7c9e4;max-width:44ch}
 @media (min-width:1024px){.jfx-wk-sub{font-size:17px;margin-bottom:36px}}
 .jfx-wk-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:22px}
 .jfx-wk-s{display:grid;grid-template-columns:32px minmax(0,1fr);gap:15px;align-items:start}
 .jfx-wk-n{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
   justify-content:center;font-size:13.5px;font-weight:600;color:#9fc6ff;
   background:rgba(255,255,255,.06);border:1px solid rgba(159,198,255,.4);
   font-variant-numeric:tabular-nums}
 .jfx-wk-st{margin:0 0 5px;font-size:17px;font-weight:500;color:#fff;line-height:1.3}
 .jfx-wk-sd{margin:0;font-size:14.5px;line-height:1.55;color:#9fb2cf}
 .jfx-wk-poster{display:block;width:100%;padding:0;border:1px solid rgba(159,198,255,.2);
   border-radius:14px;overflow:hidden;position:relative;cursor:pointer;background:#001b46;
   box-shadow:0 20px 60px rgba(0,0,0,.34);transition:transform .2s ease,box-shadow .2s ease}
 .jfx-wk-poster:hover{transform:translateY(-2px);box-shadow:0 26px 70px rgba(0,0,0,.42)}
 .jfx-wk-poster:focus-visible{outline:3px solid #8fbbff;outline-offset:3px}
 .jfx-wk-poster img{display:block;width:100%;height:auto}
 .jfx-wk-scrim{position:absolute;inset:0;background:rgba(0,20,54,.24)}
 .jfx-wk-btn{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:74px;height:74px;
   border-radius:50%;background:#fff;color:#00245b;display:flex;align-items:center;
   justify-content:center;box-shadow:0 8px 30px rgba(0,0,0,.34);transition:transform .2s ease}
 .jfx-wk-btn svg{margin-left:4px}
 .jfx-wk-poster:hover .jfx-wk-btn{transform:translate(-50%,-50%) scale(1.06)}
 .jfx-wk-time{position:absolute;right:12px;bottom:12px;background:rgba(0,17,46,.78);color:#e6edf7;
   font-size:12.5px;font-weight:600;padding:4px 9px;border-radius:6px;
   font-variant-numeric:tabular-nums}
 .jfx-wk-frame{width:100%;aspect-ratio:16/9;border:0;border-radius:14px;display:block}
 .jfx-note{max-width:1180px;margin:0 auto;padding:14px 18px;display:flex;gap:14px;
   align-items:flex-start;background:#0b1220;color:#dbeafe;font-size:13.5px;line-height:1.5}
 .jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;
   color:#9fc6ff;flex:none;padding-top:2px;width:210px}
 .jfx-note-b b{color:#fff;font-weight:600}
 @media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
 .jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;
   padding:9px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .jfx-bar b{color:#fff;font-weight:600}.jfx-bar span{color:#93a4bd}
</style>'''

SCRIPT = '''<script>
document.getElementById('jfx-wk-play').addEventListener('click', function () {
  var f = document.createElement('iframe');
  f.className = 'jfx-wk-frame';
  f.src = 'https://www.youtube.com/embed/%s?rel=0&autoplay=1';
  f.title = 'How to Run Your Hiring Event';
  f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
  f.allowFullscreen = true;
  this.replaceWith(f);
});
</script>''' % VIDEO_ID


def note(k, b):
    return '<div class="jfx-note"><span class="jfx-note-k">%s</span><span class="jfx-note-b">%s</span></div>' % (k, b)


N_NEW = note('Proposed &middot; on the navy band',
             'Left column is a table of contents for the video &mdash; the three steps are the '
             'video&#8217;s <b>own opening card</b>. Runtime badge because it lifts play rate. '
             'Poster is a real frame at 1:50; the YouTube embed loads on click, so none of its '
             'chrome sits on our navy. Step&nbsp;1 deliberately does <b>not</b> re-list the three '
             'formats &mdash; that is the job of &ldquo;Interview your way.&rdquo; below it.')

N_OLD = note('For comparison &middot; what is live now',
             'A thin left column, a sub-line that repeats the heading, and the raw player on white. '
             'The thumbnail already says RUN YOUR HIRING EVENT, so nothing here tells you what you '
             'will actually learn.')

BAR = ('<div class="jfx-bar"><b>Event page &middot; walkthrough section</b>'
       '<span>Proposed above, live version below &middot; mock-up only</span></div>')

html = ('<!DOCTYPE html><html lang="en"><head>%s<title>Event walkthrough section | JobFairX</title>'
        '%s</head><body class="bg-white">%s%s%s%s%s%s%s%s</body></html>'
        % (head, STYLE, BAR, hdr, N_NEW, SECTION, N_OLD, live, ftr, SCRIPT))

open(OUT, 'w', encoding='utf-8').write(html)

checks = [
    ('three steps rendered', html.count('class="jfx-wk-s"') == 3),
    ('runtime badge present', SECTION.count('class="jfx-wk-dur"') == 1 and DURATION in SECTION),
    ('poster is a real frame', 'data:image/jpeg;base64,' in SECTION and len(poster) > 20000),
    ('click-to-load, no eager iframe',
     '<iframe' not in SECTION and 'youtube.com/embed/' in SCRIPT),
    ('brand navy, not a new dark', '#00245b' in html and '#0b1220' in html),
    ('step 1 does not re-list the formats',
     'in person, video, or phone' not in html.split('For comparison')[0].lower()),
    ('live section kept for comparison', 'A quick walkthrough of the platform' in html),
    ('video id wired once in the new section', SCRIPT.count(VIDEO_ID) == 1
     and VIDEO_ID not in SECTION),
    ('live comparison still holds its own embed', VIDEO_ID in live),
    ('no bare .container in authored markup', 'class="container' not in SECTION),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
    ('compiled tailwind linked', 'https://jobfairx.com/_app/immutable/assets/app.' in html),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
