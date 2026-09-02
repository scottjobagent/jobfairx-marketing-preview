"""Mock-up: the Hiring Event Demo as Indeed's four boxes, in our pattern.

Indeed's "Managing your event from start to finish" is a heading over four
cards side by side: photo, title, two lines, a link. This is that structure on
our navy band with our card language, and the photos are real product
captures instead of stock.

  1 Manage your hiring event   -> the 2:40 demo (poster = the live lobby)
  2 Add interviewers           -> the 0:45 tutorial (dashboard, interviewer setup)
  3 Interview settings         -> help-centre article (the settings screen)
  4 Event performance          -> help-centre article (the event report)

Card images are 800x450 crops of the product captures in assets/product,
made by the same session. Links are placeholders except the two videos.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', 'healthcare.html')
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
VARIANT = os.environ.get('JFX_CARDS', 'product')   # 'product' | 'stock'
OUT = os.path.join(MKT, 'event-cards-markup.html' if VARIANT == 'product'
                   else 'event-cards-stock-markup.html')
BASE = 'https://jobfairx.com'
TUTORIALS = 'https://claude.ai/code/artifact/1f6bfb21-9776-41cf-988c-cd3b7c15cc05'

bb = open(BRAND_BUILDER, encoding='utf-8').read()
ns = {'re': re}
exec(bb[bb.index('CARDS = ['):bb.index('# ----------------------------------------- retire the Built-in Tools bento ---')], ns)
VIDEO_ID, POSTER, WALK_CSS = ns['VIDEO_ID'], ns['POSTER'], ns['WALK_CSS']

# Two image sets. 'product' uses real captures of the app; 'stock' uses the
# licensed people photography already on the live site (the five brand heroes) —
# the closest we get to Indeed's treatment without buying new stock.
IMAGES = {
    'product': ['card-interviewers.jpg', 'card-settings.jpg', 'card-report.jpg'],
    'stock': ['stock-manage.jpg', 'stock-interviewers.jpg', 'stock-settings.jpg', 'stock-report.jpg'],
}
if VARIANT not in IMAGES:
    raise SystemExit('JFX_CARDS must be product or stock')
for f in IMAGES[VARIANT]:
    if not os.path.exists(os.path.join(MKT, f)):
        raise SystemExit('missing card image: ' + f)


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


src = open(SRC, encoding='utf-8').read()
head = strip_runtime(re.search(r'<head\b[^>]*>(.*?)</head>', src, re.S).group(1))
head = absolutise(re.sub(r'<title>.*?</title>|<link rel="canonical"[^>]*>', '', head, flags=re.S))
hs = src.index('<header')
hdr = absolutise(strip_runtime(src[hs:close_of(src, hs, 'header')]))
fs = src.index('<footer')
ftr = absolutise(strip_runtime(src[fs:close_of(src, fs, 'footer')]))

# ---------------------------------------------------------------- the cards ---
CARDS = [
    dict(img=POSTER if VARIANT == 'product' else 'stock-manage.jpg',
         alt=('The event-day lobby with interview rooms ready to start' if VARIANT == 'product'
              else 'A hiring manager greeting a candidate'),
         title='Manage your hiring event',
         desc='The full walkthrough: set your format, manage requests, run the event-day lobby, and conduct interviews.',
         cta='Watch the video', meta='2:40', href='https://www.youtube.com/watch?v=' + VIDEO_ID, video=True),
    dict(img='card-interviewers.jpg' if VARIANT == 'product' else 'stock-interviewers.jpg',
         alt=('The events dashboard showing interviewer setup for each event' if VARIANT == 'product'
              else 'Two colleagues setting up an event together'),
         title='Add interviewers',
         desc='Put your team on the event. Who can interview, how many seats you have, and what each interviewer receives.',
         cta='Watch the video', meta='0:45', href=TUTORIALS, video=True),
    dict(img='card-settings.jpg' if VARIANT == 'product' else 'stock-settings.jpg',
         alt=('The interview settings screen with video, phone and in-person options' if VARIANT == 'product'
              else 'A recruiter preparing for interviews'),
         title='Interview settings',
         desc='Choose video, in person, or phone, set your time slots, and decide how many interviews your team runs at once.',
         cta='Read the article', meta='', href='#', video=False),
    dict(img='card-report.jpg' if VARIANT == 'product' else 'stock-report.jpg',
         alt=('The event report with yes, maybe and no outcomes for every candidate' if VARIANT == 'product'
              else 'A hiring manager reviewing results after an event'),
         title='Event performance',
         desc='Your post-event report: every interview, every outcome, who interviewed whom, and export in one click.',
         cta='Read the article', meta='', href='#', video=False),
]


def card(c):
    ext = ' target="_blank" rel="noopener"' if c['href'].startswith('http') else ''
    play = ('<span class="jfx-cd-play" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" '
            'fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>') if c['video'] else ''
    meta = (' <span class="jfx-cd-meta">&middot; %s</span>' % c['meta']) if c['meta'] else ''
    return ('<a class="jfx-cd" href="%s"%s>'
            '<span class="jfx-cd-cap"><img src="%s" width="800" height="450" alt="%s">%s</span>'
            '<span class="jfx-cd-body"><span class="jfx-cd-t">%s</span><span class="jfx-cd-d">%s</span>'
            '<span class="jfx-cd-cta">%s%s <i>&rarr;</i></span></span></a>'
            % (c['href'], ext, c['img'], c['alt'], play, c['title'], c['desc'], c['cta'], meta))


SECTION = ('<section class="jfx-wk jfx-cards-band"><div class="jfx-wk-in jfx-cards-in">'
           '<div class="jfx-cards-head"><p class="jfx-wk-eyeb">Hiring Event Demo</p>'
           '<h2 class="jfx-wk-h">Manage your hiring event from start to finish.</h2></div>'
           '<div class="jfx-cards">%s</div></div></section>' % ''.join(card(c) for c in CARDS))

CARDS_CSS = '''
 .jfx-cards-in{display:block!important;grid-template-columns:none!important}
 .jfx-cards-head{max-width:640px;margin:0 0 36px}
 @media (min-width:1024px){.jfx-cards-head{margin-bottom:44px}}
 .jfx-cards-band .jfx-wk-h{margin-bottom:0!important}
 .jfx-cards{display:grid;grid-template-columns:1fr;gap:20px}
 @media (min-width:640px){.jfx-cards{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}}
 @media (min-width:1024px){.jfx-cards{grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}}
 .jfx-cd{display:flex;flex-direction:column;background:#fff;border-radius:16px;overflow:hidden;
   text-decoration:none;color:inherit;box-shadow:0 18px 48px -12px rgba(0,0,0,.28),0 4px 12px rgba(0,0,0,.08);
   transition:transform .2s ease,box-shadow .2s ease}
 .jfx-cd:hover{transform:translateY(-3px);box-shadow:0 26px 60px -12px rgba(0,0,0,.36),0 6px 16px rgba(0,0,0,.1)}
 .jfx-cd:focus-visible{outline:3px solid #8fbbff;outline-offset:3px}
 .jfx-cd-cap{position:relative;display:block;aspect-ratio:16/9;background:#eef2f7;border-bottom:1px solid #e2e8f0}
 .jfx-cd-cap img{display:block;width:100%;height:100%;object-fit:cover}
 .jfx-cd-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;
   background:#fff;color:#00245b;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.28)}
 .jfx-cd-play svg{margin-left:2px}
 .jfx-cd-body{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}
 .jfx-cd-t{font-size:18px;font-weight:600;letter-spacing:-.01em;color:#0b1220;line-height:1.25;margin-bottom:8px}
 .jfx-cd-d{font-size:14px;line-height:1.55;color:#5a6478;margin-bottom:18px}
 .jfx-cd-cta{margin-top:auto;font-size:14px;font-weight:600;color:#2563eb}
 .jfx-cd-cta i{font-style:normal;display:inline-block;margin-left:4px;transition:transform .15s ease}
 .jfx-cd:hover .jfx-cd-cta i{transform:translateX(3px)}
 .jfx-cd-meta{font-weight:500;color:#64748b}
'''

_WHICH = ('<b>real product captures</b> &mdash; the lobby, the events dashboard, the interview settings screen '
          'and the event report' if VARIANT == 'product'
          else '<b>people photography</b> &mdash; the licensed brand photos already on the live site, which is '
               'Indeed&rsquo;s treatment')
NOTE = ('<div class="jfx-note"><span class="jfx-note-k">Four boxes &middot; ' + VARIANT + ' images</span>'
        '<span class="jfx-note-b">Indeed&rsquo;s structure &mdash; a heading over four cards side by side, each '
        'with an image, a title, two lines and a link &mdash; on our navy band with our card style. Images here '
        'are ' + _WHICH + '. Two cards are videos, two are articles. Links are placeholders except the videos.'
        '</span></div>')

STYLE = ('<style>' + WALK_CSS + CARDS_CSS + '''
 .jfx-note{max-width:1180px;margin:0 auto;padding:14px 18px;display:flex;gap:14px;align-items:flex-start;
   background:#0b1220;color:#dbeafe;font-size:13.5px;line-height:1.5}
 .jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;color:#9fc6ff;flex:none;padding-top:2px;width:190px}
 .jfx-note-b b{color:#fff;font-weight:600}
 @media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
 .jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;padding:9px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .jfx-bar b{color:#fff;font-weight:600}.jfx-bar span{color:#93a4bd}
</style>''')

_OTHER = (('event-cards-stock-markup.html', 'stock photo') if VARIANT == 'product'
          else ('event-cards-markup.html', 'product capture'))
BAR = ('<div class="jfx-bar"><b>Event page &middot; four boxes &middot; ' + VARIANT + ' images</b>'
       '<span>Houston Healthcare &middot; mock-up only</span>'
       '<a href="' + _OTHER[0] + '" style="color:#8fbbff;font-weight:600">See the ' + _OTHER[1] +
       ' version &rarr;</a></div>')

html = ('<!DOCTYPE html><html lang="en"><head>%s<title>Four boxes, ' + VARIANT +
        ' images | JobFairX</title>%s</head><body class="bg-white">%s%s%s%s%s</body></html>'
        ) % (head, STYLE, BAR, hdr, NOTE, SECTION, ftr)
open(OUT, 'w', encoding='utf-8').write(html)

checks = [
    ('four cards', html.count('class="jfx-cd"') == 4),
    ('two videos with play marks and runtimes', html.count('class="jfx-cd-play"') == 2 and '2:40' in html and '0:45' in html),
    ('two articles', html.count('Read the article') == 2),
    ('four distinct images', len(set(re.findall(r'<img src="([^"]+)" width="800"', html))) == 4),
    ('right image set for this variant',
     all(i in html for i in IMAGES[VARIANT])
     and not any(i in html for i in IMAGES['stock' if VARIANT == 'product' else 'product'])),
    ('cross-link to the other variant', _OTHER[0] in html),
    ('heading kept', 'Manage your hiring event from start to finish.' in html),
    ('four-up at desktop, two-up at tablet, one-up on mobile',
     'repeat(4,minmax(0,1fr))' in html and 'repeat(2,minmax(0,1fr))' in html and 'grid-template-columns:1fr;gap:20px' in html),
    ('no eager youtube iframe', '<iframe' not in html),
    ('no runtime capsule in the eyebrow', 'jfx-wk-dur' not in html),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
