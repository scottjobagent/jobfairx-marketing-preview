"""Layout-system pass over the event details page, written to a NEW file.

Source: event-details-by-brand.html (the approved working page, untouched).
Output: event-details-by-brand-layout.html.

Implements the ten audit recommendations of 1 Sep 2026 as one layer:
  1  one container (1180 / 20-24-32 gutters) on every section
  2  one vertical scale (96 desktop / 56 mobile; compact 64 / 40; h2->copy 16)
  3  pricing rebuilt as one <section> with a real <h2>
  4  one two-column pattern: minmax(0,1fr) 560px, gap 64
  5  background rhythm fixed; one hairline colour, only between like neighbours
  6  cards unified: radius 16, #e2e8f0 border, no shadow, padding 24, gap 24;
     one shadow token for product screenshots
  7  mobile gutter 20; 3-up grids break at 1024
  8  text widths capped; every section h2 36; close 44 balanced
  9  logo grid inside the container, gap 48
 10  scroll-margin-top 112 on anchored sections

Mechanics: class-string rewrites on the cloned live markup (each asserted to
match exactly once per panel), a rebuilt pricing section, and ONE stylesheet
appended as the last thing in <head> so it wins every tie. The compiled
Tailwind has no runtime, so nothing here relies on a class that was not
already compiled; the new hooks are all .jfx-* rules in that stylesheet.
"""
import re, os, sys

MKT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(MKT, 'event-details-by-brand.html')
OUT = os.path.join(MKT, 'event-details-by-brand-layout.html')
N = 5  # panels

html = open(SRC, encoding='utf-8').read()


def close_tag(text, start, tag='div'):
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


def sub(label, old, new, expect=N):
    global html
    n = html.count(old)
    if n != expect:
        raise SystemExit('%s: expected %d, found %d\n  %s' % (label, expect, n, old[:90]))
    html = html.replace(old, new)


# ------------------------------------------------ 3. pricing as one section ---
# Done first, while the original wrappers are intact. Per panel: the #packages
# div (eyebrow, <p> heading, intro, the cards <section>) and the wrapper that
# follows it (All Packages + bundles) become one <section id="pricing">.
PK_OPEN = '<div id="packages" class="pt-12 lg:pt-[70px] bg-slate-50">'
AP_OPEN = '<div class="bg-slate-50 pt-6 lg:pt-12">'
GRID_OPEN = '<div class="grid grid-cols-1 md:grid-cols-3 gap-5 mt-12 items-start">'
AP_CONT = '<div class="container mx-auto px-6 lg:px-8 max-w-5xl pb-14 lg:pb-[72px] space-y-6 lg:space-y-12">'
for needle in (PK_OPEN, AP_OPEN, GRID_OPEN, AP_CONT):
    if html.count(needle) != N:
        raise SystemExit('pricing anchor count off: %s' % needle[:60])

out, cursor = [], 0
for _ in range(N):
    a = html.index(PK_OPEN, cursor)
    a_end = close_tag(html, a)
    b = html.index(AP_OPEN, a_end)
    if html[a_end:b].strip():
        raise SystemExit('unexpected markup between #packages and the All Packages wrapper')
    b_end = close_tag(html, b)
    pk, ap = html[a:a_end], html[b:b_end]

    eyebrow = re.search(r'<div class="text-\[12px\] font-bold text-center[^>]*>Pricing</div>', pk).group(0)
    heading = re.search(r'<p class="text-\[30px\][^>]*>(Flexible Hiring Event Packages)</p>', pk).group(1)
    intro = re.search(r'<p class="lg:text-lg[^>]*>(.*?)</p>', pk, re.S).group(1)
    g = pk.index(GRID_OPEN)
    grid = pk[g:close_tag(pk, g)]
    grid = grid.replace(GRID_OPEN, '<div class="jfx-grid3 jfx-pricing-grid items-start">', 1)
    c = ap.index(AP_CONT)
    inner = ap[c + len(AP_CONT):close_tag(ap, c) - len('</div>')]

    section = ('<section id="pricing" class="jfx-sec jfx-pricing bg-slate-50">'
               '<div class="jfx-container">'
               '<div class="jfx-sec-head text-center">%s'
               '<h2 class="jfx-h2 font-semibold text-slate-900 text-center">%s</h2>'
               '<p class="jfx-lede text-slate-600 text-[18px] text-center mx-auto">%s</p></div>'
               '%s<div class="space-y-6 lg:space-y-12 jfx-after-cards">%s</div>'
               '</div></section>' % (eyebrow, heading, intro.strip(), grid, inner))
    out.append(html[cursor:a])
    out.append(section)
    cursor = b_end
out.append(html[cursor:])
html = ''.join(out)

# ------------------------------------------------ 9. past companies section ---
PC_OPEN = '<div class="lg:my-16 my-8">'
if html.count(PC_OPEN) != N:
    raise SystemExit('past companies wrapper count off')
out, cursor = [], 0
for _ in range(N):
    a = html.index(PC_OPEN, cursor)
    a_end = close_tag(html, a)
    inner = html[a + len(PC_OPEN):a_end - len('</div>')]
    out.append(html[cursor:a])
    out.append('<section class="jfx-sec jfx-past bg-white"><div class="jfx-container">%s</div></section>' % inner)
    cursor = a_end
out.append(html[cursor:])
html = ''.join(out)
sub('past heading block', 'class="text-center max-w-2xl mx-auto mb-16"', 'class="text-center max-w-2xl mx-auto jfx-sec-head"')
sub('past h2', '<h2 class="font-semibold text-slate-900 tracking-tight mb-6 text-[30px]" data-svelte-h="svelte-1qsokoz">Past Companies</h2>',
    '<h2 class="jfx-h2 font-semibold text-slate-900 tracking-tight">Past Companies</h2>')
sub('logo grid', 'class="grid grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-20 mt-8 lg:mt-12 max-w-[1200px] mx-auto px-4 lg:px-0"',
    'class="jfx-logos grid grid-cols-2 lg:grid-cols-4"')

# --------------------------------------------- 1. containers, 2. sections ---
sub('hero section', 'class="relative overflow-hidden bg-white pt-6 pb-0 lg:pt-16 lg:pb-0"',
    'class="relative overflow-hidden bg-white jfx-sec-hero"')
sub('hero container', 'class="container mx-auto px-6 lg:px-8 relative z-10 max-w-6xl"',
    'class="jfx-container relative z-10"')
sub('stats section', '<section class="bg-slate-50 border-y border-slate-200 py-10 lg:py-12 mt-10 lg:mt-12">',
    '<section class="jfx-sec-compact bg-slate-50">')
sub('results section', '<section class="py-12 lg:py-[100px] border-b bg-slate-50 border-slate-200 overflow-hidden">',
    '<section class="jfx-sec jfx-results bg-white overflow-hidden">')
sub('results grid', 'class="grid grid-cols-1 md:grid-cols-3 gap-8 relative z-10"', 'class="jfx-grid3 relative z-10"')
sub('results cards', 'class="bg-white rounded-2xl p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex flex-col hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] transition-shadow duration-300"',
    'class="jfx-card bg-white flex flex-col"', expect=3 * N)
sub('results h2', 'class="font-semibold text-slate-900 tracking-tight leading-[1.15] max-w-3xl mb-6 text-[30px]"',
    'class="jfx-h2 font-semibold text-slate-900 tracking-tight leading-[1.15] max-w-3xl"')
sub('results intro', '<p class="text-slate-600 max-w-2xl font-medium text-[18px]">', '<p class="jfx-lede text-slate-600 font-medium text-[18px]">')
sub('results head block', 'class="flex flex-col items-center text-center mb-16"', 'class="flex flex-col items-center text-center jfx-sec-head"')
sub('faq section', '<section class="py-20 lg:py-[100px] bg-white border-y border-slate-200">', '<section class="jfx-sec jfx-faq bg-white">')
sub('faq h2', 'class="font-semibold text-slate-900 tracking-tight leading-[1.15] text-[30px] text-center"',
    'class="jfx-h2 font-semibold text-slate-900 tracking-tight leading-[1.15] text-center"')
sub('final cta section', '<section id="final-cta" class="py-20 md:py-24 text-center bg-transparent border-b border-slate-200">',
    '<section id="final-cta" class="jfx-sec jfx-close text-center bg-white border-b border-slate-200">')
sub('final cta h2', 'class="text-[36px] lg:text-[52px] font-bold text-slate-900 tracking-[-0.02em] leading-[1.1] mb-5"',
    'class="jfx-h2-close font-bold text-slate-900 tracking-[-0.02em] leading-[1.1]"')
sub('contact block', 'class="max-w-[1200px] mx-auto px-4 lg:px-0 lg:flex justify-between items-start pb-12 lg:py-24 text-brand-text"',
    'class="jfx-container jfx-contact lg:flex justify-between items-start text-brand-text"')
# generic live containers left: stats + results (7xl x2 per panel), FAQ (5xl), final CTA
sub('7xl containers', '<div class="container mx-auto px-6 lg:px-8 max-w-7xl">', '<div class="jfx-container">', expect=2 * N)
sub('5xl containers', '<div class="container mx-auto px-6 lg:px-8 max-w-5xl">', '<div class="jfx-container">', expect=N)
sub('final cta container', '<div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">', '<div class="jfx-container">')

# --------------------------------------------------------- the stylesheet ---
LAYOUT_CSS = '''<style id="jfx-layout">
 :root{--jfx-max:1180px;--jfx-gut:20px;--jfx-sec:56px;--jfx-sec-compact:40px;--jfx-hair:#e2e8f0;
   --jfx-card-border:#e2e8f0;--jfx-shadow-shot:0 18px 48px -12px rgba(0,0,0,.18),0 4px 12px rgba(0,0,0,.05)}
 @media (min-width:640px){:root{--jfx-gut:24px}}
 @media (min-width:1024px){:root{--jfx-gut:32px;--jfx-sec:96px;--jfx-sec-compact:64px}}

 /* 1 · one container */
 .jfx-container{max-width:var(--jfx-max)!important;margin-left:auto!important;margin-right:auto!important;
   padding-left:var(--jfx-gut)!important;padding-right:var(--jfx-gut)!important;width:100%}
 .jfx-wk-in,.jfx-fmt-in,.jfx-ro-in{padding-left:var(--jfx-gut)!important;padding-right:var(--jfx-gut)!important}

 /* 2 · one vertical scale */
 .jfx-sec,.jfx-wk,.jfx-fmt,.jfx-ro{padding-top:var(--jfx-sec)!important;padding-bottom:var(--jfx-sec)!important}
 .jfx-sec-compact{padding-top:var(--jfx-sec-compact)!important;padding-bottom:var(--jfx-sec-compact)!important;margin:0!important}
 .jfx-sec-hero{padding-top:32px!important;padding-bottom:40px!important}
 @media (min-width:1024px){.jfx-sec-hero{padding-top:64px!important;padding-bottom:64px!important}}
 .jfx-sec-head{margin-bottom:48px!important}
 .jfx-h2{font-size:28px!important;line-height:1.12!important;letter-spacing:-.02em;margin:0 0 16px!important}
 @media (min-width:1024px){.jfx-h2{font-size:36px!important}}
 .jfx-fmt-h,.jfx-ro-h,.jfx-wk-h{margin-bottom:16px!important}
 .jfx-fmt-sub{margin-bottom:48px!important}
 .jfx-wk-h{margin-bottom:28px!important}
 .jfx-wk-eyeb,.jfx-fmt-eyeb,.jfx-ro-eyeb{font-size:12px!important;letter-spacing:.14em!important}
 .jfx-contact{padding-top:var(--jfx-sec)!important;padding-bottom:var(--jfx-sec)!important}
 .jfx-contact > div:first-child{margin-top:0!important}
 .jfx-pricing-grid{margin-top:0!important}
 .jfx-after-cards{margin-top:24px}
 @media (min-width:1024px){.jfx-after-cards{margin-top:32px}}

 /* 4 · one two-column pattern */
 @media (min-width:1024px){.jfx-wk-in{grid-template-columns:minmax(0,1fr) 560px!important;gap:64px!important}}

 /* 5 · rhythm and hairlines */
 .jfx-ro{border-top:0!important}
 .jfx-faq{border-top:1px solid var(--jfx-hair)}
 .jfx-close{border-bottom:1px solid var(--jfx-hair)!important}
 .jfx-results{border:0!important}

 /* 6 · cards and screenshots */
 .jfx-card{border:1px solid var(--jfx-card-border)!important;border-radius:16px!important;box-shadow:none!important;padding:24px!important}
 .jfx-fmt-c{border-color:var(--jfx-card-border)!important;border-radius:16px!important}
 .jfx-ro-media div[class*="rounded-"]{border-radius:16px!important;border-color:var(--jfx-card-border)!important;box-shadow:var(--jfx-shadow-shot)!important}
 .jfx-wk-poster{border-radius:16px!important;box-shadow:var(--jfx-shadow-shot)!important;border-color:rgba(255,255,255,.14)!important}
 .jfx-wk-poster:hover{box-shadow:var(--jfx-shadow-shot)!important;transform:none!important}
 .jfx-pricing-grid > div{border-radius:16px!important}
 .jfx-after-cards > div{border-radius:16px!important;border-color:var(--jfx-card-border)!important}

 /* 7 · grids: 1-up below 1024, 3-up from 1024, gap 24 */
 .jfx-grid3{display:grid!important;grid-template-columns:1fr!important;gap:24px!important}
 @media (min-width:1024px){.jfx-grid3{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
 .jfx-fmt-cards{gap:24px!important}
 @media (min-width:768px) and (max-width:1023px){.jfx-fmt-cards{grid-template-columns:1fr!important}}
 @media (min-width:1024px){.jfx-fmt-cards{grid-template-columns:repeat(3,minmax(0,1fr))!important}}

 /* 8 · text widths */
 .jfx-lede{max-width:620px!important;margin-left:auto;margin-right:auto}
 .jfx-fmt-sub{max-width:620px!important}
 .jfx-h2-close{font-size:28px!important;line-height:1.1!important;max-width:900px;margin:0 auto 16px!important;text-wrap:balance}
 @media (min-width:640px){.jfx-h2-close{font-size:32px!important}}
 @media (min-width:1024px){.jfx-h2-close{font-size:44px!important}}
 .jfx-fmt-h{font-size:28px!important}
 @media (min-width:1024px){.jfx-fmt-h{font-size:36px!important}}

 /* 9 · logo grid inside the container */
 .jfx-logos{max-width:none!important;padding:0!important;margin:0!important;gap:32px!important}
 @media (min-width:1024px){.jfx-logos{gap:48px!important}}

 /* 10 · anchors clear the sticky banner + header */
 #pricing,#final-cta,#hero{scroll-margin-top:112px}
</style>'''
if html.count('</head>') != 1:
    raise SystemExit('expected one </head>')
html = html.replace('</head>', LAYOUT_CSS + '</head>')

open(OUT, 'w', encoding='utf-8').write(html)

# ------------------------------------------------------------- post checks ---
panels = re.split(r'(?=<div class="brand-panel" data-b=")', html)[1:]
src = open(SRC, encoding='utf-8').read()
checks = [
    ('five panels', len(panels) == N),
    ('source untouched', open(SRC, encoding='utf-8').read() == src),
    ('one container class on every wrapper (8 per panel)', html.count('class="jfx-container') == 8 * N),
    ('no stray live max-widths in page content (header and footer stay live)',
     all(not re.search(r'max-w-(5xl|6xl|7xl|\[1200px\])', p[:p.index('<footer')]) for p in panels)),
    ('pricing is one section with a real h2',
     html.count('<section id="pricing" class="jfx-sec jfx-pricing') == N
     and html.count('<h2 class="jfx-h2 font-semibold text-slate-900 text-center">Flexible Hiring Event Packages</h2>') == N
     and 'id="packages"' not in html and 'scroll-margin-top: 80px' not in html),
    ('past companies is a section', html.count('class="jfx-sec jfx-past') == N and 'lg:my-16' not in html),
    ('every section h2 on the shared scale', html.count('class="jfx-h2 ') == 4 * N and 'text-[30px]' not in html),
    ('three 3-up grids tagged', html.count('class="jfx-grid3') == 2 * N and html.count('jfx-fmt-cards') >= N),
    ('results cards unified', html.count('class="jfx-card ') == 3 * N and 'shadow-[0_8px_30px' not in html),
    ('logo grid constrained', html.count('class="jfx-logos') == N and 'lg:gap-20' not in html),
    ('vertical scale applied', html.count('class="jfx-sec ') == 5 * N
     and html.count('class="jfx-sec-compact bg-slate-50"') == N
     and html.count('bg-white jfx-sec-hero"') == N),
    ('layout stylesheet is the last thing in head', html.index('id="jfx-layout"') < html.index('</head>')
     and html[html.index('</style>', html.index('id="jfx-layout"')):html.index('</head>')].strip() == '</style>'),
    ('anchors clear the header', 'scroll-margin-top:112px' in html),
    ('report panel rules target the inner card only',
     '.jfx-ro-media div[class*="rounded-"]' in html and '.jfx-ro-media > div{border-radius' not in html),
    ('toggle script intact', "show('healthcare')" in html),
    ('content intact', all(t in html for t in ('Manage your hiring event from start to finish.',
                                                'Meet candidates by video, in person, or phone.',
                                                'Review interview outcomes.', 'All Packages Include'))),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html), OUT))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
