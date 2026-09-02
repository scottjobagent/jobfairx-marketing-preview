"""Developer notes for the event details page update (1 Sep 2026).

Everything the developer needs, on one page: the four changes, the exact
markup / CSS / JS, the copy as plain text, the poster asset, and a link to the
visual reference. Emits the deployable HTML and a Markdown twin for the repo.

The code blocks are NOT typed here. They are read out of
build-event-details-by-brand.py at build time (the same strings that produce
the by-brand review page), so the notes cannot drift from what Scott approved.
Every extraction asserts.
"""
import re, os, sys, html as H, datetime

MKT = os.path.dirname(os.path.abspath(__file__))
BRAND_BUILDER = os.path.join(MKT, 'build-event-details-by-brand.py')
OUT_HTML = os.path.join(MKT, 'event-details-dev-notes.html')
OUT_MD = os.path.join(MKT, 'EVENT-DETAILS-DEV-NOTES.md')

PREVIEW = 'https://scottjobagent.github.io/jobfairx-marketing-preview/'
REF_PAGE = PREVIEW + 'event-details-by-brand.html'
POSTER_URL = PREVIEW + 'walkthrough-poster.jpg'
LIVE_EXAMPLE = 'https://jobfairx.com/employer/job-fairs/texas/houston/next-healthcare'
DATE = datetime.date(2026, 9, 1).strftime('%-d %b %Y')

# ------------------------------------- the approved strings, from the builder ---
bb = open(BRAND_BUILDER, encoding='utf-8').read()
start = bb.index('CARDS = [')
end = bb.index('# ----------------------------------------- retire the Built-in Tools bento ---')
ns = {'re': re}
exec(bb[start:end], ns)
for k in ('CARDS', 'section_for', 'SECTION_CSS', 'VIDEO_ID', 'POSTER', 'WALK_STEPS',
          'WALK', 'WALK_CSS', 'WALK_JS', 'outcomes_for', 'OUTCOMES_CSS', 'OUTCOME_POINTS'):
    if k not in ns:
        raise SystemExit('builder no longer defines %s' % k)


def grab(pattern, label):
    m = re.search(pattern, bb, re.S)
    if not m:
        raise SystemExit('could not find %s in the by-brand builder' % label)
    return m.group(1)


# The report panel is the live post-event component, lifted from the captured
# Houston page so the notes show the developer the exact element to reuse.
CAPTURE = os.path.join(MKT, 'captures', 'healthcare.html')
_cap = open(CAPTURE, encoding='utf-8').read()


def _close(text, start, tag):
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


_hs = _cap.index('<section class="how-section')
_sec = _cap[_hs:_close(_cap, _hs, 'section')]
_steps = [m.start() for m in re.finditer(r'<div class="how-step', _sec)]
if len(_steps) != 3:
    raise SystemExit('live How It Works no longer has three beats')
_row = _sec[_steps[2]:_close(_sec, _steps[2], 'div')]
_tx = _row.index('<div class="how-text')
REPORT_PANEL = _row[_close(_row, _tx, 'div'):_row.rindex('</div>')].strip()
REPORT_PANEL = re.sub(r'\sdata-svelte-h="[^"]*"', '', REPORT_PANEL)
REPORT_PANEL, _n = re.subn(r'\b[A-Z][a-z]{2} \d{1,2}, 20\d\d\b', '{Event date}', REPORT_PANEL)
if _n != 1 or 'feedback' not in REPORT_PANEL.lower():
    raise SystemExit('report panel lift failed')

DEMO_HTML = ns['WALK']
FMT_HTML = ns['section_for']('{City}')
if '{{CITY}}' in FMT_HTML or '{City}' not in FMT_HTML:
    raise SystemExit('city token did not land in the format section')

# Production only ever renders one event, so the click handler can be direct.
PROD_JS = '''document.querySelector('.jfx-wk-poster').addEventListener('click', function () {
  var f = document.createElement('iframe');
  f.className = 'jfx-wk-frame';
  f.src = 'https://www.youtube.com/embed/%s?rel=0&autoplay=1';
  f.title = 'How to Run Your Hiring Event';
  f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
  f.allowFullscreen = true;
  this.replaceWith(f);
});''' % ns['VIDEO_ID']

# Only the walkthrough rules that the demo section actually uses.
DEMO_CSS = '\n'.join(l for l in ns['WALK_CSS'].splitlines()
                     if l.strip() and not re.match(r'\s*\.jfx-wk-(steps|s|n|st)\b', l)
                     and 'jfx-wk-steps' not in l)


def text(x):
    return H.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()


def pretty(markup):
    """One element per line so the code block is readable; the markup is
    whitespace-insensitive so this changes nothing when pasted."""
    return re.sub(r'>\s*<', '>\n<', markup).strip()


fmt_eyebrow = text(re.search(r'jfx-fmt-eyeb">(.*?)</p>', FMT_HTML).group(1))
fmt_h2 = text(re.search(r'jfx-fmt-h">(.*?)</h2>', FMT_HTML).group(1))
fmt_sub = text(re.search(r'jfx-fmt-sub">(.*?)</p>', FMT_HTML).group(1))
demo_eyebrow = text(re.search(r'jfx-wk-eyeb">(.*?)</p>', DEMO_HTML).group(1))
demo_h2 = text(re.search(r'jfx-wk-h">(.*?)</h2>', DEMO_HTML).group(1))

# ------------------------------------------------------------ the document ---
# blocks: ('p', text) ('ul', [..]) ('code', lang, text) ('copy', label, text) ('note', text)
DOC = [
    ('Read this first', [
        ('p', 'Four changes to the <strong>event details page template</strong>. They apply to '
              'every event type and every city page, because they change the template, not one event.'),
        ('p', 'Header, footer and everything not named below stay exactly as they are on the live '
              'site. Apply only the content changes here.'),
        ('p', 'Visual reference for all four: <a href="%s">%s</a>. Toggle the brand bar at the top '
              'to see the page in each event type; the bar itself is a review tool and is not part '
              'of the update.' % (REF_PAGE, REF_PAGE)),
        ('p', 'Live example for orientation: <a href="%s">Houston Healthcare</a>.' % LIVE_EXAMPLE),
        ('ul', [
            '<strong>Change 1</strong> &mdash; replace the video section with the Hiring Event Demo band.',
            '<strong>Change 2</strong> &mdash; add the Choose Your Interview Format section directly below it.',
            '<strong>Change 3</strong> &mdash; replace How It Works with the Review Interview Outcomes section.',
            '<strong>Change 4</strong> &mdash; remove the Built-in Tools section.',
        ]),
        ('p', 'The compiled Tailwind on the live site has no runtime, so anything new here ships as '
              'scoped CSS under <code>.jfx-wk-*</code>, <code>.jfx-fmt-*</code> and '
              '<code>.jfx-ro-*</code>. No new Tailwind classes are relied on.'),
    ]),

    ('Change 1 · Replace the video section with the Hiring Event Demo', [
        ('p', '<strong>Where:</strong> the section <code>#how-it-works-video</code> &mdash; eyebrow '
              '&ldquo;Watch walkthrough&rdquo;, heading &ldquo;See How JobFairX Works&rdquo;, the YouTube '
              'embed. Remove that whole <code>&lt;section&gt;</code> and put this one in its place. It '
              'sits after the stats and logo strip, before How It Works.'),
        ('p', '<strong>What it is:</strong> a navy band. Left: eyebrow, headline, five numbered steps. '
              'Right: a poster frame with our own play button. The YouTube iframe is created only when '
              'the poster is clicked, so none of YouTube&rsquo;s chrome appears on the page until the '
              'visitor asks for the video.'),
        ('copy', 'Copy', '%s\n\n%s\n\n%s' % (demo_eyebrow.upper(), demo_h2,
                                             '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(ns['WALK_STEPS'])))),
        ('p', '<strong>Poster image:</strong> <a href="%s">walkthrough-poster.jpg</a> (1052&times;586, '
              '52&nbsp;KB). Copy it into your assets and point the <code>&lt;img src&gt;</code> at it. '
              'It is a frame from the video, so it stays accurate if the video does. No lazy-loading '
              'needed; it is one small image near the top of the page.' % POSTER_URL),
        ('p', '<strong>Video:</strong> YouTube <code>%s</code> (&ldquo;How to Run Your Hiring '
              'Event&rdquo;). Same video for every event type.' % ns['VIDEO_ID']),
        ('code', 'html', pretty(DEMO_HTML)),
        ('code', 'css', DEMO_CSS.strip()),
        ('code', 'js', PROD_JS),
        ('note', 'Navy is <code>#00245b</code>, the same dark used on the employer home page&rsquo;s '
                 'reschedule section. Not a new colour.'),
    ]),

    ('Change 2 · Add the Choose Your Interview Format section', [
        ('p', '<strong>Where:</strong> a new section directly below the Hiring Event Demo and above '
              'How It Works. White background.'),
        ('p', '<strong>What it is:</strong> centred eyebrow, headline and one-paragraph sub, then three '
              'equal cards &mdash; Video, In person, Phone, in that order. Each card has a soft '
              'gradient header, an icon tile, a title and a description. No links on the cards.'),
        ('p', '<strong>The city token:</strong> the sub names the event&rsquo;s city. Render '
              '<code>{City}</code> from the event record, city only, no state &mdash; '
              '&ldquo;Houston&rdquo;, &ldquo;Los Angeles&rdquo;, &ldquo;Chicago&rdquo;.'),
        ('copy', 'Copy', '%s\n\n%s\n\n%s\n\n%s' % (
            fmt_eyebrow.upper(), fmt_h2, fmt_sub,
            '\n\n'.join('%s\n%s' % (c['title'], c['desc']) for c in ns['CARDS']))),
        ('code', 'html', pretty(FMT_HTML)),
        ('code', 'css', ns['SECTION_CSS'].strip()),
        ('note', 'The three card colours are the calendar&rsquo;s existing event-type palette '
                 '(<code>#2563eb</code>, <code>#0e9488</code>, <code>#b45309</code>). The '
                 'decorative arc and dot pattern are pure CSS on the section; nothing to export.'),
    ]),

    ('Change 3 · Replace How It Works with Review Interview Outcomes', [
        ('p', '<strong>Where:</strong> the How It Works section &mdash; eyebrow &ldquo;How It Works&rdquo;, '
              'heading &ldquo;Hiring Events Built Around Interviews&rdquo;, three alternating rows with '
              'product panels. Remove that whole <code>&lt;section class="how-section&hellip;"&gt;</code> '
              'and put this one in its place, between the format cards and the testimonials.'),
        ('p', '<strong>Why:</strong> two of its three rows repeat what the Hiring Event Demo now says. The '
              'third row &mdash; the post-event report &mdash; is the one thing nothing else on the page '
              'covers, so it becomes its own section.'),
        ('p', '<strong>What it is:</strong> light-grey band. Left: eyebrow, headline, one line, three '
              'checked points, a link. Right: the <strong>post-event report panel you already have</strong> '
              '&mdash; it is the third row&rsquo;s visual from the current How It Works, moved here '
              'unchanged. Its date line must be the event&rsquo;s own date; today the live panel shows a '
              'different old date on every event type (Apr 22 on Healthcare, Nov 13 2025 on Technology, and '
              'so on), which is a bug worth fixing while you are in there.'),
        ('copy', 'Copy', 'AFTER THE EVENT\n\nReview interview outcomes.\n\nYour post-event report is ready '
                         'in your dashboard. Every interview, every outcome, and who on your team saw whom.\n\n'
                         + '\n'.join('\u2713 %s%s' % (h, t.replace('&#8217;', '\u2019').replace('&#8209;', '-'))
                                     for h, t in ns['OUTCOME_POINTS'])
                         + '\n\nRegister for an event \u2192'),
        ('code', 'html', pretty(ns['outcomes_for']('<!-- your existing post-event report panel, dated to the event -->'))),
        ('code', 'css', ns['OUTCOMES_CSS'].strip()),
        ('p', 'For reference, the report panel as it exists on the live page today, with the date line '
              'tokenised. Reuse your component rather than pasting this.'),
        ('code', 'html', pretty(REPORT_PANEL)),
    ]),

    ('Change 4 · Remove the Built-in Tools section', [
        ('p', '<strong>Where:</strong> between How It Works and the testimonials. Eyebrow '
              '&ldquo;Built-in Tools&rdquo;, heading &ldquo;Candidate Messaging and Interview '
              'Scheduling&rdquo;, three sticky-scroll panels (Candidate Messaging, Flexible Scheduling, '
              'Interview Tracking) with the messaging and scheduling mock-ups. Opens with '
              '<code>&lt;section class="py-12 min-[901px]:py-24 bg-[#f8f7f4]"&gt;</code>.'),
        ('p', 'Remove the whole section. Nothing replaces it; the testimonials move up to follow '
              'How It Works directly. It was already removed from the employer home page in the '
              'previous update.'),
    ]),

    ('Checking your work', [
        ('ul', [
            'Top of the page reads: hero &rarr; stats and logos &rarr; <strong>Hiring Event Demo</strong> '
            '&rarr; <strong>Choose Your Interview Format</strong> &rarr; <strong>Review Interview '
            'Outcomes</strong> &rarr; testimonials.',
            'No &ldquo;See How JobFairX Works&rdquo;, no &ldquo;Hiring Events Built Around '
            'Interviews&rdquo; and no &ldquo;Built-in Tools&rdquo; anywhere on the page.',
            'The report panel&rsquo;s date line is the event&rsquo;s own date.',
            'No runtime appears anywhere in the demo &mdash; not next to the eyebrow, not on the poster.',
            'Clicking the poster loads the video in place and it starts playing; before that click, '
            'the page makes no request to youtube.com.',
            'The format sub names the event&rsquo;s city, city only.',
            'Cards read Video, In person, Phone, left to right, and none of them is a link.',
            'Nothing scrolls sideways at 375px. Cards and the poster stack full-width.',
            'Open any two event types side by side: the only differences in these sections are the city '
            'in the sub and nothing else.',
        ]),
    ]),

    ('Files', [
        ('ul', [
            'Visual reference, all five event types: <a href="%s">event-details-by-brand.html</a>' % REF_PAGE,
            'Poster: <a href="%s">walkthrough-poster.jpg</a>' % POSTER_URL,
            'This page: <a href="%sevent-details-dev-notes.html">event-details-dev-notes.html</a>' % PREVIEW,
        ]),
        ('p', 'The review page carries all five event types in one file behind a brand bar. That is a '
              'review convenience only &mdash; production renders one event per page exactly as it does today.'),
    ]),
]

# -------------------------------------------------------------- render html ---
CSS = '''
 :root{--ink:#0f172a;--soft:#475569;--mut:#64748b;--rule:#e2e8f0;--blue:#2563eb;--navy:#00245b;
   --amber:#b45309;--amberbg:#fffbeb;--amberbd:#fde68a}
 *{box-sizing:border-box}
 body{margin:0;background:#fff;color:var(--ink);
  font:400 16px/1.65 Inter,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
 .wrap{max-width:900px;margin:0 auto;padding:48px 24px 110px}
 .kick{font:700 11px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);margin:0 0 14px}
 h1{font-size:36px;line-height:1.15;letter-spacing:-.022em;margin:0 0 10px;font-weight:600}
 .lede{font-size:18px;color:var(--soft);margin:0 0 4px;max-width:68ch}
 .meta{color:var(--mut);font-size:14px;margin:0 0 8px}
 h2{font-size:23px;line-height:1.3;letter-spacing:-.012em;margin:52px 0 14px;font-weight:600;padding-top:22px;border-top:1px solid var(--rule)}
 p{margin:0 0 14px;color:var(--soft);max-width:72ch}
 ul{margin:0 0 16px;padding-left:22px;max-width:72ch}
 li{margin:0 0 10px;color:var(--soft)}
 code{font:500 13.5px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;background:#f1f5f9;color:var(--ink);padding:1.5px 5px;border-radius:4px}
 strong{color:var(--ink);font-weight:600}
 a{color:var(--blue)}
 .links{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 10px}
 .links a{display:inline-block;background:var(--blue);color:#fff;text-decoration:none;border-radius:8px;padding:10px 16px;font-weight:600;font-size:14px}
 .links a.alt{background:#fff;color:var(--blue);border:1px solid var(--blue)}
 .toc{margin:26px 0 0;padding:16px 20px;background:#f8fafc;border:1px solid var(--rule);border-radius:10px}
 .toc ol{margin:0;padding-left:20px}.toc li{margin:4px 0}
 .copy{margin:14px 0 18px;padding:16px 20px;background:#f8fafc;border-left:3px solid var(--navy);border-radius:0 8px 8px 0;
   white-space:pre-wrap;font-size:15px;line-height:1.55;color:var(--ink);max-width:72ch}
 .copy .lab{display:block;font:700 11px/1 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
 pre{margin:12px 0 22px;padding:16px 18px;background:#0b1220;color:#e6edf7;border-radius:10px;overflow:auto;
   font:400 12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;tab-size:2;position:relative}
 pre .lang{position:absolute;right:12px;top:10px;font:700 10px/1 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#93a4bd}
 .note{margin:0 0 18px;padding:12px 16px;background:var(--amberbg);border:1px solid var(--amberbd);border-radius:8px;color:#78350f;font-size:15px;max-width:72ch}
 .note code{background:#fff3c4}
'''


def render_block(b):
    kind = b[0]
    if kind == 'p':
        return '<p>%s</p>' % b[1]
    if kind == 'ul':
        return '<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in b[1])
    if kind == 'code':
        return '<pre><span class="lang">%s</span>%s</pre>' % (b[1], H.escape(b[2]))
    if kind == 'copy':
        return '<div class="copy"><span class="lab">%s</span>%s</div>' % (b[1], H.escape(b[2]))
    if kind == 'note':
        return '<div class="note">%s</div>' % b[1]
    raise SystemExit('unknown block %r' % (kind,))


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', text(t).lower()).strip('-')[:60]


body = []
body.append('<p class="kick">JobFairX &middot; employer marketing</p>')
body.append('<h1>Event details page &mdash; developer notes</h1>')
body.append('<p class="lede">Four changes to the event details page template, approved %s. '
            'Everything you need is on this page.</p>' % DATE)
body.append('<div class="links"><a href="%s">Open the visual reference</a>'
            '<a class="alt" href="%s">Download the poster</a></div>' % (REF_PAGE, POSTER_URL))
body.append('<div class="toc"><ol>%s</ol></div>' % ''.join(
    '<li><a href="#%s">%s</a></li>' % (slug(h), h) for h, _ in DOC))
for heading, blocks in DOC:
    body.append('<h2 id="%s">%s</h2>' % (slug(heading), heading))
    body.extend(render_block(b) for b in blocks)

html_out = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex">'
            '<title>Event details page: developer notes | JobFairX</title>'
            '<style>%s</style></head><body><div class="wrap">%s</div></body></html>'
            % (CSS, ''.join(body)))
open(OUT_HTML, 'w', encoding='utf-8').write(html_out)


# ---------------------------------------------------------------- render md ---
def md_block(b):
    kind = b[0]
    if kind == 'p':
        return text(b[1]) + '\n'
    if kind == 'ul':
        return '\n'.join('- ' + text(x) for x in b[1]) + '\n'
    if kind == 'code':
        return '```%s\n%s\n```\n' % (b[1], b[2])
    if kind == 'copy':
        return '> **%s**\n>\n%s\n' % (b[1], '\n'.join('> ' + l for l in b[2].splitlines()))
    if kind == 'note':
        return '> Note: ' + text(b[1]) + '\n'


md = ['# Event details page — developer notes', '',
      'Four changes to the event details page template, approved %s. The deployed copy of this '
      'document, with the same content, is %sevent-details-dev-notes.html' % (DATE, PREVIEW), '']
for heading, blocks in DOC:
    md.append('## ' + heading)
    md.append('')
    md.extend(md_block(b) for b in blocks)
open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(md))

# ------------------------------------------------------------- post checks ---
checks = [
    ('four changes present', all(('Change %d' % i) in html_out for i in (1, 2, 3, 4))),
    ('demo markup included, five steps', html_out.count(H.escape('class="jfx-wk-s"')) == 5),
    ('no runtime anywhere', 'jfx-wk-dur' not in html_out and 'jfx-wk-time' not in html_out
     and '2:40' not in html_out),
    ('format markup included with the city token',
     H.escape('for the {City} hiring event') in html_out and '{{CITY}}' not in html_out),
    ('three cards in the approved order',
     [c['title'] for c in ns['CARDS']] == ['Video', 'In person', 'Phone']),
    ('outcomes section documented', 'Review interview outcomes.' in html_out
     and H.escape('class="jfx-ro"') in html_out and '.jfx-ro{' in html_out),
    ('report panel reference carries the date token', H.escape('{Event date}') in html_out),
    ('no leftover event-day swap', 'Event day step: copy only' not in html_out),
    ('built-in tools removal present', 'Candidate Messaging and Interview Scheduling' in html_out),
    ('poster and video wired', POSTER_URL in html_out and ns['VIDEO_ID'] in html_out),
    ('production js is direct, not delegated', 'closest' not in PROD_JS and 'addEventListener' in PROD_JS),
    ('demo css carries the poster rules but not the step rules',
     '.jfx-wk-poster' in DEMO_CSS and '.jfx-wk-n{' not in DEMO_CSS and '.jfx-wk-steps' not in DEMO_CSS),
    ('reference link present', REF_PAGE in html_out),
    ('markdown twin written', os.path.getsize(OUT_MD) > 4000),
    ('no vocabulary breaches', not re.search(r'virtual event|career fair|\bbooth\b|applicants', html_out, re.I)),
    ('no reference to the discarded reshuffle prefix', 'jfx-dm' not in html_out),
]
bad = [n for n, ok in checks if not ok]
print('%d bytes -> %s' % (len(html_out), OUT_HTML))
print('%d bytes -> %s' % (os.path.getsize(OUT_MD), OUT_MD))
for n, ok in checks:
    print(('  ok   ' if ok else '  FAIL ') + n)
sys.exit(1 if bad else 0)
