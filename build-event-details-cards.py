"""The four-box demo section, at Indeed's measured sizes, on the event page.

Source: event-details-by-brand.html (the working page, untouched).
Output: event-details-by-brand-cards.html.

The four boxes take the slot the navy demo band occupies, because card one
carries the 2:40 demo video. Nothing is lost, and the heading does not appear
twice. Placement is Scott's call and this is a separate file, so moving it is
one edit.

Geometry is Indeed's, measured at a 1440 viewport on
indeed.com/employers/hiring-events/onboarding:

  content 1314 wide, four cards 306, gap 30, image 2:1 full-bleed,
  56px from image to title, title 28/35, body 16/24, padding 32, white page.

Ours by choice: radius 16, border #e2e8f0, semibold titles, brand blue links.
Card one uses each brand's own hero photo; cards two to four are real product
captures and are the same for every brand.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'event-details-by-brand.html')
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
OUT = os.path.join(MKT, 'event-details-by-brand-cards.html')
N = 5
TUTORIALS = 'https://claude.ai/code/artifact/1f6bfb21-9776-41cf-988c-cd3b7c15cc05'

bb = open(BRAND_BUILDER, encoding='utf-8').read()
ns = {'re': re}
exec(bb[bb.index('CARDS = ['):bb.index('# ----------------------------------------- retire the Built-in Tools bento ---')], ns)
VIDEO_ID = ns['VIDEO_ID']
YT = 'https://www.youtube.com/watch?v=' + VIDEO_ID

for f in ('card-interviewers.jpg', 'card-settings.jpg', 'card-report.jpg'):
    if not os.path.exists(os.path.join(MKT, f)):
        raise SystemExit('missing card image: ' + f)

html = open(SRC, encoding='utf-8').read()


def close_section(text, start):
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


def card(img, alt, title, desc, cta, meta, href, video):
    ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    play = ('<span class="jfx-hx-play" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" '
            'fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>') if video else ''
    m = (' <span class="jfx-hx-meta">&middot; %s</span>' % meta) if meta else ''
    return ('<a class="jfx-hx-c" href="%s"%s>'
            '<span class="jfx-hx-cap"><img src="%s" width="800" height="400" alt="%s">%s</span>'
            '<span class="jfx-hx-body"><span class="jfx-hx-t">%s</span><span class="jfx-hx-d">%s</span>'
            '<span class="jfx-hx-cta">%s%s <i>&rarr;</i></span></span></a>'
            % (href, ext, img, alt, play, title, desc, cta, m))


def section_for(brand, type_label):
    cards = [
        card('brand-%s.jpg' % brand, 'A %s hiring event in progress' % type_label.lower(),
             'Manage your hiring event',
             'The full walkthrough: set your format, manage requests, run the event-day lobby, and conduct interviews.',
             'Watch the video', '2:40', YT, True),
        card('card-interviewers.jpg', 'The events dashboard showing interviewer setup for each event',
             'Add interviewers',
             'Put your team on the event. Who can interview, how many seats you have, and what each interviewer receives.',
             'Watch the video', '0:45', TUTORIALS, True),
        card('card-settings.jpg', 'The interview settings screen with video, phone and in-person options',
             'Interview settings',
             'Choose video, in person, or phone, set your time slots, and decide how many interviews your team runs at once.',
             'Read the article', '', '#', False),
        card('card-report.jpg', 'The event report with yes, maybe and no outcomes for every candidate',
             'Event performance',
             'Your post-event report: every interview, every outcome, who interviewed whom, and export in one click.',
             'Read the article', '', '#', False),
    ]
    return ('<section class="jfx-hx"><div class="jfx-hx-in">'
            '<p class="jfx-hx-eyeb">Hiring Event Demo</p>'
            '<h2 class="jfx-hx-h">Manage your hiring event from start to finish.</h2>'
            '<div class="jfx-hx-cards">%s</div></div></section>' % ''.join(cards))


# --------------------------------------- swap the navy band for the cards ---
ANCHOR = '<section class="jfx-wk">'
if html.count(ANCHOR) != N:
    raise SystemExit('expected %d demo bands, found %d' % (N, html.count(ANCHOR)))
meta = re.findall(r'<div class="brand-panel" data-b="([^"]+)" data-city="[^"]+" data-date="[^"]+"', html)
if len(meta) != N:
    raise SystemExit('could not read the five brands')
LABEL = {'healthcare': 'Healthcare', 'technology': 'Technology', 'diversity': 'Diversity',
         'veteran': 'Veterans', 'entry-level': 'Entry-Level'}

out, cursor, search = [], 0, 0
for brand in meta:
    i = html.index(ANCHOR, search)
    end = close_section(html, i)
    if 'jfx-wk-poster' not in html[i:end]:
        raise SystemExit('the band at %d is not the demo band' % i)
    out.append(html[cursor:i])
    out.append(section_for(brand, LABEL[brand]))
    cursor, search = end, end
out.append(html[cursor:])
html = ''.join(out)

# ------------------- retire Review interview outcomes (card four covers it) ---
# Scott: "under Manage your hiring event from start to finish you have Event
# performance" - so the post-event section is now said twice on one page.
RO = '<section class="jfx-ro">'
if html.count(RO) != N:
    raise SystemExit('expected %d outcomes sections, found %d' % (N, html.count(RO)))
out, cursor, search = [], 0, 0
for _ in range(N):
    i = html.index(RO, search)
    end = close_section(html, i)
    if 'Review interview outcomes' not in html[i:end]:
        raise SystemExit('the section at %d is not Review interview outcomes' % i)
    out.append(html[cursor:i])
    cursor, search = end, end
out.append(html[cursor:])
html = ''.join(out)

# and its now-unused rules, which sit last in the style block
_ro = html.index('\n .jfx-ro{')
_end = html.index('</style>', _ro)
html = html[:_ro] + '\n' + html[_end:]

# --------------------------------------------------------------- styles ---
CSS = '''
 .jfx-hx{background:#fff;padding:56px 0}
 @media (min-width:1024px){.jfx-hx{padding:96px 0}}
 /* the live stylesheet leaves box-sizing at content-box, so max-width would
    apply to the content box and the cards would land at 316, not 306 */
 .jfx-hx-in{box-sizing:border-box;max-width:1354px;margin:0 auto;padding:0 20px}
 @media (min-width:640px){.jfx-hx-in{padding:0 24px}}
 /* at lg the 20px gutter makes the content exactly 1314, so the four cards
    land on Indeed's 306 rather than 304 */
 @media (min-width:1024px){.jfx-hx-in{padding:0 20px}}
 .jfx-hx-eyeb{margin:0 0 14px;font-size:12px;font-weight:700;letter-spacing:.14em;
   text-transform:uppercase;color:#2563eb}
 .jfx-hx-h{margin:0 0 40px;font-size:28px;font-weight:600;letter-spacing:-.02em;line-height:1.12;color:#0b1220}
 @media (min-width:1024px){.jfx-hx-h{font-size:36px;margin-bottom:44px}}
 .jfx-hx-cards{display:grid;grid-template-columns:1fr;gap:20px}
 @media (min-width:640px){.jfx-hx-cards{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}}
 @media (min-width:1024px){.jfx-hx-cards{grid-template-columns:repeat(4,minmax(0,1fr));gap:30px}}
 .jfx-hx-c{display:flex;flex-direction:column;background:#fff;border:1px solid #e2e8f0;border-radius:16px;
   overflow:hidden;text-decoration:none;color:inherit;
   transition:border-color .2s ease,box-shadow .2s ease,transform .2s ease}
 .jfx-hx-c:hover{border-color:#cbd5e1;box-shadow:0 12px 32px rgba(15,23,42,.08);transform:translateY(-2px)}
 .jfx-hx-c:focus-visible{outline:3px solid #2563eb;outline-offset:3px}
 .jfx-hx-cap{position:relative;display:block;aspect-ratio:2/1;background:#eef2f7;border-bottom:1px solid #e2e8f0}
 /* the image is taken out of flow so its own 16:9 intrinsic ratio cannot
    stretch the 2:1 frame; without this, cards two to four run 19px taller */
 .jfx-hx-cap img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover}
 .jfx-hx-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:48px;height:48px;
   border-radius:50%;background:#fff;color:#00245b;display:flex;align-items:center;justify-content:center;
   box-shadow:0 6px 18px rgba(0,0,0,.24)}
 .jfx-hx-play svg{margin-left:2px}
 .jfx-hx-body{display:flex;flex-direction:column;flex:1;padding:0 24px 24px}
 @media (min-width:1024px){.jfx-hx-body{padding:0 32px 32px}}
 .jfx-hx-t{font-size:22px;line-height:28px;font-weight:600;letter-spacing:-.015em;color:#0b1220;margin:28px 0 8px}
 @media (min-width:1024px){.jfx-hx-t{font-size:28px;line-height:35px;margin:56px 0 8px}}
 .jfx-hx-d{font-size:15px;line-height:23px;color:#5a6478;margin:0 0 24px}
 @media (min-width:1024px){.jfx-hx-d{font-size:16px;line-height:24px;margin-bottom:28px}}
 .jfx-hx-cta{margin-top:auto;font-size:15px;font-weight:700;color:#2563eb}
 @media (min-width:1024px){.jfx-hx-cta{font-size:16px}}
 .jfx-hx-cta i{font-style:normal;display:inline-block;margin-left:4px;transition:transform .15s ease}
 .jfx-hx-c:hover .jfx-hx-cta i{transform:translateX(3px)}
 .jfx-hx-meta{font-weight:500;color:#64748b}
'''
ANCH = ' .brand-panel .sticky.top-0{top:36px !important}'
if html.count(ANCH) != 1:
    raise SystemExit('style anchor missing')
html = html.replace(ANCH, ANCH + '\n' + CSS)

# The demo band's rules and its click-to-load handler are now unused. Drop them
# so the file has no dead code in it.
_n0 = len(html)
html = re.sub(r'\n \.jfx-wk[^\n]*\n(?:[^\n]*\n)*?(?= \.jfx-fmt\{|\n?</style>)', '\n', html, count=1)
html = re.sub(r'\n\}\)\(\);\n\(function\(\)\{\n?document\.addEventListener\(\'click\'.*?\n\}\);\n',
              '\n', html, count=1, flags=re.S)
if len(html) >= _n0:
    raise SystemExit('dead demo code was not removed')

open(OUT, 'w', encoding='utf-8').write(html)

# ------------------------------------------------------------ post checks ---
panels = re.split(r'(?=<div class="brand-panel" data-b=")', html)[1:]
checks = [
    ('five panels', len(panels) == N),
    ('source untouched', open(SRC, encoding='utf-8').read() != html),
    ('cards section on every panel', html.count('<section class="jfx-hx">') == N),
    ('four cards per panel', html.count('class="jfx-hx-c"') == 4 * N),
    ('navy demo band retired', '<section class="jfx-wk">' not in html
     and 'class="jfx-wk-poster"' not in html),
    ('no dead demo css or handler left', '.jfx-wk-poster{' not in html and '.jfx-wk{' not in html),
    ('heading appears once per panel',
     html.count('Manage your hiring event from start to finish.') == N),
    ('brand photo on card one, per brand',
     all(('brand-%s.jpg' % b) in p for b, p in zip(meta, panels))),
    ('product captures on cards two to four',
     all(html.count(i) == N for i in ('card-interviewers.jpg', 'card-settings.jpg', 'card-report.jpg'))),
    ('indeed geometry', all(v in html for v in ('max-width:1354px', 'gap:30px', 'font-size:28px;line-height:35px',
                                                'font-size:16px;line-height:24px', 'padding:0 32px 32px',
                                                'margin:56px 0 8px', 'aspect-ratio:2/1'))),
    ('two videos per panel', html.count('class="jfx-hx-play"') == 2 * N and html.count('2:40') == N),
    ('image frame owns its height', 'position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover' in html),
    ('lg gutter gives 306-wide cards', '@media (min-width:1024px){.jfx-hx-in{padding:0 20px}}' in html
     and 'box-sizing:border-box;max-width:1354px' in html),
    ('no eager youtube iframe', not re.search(r'<iframe[^>]*youtube', html)),
    ('sits where the demo band was, above the format section',
     all(p.index('jfx-hx') < p.index('jfx-fmt') for p in panels)),
    ('review interview outcomes retired',
     'jfx-ro' not in html and 'Review interview outcomes' not in html),
    ('post-event said once, on card four', html.count('Event performance') == N),
    ('toggle script intact', "show('healthcare')" in html),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
