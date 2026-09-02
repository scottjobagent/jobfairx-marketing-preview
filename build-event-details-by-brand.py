"""Five live event-detail pages behind one brand toggle, plus the new
"Interview your way." interview-format section.

SOURCE OF TRUTH: captures/_by-brand-deployed.html — the previously published
by-brand page, which is itself the rendered DOM of five real jobfairx.com event
pages (banners are client-rendered, so curl alone will not capture them).
Re-capture that file from the preview URL, or re-render the five live events,
if the live site changes.

The interview-format section is AUTHORED here and injected into every panel,
immediately after the walkthrough video and before How It Works. The How It
Works "Event day" beat is rewritten at the same time, because it used to be the
page's answer on interview formats and would otherwise repeat this new section
word for word.

Every substitution asserts its match count. Edit this file, never the output.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', '_by-brand-deployed.html')
OUT = os.path.join(MKT, 'event-details-by-brand.html')

src = open(SRC, encoding='utf-8').read()

BRANDS = ['healthcare', 'technology', 'diversity', 'veteran', 'entry-level']


def close_section(text, start):
    """Index just past the </section> matching the element opening at start."""
    pat = re.compile(r'</?section\b')
    depth, i = 0, start
    while True:
        m = pat.search(text, i)
        if not m:
            raise SystemExit('unbalanced <section>')
        depth += -1 if text[m.start():m.start() + 9] == '</section' else 1
        i = m.end()
        if depth == 0:
            return text.index('>', i) + 1


def close_tag(text, start, tag):
    """Index just past the close tag matching the element opening at start."""
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


def one(needle, text, label, expect=1):
    n = text.count(needle)
    if n != expect:
        raise SystemExit('%s: expected %d, found %d' % (label, expect, n))


# ------------------------------------------------------------- the section ---
CARDS = [
    dict(key='blue', title='Video',
         desc='Conduct interviews directly on the JobFairX platform. Candidates receive a '
              'secure link to join their interview.',
         icon='<path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2"/>'),
    dict(key='green', title='In person',
         desc='Provide the interview address and attendance instructions. Candidates receive '
              'the details they need to arrive prepared.',
         icon='<circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>'
              '<circle cx="12" cy="12" r="1.2" fill="currentColor" stroke="none"/>'),
    dict(key='amber', title='Phone',
         desc='Call candidates at their scheduled interview time. Their phone number and '
              'interview details are available in JobFairX.',
         icon='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 '
              '19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 '
              '2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
]


def card(c):
    return (
        '<div class="jfx-fmt-c jfx-fmt-%s">'
        '<div class="jfx-fmt-cap"><span></span></div>'
        '<div class="jfx-fmt-body">'
        '<div class="jfx-fmt-tile"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true">%s</svg></div>'
        '<h3 class="jfx-fmt-t">%s</h3>'
        '<p class="jfx-fmt-d">%s</p>'
        '</div></div>' % (c['key'], c['icon'], c['title'], c['desc']))


def section_for(city):
    """The city is resolved per panel, so each brand names its own event."""
    return (
        '<section class="jfx-fmt">'
        '<span class="jfx-fmt-arc" aria-hidden="true"></span>'
        '<span class="jfx-fmt-dots" aria-hidden="true"></span>'
        '<div class="jfx-fmt-in">'
        '<p class="jfx-fmt-eyeb">Choose Your Interview Format</p>'
        '<h2 class="jfx-fmt-h">Meet candidates by video, in person, or phone.</h2>'
        '<p class="jfx-fmt-sub">Select how you want to conduct interviews for the %s hiring '
        'event. Choose the format that works best for your hiring process.</p>'
        '<div class="jfx-fmt-cards">%s</div>'
        '</div></section>' % (city, ''.join(card(c) for c in CARDS)))


SECTION_CSS = '''
 .jfx-fmt{position:relative;overflow:hidden;background:#fff;padding:56px 0}
 @media (min-width:1024px){.jfx-fmt{padding:90px 0}}
 .jfx-fmt-arc{position:absolute;top:-190px;right:-140px;width:520px;height:520px;
   border-radius:50%;background:#F4F7FF;pointer-events:none}
 .jfx-fmt-dots{position:absolute;left:22px;bottom:34px;width:170px;height:78px;opacity:.55;
   pointer-events:none;background-image:radial-gradient(#C7D2FE 1.6px,transparent 1.6px);
   background-size:14px 14px}
 .jfx-fmt-in{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 16px}
 @media (min-width:640px){.jfx-fmt-in{padding:0 24px}}
 @media (min-width:1024px){.jfx-fmt-in{padding:0 32px}}
 .jfx-fmt-eyeb{margin:0 0 14px;text-align:center;font-size:13px;font-weight:700;
   letter-spacing:.12em;text-transform:uppercase;color:#2563eb}
 .jfx-fmt-h{margin:0 0 14px;text-align:center;font-size:28px;font-weight:600;
   letter-spacing:-.02em;line-height:1.12;color:#0b1220}
 @media (min-width:1024px){.jfx-fmt-h{font-size:40px}}
 .jfx-fmt-sub{margin:0 auto 40px;max-width:660px;text-align:center;font-size:16px;
   line-height:1.6;color:#5a6478}
 @media (min-width:1024px){.jfx-fmt-sub{font-size:18px;margin-bottom:52px}}
 .jfx-fmt-cards{display:grid;grid-template-columns:1fr;gap:18px}
 @media (min-width:768px){.jfx-fmt-cards{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}}
 .jfx-fmt-c{display:flex;flex-direction:column;background:#fff;border:1px solid #e9e7e3;
   border-radius:16px;overflow:hidden;transition:box-shadow .2s ease,transform .2s ease}
 .jfx-fmt-c:hover{box-shadow:0 10px 34px rgba(0,0,0,.06);transform:translateY(-2px)}
 .jfx-fmt-cap{position:relative;height:132px;overflow:hidden}
 .jfx-fmt-cap span{position:absolute;right:-52px;top:-46px;width:172px;height:172px;
   border-radius:50%;background:rgba(255,255,255,.34)}
 .jfx-fmt-blue .jfx-fmt-cap{background:linear-gradient(135deg,#edf1ff,#d9e2ff)}
 .jfx-fmt-green .jfx-fmt-cap{background:linear-gradient(135deg,#e8f7f1,#cbeade)}
 .jfx-fmt-amber .jfx-fmt-cap{background:linear-gradient(135deg,#fef5e6,#fae6c2)}
 .jfx-fmt-body{display:flex;flex-direction:column;flex:1;padding:0 24px 26px}
 .jfx-fmt-tile{position:relative;z-index:1;width:56px;height:56px;border-radius:15px;
   display:flex;align-items:center;justify-content:center;margin:-28px 0 16px;
   box-shadow:0 1px 2px rgba(0,0,0,.04)}
 .jfx-fmt-blue .jfx-fmt-tile{background:#edf1ff;color:#2563eb}
 .jfx-fmt-green .jfx-fmt-tile{background:#e8f7f1;color:#0e9488}
 .jfx-fmt-amber .jfx-fmt-tile{background:#fef5e6;color:#b45309}
 .jfx-fmt-t{margin:0 0 10px;font-size:22px;font-weight:500;letter-spacing:-.01em;color:#0b1220}
 .jfx-fmt-d{margin:0;font-size:15.5px;line-height:1.55;color:#5a6478}
'''

# ------------------------------------------- the navy walkthrough section ---
# Replaces the live section (thin left column, sub-line that restates the
# heading, raw YouTube player on white). The three steps are the video's OWN
# opening card, so the panel promises exactly what the 2:40 delivers. The poster
# is a real frame at 1:50 and the embed only loads on click, so no YouTube
# chrome ever sits on the navy.
VIDEO_ID = 'cDvxtuvm7mA'
POSTER = 'walkthrough-poster.jpg'

WALK_STEPS = [
    'Choose your interview format',
    'Add interviewers',
    'Manage interview requests',
    'Manage the event-day lobby',
    'Conduct interviews',
]

WALK = ('<section class="jfx-wk"><div class="jfx-wk-in"><div class="jfx-wk-text">'
        '<p class="jfx-wk-eyeb">Hiring Event Demo</p>'
        '<h2 class="jfx-wk-h">Manage your hiring event from start to finish.</h2>'
        '<ul class="jfx-wk-steps">%s</ul></div>'
        '<div class="jfx-wk-media"><button type="button" class="jfx-wk-poster" '
        'data-yt="%s" aria-label="Play the hiring event demo">'
        # No loading="lazy": five stacked panels mean four of these parse inside a
        # hidden element, and Chrome then never re-evaluates them, so the card
        # renders empty. It is one 52KB image.
        '<img src="%s" width="1052" height="586" '
        'alt="The JobFairX event-day lobby, with interview rooms ready to start">'
        '<span class="jfx-wk-scrim"></span><span class="jfx-wk-btn">'
        '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="M8 5v14l11-7z"/></svg></span></button></div></div></section>'
        % (''.join('<li class="jfx-wk-s"><span class="jfx-wk-n">%d</span>'
                   '<span class="jfx-wk-st">%s</span></li>'
                   % (i + 1, t) for i, t in enumerate(WALK_STEPS)),
           VIDEO_ID, POSTER))

WALK_CSS = """
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
 .jfx-wk-h{margin:0 0 30px;font-size:28px;font-weight:600;letter-spacing:-.025em;
   line-height:1.12;color:#fff}
 @media (min-width:1024px){.jfx-wk-h{font-size:36px}}
 .jfx-wk-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:16px}
 .jfx-wk-s{display:grid;grid-template-columns:32px minmax(0,1fr);gap:15px;align-items:center}
 .jfx-wk-n{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
   justify-content:center;font-size:13.5px;font-weight:600;color:#9fc6ff;
   background:rgba(255,255,255,.06);border:1px solid rgba(159,198,255,.4);
   font-variant-numeric:tabular-nums}
 .jfx-wk-st{font-size:17px;font-weight:500;color:#fff;line-height:1.35}
 @media (min-width:1024px){.jfx-wk-st{font-size:18px}}
 .jfx-wk-poster{display:block;width:100%;padding:0;border:1px solid rgba(159,198,255,.2);
   border-radius:14px;overflow:hidden;position:relative;cursor:pointer;background:#001b46;
   box-shadow:0 20px 60px rgba(0,0,0,.34);transition:transform .2s ease,box-shadow .2s ease}
 .jfx-wk-poster:hover{transform:translateY(-2px);box-shadow:0 26px 70px rgba(0,0,0,.42)}
 .jfx-wk-poster:focus-visible{outline:3px solid #8fbbff;outline-offset:3px}
 .jfx-wk-poster img{display:block;width:100%;height:auto}
 .jfx-wk-scrim{position:absolute;inset:0;background:rgba(0,20,54,.24)}
 .jfx-wk-btn{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:74px;
   height:74px;border-radius:50%;background:#fff;color:#00245b;display:flex;align-items:center;
   justify-content:center;box-shadow:0 8px 30px rgba(0,0,0,.34);transition:transform .2s ease}
 .jfx-wk-btn svg{margin-left:4px}
 .jfx-wk-poster:hover .jfx-wk-btn{transform:translate(-50%,-50%) scale(1.06)}
 .jfx-wk-frame{width:100%;aspect-ratio:16/9;border:0;border-radius:14px;display:block}
"""

WALK_JS = """
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('.jfx-wk-poster');
  if (!b) return;
  var f = document.createElement('iframe');
  f.className = 'jfx-wk-frame';
  f.src = 'https://www.youtube.com/embed/' + b.getAttribute('data-yt') + '?rel=0&autoplay=1';
  f.title = 'How to Run Your Hiring Event';
  f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
  f.allowFullscreen = true;
  b.replaceWith(f);
});
"""

# ------------------------------------- the review-outcomes section ---
# Replaces How It Works. Two of its three beats repeated the demo; the third,
# the post-event report, is the one thing nothing else on the page said, so it
# becomes its own section with the live report panel as the visual.
CHECK = ('<span class="jfx-ro-ck" aria-hidden="true"><svg width="10" height="10" viewBox="0 0 24 24" '
         'fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span>')

OUTCOME_POINTS = [
    ('Yes, maybe, or no', ' for each candidate, with your team&#8217;s notes'),
    ('Who interviewed whom,', ' and who didn&#8217;t show'),
    ('Message candidates or schedule next&#8209;round interviews', ' straight from the report'),
]


def outcomes_for(report_panel):
    """report_panel is the live post-event report component, lifted per panel."""
    return (
        '<section class="jfx-ro"><div class="jfx-ro-in">'
        '<div class="jfx-ro-text">'
        '<p class="jfx-ro-eyeb">After the Event</p>'
        '<h2 class="jfx-ro-h">Review interview outcomes.</h2>'
        '<p class="jfx-ro-sub">Your post&#8209;event report is ready in your dashboard. Every interview, '
        'every outcome, and who on your team saw whom.</p>'
        '<ul class="jfx-ro-list">%s</ul>'
        '<a href="#" class="jfx-ro-link">Register for an event <span>&rarr;</span></a>'
        '</div>'
        '<div class="jfx-ro-media">%s</div>'
        '</div></section>'
        % (''.join('<li>%s<span><b>%s</b>%s</span></li>' % (CHECK, h, t) for h, t in OUTCOME_POINTS),
           report_panel))


OUTCOMES_CSS = """
 .jfx-ro{background:#f8fafc;padding:56px 0;border-top:1px solid #eef2f7}
 @media (min-width:1024px){.jfx-ro{padding:90px 0}}
 .jfx-ro-in{max-width:1180px;margin:0 auto;padding:0 16px;display:grid;grid-template-columns:1fr;
   gap:28px;align-items:center}
 @media (min-width:640px){.jfx-ro-in{padding:0 24px}}
 @media (min-width:1024px){.jfx-ro-in{padding:0 32px;gap:64px;grid-template-columns:minmax(0,1fr) 560px}}
 .jfx-ro-eyeb{margin:0 0 14px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#2563eb}
 .jfx-ro-h{margin:0 0 14px;font-size:28px;font-weight:600;letter-spacing:-.02em;line-height:1.12;color:#0b1220}
 @media (min-width:1024px){.jfx-ro-h{font-size:36px}}
 .jfx-ro-sub{margin:0 0 20px;font-size:16px;line-height:1.6;color:#5a6478;max-width:48ch}
 @media (min-width:1024px){.jfx-ro-sub{font-size:17px}}
 .jfx-ro-list{list-style:none;margin:0 0 24px;padding:0;display:flex;flex-direction:column;gap:12px}
 .jfx-ro-list li{display:grid;grid-template-columns:20px minmax(0,1fr);gap:11px;font-size:15.5px;
   line-height:1.5;color:#334155;align-items:start}
 .jfx-ro-list b{color:#0f172a;font-weight:600}
 .jfx-ro-ck{width:20px;height:20px;border-radius:50%;background:#dcfce7;color:#15803d;display:flex;
   align-items:center;justify-content:center;margin-top:2px}
 .jfx-ro-link{display:inline-block;font-size:15px;font-weight:600;color:#2563eb;text-decoration:none}
 .jfx-ro-link:hover{text-decoration:underline}
 .jfx-ro-link span{display:inline-block;margin-left:4px}
 .jfx-ro-media > div{margin-left:auto;margin-right:auto}
"""

# ----------------------------------------- retire the Built-in Tools bento ---
# The sticky-scroll "Candidate Messaging and Interview Scheduling" section. It
# was already replaced on the employer home page, and on the event page it now
# sits between two sections that cover the same ground.
def drop_builtin_tools(text):
    tag = ('<section class="py-12 min-[901px]:py-24 bg-[#f8f7f4]">'
           '<div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">')
    one(tag, text, 'built-in tools section', expect=5)
    out, cursor, search = [], 0, 0
    for _ in range(5):
        i = text.index(tag, search)
        end = close_section(text, i)
        if 'Built-in Tools' not in text[i:end]:
            raise SystemExit('built-in tools lift grabbed the wrong section')
        out.append(text[cursor:i])
        cursor, search = end, end
    out.append(text[cursor:])
    return ''.join(out)


# ------------------------------------------------ inject into every panel ---
ANCHOR = '<section class="how-section'
one(ANCHOR, src, 'how-section anchor', expect=5)
one('See How JobFairX Works', src, 'walkthrough heading', expect=5)

# Panels carry their own city, so inject in document order rather than with one
# blanket replace.
panel_meta = re.findall(r'<div class="brand-panel" data-b="([^"]+)" data-city="([^"]+)"', src)
if [b for b, _ in panel_meta] != BRANDS:
    raise SystemExit('panel order changed: %r' % (panel_meta,))
CITIES = [c.split(',')[0].strip() for _, c in panel_meta]

out, cursor, search = [], 0, 0
for city in CITIES:
    i = src.index(ANCHOR, search)
    out.append(src[cursor:i])
    out.append(section_for(city))
    cursor, search = i, i + len(ANCHOR)
out.append(src[cursor:])
html = drop_builtin_tools(''.join(out))

WALK_ANCHOR = '<section id="how-it-works-video"'
one(WALK_ANCHOR, html, 'live walkthrough section', expect=5)
_ws = [m.start() for m in re.finditer(re.escape(WALK_ANCHOR), html)]
_live_walk = html[_ws[0]:close_section(html, _ws[0])]
if 'A quick walkthrough of the platform' not in _live_walk:
    raise SystemExit('live walkthrough lift failed')
one(_live_walk, html, 'identical live walkthrough copies', expect=5)
html = html.replace(_live_walk, WALK)

# ------------------------------------ How It Works -> Review interview outcomes ---
# Per panel: lift the post-event report panel out of the live How It Works
# (its third beat), re-date it to this event, and replace the whole section.
HIW_ANCHOR = '<section class="how-section'
one(HIW_ANCHOR, html, 'live How It Works section', expect=5)
_dates = re.findall(r'<div class="brand-panel" data-b="[^"]+" data-city="[^"]+" data-date="([^"]+)"', html)
if len(_dates) != 5:
    raise SystemExit('could not read the five event dates')
out, cursor, search = [], 0, 0
for date in _dates:
    i = html.index(HIW_ANCHOR, search)
    end_sec = close_section(html, i)
    sec = html[i:end_sec]
    steps = [m.start() for m in re.finditer(r'<div class="how-step', sec)]
    if len(steps) != 3:
        raise SystemExit('expected 3 beats in the live How It Works, got %d' % len(steps))
    row = sec[steps[2]:close_tag(sec, steps[2], 'div')]
    tx = row.index('<div class="how-text')
    panel = row[close_tag(row, tx, 'div'):row.rindex('</div>')].strip()
    if 'feedback' not in panel.lower():
        raise SystemExit('report panel lift failed: no feedback column')
    # The live mock is dated to some old event; each brand's differs. Re-date to this event.
    panel, n = re.subn(r'\b[A-Z][a-z]{2} \d{1,2}, 20\d\d\b', '%s, 2026' % date, panel)
    if n != 1:
        raise SystemExit('expected one date in the report panel, found %d' % n)
    out.append(html[cursor:i])
    out.append(outcomes_for(panel))
    cursor, search = end_sec, end_sec
out.append(html[cursor:])
html = ''.join(out)

# ------------------------------------------------------- styles into head ---
STYLE_ANCHOR = ' .brand-panel .sticky.top-0{top:36px !important}'
one(STYLE_ANCHOR, html, 'panel style anchor')
html = html.replace(STYLE_ANCHOR, STYLE_ANCHOR + '\n' + SECTION_CSS + WALK_CSS + OUTCOMES_CSS)

JS_ANCHOR = " show('healthcare');"
one(JS_ANCHOR, html, 'toggle script anchor')
html = html.replace(JS_ANCHOR, JS_ANCHOR + '\n})();\n(function(){' + WALK_JS)

open(OUT, 'w', encoding='utf-8').write(html)

# ------------------------------------------------------------ post checks ---
def before(a, b, text):
    """True when every occurrence of a precedes the matching occurrence of b."""
    ia = [m.start() for m in re.finditer(re.escape(a), text)]
    ib = [m.start() for m in re.finditer(re.escape(b), text)]
    return len(ia) == len(ib) == 5 and all(x < y for x, y in zip(ia, ib))


checks = [
    ('five brand panels', html.count('class="brand-panel"') == 5),
    ('section on every panel', html.count('class="jfx-fmt"') == 5),
    ('three cards per panel', html.count('class="jfx-fmt-c ') == 15),
    ('walkthrough sits above the format section',
     before('<section class="jfx-wk"', '<section class="jfx-fmt"', html)),
    ('formats stated once per panel', html.count('>Phone</h3>') == 5),
    ('How It Works retired', 'how-section' not in html and 'Hiring Events Built Around Interviews' not in html),
    ('outcomes section on every panel', html.count('class="jfx-ro"') == 5
     and html.count('Review interview outcomes.') == 5),
    ('report panel re-dated per event',
     all(('%s, 2026' % d) in html for d in _dates)
     and not re.search(r'jfx-ro-media.{0,600}?(Apr|May|Jun|Jul) \d{1,2}, 2026', html, re.S)),
    ('order walkthrough -> format -> outcomes -> results',
     before('<section class="jfx-fmt"', '<section class="jfx-ro"', html)
     and before('<section class="jfx-ro"', 'Hiring event results', html)),
    ('video leads, then in person, then phone',
     re.findall(r'class="jfx-fmt-t">([^<]+)<', html)[:3] == ['Video', 'In person', 'Phone']),
    ('no link-styled flow lines', 'jfx-fmt-flow' not in html),
    ('card copy on every panel', all(html.count(t) == 5 for t in (
        'Conduct interviews directly on the JobFairX platform.',
        'Provide the interview address and attendance instructions.',
        'Call candidates at their scheduled interview time.'))),
    ('headline on every panel',
     html.count('>Meet candidates by video, in person, or phone.</h2>') == 5),
    ('city resolved per panel, no token left',
     '{{CITY}}' not in html
     and all('for the %s hiring event' % c in html for c in CITIES)
     and len(set(CITIES)) == 5),
    ('scoped css present once', html.count('.jfx-fmt-cards{display:grid') == 1),
    ('icon tile lifted above the header block', 'position:relative;z-index:1;width:56px' in html),
    ('toggle script intact', "show('healthcare')" in html),
    ('navy walkthrough on every panel', html.count('class="jfx-wk"') == 5),
    ('live walkthrough retired', 'A quick walkthrough of the platform' not in html
     and 'how-it-works-video' not in html),
    ('five demo steps per panel', html.count('class="jfx-wk-s"') == 25),
    ('demo eyebrow and headline', html.count('>Hiring Event Demo</p>') == 5
     and html.count('>Manage your hiring event from start to finish.</h2>') == 5),
    ('walkthrough subtext retired', 'jfx-wk-sub' not in html and 'jfx-wk-sd' not in html),
    ('poster referenced, not inlined', html.count('walkthrough-poster.jpg') == 5
     and 'data:image/jpeg;base64' not in html),
    ('poster not lazy inside hidden panels', 'loading="lazy"' not in WALK),
    ('no runtime anywhere', 'jfx-wk-dur' not in html and 'jfx-wk-time' not in html
     and '2:40' not in html),
    ('built-in tools section removed',
     'Built-in Tools' not in html and 'Candidate Messaging' not in html),
    ('youtube only loads on click',
     not re.search(r'<iframe[^>]*youtube', html) and 'youtube.com/embed/' in WALK_JS),
    ('every brand still addressed', all('data-b="%s"' % b in html for b in BRANDS)),
    ('no vocabulary breaches',
     not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
