"""Mock-up of the reshuffled top of the event details page.

The working page currently says "how it works" three times in a row: the demo's
five-step list, the interview-format cards, and How It Works. This mock shows
the fix Scott asked to see before anything moves:

  Demo          -> video only. The five-step list goes; it was a table of
                   contents for the section two below.
  Format        -> unchanged.
  How It Works  -> takes "Manage your hiring event from start to finish." as
                   its heading and gains a SET-UP beat at the front, so it
                   genuinely runs start to finish. Four beats, four product
                   visuals.

Shared pieces (format cards, walkthrough styles, poster, video id) are read out
of build-event-details-by-brand.py at build time, so this mock cannot drift
from the working page. Chrome is lifted from the captured live event page so it
renders in the real compiled Tailwind. Every lift asserts.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', 'healthcare.html')
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
V2_BUILDER = os.path.join(MKT, 'build-event-healthcare.py')
OUT = os.path.join(MKT, 'event-reshuffle-markup.html')

BASE = 'https://jobfairx.com'
CITY, TYPE, DATE = 'Houston', 'Healthcare', 'September 16'


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


def grab(pattern, text, label):
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit('could not find %s in the by-brand builder' % label)
    return m.group(1)


# ------------------------------------- shared pieces from the working page ---
bb = open(BRAND_BUILDER, encoding='utf-8').read()

# CARDS, card() and section_for() are plain Python with no other dependencies.
_defs = bb[bb.index('CARDS = ['):bb.index("SECTION_CSS = '''")]
_ns = {}
exec(_defs, _ns)
section_for = _ns['section_for']

SECTION_CSS = grab(r"SECTION_CSS = '''(.*?)'''", bb, 'SECTION_CSS')
WALK_CSS = grab(r'WALK_CSS = """(.*?)"""', bb, 'WALK_CSS')
WALK_JS = grab(r'WALK_JS = """(.*?)"""', bb, 'WALK_JS')
POSTER = grab(r"POSTER = '([^']+)'", bb, 'POSTER')
VIDEO_ID = grab(r"VIDEO_ID = '([^']+)'", bb, 'VIDEO_ID')

# ------------------------------------------------------------ donor chrome ---
src = open(SRC, encoding='utf-8').read()
head = strip_runtime(re.search(r'<head\b[^>]*>(.*?)</head>', src, re.S).group(1))
head = absolutise(re.sub(r'<title>.*?</title>|<link rel="canonical"[^>]*>', '', head, flags=re.S))
hs = src.index('<header')
hdr = absolutise(strip_runtime(src[hs:close_of(src, hs, 'header')]))
fs = src.index('<footer')
ftr = absolutise(strip_runtime(src[fs:close_of(src, fs, 'footer')]))

# The three live product panels, lifted out of the live How It Works rows.
panels = []
for m in re.finditer(r'<div class="how-step[^"]*"[^>]*>', src):
    row = src[m.start():close_of(src, m.start())]
    tx = row.index('<div class="how-text')
    vis = row[close_of(row, tx):row.rindex('</div>')].strip()
    panels.append(absolutise(strip_runtime(vis)))
if len(panels) != 3:
    raise SystemExit('expected 3 live panels, got %d' % len(panels))
REVIEW_PANEL, EVENTDAY_PANEL, REPORT_PANEL = panels
if 'Apr 22, 2026' not in REPORT_PANEL:
    raise SystemExit('report panel date anchor moved')
REPORT_PANEL = REPORT_PANEL.replace('Apr 22, 2026', 'Sep 16, 2026')

# The set-up panel was authored for v2; lift the panel only, not its caption.
v2 = open(V2_BUILDER, encoding='utf-8').read()
a = v2.index('<div><div class="w-full max-w-[560px] h-[420px]')
SETUP_PANEL = v2[a:close_of(v2, a)]
SETUP_PANEL = re.sub(r'\s*<p class="text-\[13px\][^>]*>.*?</p>\s*', '', SETUP_PANEL, flags=re.S)
SETUP_PANEL = SETUP_PANEL[len('<div>'):SETUP_PANEL.rindex('</div>')].strip()
SETUP_PANEL = SETUP_PANEL.replace('600 Congress Ave', '1200 Smith St').replace('Suite 1400', 'Suite 900')
if 'Interview settings' not in SETUP_PANEL:
    raise SystemExit('set-up panel lift failed')

# ------------------------------------------------------- 1. demo, video only ---
DEMO = '''<section class="jfx-dm">
<div class="jfx-dm-in">
<p class="jfx-dm-eyeb">Hiring Event Demo</p>
<h2 class="jfx-dm-h">See the platform in action.</h2>
<p class="jfx-dm-sub">A walkthrough of a real hiring event, shot from the JobFairX platform.</p>
<div class="jfx-dm-media">
<button type="button" class="jfx-wk-poster" data-yt="%s" aria-label="Play the hiring event demo">
<img src="%s" width="1052" height="586" alt="The JobFairX event-day lobby, with interview rooms ready to start">
<span class="jfx-wk-scrim"></span>
<span class="jfx-wk-btn"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
</button>
</div>
</div></section>''' % (VIDEO_ID, POSTER)

DEMO_CSS = '''
 .jfx-dm{position:relative;overflow:hidden;background:#00245b;padding:56px 0;
   background-image:radial-gradient(900px 460px at 86% -8%,#00306f 0%,rgba(0,48,111,0) 62%)}
 @media (min-width:1024px){.jfx-dm{padding:84px 0}}
 .jfx-dm-in{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 16px;text-align:center}
 @media (min-width:640px){.jfx-dm-in{padding:0 24px}}
 @media (min-width:1024px){.jfx-dm-in{padding:0 32px}}
 .jfx-dm-eyeb{margin:0 0 14px;font-size:12.5px;font-weight:700;letter-spacing:.14em;
   text-transform:uppercase;color:#8fbbff}
 .jfx-dm-h{margin:0 0 12px;font-size:28px;font-weight:600;letter-spacing:-.025em;line-height:1.12;color:#fff}
 @media (min-width:1024px){.jfx-dm-h{font-size:36px}}
 .jfx-dm-sub{margin:0 auto 36px;max-width:56ch;font-size:16px;line-height:1.6;color:#b7c9e4}
 @media (min-width:1024px){.jfx-dm-sub{font-size:17px;margin-bottom:44px}}
 .jfx-dm-media{max-width:880px;margin:0 auto}
'''

# ------------------------------------------------------- 2. format, unchanged ---
FMT = section_for(CITY)

# ------------------------------------------- 3. how it works, four beats ---
BEATS = [
    dict(eyebrow='Set up',
         h3='Set up your event',
         body='Choose how you&#8217;ll interview, add the people who&#8217;ll be interviewing, and post '
              'your open roles. Candidate matching starts as soon as your jobs are live, and qualified '
              'candidates begin requesting interviews immediately.',
         link=('View upcoming events', '#'), panel=SETUP_PANEL),
    dict(eyebrow='Review &amp; confirm',
         h3='Review and confirm interviews',
         body='Matched candidates request interview times. Accept requests individually, or enable '
              'auto&#8209;accept to confirm interviews automatically.',
         link=('See how it works', '#'), panel=REVIEW_PANEL),
    dict(eyebrow='Event day',
         h3='You already know who you&#8217;re interviewing, and when',
         body='Every candidate on your schedule is qualified and interview&#8209;ready. You know who '
              'you&#8217;re interviewing, who each of your teammates is interviewing, and at what time. '
              'The schedule, resumes, and notes all sit in the same place.',
         link=('', ''), panel=EVENTDAY_PANEL),
    dict(eyebrow='Post-event',
         h3='Post-Event Reporting',
         body='Gain complete visibility into your hiring metrics with a comprehensive event report that '
              'consolidates your team&#8217;s input. Track which team member interviewed each candidate, '
              'review yes, no, or maybe outcomes, and identify no&#8209;shows. Message candidates or '
              'schedule next&#8209;round interviews directly from the dashboard.',
         link=('Register for an event', '#'), panel=REPORT_PANEL),
]


def beat_html(b, i):
    visual_left = (i % 2 == 0)
    cols = '560px_1fr' if visual_left else '1fr_560px'
    order = ' lg:order-2' if visual_left else ''
    last = ' mb-20 lg:mb-[120px]' if i < len(BEATS) - 1 else ''
    label, href = b['link']
    link = ('<a href="%s" class="how-step-link inline-block mt-3.5 text-[15px] font-semibold '
            'text-brand hover:underline">%s <span class="arrow inline-block ml-1">&rarr;</span></a>'
            % (href, label)) if label else ''
    return (f'<div class="how-step relative isolate grid grid-cols-1 lg:grid-cols-[{cols}] gap-3.5 '
            f'lg:gap-20 items-center{last}">'
            f'<div class="how-text{order}"><div class="flex items-center gap-2.5 mb-3.5">'
            f'<span class="jfx-beatnum">{i + 1}</span>'
            f'<span class="step-eyebrow inline-block text-xs font-bold text-brand uppercase '
            f'tracking-[0.14em]">{b["eyebrow"]}</span></div>'
            f'<h3 class="text-lg lg:text-2xl font-semibold text-slate-900 leading-tight mb-4">{b["h3"]}</h3>'
            f'<p class="text-base text-slate-600 leading-[1.55]">{b["body"]}</p>{link}</div>'
            f'<div>{b["panel"]}</div></div>')


HIW = ('<section class="how-section relative overflow-hidden bg-slate-50 py-12 lg:py-[90px]">'
       '<div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">'
       '<div class="text-center mb-12 lg:mb-16">'
       '<div class="inline-block text-[13px] font-bold text-brand uppercase tracking-[0.12em] mb-3.5">How It Works</div>'
       '<h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight">'
       'Manage your hiring event from start to finish.</h2></div>'
       + ''.join(beat_html(b, i) for i, b in enumerate(BEATS)) +
       '</div></section>')

# ------------------------------------------------------------- annotations ---
def note(k, b):
    return ('<div class="jfx-note"><span class="jfx-note-k">%s</span>'
            '<span class="jfx-note-b">%s</span></div>' % (k, b))


N1 = note('1 &middot; Demo, video only',
          'The five-step list is gone &mdash; it was a table of contents for the section two below. '
          'The video is now the whole point of the band.')
N2 = note('2 &middot; Format, unchanged',
          'Exactly as it is on the working page.')
N3 = note('3 &middot; How It Works, start to finish',
          'Takes <b>Manage your hiring event from start to finish.</b> as its heading and gains a '
          'set-up beat at the front, so it genuinely runs start to finish. Four beats, four product '
          'visuals &mdash; Indeed&#8217;s four boxes, built from real screenshots.')

STYLE = '<style>' + SECTION_CSS + WALK_CSS + DEMO_CSS + '''
 .jfx-beatnum{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;
   border-radius:9999px;background:#2563eb;color:#fff;font-size:12.5px;font-weight:700;
   font-variant-numeric:tabular-nums;flex:none}
 .jfx-note{max-width:1180px;margin:0 auto;padding:14px 18px;display:flex;gap:14px;align-items:flex-start;
   background:#0b1220;color:#dbeafe;font-size:13.5px;line-height:1.5}
 .jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;color:#9fc6ff;
   flex:none;padding-top:2px;width:230px}
 .jfx-note-b b{color:#fff;font-weight:600}
 @media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
 .jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;
   padding:9px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .jfx-bar b{color:#fff;font-weight:600}.jfx-bar span{color:#93a4bd}
</style>'''

BAR = ('<div class="jfx-bar"><b>Event page &middot; reshuffle mock-up</b>'
       '<span>Demo &rarr; Format &rarr; How It Works &middot; Houston Healthcare &middot; links are placeholders</span></div>')

html = ('<!DOCTYPE html><html lang="en"><head>%s<title>Event page reshuffle | JobFairX</title>%s</head>'
        '<body class="bg-white">%s%s%s%s%s%s%s%s%s<script>(function(){%s})();</script></body></html>'
        % (head, STYLE, BAR, hdr, N1, DEMO, N2, FMT, N3, HIW, ftr, WALK_JS))

open(OUT, 'w', encoding='utf-8').write(html)

checks = [
    ('demo is video only', 'class="jfx-wk-s"' not in DEMO and 'jfx-wk-steps' not in DEMO
     and '<li' not in DEMO),
    ('demo heading present', 'See the platform in action.' in html),
    ('format section from the working page', html.count('class="jfx-fmt"') == 1
     and 'Meet candidates by video, in person, or phone.' in html),
    ('how it works takes the start-to-finish heading',
     HIW.count('Manage your hiring event from start to finish.') == 1
     and 'start to finish' not in DEMO),
    ('four beats, numbered', html.count('class="how-step relative') == 4
     and html.count('class="jfx-beatnum"') == 4),
    ('set-up beat leads', re.search(r'jfx-beatnum">1</span>.*?Set up', html, re.S) is not None),
    ('four product panels', html.count('max-w-[560px] h-[420px]') == 4),
    ('report dated to this event', 'Sep 16, 2026' in html and 'Apr 22, 2026' not in html),
    ('order demo -> format -> how it works',
     html.index('class="jfx-dm"') < html.index('class="jfx-fmt"') < html.index('class="how-section')),
    ('youtube only loads on click', not re.search(r'<iframe[^>]*youtube', html)
     and 'youtube.com/embed/' in WALK_JS),
    ('no runtime capsule', 'jfx-wk-dur' not in html and '2:40' not in html),
    ('no vocabulary breaches',
     not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
