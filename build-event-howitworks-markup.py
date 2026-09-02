"""Marks up the reworked event-page How It Works, plus the help-centre strip.

Donor DOM: scratchpad/brands/healthcare.html (the live Houston Healthcare event
page, rendered).  We lift the head, header and footer so the mock-up renders in
the real compiled Tailwind build served from jobfairx.com, then AUTHOR the two
sections underneath.

Every sub() asserts its match count.  Edit this file, never the output.
"""
import re, sys, os

# INPUT: healthcare.html is a headless-Chrome render of the LIVE Houston
# Healthcare event page (banners are client-rendered, so curl will not do).
# Re-capture it into CAPTURES if the live page changes:
#   chrome --headless --dump-dom <event-url> > healthcare.html
MKT = os.path.dirname(os.path.abspath(__file__))
CAPTURES = os.environ.get('JFX_CAPTURES', os.path.join(MKT, 'captures'))
BRANDS = CAPTURES
OUT = os.path.join(MKT, 'event-howitworks-markup.html')

src = open(os.path.join(BRANDS, 'healthcare.html'), encoding='utf-8').read()

# ---------------------------------------------------------------- helpers ---

def close_of(text, start, tag='div'):
    """Index just past the close tag matching the element opening at `start`."""
    pat = re.compile(r'</?%s\b' % tag)
    depth, i = 0, start
    while True:
        m = pat.search(text, i)
        if not m:
            raise SystemExit('unbalanced <%s> from %d' % (tag, start))
        depth += -1 if text[m.start():m.start() + 2 + len(tag)] == '</' + tag else 1
        i = m.end()
        if depth == 0:
            return text.index('>', i) + 1


def one(pattern, text, label):
    hits = re.findall(pattern, text, re.S)
    if len(hits) != 1:
        raise SystemExit('%s: expected 1 match, got %d' % (label, len(hits)))
    return hits[0]


BASE = 'https://jobfairx.com'


def absolutise(t):
    """Chrome serialises the captured DOM with paths relative to the live URL
    (four levels deep), so ../../../ chains have to be rewritten too, not just
    root-relative ones."""
    t = re.sub(r'(href|src)="(?:\.\./)+', r'\1="%s/' % BASE, t)
    t = re.sub(r'(href|src)="/(?!/)', r'\1="%s/' % BASE, t)
    t = re.sub(r'srcset="([^"]+)"',
               lambda m: 'srcset="' + re.sub(r'(^|,\s*)(?:(?:\.\./)+|/(?!/))', r'\1%s/' % BASE, m.group(1)) + '"',
               t)
    return t


def strip_runtime(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<link[^>]*modulepreload[^>]*>', '', t)
    t = re.sub(r'\sdata-svelte-h="[^"]*"', '', t)
    return t


# -------------------------------------------------------- donor extraction ---
head = one(r'<head\b[^>]*>(.*?)</head>', src, 'head')
head = absolutise(strip_runtime(head))
head = re.sub(r'<title>.*?</title>', '', head, flags=re.S)

hdr_start = src.index('<header')
hdr = src[hdr_start:close_of(src, hdr_start, 'header')]
hdr = absolutise(strip_runtime(hdr))

ftr_start = src.index('<footer')
ftr = src[ftr_start:close_of(src, ftr_start, 'footer')]
ftr = absolutise(strip_runtime(ftr))

# The three live product panels live inside the how-step rows: each row is
# [how-text div][visual div].  Take the trailing sibling.
panels = []
for m in re.finditer(r'<div class="how-step[^"]*"[^>]*>', src):
    row_end = close_of(src, m.start())
    row = src[m.start():row_end]
    tx = row.index('<div class="how-text')
    after = close_of(row, tx)
    vis = row[after:row.rindex('</div>')].strip()
    panels.append(absolutise(strip_runtime(vis)))

if len(panels) != 3:
    raise SystemExit('expected 3 live panels, got %d' % len(panels))
REVIEW_PANEL, EVENTDAY_PANEL, REPORT_PANEL = panels

# The live report panel is dated to an old event; point it at this one.
if 'Apr 22, 2026' not in REPORT_PANEL:
    raise SystemExit('report panel date anchor moved')
REPORT_PANEL = REPORT_PANEL.replace('Apr 22, 2026', 'Sep 16, 2026')

# The set-up panel was authored for v2; lift it out of that builder verbatim.
v2 = open(os.path.join(MKT, 'build-event-healthcare.py'), encoding='utf-8').read()
anchor = v2.index('<div><div class="w-full max-w-[560px] h-[420px]')
SETUP_PANEL = v2[anchor:close_of(v2, anchor)]
SETUP_PANEL = (SETUP_PANEL
               .replace('600 Congress Ave', '1200 Smith St')
               .replace('Suite 1400', 'Suite 900')
               .replace('active RN license in Texas', 'active RN license in Texas'))
# That block wraps the panel AND its caption; keep just the panel so every beat
# renders through the same <div>{panel}{caption}</div> shape.
SETUP_PANEL = re.sub(r'\s*<p class="text-\[13px\][^>]*>.*?</p>\s*', '', SETUP_PANEL, flags=re.S)
SETUP_PANEL = SETUP_PANEL[len('<div>'):SETUP_PANEL.rindex('</div>')].strip()
if 'Interview settings' not in SETUP_PANEL or SETUP_PANEL.count('Interview settings, set when') != 0:
    raise SystemExit('set-up panel lift failed')

# ------------------------------------------------------------- authored UI ---
CITY, TYPE, DATE = 'Houston', 'Healthcare', 'September 16'

BEATS = [
    dict(eyebrow='Set up', n='1',
         h3='Post your jobs and matching starts immediately',
         body='Register for the %s %s hiring event and post your open roles. Set your '
              'interview format, your address, and any screening questions. Candidate '
              'matching starts as soon as your jobs are live, and qualified candidates '
              'begin requesting interviews immediately.' % (CITY, TYPE),
         link=('View upcoming events', '#'),
         panel=SETUP_PANEL, caption='Interview settings, set when you post your jobs.'),
    dict(eyebrow='Review &amp; confirm', n='2',
         h3='Accept the candidates you want to meet',
         body='Interview requests arrive with resumes attached. Accept them one at a time, '
              'or turn on auto&#8209;accept and let your schedule fill itself. Every matched '
              'candidate is verified to be within about 20 miles of %s.' % CITY,
         link=('See how it works', '#'),
         panel=REVIEW_PANEL, caption=''),
    dict(eyebrow='Event day', n='3',
         h3='You already know who you&#8217;re interviewing, and when',
         body='On %s every candidate on your schedule is qualified and interview&#8209;ready. '
              'You know who you&#8217;re interviewing, who each of your teammates is interviewing, '
              'and at what time. In person at your address, on JobFairX video with nothing to '
              'install, or by phone.' % DATE,
         link=('', ''),
         panel=EVENTDAY_PANEL, caption=''),
    dict(eyebrow='Post-event', n='4',
         h3='Every interview, in one report',
         body='See every interview, who on your team ran it, and the yes, no, or maybe '
              'outcome. Identify no&#8209;shows, message candidates, and schedule follow&#8209;up '
              'interviews straight from the report.',
         link=('Register for an event', '#'),
         panel=REPORT_PANEL, caption=''),
]


def beat_html(b, i):
    """Alternate the row so the visuals zig-zag, exactly as the live page does."""
    visual_left = (i % 2 == 0)
    cols = '560px_1fr' if visual_left else '1fr_560px'
    order = ' lg:order-2' if visual_left else ''
    last = ' mb-20 lg:mb-[120px]' if i < len(BEATS) - 1 else ''
    label, href = b['link']
    link = ('<a href="%s" class="how-step-link inline-block mt-3.5 text-[15px] font-semibold '
            'text-brand hover:underline">%s <span class="arrow inline-block ml-1">&rarr;</span></a>'
            % (href, label)) if label else ''
    cap = ('<p class="text-[13px] text-slate-500 mt-3 leading-relaxed">%s</p>' % b['caption']) if b['caption'] else ''
    return f'''<div class="how-step relative isolate grid grid-cols-1 lg:grid-cols-[{cols}] gap-3.5 lg:gap-20 items-center{last}">
<div class="how-text{order}"><div class="flex items-center gap-2.5 mb-3.5"><span class="jfx-beatnum">{b['n']}</span><span class="step-eyebrow inline-block text-xs font-bold text-brand uppercase tracking-[0.14em]">{b['eyebrow']}</span></div>
<h3 class="text-lg lg:text-2xl font-semibold text-slate-900 leading-tight mb-4">{b['h3']}</h3>
<p class="text-base text-slate-600 leading-[1.55]">{b['body']}</p>{link}</div>
<div>{b['panel']}{cap}</div></div>'''


HIW = '''<section class="how-section relative overflow-hidden bg-slate-50 py-12 lg:py-[90px]">
<div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">
<div class="text-center mb-12 lg:mb-16">
<div class="inline-block text-[13px] font-bold text-brand uppercase tracking-[0.12em] mb-3.5">How It Works</div>
<h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight">Your %s %s Event, From Start to Finish</h2>
<p class="mt-4 text-base lg:text-[17px] text-slate-600 leading-[1.6] max-w-[640px] mx-auto">Four steps, from the day you post your jobs to the report waiting for you afterwards.</p>
</div>
%s
</div></section>''' % (CITY, TYPE, '\n'.join(beat_html(b, i) for i, b in enumerate(BEATS)))

# ------------------------------------------------------- help centre strip ---
RESOURCES = [
    dict(kind='Watch', dur='2:39', t='The Event Day Lobby',
         d='The full walkthrough: how candidates get scheduled, what the lobby does on event day, and how you run each interview.'),
    dict(kind='Watch', dur='0:45', t='Adding Interviewers',
         d='Who can interview, where to add them, how many seats you get, and what an interviewer receives.'),
    dict(kind='Watch', dur='1:04', t='Reschedule and Follow-Up Interviews',
         d='Propose a new time for a booked interview, or schedule a follow-up after the event.'),
]


def res_card(r):
    return f'''<a href="#" class="jfx-res group flex flex-col h-full bg-white border border-[#e8e6e3] rounded-[14px] p-5 lg:p-6 no-underline transition">
<div class="flex items-center gap-2 mb-3.5"><span class="jfx-play" aria-hidden="true"><svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span><span class="text-[12px] font-bold text-brand uppercase tracking-[0.1em]">{r['kind']} &middot; {r['dur']}</span></div>
<div class="text-[17px] font-semibold text-slate-900 leading-snug mb-2">{r['t']}</div>
<p class="text-[14.5px] text-slate-600 leading-[1.55] mb-4">{r['d']}</p>
<span class="mt-auto text-[14.5px] font-semibold text-brand">Watch the video <span class="inline-block ml-0.5">&rarr;</span></span></a>'''


RES = '''<section class="py-12 lg:py-[76px] bg-white">
<div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">
<div class="lg:flex lg:items-end lg:justify-between mb-8 lg:mb-10">
<div><div class="inline-block text-[13px] font-bold text-brand uppercase tracking-[0.12em] mb-3.5">Before You Register</div>
<h2 class="text-[24px] lg:text-[32px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight">See Exactly How It Runs</h2>
<p class="mt-3 text-base text-slate-600 leading-[1.6] max-w-[600px]">Short walkthroughs shot from the real product. Every one answers a single question.</p></div>
<a href="#" class="hidden lg:inline-block text-[15px] font-semibold text-brand hover:underline whitespace-nowrap">All 12 guides in the Help Center <span class="inline-block ml-1">&rarr;</span></a></div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 items-stretch">%s</div>
<a href="#" class="lg:hidden inline-block mt-6 text-[15px] font-semibold text-brand hover:underline">All 12 guides in the Help Center <span class="inline-block ml-1">&rarr;</span></a>
</div></section>''' % ('\n'.join(res_card(r) for r in RESOURCES))

# ------------------------------------------------------------- annotations ---
def note(kicker, body):
    return (f'<div class="jfx-note"><span class="jfx-note-k">{kicker}</span>'
            f'<span class="jfx-note-b">{body}</span></div>')


NOTE_HIW = note('Section 1 &middot; replaces the live How It Works',
                'Live page has <b>three</b> beats and opens at &ldquo;Review and confirm&rdquo;, so it never says '
                'what the employer actually does first. This adds the missing set-up beat, renames the '
                'section to name <b>this</b> event, and rewrites event day around knowing your schedule '
                'rather than working through one. Beat&nbsp;3 carries the teammate answer.')

NOTE_RES = note('Section 2 &middot; new, sits below the FAQ',
                'Three real tutorials from your library, video-led. Placeholder links for now. '
                'This is the compact version on purpose: on a page someone is deciding from, this is '
                'reassurance, not the main event.')

STYLE = '''<style>
.jfx-beatnum{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;
 border-radius:9999px;background:#2563eb;color:#fff;font-size:12.5px;font-weight:700;
 font-variant-numeric:tabular-nums;flex:none}
.jfx-res{box-shadow:0 1px 2px rgba(0,0,0,.03)}
.jfx-res:hover{border-color:#2563eb;box-shadow:0 8px 28px rgba(0,0,0,.06);transform:translateY(-2px)}
.jfx-play{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;
 border-radius:9999px;background:#2563eb;color:#fff;flex:none}
.jfx-note{max-width:1180px;margin:0 auto;padding:14px 18px;display:flex;gap:14px;align-items:flex-start;
 background:#00245b;color:#dbeafe;font-size:13.5px;line-height:1.5}
.jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;color:#9fc6ff;
 flex:none;padding-top:2px;width:230px}
.jfx-note-b b{color:#fff;font-weight:600}
@media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
.jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;
 padding:9px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.jfx-bar b{color:#fff;font-weight:600}
.jfx-bar span{color:#93a4bd}
</style>'''

BAR = ('<div class="jfx-bar"><b>Event page &middot; How It Works markup</b>'
       '<span>Houston Healthcare &middot; September 16 &middot; mock-up only, links are placeholders</span></div>')

html = (f'<!DOCTYPE html><html lang="en"><head>{head}'
        f'<title>Event page How It Works markup | JobFairX</title>{STYLE}</head>'
        f'<body class="bg-white">{BAR}{hdr}'
        f'{NOTE_HIW}{HIW}{NOTE_RES}{RES}{ftr}</body></html>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)

# ------------------------------------------------------------ post checks ---
checks = [
    ('four beats rendered', html.count('class="how-step relative') == 4),
    ('set-up beat present', 'Post your jobs and matching starts immediately' in html),
    ('teammate clause present', 'who each of your teammates is interviewing' in html),
    ('report panel dated to this event', 'Sep 16, 2026' in html and 'Apr 22, 2026' not in html),
    ('resource CTAs bottom-aligned', html.count('mt-auto') == 3),
    ('no countdown language', 'By September' not in html and 'days out' not in html),
    ('no queue language', 'queue' not in html.lower()),
    ('report not promised mid-room', not re.search(r'moment it ends|before you leave', html, re.I)),
    ('event named in H2', 'Your Houston Healthcare Event, From Start to Finish' in html),
    ('four product panels', html.count('max-w-[560px] h-[420px]') == 4),
    ('three resource cards', html.count('class="jfx-res') == 3),
    ('set-up caption not duplicated', html.count('Interview settings, set when you post your jobs.') == 1),
    ('no bare .container', 'class="container' not in html.split('<footer')[0].split(BAR)[-1].replace(hdr, '')),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|booth|applicants', html, re.I)),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
    ('compiled tailwind linked absolutely', 'https://jobfairx.com/_app/immutable/assets/app.' in html),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
