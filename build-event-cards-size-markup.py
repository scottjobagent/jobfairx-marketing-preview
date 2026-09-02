"""Card-size comparison: Indeed's measured dimensions vs our 1180 grid.

Measured off indeed.com/employers/hiring-events/onboarding at a 1440 viewport:

  container   1314 wide (63px gutters)
  grid        4 columns, card 306 wide, gap 30
  card        306 x 548, radius 8, 1px #b4b2b1, no shadow, white
  image       304 x 155 -> 1.96:1 (call it 2:1), full-bleed inside the border
  image->title 56px
  title       28px / 35px line-height, weight 400, margin-bottom 8
  body        16px / 24px, #595959
  link        16px, weight 700, #004fcb
  padding     32 sides and bottom (the image sits above it, edge to edge)
  section h   24px bold, margin-bottom 40
  page        white

Our current cards are 261 x ~340 with an 18px title and 14px body, which is why
they read smaller. This page shows both sizes on white so the difference is
visible in one scroll:

  BAND A  Indeed's exact geometry, our colours and radius
  BAND B  the same card fitted to our 1180 container (261 wide)

Images are the hybrid set: people photo on card 1, product captures on 2-4.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'captures', 'healthcare.html')
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
OUT = os.path.join(MKT, 'event-cards-size-markup.html')
BASE = 'https://jobfairx.com'
TUTORIALS = 'https://claude.ai/code/artifact/1f6bfb21-9776-41cf-988c-cd3b7c15cc05'

bb = open(BRAND_BUILDER, encoding='utf-8').read()
ns = {'re': re}
exec(bb[bb.index('CARDS = ['):bb.index('# ----------------------------------------- retire the Built-in Tools bento ---')], ns)
VIDEO_ID = ns['VIDEO_ID']

IMGS = ['stock-manage.jpg', 'card-interviewers.jpg', 'card-settings.jpg', 'card-report.jpg']
for f in IMGS:
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
    return re.sub(r'(href|src)="/(?!/)', r'\1="%s/' % BASE, t)


def strip_runtime(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<link[^>]*modulepreload[^>]*>', '', t)
    return re.sub(r'\sdata-svelte-h="[^"]*"', '', t)


src = open(SRC, encoding='utf-8').read()
head = strip_runtime(re.search(r'<head\b[^>]*>(.*?)</head>', src, re.S).group(1))
head = absolutise(re.sub(r'<title>.*?</title>|<link rel="canonical"[^>]*>', '', head, flags=re.S))
hs = src.index('<header')
hdr = absolutise(strip_runtime(src[hs:close_of(src, hs, 'header')]))
fs = src.index('<footer')
ftr = absolutise(strip_runtime(src[fs:close_of(src, fs, 'footer')]))

CARDS = [
    dict(img=IMGS[0], alt='A hiring manager greeting a candidate',
         title='Manage your hiring event',
         desc='The full walkthrough: set your format, manage requests, run the event-day lobby, and conduct interviews.',
         cta='Watch the video', meta='2:40', href='https://www.youtube.com/watch?v=' + VIDEO_ID, video=True),
    dict(img=IMGS[1], alt='The events dashboard showing interviewer setup for each event',
         title='Add interviewers',
         desc='Put your team on the event. Who can interview, how many seats you have, and what each interviewer receives.',
         cta='Watch the video', meta='0:45', href=TUTORIALS, video=True),
    dict(img=IMGS[2], alt='The interview settings screen with video, phone and in-person options',
         title='Interview settings',
         desc='Choose video, in person, or phone, set your time slots, and decide how many interviews your team runs at once.',
         cta='Read the article', meta='', href='#', video=False),
    dict(img=IMGS[3], alt='The event report with yes, maybe and no outcomes for every candidate',
         title='Event performance',
         desc='Your post-event report: every interview, every outcome, who interviewed whom, and export in one click.',
         cta='Read the article', meta='', href='#', video=False),
]


def card(c):
    ext = ' target="_blank" rel="noopener"' if c['href'].startswith('http') else ''
    play = ('<span class="jfx-cd-play" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" '
            'fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>') if c['video'] else ''
    meta = (' <span class="jfx-cd-meta">&middot; %s</span>' % c['meta']) if c['meta'] else ''
    return ('<a class="jfx-cd" href="%s"%s>'
            '<span class="jfx-cd-cap"><img src="%s" width="800" height="400" alt="%s">%s</span>'
            '<span class="jfx-cd-body"><span class="jfx-cd-t">%s</span><span class="jfx-cd-d">%s</span>'
            '<span class="jfx-cd-cta">%s%s <i>&rarr;</i></span></span></a>'
            % (c['href'], ext, c['img'], c['alt'], play, c['title'], c['desc'], c['cta'], meta))


def band(mod, eyebrow, heading):
    return ('<section class="jfx-cb %s"><div class="jfx-cb-in">'
            '<p class="jfx-cb-eyeb">%s</p><h2 class="jfx-cb-h">%s</h2>'
            '<div class="jfx-cards">%s</div></div></section>'
            % (mod, eyebrow, heading, ''.join(card(c) for c in CARDS)))


CSS = '''
 .jfx-cb{background:#fff;padding:56px 0}
 @media (min-width:1024px){.jfx-cb{padding:96px 0}}
 .jfx-cb-in{margin:0 auto;padding:0 20px}
 @media (min-width:640px){.jfx-cb-in{padding:0 24px}}
 .jfx-cb-eyeb{margin:0 0 14px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#2563eb}
 .jfx-cb-h{margin:0 0 40px;font-size:28px;font-weight:600;letter-spacing:-.02em;line-height:1.12;color:#0b1220}
 @media (min-width:1024px){.jfx-cb-h{font-size:36px}}
 .jfx-cards{display:grid;grid-template-columns:1fr;gap:20px}
 @media (min-width:640px){.jfx-cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
 .jfx-cd{display:flex;flex-direction:column;background:#fff;border:1px solid #e2e8f0;border-radius:16px;
   overflow:hidden;text-decoration:none;color:inherit;transition:border-color .2s ease,box-shadow .2s ease,transform .2s ease}
 .jfx-cd:hover{border-color:#cbd5e1;box-shadow:0 12px 32px rgba(15,23,42,.08);transform:translateY(-2px)}
 .jfx-cd:focus-visible{outline:3px solid #2563eb;outline-offset:3px}
 .jfx-cd-cap{position:relative;display:block;aspect-ratio:2/1;background:#eef2f7;border-bottom:1px solid #e2e8f0}
 .jfx-cd-cap img{display:block;width:100%;height:100%;object-fit:cover}
 .jfx-cd-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#fff;
   color:#00245b;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.24)}
 .jfx-cd-play svg{margin-left:2px}
 .jfx-cd-body{display:flex;flex-direction:column;flex:1}
 .jfx-cd-t{font-weight:600;letter-spacing:-.015em;color:#0b1220}
 .jfx-cd-d{color:#5a6478}
 .jfx-cd-cta{margin-top:auto;font-weight:700;color:#2563eb}
 .jfx-cd-cta i{font-style:normal;display:inline-block;margin-left:4px;transition:transform .15s ease}
 .jfx-cd:hover .jfx-cd-cta i{transform:translateX(3px)}
 .jfx-cd-meta{font-weight:500;color:#64748b}

 /* BAND A -- Indeed's measured geometry */
 .jfx-a .jfx-cb-in{max-width:1314px}
 @media (min-width:1024px){
   .jfx-a .jfx-cb-in{padding:0 63px}
   .jfx-a .jfx-cards{grid-template-columns:repeat(4,minmax(0,1fr));gap:30px}
   .jfx-a .jfx-cd-play{width:52px;height:52px}
   .jfx-a .jfx-cd-body{padding:0 32px 32px}
   .jfx-a .jfx-cd-t{font-size:28px;line-height:35px;margin:56px 0 8px}
   .jfx-a .jfx-cd-d{font-size:16px;line-height:24px;margin:0 0 28px}
   .jfx-a .jfx-cd-cta{font-size:16px}
 }

 /* BAND B -- the same card fitted to our 1180 container */
 .jfx-b .jfx-cb-in{max-width:1180px}
 @media (min-width:1024px){
   .jfx-b .jfx-cb-in{padding:0 32px}
   .jfx-b .jfx-cards{grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
   .jfx-b .jfx-cd-play{width:46px;height:46px}
   .jfx-b .jfx-cd-body{padding:0 24px 24px}
   .jfx-b .jfx-cd-t{font-size:22px;line-height:28px;margin:32px 0 8px}
   .jfx-b .jfx-cd-d{font-size:15px;line-height:23px;margin:0 0 24px}
   .jfx-b .jfx-cd-cta{font-size:15px}
 }

 /* below lg both bands share one comfortable size */
 @media (max-width:1023px){
   .jfx-cb-in{max-width:1180px}
   .jfx-cd-play{width:46px;height:46px}
   .jfx-cd-body{padding:0 24px 24px}
   .jfx-cd-t{font-size:22px;line-height:28px;margin:28px 0 8px}
   .jfx-cd-d{font-size:15px;line-height:23px;margin:0 0 22px}
   .jfx-cd-cta{font-size:15px}
 }
'''


def note(k, b):
    return ('<div class="jfx-note"><span class="jfx-note-k">%s</span><span class="jfx-note-b">%s</span></div>' % (k, b))


NA = note('Band A &middot; Indeed&rsquo;s dimensions',
          'Their measured geometry: container <b>1314</b>, four cards <b>306&times;548</b>, gap <b>30</b>, image '
          '<b>2:1</b> full-bleed, <b>56px</b> to the title, title <b>28/35</b>, body <b>16/24</b>, padding <b>32</b>. '
          'Our colours, our radius, white background.')
NB = note('Band B &middot; fitted to our grid',
          'The same card inside our <b>1180</b> container: four cards <b>261</b> wide, gap 24, title 22/28, body '
          '15/23, padding 24. Everything else identical. This is the cost of keeping one container width across '
          'the page.')

STYLE = ('<style>' + CSS + '''
 .jfx-note{max-width:1314px;margin:0 auto;padding:14px 20px;display:flex;gap:14px;align-items:flex-start;
   background:#0b1220;color:#dbeafe;font-size:13.5px;line-height:1.5}
 .jfx-note-k{font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:11px;color:#9fc6ff;flex:none;padding-top:2px;width:200px}
 .jfx-note-b b{color:#fff;font-weight:600}
 @media (max-width:800px){.jfx-note{flex-direction:column;gap:6px}.jfx-note-k{width:auto}}
 .jfx-bar{position:sticky;top:0;z-index:60;background:#0b1220;color:#e6edf7;font-size:12.5px;padding:9px 18px;
   display:flex;gap:14px;align-items:center;flex-wrap:wrap}
 .jfx-bar b{color:#fff;font-weight:600}.jfx-bar span{color:#93a4bd}
 .jfx-rule{height:1px;background:#e2e8f0;max-width:1314px;margin:0 auto}
</style>''')

BAR = ('<div class="jfx-bar"><b>Event page &middot; card size comparison</b>'
       '<span>Indeed&rsquo;s measured dimensions vs our 1180 grid &middot; white background &middot; mock-up only</span></div>')

html = ('<!DOCTYPE html><html lang="en"><head>%s<title>Card size comparison | JobFairX</title>%s</head>'
        '<body class="bg-white">%s%s%s%s<div class="jfx-rule"></div>%s%s%s</body></html>'
        % (head, STYLE, BAR, hdr,
           NA, band('jfx-a', 'Hiring Event Demo', 'Manage your hiring event from start to finish.'),
           NB, band('jfx-b', 'Hiring Event Demo', 'Manage your hiring event from start to finish.'),
           ftr))
open(OUT, 'w', encoding='utf-8').write(html)

checks = [
    ('two bands', html.count('class="jfx-cb jfx-a"') == 1 and html.count('class="jfx-cb jfx-b"') == 1),
    ('eight cards', html.count('class="jfx-cd"') == 8),
    ('indeed geometry encoded', all(v in html for v in ('max-width:1314px', 'gap:30px', 'font-size:28px;line-height:35px',
                                                        'font-size:16px;line-height:24px', 'padding:0 32px 32px', 'padding:0 63px'))),
    ('our grid encoded', all(v in html for v in ('max-width:1180px', 'gap:24px', 'font-size:22px;line-height:28px'))),
    ('2:1 images', 'aspect-ratio:2/1' in html),
    ('white background, no navy', '#fff' in html and '#00245b' not in html.split('<footer')[0].split(BAR)[-1]),
    ('four distinct images per band', len(set(re.findall(r'<img src="([^"]+)" width="800"', html))) == 4),
    ('two videos per band', html.count('class="jfx-cd-play"') == 4 and html.count('2:40') == 2),
    ('no eager youtube iframe', '<iframe' not in html),
    ('assets absolutised', not re.search(r'(href|src)="(?:\.\./|/(?!/))', html)),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|\bbooth\b|applicants', html, re.I)),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
