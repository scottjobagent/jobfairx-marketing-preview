#!/usr/bin/env python3
"""Build seeker-home.html from the captured live DOM of jobfairx.com/ (the job seeker home page).

Source of truth: assets/live-capture/seeker-home-live-dom.html (rendered DOM, Aug 30 2026).

The rule of this stream is EDIT THE BUILDER, NEVER THE OUTPUT. Every replacement
asserts its anchor matches an exact number of times, so drift in the live page
fails loudly instead of silently shipping stale copy.

Chrome is cloned byte-identical: head, nav, footer, the 349-link city farm and
the mobile search block. The body argument is authored, because the live one
teaches a product model that no longer exists (its step 3 promises every
interview is a video call on JobFairX).

New markup uses scoped .sk-* classes in one injected <style>, never bare Tailwind
utilities — the live compiled CSS is purged and only carries classes the live
pages already used.
"""
import re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/seeker-home-live-dom.html"
OUT = f"{W}/seeker-home.html"
s = open(SRC, encoding="utf-8").read()
orig_len = len(s)
log = []


def sub(label, old, new, count=1, flags=0, regex=False):
    global s
    if regex:
        new_s, n = re.subn(old, new, s, flags=flags)
    else:
        n = s.count(old)
        new_s = s.replace(old, new) if n == count else s
    if n != count:
        print(f"ABORT [{label}]: {n} matches, expected {count}")
        sys.exit(1)
    s = new_s
    log.append((label, n))


def frozen(label, needle, count):
    """Assert a string survives untouched. The SEO contract, enforced by the build."""
    n = s.count(needle)
    if n != count:
        print(f"ABORT [FROZEN {label}]: {n} occurrences, expected {count}")
        sys.exit(1)
    log.append((f"frozen {label}", n))


# ═══════════════════════════ 1. De-frameworkise ═══════════════════════════
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "", count=34, regex=True)
sub("strip sveltekit preload", ' data-sveltekit-preload-data="hover"', "")
sub("strip HEAD markers", r'<!-- HEAD_svelte-[a-z0-9]+_(?:START|END) -->', "", count=4, regex=True)
sub("strip HTML_TAG markers", r'<!-- HTML_TAG_(?:START|END) -->', "", count=2, regex=True)

# ═══════════════════════════ 2. Localise assets ═══════════════════════════
CSS_V = "v=1"
sub("app css", './_app/immutable/assets/app.7a058851.css', f'assets/seeker-home/app.css?{CSS_V}')
sub("page css", './_app/immutable/assets/2.557b8e8a.css', f'assets/seeker-home/page.css?{CSS_V}')
sub("favicon", './favicon.png', 'assets/seeker-home/favicon.png')
sub("logo", '/jobfairx-logo.png', 'assets/seeker-home/jobfairx-logo.png', count=4)
sub("companies img", '/_app/immutable/assets/companies.3017771d.png',
    'assets/seeker-home/companies.3017771d.png')
sub("mobile companies img", '/_app/immutable/assets/mobile-companies.ee028fce.png',
    'assets/seeker-home/mobile-companies.ee028fce.png')

# The captured stylesheet points three levels up for its fonts; from
# assets/seeker-home/ that lands outside the repo.
_css_p = f"{W}/assets/seeker-home/app.css"
_css = open(_css_p, encoding="utf-8").read()
if "url(../../../fonts/Inter/" in _css:
    open(_css_p, "w", encoding="utf-8").write(_css.replace("url(../../../fonts/Inter/", "url(../../fonts/Inter/"))
    log.append(("app.css font paths -> ../../fonts", _css.count("url(../../../fonts/Inter/")))

# ═══════════════════════════ 3. Head / SEO ════════════════════════════════
# FROZEN, asserted below: <title>, canonical, og:title, twitter:title, og:image,
# og:url, og:type, twitter:card, fo-verify, GA4. Those are the ranking surface.
frozen("title", "<title>Job Fairs | JobFairX</title>", 1)
frozen("canonical", '<link rel="canonical" href="https://jobfairx.com/">', 1)
frozen("og:title", '<meta property="og:title" content="Job Fairs | JobFairX">', 1)
frozen("twitter:title", '<meta name="twitter:title" content="Job Fairs | JobFairX">', 1)
frozen("og:image", '<meta property="og:image" content="https://jobfairx.com/images/og-image.png">', 1)
frozen("fo-verify", 'content="5df63e6a-79e6-4d4f-89dc-342a42b5e8a7"', 1)
frozen("GA4", "G-WCR44WE8MC", 2)

# The description is a click-through surface, not a ranking one. The live string
# says "Attend" (implies a venue we do not have), claims "top employers"
# (unsourced), and promises "get hired" (an outcome nobody can promise).
DESC_OLD = "JobFairX connects job seekers with top employers across the United States. Attend a job fair for free in a city near you, and get hired."
DESC_NEW = "Register free for a job fair in your city, get matched to open jobs, and pick your interview time. Interviews happen in person, on video, or by phone."
sub("meta + og + twitter + payload description x4", DESC_OLD, DESC_NEW, count=4)

# ═══════════════════════════ 4. Scoped stylesheet ═════════════════════════
# Everything authored below styles itself here. The live sheet is purged, so a
# bare Tailwind utility that the live pages never used would silently do nothing.
SK_CSS = """<style id="sk-style">
/* LIVE-SITE DEFECT, fixed here and flagged for the developer: neither <html> nor
   <body> paints a background on jobfairx.com, so a browser in dark mode renders
   the whole seeker site dark-on-dark. Measured on the live page: body and html
   both compute to rgba(0,0,0,0) and there is no color-scheme meta. */
html{background:#fff;color-scheme:light}
.sk{--sk-brand:#2563eb;--sk-ink:#0f172a;--sk-ink-2:#475569;--sk-ink-3:#6b7280;
    --sk-line:#e5e7eb;--sk-wash:#f8fafc;--sk-blue-wash:#eff6ff}
.sk-sec{padding:80px 20px}
.sk-sec--wash{background:#f9fafb}
.sk-in{max-width:1000px;margin:0 auto}
.sk-in--narrow{max-width:900px}
.sk-eyebrow{display:block;font-size:12px;font-weight:700;color:#2563eb;text-transform:uppercase;
  letter-spacing:.12em;margin:0 0 14px}
.sk-h2{font-size:30px;line-height:1.18;font-weight:600;color:#0f172a;letter-spacing:-.02em;margin:0 0 14px}
.sk-lead{font-size:17px;line-height:1.65;color:#6b7280;margin:0 0 8px;max-width:66ch}
.sk-center{text-align:center}
.sk-center .sk-lead{margin-left:auto;margin-right:auto}
/* alternating rows — the employer home page's workhorse pattern */
.sk-rows{display:flex;flex-direction:column;gap:56px;margin-top:44px}
.sk-row{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.sk-row:nth-child(even) .sk-row-copy{order:2}
.sk-row-copy .sk-eyebrow{margin-bottom:10px}
.sk-h3{font-size:22px;line-height:1.3;font-weight:700;color:#111827;letter-spacing:-.01em;margin:0 0 10px}
.sk-body{font-size:16px;line-height:1.7;color:#6b7280;margin:0 0 12px}
.sk-body:last-child{margin-bottom:0}
.sk-link{display:inline-block;margin-top:6px;color:#2563eb;font-weight:600;text-decoration:none;font-size:15px}
.sk-link:hover{text-decoration:underline}
/* figure frames */
.sk-fig{border:1px solid #e5e7eb;border-radius:14px;background:#fff;overflow:hidden;
  box-shadow:0 1px 2px rgba(15,23,42,.04),0 12px 28px -18px rgba(15,23,42,.25)}
.sk-fig img{display:block;width:100%;height:auto}
.sk-fig--pending{display:flex;align-items:center;justify-content:center;text-align:center;
  min-height:280px;background:#fff6d9;border:1px dashed #b8860b;color:#7a5c00;
  font-size:13px;font-weight:600;padding:24px;line-height:1.6}
/* cards */
.sk-cards{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:36px}
.sk-card{border:1px solid #e5e7eb;border-radius:14px;padding:24px 26px;background:#fff}
.sk-card h3{font-size:17px;font-weight:700;color:#111827;margin:0 0 8px;display:flex;align-items:center;gap:10px}
.sk-card p{font-size:15.5px;line-height:1.65;color:#6b7280;margin:0}
.sk-ico{width:34px;height:34px;border-radius:9px;background:#eff6ff;color:#2563eb;
  display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.sk-ico svg{width:18px;height:18px}
/* check list */
.sk-checks{list-style:none;margin:26px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:14px 32px}
.sk-checks li{position:relative;padding-left:30px;font-size:15.5px;line-height:1.6;color:#374151}
.sk-checks li::before{content:"";position:absolute;left:0;top:6px;width:18px;height:18px;border-radius:50%;
  background:#eff6ff}
.sk-checks li::after{content:"";position:absolute;left:5px;top:11px;width:8px;height:4px;
  border-left:2px solid #2563eb;border-bottom:2px solid #2563eb;transform:rotate(-45deg)}
/* the quiet panel */
.sk-panel{margin-top:38px;border:1px solid #e5e7eb;border-radius:14px;background:#f9fafb;padding:26px 28px}
.sk-panel h3{font-size:17px;font-weight:700;color:#111827;margin:0 0 8px}
.sk-panel p{font-size:16px;line-height:1.7;color:#4b5563;margin:0;max-width:70ch}
/* cost columns */
.sk-cost{display:grid;grid-template-columns:repeat(2,1fr);gap:36px;margin-top:34px;text-align:left}
.sk-cost h3{font-size:15px;font-weight:700;color:#111827;margin:0 0 12px}
/* FAQ — native details, server rendered, no JavaScript */
.sk-faq{border:1px solid #e2e8f0;border-radius:12px;background:#fff}
.sk-faq + .sk-faq{margin-top:16px}
.sk-faq > summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;
  align-items:flex-start;gap:20px;padding:18px 22px;font-size:16px;font-weight:600;color:#0f172a}
.sk-faq > summary::-webkit-details-marker{display:none}
.sk-faq > summary::after{content:"";flex-shrink:0;width:10px;height:10px;margin-top:5px;
  border-right:2px solid #6b7280;border-bottom:2px solid #6b7280;transform:rotate(45deg)}
.sk-faq[open] > summary::after{transform:rotate(225deg);margin-top:9px}
.sk-faq > div{padding:0 22px 20px;font-size:15.5px;line-height:1.7;color:#4b5563;max-width:72ch}
/* closing band */
.sk-close{background:#0f172a;color:#fff;padding:72px 20px;text-align:center}
.sk-close h2{font-size:30px;font-weight:600;letter-spacing:-.02em;margin:0 0 12px;color:#fff}
.sk-close p{font-size:17px;color:#cbd5e1;margin:0 0 26px}
.sk-btn{display:inline-block;background:#2563eb;color:#fff;font-weight:600;font-size:16px;
  padding:14px 30px;border-radius:10px;text-decoration:none}
.sk-btn:hover{background:#1d4ed8}
/* the city farm reads at every width now */
.sk-farm-grid{display:grid;grid-template-columns:repeat(3,1fr)}
@media (max-width:1023px){
  .sk-sec{padding:56px 18px}
  .sk-h2{font-size:26px}
  .sk-row{grid-template-columns:1fr;gap:26px}
  .sk-row:nth-child(even) .sk-row-copy{order:0}
  .sk-cards,.sk-checks,.sk-cost{grid-template-columns:1fr}
  .sk-farm-grid{grid-template-columns:1fr}
  .sk-close{padding:56px 18px}
  .sk-close h2{font-size:26px}
}
</style>"""
sub("inject scoped stylesheet", "</head>", SK_CSS + "\n  </head>")


def fig(shot, alt, note):
    """A product screenshot frame. Until the capture pass lands, the frame carries a
    visible placeholder rather than a fabricated mock — mock UI is banned."""
    return (f'<div class="sk-fig sk-fig--pending" role="img" aria-label="{alt}">'
            f'[SCREENSHOT PENDING &mdash; {shot}: {note}]</div>')


# ═══════════════════════════ 5. Hero ══════════════════════════════════════
sub("H1",
    '<h1 class="text-[36px] lg:text-[3.75rem] font-semibold leading-tight text-[#0f1a2e] mb-5">'
    'Skip the Applications.<br>Get Invited to Interview.</h1>',
    '<h1 class="text-[36px] lg:text-[3.75rem] font-semibold leading-tight text-[#0f1a2e] mb-5">'
    'Skip the Applications.<br>Get a Confirmed Interview Time.</h1>')

sub("hero subhead",
    '<p class="text-lg text-gray-500 leading-relaxed mb-9">Register for a hiring event. Get matched to jobs.'
    '<br class="hidden sm:block"> Always 100% free for job seekers.</p>',
    '<p class="text-lg text-gray-500 leading-relaxed mb-9">Employers post their open jobs to a job fair in your city. '
    'We match you to the ones that fit and invite you to request an interview at a time you choose.'
    '<br class="hidden sm:block"> The employer confirms it, and you meet them in person, on video, or by phone. '
    'Always 100% free for job seekers.</p>')

# The search box is a client-side filter today and emits no URL. A GET form
# degrades correctly to the unfiltered calendar.
sub("search -> GET form (open)",
    '<div class="flex items-center max-w-[560px] mx-auto gap-3 mb-12"><div class="relative flex-1">',
    '<form method="get" action="/job-fair-calendar" role="search" aria-label="Find a job fair by city" '
    'class="flex items-center max-w-[560px] mx-auto gap-3 mb-12"><div class="relative flex-1">')
sub("search inputs named x2",
    '<input type="text" autocomplete="off" value="" placeholder="Search by city"',
    '<input type="text" name="search" autocomplete="off" value="" placeholder="Search by city" aria-label="Search by city"',
    count=2)
sub("mobile search -> GET form (open)",
    '<div class="flex items-center gap-3"><div class="relative flex-1">',
    '<form method="get" action="/job-fair-calendar" role="search" aria-label="Find a job fair by city" '
    'class="flex items-center gap-3"><div class="relative flex-1">')
sub("close both search forms",
    '<button class="button button-primary">Search</button></div>',
    '<button type="submit" class="button button-primary">Search</button></form>', count=2)

# ═══════════════════════════ 6. Companies ═════════════════════════════════
# String byte-identical; the tag becomes a heading because it is one.
sub("companies p -> h2",
    '<p class="text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight">Companies That Hire on JobFairX</p>',
    '<h2 class="text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight">Companies That Hire on JobFairX</h2>'
    ' <p class="sk-lead sk-center" style="margin:14px auto 0">These are the employers who take part. '
    'Every job fair is a different mix, and the jobs at yours are posted before the day so matching can start.</p>')
# alt stays "Customer Logos": logo rights are unverified and alt text is bound by
# the same rule as visible copy, so it must not become an attendance claim.
frozen("logo alt", 'alt="Customer Logos"', 2)

# ═══════════════════════════ 7. Event board ═══════════════════════════════
sub("events subhead",
    '<p class="text-center text-gray-500 text-base mb-10">Register for free and start getting matched to employers</p>',
    '<p class="text-center text-gray-500 text-base mb-10 mx-auto max-w-[640px]">Every job fair is a city, a date, '
    'and a hiring type. Employers post their jobs ahead of the day, matching opens as soon as they do, and it stays '
    'open right up until the job fair starts.</p>')

# The five cards render in feed order (Sep 11, 3, 16, 8, 10) and drop the start
# time the payload already carries. Rebuilt sorted, with the time, and pointed at
# the evergreen next-{type} URL each dated URL already canonicalises to.
EVENTS = [
    ("Sep 3, 2026",  "Thu, September 3",  "11:00 AM CDT", "Milwaukee, WI Diversity Job Fair",
     "wisconsin/milwaukee/next-diversity",         "Diversity",   "bg-orange-50 text-orange-700 border-orange-200"),
    ("Sep 8, 2026",  "Tue, September 8",  "11:00 AM PDT", "San Luis Obispo, CA Healthcare Job Fair",
     "california/san-luis-obispo/next-healthcare", "Healthcare",  "bg-teal-50 text-teal-700 border-teal-200"),
    ("Sep 10, 2026", "Thu, September 10", "11:00 AM EDT", "Miami, FL Technology Job Fair",
     "florida/miami/next-technology",              "Technology",  "bg-blue-50 text-blue-700 border-blue-200"),
    ("Sep 11, 2026", "Fri, September 11", "11:00 AM CDT", "New Orleans, LA Technology Job Fair",
     "louisiana/new-orleans/next-technology",      "Technology",  "bg-blue-50 text-blue-700 border-blue-200"),
    ("Sep 16, 2026", "Wed, September 16", "11:00 AM CDT", "Fort Worth, TX Entry-Level Job Fair",
     "texas/fort-worth/next-entry-level",          "Entry-Level", "bg-sky-50 text-sky-700 border-sky-200"),
]


def card(date, mdate, time, title, slug, typ, chip):
    return (
        f'<a href="/job-fairs/{slug}" class="block rounded-lg border border-gray-200 bg-white py-[18px] px-6 '
        f'hover:border-gray-300 hover:shadow-sm transition-all no-underline"> '
        f'<div class="hidden sm:grid grid-cols-[100px_1fr_auto_auto] items-center gap-16">'
        f'<span class="text-sm text-gray-500 font-medium">{date}<span class="block text-gray-400 font-normal">{time}</span></span> '
        f'<span class="text-sm font-semibold text-gray-900">{title}</span> '
        f'<span><span class="inline-flex items-center px-3 py-1 rounded-md text-xs font-semibold border {chip}">{typ}</span></span> '
        f'<span class="text-sm font-semibold text-brand whitespace-nowrap">Learn More</span></div>  '
        f'<div class="sm:hidden flex flex-col gap-3"><div class="flex items-start justify-between gap-3"><div>'
        f'<p class="font-semibold text-slate-900 text-[15px]">{title}</p> '
        f'<p class="text-slate-500 mt-1 text-[13px]">{mdate} &middot; {time}</p></div> '
        f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-md font-semibold border flex-shrink-0 {chip} text-[13px]">{typ}</span></div> '
        f'<span class="inline-flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium text-slate-700 '
        f'border border-slate-200 rounded-lg hover:border-slate-300 hover:bg-slate-50 transition-all">View Event Details</span></div> </a>')


_start = s.find('<div class="flex flex-col gap-3 mb-8">')
_end = s.find('</a></div>', _start)
if _start < 0 or _end < 0:
    print("ABORT [event list]: could not locate the card container")
    sys.exit(1)
_old_cards = s[_start:_end + len('</a></div>')]
if _old_cards.count('<a href="/job-fairs/') != 5:
    print(f"ABORT [event list]: found {_old_cards.count('<a href=/job-fairs/')} cards, expected 5")
    sys.exit(1)
sub("event cards rebuilt sorted, with times, on next-{type} URLs", _old_cards,
    '<div class="flex flex-col gap-3 mb-8">' + "".join(card(*e) for e in EVENTS) + '</div>')

# A second door out of this section: /job-fairs-near-me receives exactly one
# inbound link from this page today, and it is the exact-match page for the
# money query.
sub("second link under the board",
    '<a href="/job-fair-calendar" class="button button-primary">View All Job Fairs</a>',
    '<a href="/job-fair-calendar" class="button button-primary">View All Job Fairs</a>'
    ' <a href="/job-fairs-near-me" class="sk-link" style="margin-left:14px">Browse job fairs by city &rarr;</a>')

# ═══════════════════════════ 8. How it works ══════════════════════════════
STEPS = [
    ("Register", "A job fair in your city, on a date you choose",
     ["Choose a job fair by city, date, and hiring type, then register for free. Job seekers are verified within "
      "about 20 miles of the event city, so the job fair you register for is one you can actually get to."],
     ("Shot 1", "the live job fair calendar, real cities and dates"),
     ("See job fairs near you &rarr;", "/job-fairs-near-me")),
    ("Get matched", "Employers post jobs and we match you to the ones that fit",
     ["You never send an application. When an employer posts a job your profile matches, we email you and invite "
      "you to request an interview with that company. Matching stays open right up until the job fair starts, so "
      "jobs keep arriving after you register."],
     ("Shot 2", "the Events tab showing Waiting to be matched above Matched"),
     ("What matching looks at &rarr;", "/job-seeker-faqs")),
    ("Pick your time", "You choose the time and the employer confirms it",
     ["Interviews run in 30-minute slots between 11:00 AM and 3:00 PM. You pick the slot that works for you and "
      "your request carries that time to the employer. Times an employer has already filled are never shown, so "
      "every time you can see is a time you can have. Employers usually respond within 72 hours.",
      "Before anything is sent, one screen shows you exactly what the employer receives: your name, your email, "
      "your answers to their screening questions, and the time you picked."],
     ("Shot 3", "the slot picker and the review screen from the scheduling flow"),
     ("See how scheduling works &rarr;", "/job-seeker-faqs")),
    ("Confirmed", "Everything you need arrives with the confirmation",
     ["The employer confirming your request is what books the interview. It appears on your Interviews tab with "
      "the date, your slot, your time zone, and where to be: the address, the phone number, or the link. The same "
      "details arrive by email."],
     ("Shot 4", "the confirmation email, in-person variant"),
     None),
]

rows = []
for eyebrow, h3, paras, (shot, note), link in STEPS:
    body = "".join(f'<p class="sk-body">{p}</p>' for p in paras)
    cta = f'<a class="sk-link" href="{link[1]}">{link[0]}</a>' if link else ""
    rows.append(
        f'<div class="sk-row"><div class="sk-row-copy"><span class="sk-eyebrow">{eyebrow}</span>'
        f'<h3 class="sk-h3">{h3}</h3>{body}{cta}</div>'
        f'<div class="sk-row-art">{fig(shot, h3, note)}</div></div>')

HOWITWORKS = (
    '<section class="sk sk-sec" id="how-it-works"><div class="sk-in">'
    '<div class="sk-center"><span class="sk-eyebrow">How JobFairX Works</span>'
    '<h2 class="sk-h2">A Confirmed Interview Time, Not a Resume in a Pile</h2></div>'
    '<div class="sk-rows">' + "".join(rows) + '</div></div></section>')

_hw_start = s.find('<p class="inline-block text-xs lg:text-sm font-bold text-brand uppercase tracking-[0.12em] mb-4">How JobFairX Works</p>')
if _hw_start < 0:
    print("ABORT [how it works]: eyebrow not found")
    sys.exit(1)
_hw_open = s.rfind("<section", 0, _hw_start)
_hw_close = s.find("</section>", _hw_start) + len("</section>")
_old_hw = s[_hw_open:_hw_close]
for banned in ["Invite-only Interviews, Three Steps", "No Zoom, no downloads", "That is all it takes to be seen"]:
    if banned not in _old_hw:
        print(f"ABORT [how it works]: expected {banned!r} inside the replaced block")
        sys.exit(1)
sub("how-it-works section replaced", _old_hw, HOWITWORKS)

# ═══════════════════════════ 9. Interview locations (new) ═════════════════
IC = {
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="13" height="12" rx="2"/><path d="M15 11l6-3v8l-6-3z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 3h3l2 5-2 1a12 12 0 006 6l1-2 5 2v3a2 2 0 01-2 2A16 16 0 014 5a2 2 0 012-2z"/></svg>',
    "pin":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "link":  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.5.5l3-3a5 5 0 00-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 00-7.5-.5l-3 3a5 5 0 007 7l1.7-1.7"/></svg>',
}
LOCATIONS = [
    (IC["video"], "JobFairX video call",
     "Runs in your browser, so there is nothing to download. The Join button appears on your Interviews tab when "
     "it is time, and you test your camera and microphone in the same flow you join from."),
    (IC["phone"], "Phone call",
     "Nothing to join. The employer calls the number on your interview at your scheduled time."),
    (IC["pin"], "In person",
     "The employer's own address, with their own instructions for where to check in. You get both when they "
     "confirm your interview, on your Interviews tab and by email."),
    (IC["link"], "The employer's own link",
     "Some employers use their own video link. Your confirmation email names the platform, so you know whether "
     "you need to install anything before you start."),
]
LOC_SECTION = (
    '<section class="sk sk-sec sk-sec--wash" id="interview-locations"><div class="sk-in">'
    '<div class="sk-center"><span class="sk-eyebrow">Interview Locations</span>'
    '<h2 class="sk-h2">Every Employer Chooses Where Your Interview Happens</h2>'
    '<p class="sk-lead">A job fair is a city and a date, not a place. Each employer decides how they interview, '
    'so two employers at the same job fair can meet you in completely different ways. Your interview details '
    'always name which one, and carry whatever that format needs: the address, the number, or the link.</p></div>'
    '<div class="sk-cards">'
    + "".join(f'<div class="sk-card"><h3><span class="sk-ico">{i}</span>{t}</h3><p>{b}</p></div>'
              for i, t, b in LOCATIONS)
    + '</div>'
    '<div style="margin-top:34px">' + fig("Shot 5", "Four interviews, one in each format",
                                          "four interview cards, one per format") + '</div>'
    '</div></section>')

# ═══════════════════════════ 10. Your interviews (new) ════════════════════
TOOLS = [
    "Three tabs with counts: Upcoming, Pending, and Past",
    "A status on every card: waiting to be matched, matched, awaiting an employer response, or scheduled",
    "A countdown inside the last 24 hours, and a live label when your interview slot opens",
    "Reschedule up until the job fair opens, and cancel up until your own interview starts",
    "Cancelling one interview keeps your registration, so you can still be matched to other jobs at that job fair",
    "A device check for camera and microphone inside the flow you join from",
]
TOOLS_SECTION = (
    '<section class="sk sk-sec" id="your-interviews"><div class="sk-in">'
    '<div class="sk-center"><span class="sk-eyebrow">Your Dashboard</span>'
    '<h2 class="sk-h2">You Always Know Where Every Interview Stands</h2>'
    '<p class="sk-lead">Requests, confirmed interviews, and finished ones sit in three tabs with a live count on '
    'each. Nothing is a mystery and nothing needs chasing.</p></div>'
    '<ul class="sk-checks">' + "".join(f'<li>{t}</li>' for t in TOOLS) + '</ul>'
    '<div style="margin-top:34px">' + fig("Shot 6", "The Interviews tab with Upcoming, Pending and Past",
                                          "the Interviews view, three tabs with their counts") + '</div>'
    '<div class="sk-panel"><h3>If an employer does not reply</h3>'
    '<p>Employers follow up directly with the candidates they want to move forward, so there is no result to go '
    'and check here. Not every employer replies, and no reply is not a decision you need to chase. The strongest '
    'next step is registering for another job fair, because your profile is already done.</p></div>'
    '</div></section>')

# ═══════════════════════════ 11. What it costs (new) ══════════════════════
COST_SECTION = (
    '<section class="sk sk-sec sk-sec--wash" id="what-it-costs"><div class="sk-in sk-in--narrow">'
    '<div class="sk-center"><span class="sk-eyebrow">Before You Start</span>'
    '<h2 class="sk-h2">Free for Job Seekers, Always</h2>'
    '<p class="sk-lead">Employers pay to hire at the job fair. You never do. There is nothing to buy, nothing to '
    'subscribe to, and no upgrade that gets you seen faster.</p></div>'
    '<div class="sk-cost">'
    '<div><h3>What you need</h3><ul class="sk-checks" style="grid-template-columns:1fr;margin-top:0">'
    '<li>A free account and a profile you build once</li>'
    '<li>A job fair in a city within about 20 miles of you</li>'
    '<li>A 30-minute slot for each interview you request</li>'
    '<li>A camera and microphone, only if the employer you matched with chose a video interview</li>'
    '</ul></div>'
    '<div><h3>What you never pay for</h3><ul class="sk-checks" style="grid-template-columns:1fr;margin-top:0">'
    '<li>Registering for a job fair</li>'
    '<li>Getting matched to open jobs</li>'
    '<li>Requesting and attending interviews</li>'
    '<li>Rescheduling or cancelling an interview</li>'
    '</ul></div></div></div></section>')

sub("insert locations + tools + cost before the FAQ",
    '<section class="pb-20 lg:py-20 px-5 max-w-[900px] mx-auto"><h2 class="text-center text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight mb-10">Frequently Asked Questions</h2>',
    LOC_SECTION + TOOLS_SECTION + COST_SECTION +
    '<section class="pb-20 lg:py-20 px-5 max-w-[900px] mx-auto"><h2 class="text-center text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight mb-10">Frequently Asked Questions</h2>')

# ═══════════════════════════ 12. FAQ: real answers, server rendered ═══════
# Today the served HTML carries four questions and no answers at all. These become
# <details>, so the answers are in the DOM with no JavaScript, and they are
# mirrored into FAQPage JSON-LD below.
FAQ = [
    ("How do I register for a job fair?",
     "Find the job fair in your city, click Register, and create a free account. It is free, and matching starts "
     "as soon as employers post their jobs to that event. You need to be within about 20 miles of the event city."),
    ("How does matching work?",
     "Employers post their open jobs to the job fair. We match your profile against those jobs, and when you match "
     "one we email you and invite you to request an interview with that company. Matching opens as soon as "
     "employers post and stays open until the job fair starts. There is nothing to apply to."),
    ("Where do interviews take place?",
     "That is set by each employer, not by the job fair. An employer can interview you on a JobFairX video call in "
     "your browser, by phone, on their own video link, or in person at their address. Two employers at the same "
     "job fair can interview completely differently. Your interview details always name which one, and carry "
     "whatever that format needs: the address, the number, or the link."),
    ("Is it really free?",
     "Yes. JobFairX is always 100% free for job seekers. Registering, matching, requesting an interview, and "
     "interviewing all cost nothing. Employers pay to take part."),
]

_faq_start = s.find('<div class="max-w-3xl mx-auto flex flex-col gap-4">')
_faq_end = s.find('<div class="text-center mt-4">', _faq_start)
if _faq_start < 0 or _faq_end < 0:
    print("ABORT [faq]: container not found")
    sys.exit(1)
_old_faq = s[_faq_start:_faq_end]
for q, _ in FAQ:
    if q not in _old_faq:
        print(f"ABORT [faq]: question missing from the captured block: {q!r}")
        sys.exit(1)
NEW_FAQ = ('<div class="sk max-w-3xl mx-auto">'
           + "".join(f'<details class="sk-faq"><summary>{q}</summary><div>{a}</div></details>' for q, a in FAQ)
           + '</div> ')
sub("FAQ accordions -> server-rendered details", _old_faq, NEW_FAQ)

import json as _json

FAQ_LD = ('<script type="application/ld+json">'
          + _json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
                        separators=(",", ":"))
          + '</script>')
sub("inject FAQPage JSON-LD", '<style id="sk-style">', FAQ_LD + '\n  <style id="sk-style">')

# ═══════════════════════════ 13. The city farm ════════════════════════════
# String byte-identical; the tag becomes the heading it already reads as.
sub("farm p -> h2",
    '<p class="text-center text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight">Job Fairs Near Me</p>',
    '<h2 class="text-center text-[30px] lg:text-4xl font-semibold text-slate-900 tracking-tight">Job Fairs Near Me</h2>'
    ' <p class="sk sk-lead sk-center" style="margin:14px auto 0;padding:0 20px">Job fairs are local. Job seekers are '
    'verified within about 20 miles of the event city, so pick the city you can actually get to.</p>')

# The farm is present in the served HTML at every width but hidden below lg, so a
# phone user's entire browse surface is one search box. No href, anchor string or
# node is removed here — this is visibility only.
sub("farm visible on phones",
    '<div class="lg:py-24 py-12 hidden lg:block mx-auto max-w-screen-xl">',
    '<div class="sk lg:py-24 py-12 mx-auto max-w-screen-xl">')
sub("farm grid responds", '<div class="grid grid-cols-3 mt-12 ml-6 lg:ml-20 mr-6 lg:mr-5 self-start">',
    '<div class="sk-farm-grid grid-cols-3 mt-12 ml-6 lg:ml-20 mr-6 lg:mr-5 self-start">')

# Wisconsin is absent from the farm while the board above features a Milwaukee
# job fair. Three city pages and their next-{type} children have no internal
# inbound link at all as a result.
WI = ('<div class="flex flex-col mt-2"><h2 class="text-xl lg:text-22p text-gray-800 font-bold">Wisconsin</h2> '
      + " ".join(f'<a href="/job-fairs-near-me/wisconsin/{slug}" class="text-lg text-gray-500 leading-8">{name} Job Fairs &rsaquo;</a>'
                 for slug, name in [("green-bay", "Green Bay"), ("madison", "Madison"), ("milwaukee", "Milwaukee")])
      + '</div>')
sub("add the missing Wisconsin block",
    '<a href="/job-fairs-near-me/washington/vancouver" class="text-lg text-gray-500 leading-8">Vancouver Job Fairs ›</a> </div>',
    '<a href="/job-fairs-near-me/washington/vancouver" class="text-lg text-gray-500 leading-8">Vancouver Job Fairs ›</a> </div>'
    + WI)

# Florida and New York each split across a column boundary and repeat their state
# name as a second <h2>. Same visual, two duplicate headings gone, zero links touched.
for st in ["Florida", "New York"]:
    sub(f"dedupe {st} continuation heading",
        f'<h2 class="text-xl lg:text-22p text-gray-800 font-bold">{st}</h2>',
        f'<p class="text-xl lg:text-22p text-gray-800 font-bold">{st}</p>', count=2)
    # restore the first (real) heading — replace() hit both, so put the first back
    s = s.replace(f'<p class="text-xl lg:text-22p text-gray-800 font-bold">{st}</p>',
                  f'<h2 class="text-xl lg:text-22p text-gray-800 font-bold">{st}</h2>', 1)

# ═══════════════════════════ 14. Closing band (new) ═══════════════════════
CLOSE = ('<section class="sk sk-close"><h2>Interview With Employers Hiring in Your City</h2>'
         '<p>Pick your city, find the next job fair, and register free.</p>'
         '<a class="sk-btn" href="/job-fairs-near-me">Browse Job Fairs Near You &rarr;</a></section>')
sub("closing band before the footer", '<footer', CLOSE + '\n<footer')

# ═══════════════════════════ 15. Guards ═══════════════════════════════════
frozen("city farm hrefs: 349 live + 3 Wisconsin", '/job-fairs-near-me/', 352)
frozen("single h1", "<h1", 1)
frozen("job-seeker-faqs links: 4 live + 2 new step links", '/job-seeker-faqs', 6)

_virtual = [m.start() for m in re.finditer(r'[Vv]irtual', s)]
_bad = [i for i in _virtual if 'virtual.jobfairx.com' not in s[max(0, i - 40):i + 40]]
if _bad:
    print(f"ABORT [virtual]: {len(_bad)} occurrence(s) outside the permitted app host")
    for i in _bad[:5]:
        print("   ", re.sub(r"\s+", " ", s[max(0, i - 90):i + 90]))
    sys.exit(1)
log.append(("virtual = app host only", len(_virtual)))

for banned, why in [
    ("No Zoom, no downloads", "the false video-only claim"),
    ("Invite-only Interviews", "a mechanic that does not exist"),
    ("That is all it takes to be seen", "false without the radius rule"),
    ("Register for a hiring event", "employer vocabulary in seeker copy"),
]:
    if banned in s:
        print(f"ABORT [banned copy]: {banned!r} survives ({why})")
        sys.exit(1)
log.append(("banned copy removed", 4))

# No motion: Scott ruled it out twice.
for cls in ["animate-pulse", "animate-bounce", "animate-spin"]:
    if cls in s:
        print(f"ABORT [motion]: {cls} present")
        sys.exit(1)
log.append(("no motion classes", 3))

# No em dash inside any heading.
for m in re.finditer(r"<(h[1-3])\b[^>]*>(.*?)</\1>", s, re.S):
    if "—" in m.group(2) or "&mdash;" in m.group(2):
        print(f"ABORT [em dash in heading]: {re.sub(r'<[^>]+>', '', m.group(2))[:80]!r}")
        sys.exit(1)
log.append(("no em dashes in headings", 1))

open(OUT, "w", encoding="utf-8").write(s)
print(f"WROTE {OUT}  {orig_len:,} -> {len(s):,} bytes")
for label, n in log:
    print(f"  ok  {label}  ({n})")
