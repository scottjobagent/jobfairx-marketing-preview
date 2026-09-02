#!/usr/bin/env python3
"""Build seeker-home-c.html — the "One Path" job seeker home page.

Chrome is taken VERBATIM from the live site, per Scott: the navigation and the
footer are sliced out of the frozen capture and pasted in untouched, so every
link, class and breakpoint matches jobfairx.com exactly. The city link farm comes
from the same capture. Only the body argument between them is authored.

  assets/live-capture/seeker-home-live-dom.html   the frozen capture (Aug 30 2026)
  assets/live-capture/seeker-nav.html             sliced from it, verbatim
  assets/live-capture/seeker-footer.html          sliced from it, verbatim

Brand font is Inter (the live stylesheet sets it on <html>). Brand colours are
measured, not chosen: #2563EB primary (the `brand` token in the compiled CSS on
both sites), #0044B3 deep (nav button, and the app's own accent), #1A1A1A ink,
#F0EEEA warm neutral.

Product screenshots are real captures of the seeker application, taken by
capture-seeker.py with company names, a recruiter name and a street address
neutralised. Nothing on this page is mock UI.

EDIT THE BUILDER, NEVER THE OUTPUT.
"""
import json, os, re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
CAP = f"{W}/assets/live-capture/seeker-home-live-dom.html"
OUT = f"{W}/seeker-home-c.html"
IMG = "assets/seeker-home/product"

cap = open(CAP, encoding="utf-8").read()
NAV = open(f"{W}/assets/live-capture/seeker-nav.html", encoding="utf-8").read()
FOOT = open(f"{W}/assets/live-capture/seeker-footer.html", encoding="utf-8").read()
log = []


def need(label, hay, needle, count=1):
    n = hay.count(needle)
    if n != count:
        print(f"ABORT [{label}]: {n} occurrences, expected {count}")
        sys.exit(1)
    log.append((label, n))


def clean(frag):
    """De-frameworkise a slice of the capture."""
    frag = re.sub(r'\s+data-svelte-h="svelte-[a-z0-9]+"', "", frag)
    frag = re.sub(r"<!-- HTML_TAG_(?:START|END) -->", "", frag)
    frag = frag.replace("./_app/immutable/assets/app.7a058851.css", "assets/seeker-home/app.css")
    frag = frag.replace("./_app/immutable/assets/2.557b8e8a.css", "assets/seeker-home/page.css")
    frag = frag.replace("/_app/immutable/assets/companies.3017771d.png",
                        "assets/seeker-home/companies.3017771d.png")
    frag = frag.replace("/_app/immutable/assets/mobile-companies.ee028fce.png",
                        "assets/seeker-home/mobile-companies.ee028fce.png")
    frag = frag.replace("/jobfairx-logo.png", "assets/seeker-home/jobfairx-logo.png")
    frag = frag.replace("./favicon.png", "assets/seeker-home/favicon.png")
    return frag


NAV, FOOT = clean(NAV), clean(FOOT)
need("nav: live sign-in host", NAV, "https://virtual.jobfairx.com/auth/#/?countryCode=US", 2)
need("nav: employer link", NAV, 'href="/employer"', 2)
need("footer: city hub link", FOOT, 'href="/job-fairs-near-me"', 1)
need("footer: social", FOOT, "linkedin.com/company/jobfairx.com", 1)

# ── the city farm, verbatim from the capture ──────────────────────────────
f_start = cap.index('<div class="lg:py-24 py-12 hidden lg:block mx-auto max-w-screen-xl">')
f_end = cap.index('<div class="py-16 px-5 lg:hidden">', f_start)
FARM = clean(cap[f_start:f_end])
need("farm: live city links", FARM, "/job-fairs-near-me/", 349)
# Wisconsin is missing from the live farm while the board above features a
# Milwaukee job fair; three city pages have no internal inbound link at all.
WI = ('<div class="flex flex-col mt-2"><h2 class="text-xl lg:text-22p text-gray-800 font-bold">Wisconsin</h2> '
      + " ".join(f'<a href="/job-fairs-near-me/wisconsin/{s}" class="text-lg text-gray-500 leading-8">{n} Job Fairs &rsaquo;</a>'
                 for s, n in [("green-bay", "Green Bay"), ("madison", "Madison"), ("milwaukee", "Milwaukee")])
      + "</div>")
anchor = '<a href="/job-fairs-near-me/washington/vancouver" class="text-lg text-gray-500 leading-8">Vancouver Job Fairs ›</a> </div>'
need("farm: Washington tail", FARM, anchor, 1)
FARM = FARM.replace(anchor, anchor + WI)
# present in the served HTML at every width, but invisible below lg
FARM = FARM.replace('<div class="lg:py-24 py-12 hidden lg:block mx-auto max-w-screen-xl">',
                    '<div class="sk lg:py-24 py-12 mx-auto max-w-screen-xl">')
FARM = FARM.replace('<div class="grid grid-cols-3 mt-12 ml-6 lg:ml-20 mr-6 lg:mr-5 self-start">',
                    '<div class="sk-farm grid-cols-3 mt-12 ml-6 lg:ml-20 mr-6 lg:mr-5 self-start">')
for st in ("Florida", "New York"):
    h = f'<h2 class="text-xl lg:text-22p text-gray-800 font-bold">{st}</h2>'
    need(f"farm: {st} split", FARM, h, 2)
    FARM = FARM.replace(h, f'<p class="text-xl lg:text-22p text-gray-800 font-bold">{st}</p>')
    FARM = FARM.replace(f'<p class="text-xl lg:text-22p text-gray-800 font-bold">{st}</p>', h, 1)

# ── SEO, measured from the live page ──────────────────────────────────────
TITLE = "Job Fairs | JobFairX"                       # ranking anchor, frozen
CANON = "https://jobfairx.com/"                      # frozen
DESC = ("Register free for a job fair in your city, get matched to open jobs, and pick your interview "
        "time. Interviews happen in person, on video, or by phone.")
OGIMG = "https://jobfairx.com/images/og-image.png"

FAQ = [
    ("How do I register for a job fair?",
     "Find the job fair in your city, click Register, and create a free account. It is free, and matching "
     "starts as soon as employers post their jobs to that event. You need to be within about 20 miles of "
     "the event city."),
    ("How does matching work?",
     "Employers post their open jobs to the job fair. We match your profile against those jobs, and when "
     "you match one we email you and invite you to request an interview with that company. Matching opens "
     "as soon as employers post and stays open until the job fair starts. There is nothing to apply to."),
    ("Where do interviews take place?",
     "That is set by each employer, not by the job fair. An employer can interview you on a JobFairX video "
     "call in your browser, by phone, on their own video link, or in person at their address. Two employers "
     "at the same job fair can interview completely differently. Your interview details always name which "
     "one, and carry whatever that format needs: the address, the number, or the link."),
    ("Do I need a resume?",
     "No. There is no resume step to get started, and a request can be sent without one. You build a "
     "profile once and it works for every job fair you register for. If you do add a resume, the review "
     "screen shows you before anything is sent."),
    ("What happens if an employer does not reply?",
     "Employers usually respond within 72 hours. If one does not, there is no result to go and check and "
     "nothing you need to chase. You stay registered for the job fair and can still be matched to other "
     "jobs at it."),
    ("Is it really free?",
     "Yes. JobFairX is always 100% free for job seekers. Registering, matching, requesting an interview, "
     "and interviewing all cost nothing. Employers pay to take part."),
]

FAQ_LD = ('<script type="application/ld+json">' + json.dumps(
    {"@context": "https://schema.org", "@type": "FAQPage",
     "mainEntity": [{"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    separators=(",", ":")) + "</script>")

# Organization + WebSite are carried from the live page. The live description is
# an unsourced superlative ("the largest job fairs in the country") and an
# uncited count; description is not a ranking surface, so it is corrected.
ORG_LD = ('<script type="application/ld+json">' + json.dumps(
    {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": "https://jobfairx.com/#organization", "name": "JobFairX",
         "url": "https://jobfairx.com",
         "logo": {"@type": "ImageObject", "url": "https://jobfairx.com/jobfairx-logo.png",
                  "width": 830, "height": 168},
         "description": "JobFairX runs job fairs across the United States, matching job seekers to "
                        "employers' open jobs and scheduling interviews in person, on video, or by phone. "
                        "Free for job seekers.",
         "sameAs": ["https://www.linkedin.com/company/jobfairx.com", "https://www.facebook.com/jobfairx"]},
        {"@type": "WebSite", "@id": "https://jobfairx.com/#website", "url": "https://jobfairx.com",
         "name": "JobFairX", "publisher": {"@id": "https://jobfairx.com/#organization"}}]},
    separators=(",", ":")) + "</script>")

# Deliberately NO Event / ItemList block. Google's event experience only supports
# pages focused on a single event and explicitly advises against marking up pages
# that list several; the five cards below link to the leaf pages, which carry it.

# ── the five real job fairs, from the live payload, sorted by date ─────────
EVENTS = [
    ("Sep 3, 2026", "Thu, September 3", "11:00 AM CDT", "Milwaukee, WI Diversity Job Fair",
     "wisconsin/milwaukee/next-diversity", "Diversity", "bg-orange-50 text-orange-700 border-orange-200"),
    ("Sep 8, 2026", "Tue, September 8", "11:00 AM PDT", "San Luis Obispo, CA Healthcare Job Fair",
     "california/san-luis-obispo/next-healthcare", "Healthcare", "bg-teal-50 text-teal-700 border-teal-200"),
    ("Sep 10, 2026", "Thu, September 10", "11:00 AM EDT", "Miami, FL Technology Job Fair",
     "florida/miami/next-technology", "Technology", "bg-blue-50 text-blue-700 border-blue-200"),
    ("Sep 11, 2026", "Fri, September 11", "11:00 AM CDT", "New Orleans, LA Technology Job Fair",
     "louisiana/new-orleans/next-technology", "Technology", "bg-blue-50 text-blue-700 border-blue-200"),
    ("Sep 16, 2026", "Wed, September 16", "11:00 AM CDT", "Fort Worth, TX Entry-Level Job Fair",
     "texas/fort-worth/next-entry-level", "Entry-Level", "bg-sky-50 text-sky-700 border-sky-200"),
]

STATIONS = [
    ("01", "Register", "A job fair in your city, on a date you choose",
     ["Choose a job fair by city, date, and hiring type, then register for free. Job seekers are verified "
      "within about 20 miles of the event city, so the job fair you register for is one you can actually "
      "get to.",
      "Registering is the whole setup. You build a profile once and it works for every job fair you "
      "register for after that."],
     f"{IMG}/s1-events.png",
     "The JobFairX Events tab, showing job fairs this candidate has registered for, each with its date, "
     "its hours, and how that employer will interview.",
     ("See job fairs near you", "/job-fairs-near-me")),

    ("02", "Get matched", "Employers post jobs and we match you to the ones that fit",
     ["You never send an application. When an employer posts a job your profile matches, we email you and "
      "invite you to request an interview with that company.",
      "Matching opens the moment employers post and stays open right up until the job fair starts, so jobs "
      "keep arriving after you register."],
     f"{IMG}/s2-matched.png",
     "A matched job fair card in the JobFairX app: the job title, the employer, the interview format, and "
     "a Request interview button.",
     ("What matching looks at", "/job-seeker-faqs")),

    ("03", "Pick your time", "You choose the time and the employer confirms it",
     ["Interviews run in 30-minute slots between 11:00 AM and 3:00 PM. You pick the slot that works for "
      "you, and your request carries that time to the employer. Times an employer has already filled are "
      "never shown, so every time you can see is a time you can have.",
      "Employers usually respond within 72 hours. Before anything is sent, one screen shows you exactly "
      "what they receive."],
     f"{IMG}/s3-slots.png",
     "The JobFairX time picker, showing the open 30-minute interview slots for one job fair between "
     "11:00 AM and 3:00 PM.",
     None),

    ("04", "Confirmed", "Everything you need arrives with the confirmation",
     ["The employer confirming your request is what books the interview. It appears on your Interviews tab "
      "with the date, your slot, your time zone, and where to be.",
      "The same details arrive by email, including the employer's own instructions for the day."],
     f"{IMG}/s4-confirmed.png",
     "A JobFairX confirmation email for an in-person interview, carrying the date, the time, the "
     "employer's street address and their own instructions for where to check in.",
     None),
]

FORMATS = [
    ("JobFairX video call",
     "Runs in your browser, so there is nothing to download. The Join button appears on your Interviews "
     "tab when it is time, and you check your camera and microphone in the same flow you join from.",
     f"{IMG}/fork-video.png",
     "A confirmed JobFairX video interview in the app, showing the date, the time slot and the format."),
    ("Phone call",
     "Nothing to join. The employer calls the number on your interview at your scheduled time, and the "
     "number they will call is shown on the card.",
     f"{IMG}/fork-phone.png",
     "A confirmed phone interview in the app, showing the number the employer will call and a link to "
     "correct it."),
    ("In person",
     "The employer's own address, with their own instructions for where to check in and where to park. "
     "You get all of it when they confirm, on your Interviews tab and by email.",
     f"{IMG}/fork-person.png",
     "A confirmed in-person interview in the app, showing the street address, the arrival instructions "
     "and the parking note."),
    ("The employer's own link",
     "Some employers interview on their own video platform. The link arrives when they approve your "
     "interview, by email and on the same card, and we name the platform so you know whether you need to "
     "install anything.",
     f"{IMG}/fork-link.png",
     "A confirmed interview on an employer's own video link, showing that the link arrives once the "
     "employer approves the request."),
]

TOOLS = [
    "Three tabs with a live count on each: Upcoming, Pending, and Past",
    "A status on every card, from waiting to be matched through to scheduled",
    "A countdown inside the last 24 hours, and a live label when your slot opens",
    "Reschedule up until the job fair opens, and cancel up until your own interview starts",
    "Cancelling one interview keeps your registration, so you can still be matched to other jobs",
    "A camera and microphone check inside the flow you join from",
]

# ══════════════════════════════ STYLES ════════════════════════════════════
# Scoped .sk-* only. The live stylesheet is purged, so a bare Tailwind utility
# the live pages never used silently does nothing.
CSS = """
/* LIVE-SITE DEFECT, fixed here: neither <html> nor <body> paints a background on
   jobfairx.com, so a dark-mode browser renders the seeker site dark-on-dark. */
html{background:#fff;color-scheme:light}
.sk{--b:#2563EB;--b-deep:#0044B3;--ink:#1A1A1A;--ink-2:#55524D;--ink-3:#6B6862;
    --paper:#F7F5F1;--warm:#F0EEEA;--line:#E2DFD8;--rail:#C3CBD8;--wash:#EAF1FD}
.sk *{box-sizing:border-box}
.sk-sec{padding:76px 20px}
.sk-sec--warm{background:var(--paper)}
.sk-in{max-width:1080px;margin:0 auto}
.sk-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
  color:var(--b);margin:0 0 12px}
.sk-h2{font-size:32px;line-height:1.16;font-weight:700;letter-spacing:-.022em;color:var(--ink);margin:0 0 14px}
.sk-lead{font-size:17.5px;line-height:1.65;color:var(--ink-2);margin:0;max-width:64ch}
.sk-center{text-align:center}.sk-center .sk-lead{margin:0 auto}

/* ── hero ── */
.sk-hero{padding:60px 20px 54px}
.sk-hero-grid{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1fr 420px;gap:56px;align-items:center}
.sk-h1{font-size:clamp(38px,4.6vw,58px);line-height:1.05;font-weight:700;letter-spacing:-.032em;
  color:var(--ink);margin:0 0 20px}
.sk-h1 .l2{display:block;color:var(--b)}
.sk-hero p{font-size:18px;line-height:1.6;color:var(--ink-2);margin:0 0 10px;max-width:56ch}
.sk-free{display:inline-block;font-size:15px;font-weight:700;color:var(--ink);
  border-bottom:2px solid var(--b);padding-bottom:2px;margin:6px 0 26px}
.sk-find{display:block;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:9px}
.sk-search{display:flex;gap:10px;max-width:460px}
.sk-search input{flex:1;min-width:0;padding:14px 16px;border:1px solid #CBD5E1;border-radius:10px;
  font-family:inherit;font-size:15px;color:var(--ink);background:#fff;min-height:50px}
.sk-search input::placeholder{color:#94A3B8}
.sk-search button{background:var(--b);color:#fff;border:0;border-radius:10px;padding:0 24px;
  font-family:inherit;font-size:15px;font-weight:700;cursor:pointer;min-height:50px}
.sk-search button:hover{background:var(--b-deep)}
.sk-under{display:inline-block;margin-top:14px;color:var(--b);font-weight:600;font-size:15px;
  text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px}

/* the whole path, as a diagram — authored, not a screenshot */
.sk-map{border:1px solid var(--line);border-radius:16px;background:#fff;padding:24px 22px}
.sk-map .cap{font-size:11px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 18px}
.sk-map ol{list-style:none;margin:0;padding:0 0 0 26px;position:relative}
.sk-map ol::before{content:"";position:absolute;left:5px;top:6px;bottom:34px;width:2px;background:var(--b-deep)}
.sk-map li{position:relative;font-size:15px;font-weight:600;color:var(--ink);padding:0 0 20px}
.sk-map li::before{content:"";position:absolute;left:-26px;top:5px;width:12px;height:12px;border-radius:50%;
  background:var(--b-deep);box-shadow:0 0 0 3px #fff}
.sk-map li:last-child{padding-bottom:6px}
.sk-map .split{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px;padding-left:26px}
.sk-map .split span{font-size:11.5px;font-weight:600;color:var(--ink-2);text-align:center;
  border-top:2px solid var(--rail);padding-top:8px;line-height:1.3}

/* ── the board ── */
.sk-board{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;margin-top:28px}
.sk-row{display:grid;grid-template-columns:150px 1fr 132px 96px;align-items:center;gap:18px;
  padding:16px 22px;border-top:1px solid var(--line);text-decoration:none;color:inherit}
.sk-row:first-child{border-top:0}
.sk-row:hover{background:var(--wash)}
.sk-row .d{font-size:14px;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}
.sk-row .d span{display:block;font-weight:400;color:var(--ink-3);font-size:13px}
.sk-row .t{font-size:15px;font-weight:600;color:var(--ink)}
.sk-row .go{font-size:14px;font-weight:700;color:var(--b);text-align:right}
.sk-chip{display:inline-flex;align-items:center;padding:4px 11px;border-radius:6px;font-size:12px;
  font-weight:700;border:1px solid}
.sk-boardfoot{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-top:22px}
.sk-btn{display:inline-block;background:var(--b);color:#fff;font-weight:700;font-size:15px;
  padding:13px 26px;border-radius:10px;text-decoration:none;min-height:48px;line-height:22px}
.sk-btn:hover{background:var(--b-deep)}
.sk-btn--ghost{background:#fff;color:var(--b);border:1px solid var(--b)}
.sk-btn--ghost:hover{background:var(--wash)}

/* ── the spine ── */
.sk-path{max-width:1080px;margin:0 auto;position:relative}
.sk-station{display:grid;grid-template-columns:72px minmax(0,1fr);position:relative;padding-bottom:56px}
.sk-station::before{content:"";position:absolute;left:23px;top:0;bottom:0;width:2px;background:var(--rail)}
.sk-station:last-of-type::before{bottom:auto;height:52px}
.sk-num{position:relative;z-index:2;width:48px;height:48px;border-radius:50%;background:var(--b-deep);
  color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;
  box-shadow:0 0 0 6px var(--paper)}
.sk-station-body{padding-top:2px}
.sk-h3{font-size:24px;line-height:1.22;font-weight:700;letter-spacing:-.015em;color:var(--ink);margin:6px 0 12px}
.sk-p{font-size:16.5px;line-height:1.68;color:var(--ink-2);margin:0 0 12px;max-width:60ch}
.sk-shot{margin-top:20px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;
  box-shadow:0 1px 2px rgba(26,26,26,.04),0 14px 32px -22px rgba(26,26,26,.4);max-width:760px}
.sk-shot img{display:block;width:100%;height:auto}
.sk-shot figcaption{font-size:12.5px;color:var(--ink-3);padding:10px 16px;border-top:1px solid var(--line);
  background:var(--warm)}
.sk-link{display:inline-block;margin-top:14px;color:var(--b);font-weight:600;font-size:15px;
  text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px}

/* ── the fork ── */
.sk-fork{display:grid;grid-template-columns:72px minmax(0,1fr);position:relative}
.sk-fork::before{content:"";position:absolute;left:23px;top:0;height:56px;width:2px;background:var(--rail)}
.sk-forkmark{position:relative;z-index:2;width:48px;height:48px;border-radius:50%;background:#fff;
  border:2px solid var(--b-deep);box-shadow:0 0 0 6px var(--paper);display:flex;align-items:center;justify-content:center}
.sk-forkmark span{width:16px;height:16px;border-left:2px solid var(--b-deep);border-bottom:2px solid var(--b-deep);
  transform:rotate(-45deg);display:block;margin-bottom:3px}
.sk-branches{margin-top:34px;display:flex;flex-direction:column;gap:26px}
.sk-branch{position:relative;padding-left:34px}
.sk-branch::before{content:"";position:absolute;left:-49px;top:-10px;width:60px;height:44px;
  border-left:2px solid var(--rail);border-bottom:2px solid var(--rail);border-bottom-left-radius:16px}
.sk-branch::after{content:"";position:absolute;left:9px;top:30px;width:9px;height:9px;border-radius:50%;
  background:var(--b-deep)}
.sk-branch h3{font-size:19px;font-weight:700;color:var(--ink);margin:0 0 8px}
.sk-branch p{font-size:16px;line-height:1.62;color:var(--ink-2);margin:0;max-width:58ch}

/* ── tools ── */
.sk-checks{list-style:none;margin:26px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:14px 34px}
.sk-checks li{position:relative;padding-left:30px;font-size:16px;line-height:1.6;color:var(--ink-2)}
.sk-checks li::before{content:"";position:absolute;left:0;top:5px;width:19px;height:19px;border-radius:50%;background:var(--wash)}
.sk-checks li::after{content:"";position:absolute;left:5.5px;top:10px;width:8px;height:4px;
  border-left:2px solid var(--b);border-bottom:2px solid var(--b);transform:rotate(-45deg)}
.sk-panel{margin-top:34px;border-left:3px solid var(--b-deep);background:#fff;border-radius:0 12px 12px 0;
  padding:22px 26px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.sk-panel h3{font-size:17px;font-weight:700;color:var(--ink);margin:0 0 8px}
.sk-panel p{font-size:16px;line-height:1.68;color:var(--ink-2);margin:0;max-width:68ch}

/* ── cost ── */
.sk-cost{display:grid;grid-template-columns:repeat(2,1fr);gap:36px;margin-top:32px}
.sk-cost h3{font-size:15px;font-weight:700;color:var(--ink);margin:0 0 12px}
.sk-cost .sk-checks{grid-template-columns:1fr;margin-top:0}

/* ── FAQ ── */
.sk-faq{border:1px solid var(--line);border-radius:12px;background:#fff}
.sk-faq+.sk-faq{margin-top:12px}
.sk-faq>summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;
  padding:18px 22px;font-size:16.5px;font-weight:600;color:var(--ink);min-height:56px;align-items:center}
.sk-faq>summary::-webkit-details-marker{display:none}
.sk-faq>summary::after{content:"";flex-shrink:0;width:10px;height:10px;border-right:2px solid var(--ink-3);
  border-bottom:2px solid var(--ink-3);transform:rotate(45deg);margin-top:-4px}
.sk-faq[open]>summary::after{transform:rotate(225deg);margin-top:4px}
.sk-faq>div{padding:0 22px 20px;font-size:16px;line-height:1.68;color:var(--ink-2);max-width:72ch}

/* ── close ── */
.sk-close{background:var(--ink);color:#fff;padding:70px 20px;text-align:center}
.sk-close h2{font-size:32px;font-weight:700;letter-spacing:-.022em;margin:0 0 12px;color:#fff}
.sk-close p{font-size:17.5px;color:#CFCCC7;margin:0 0 26px}
.sk-close .sk-btn{background:#fff;color:var(--ink)}
.sk-close .sk-btn:hover{background:var(--wash)}

.sk a:focus-visible,.sk button:focus-visible,.sk summary:focus-visible{outline:3px solid var(--b);outline-offset:3px}
.sk-farm{display:grid;grid-template-columns:repeat(3,1fr)}
.sk-trust{background:var(--ink);padding:20px}
.sk-trust ul{list-style:none;margin:0 auto;padding:0;display:flex;flex-wrap:wrap;gap:10px 26px;
  justify-content:center;align-items:center}
.sk-trust li{position:relative;padding-left:24px;font-size:14.5px;font-weight:600;color:#fff}
.sk-trust li::before{content:"";position:absolute;left:2px;top:6px;width:9px;height:5px;
  border-left:2px solid #7DA5FF;border-bottom:2px solid #7DA5FF;transform:rotate(-45deg)}
.sk-types{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:34px}
.sk-type{display:block;border:1px solid var(--line);border-radius:12px;padding:18px;background:#fff;
  text-decoration:none;color:inherit}
.sk-type:hover{border-color:var(--b);background:var(--wash)}
.sk-type span:last-child{display:block;margin-top:10px;font-size:14.5px;line-height:1.5;color:var(--ink-2)}
@media (max-width:1023px){.sk-types{grid-template-columns:1fr}.sk-trust ul{gap:8px 18px}.sk-trust li{font-size:13.5px}}

@media (max-width:1023px){
  .sk-sec{padding:52px 18px}
  .sk-hero{padding:36px 18px 40px}
  .sk-hero-grid{grid-template-columns:1fr;gap:32px}
  .sk-h2{font-size:26px}.sk-h3{font-size:21px}
  .sk-station,.sk-fork{grid-template-columns:52px minmax(0,1fr)}
  .sk-station::before,.sk-fork::before{left:15px}
  .sk-num,.sk-forkmark{width:32px;height:32px;font-size:12px;box-shadow:0 0 0 5px var(--paper)}
  .sk-forkmark span{width:11px;height:11px}
  .sk-branch{padding-left:18px}
  .sk-branch::before{left:-37px;width:48px;height:38px}
  .sk-branch::after{left:-3px;top:26px}
  .sk-checks,.sk-cost{grid-template-columns:1fr}
  .sk-row{grid-template-columns:1fr auto;gap:6px 12px;padding:14px 16px}
  .sk-row .d{grid-column:1;font-size:13px}
  .sk-row .t{grid-column:1/-1;order:3}
  .sk-row .go{grid-column:2;grid-row:1}
  .sk-row .c{grid-column:1/-1;order:4}
  .sk-farm{grid-template-columns:1fr}
  .sk-close{padding:52px 18px}.sk-close h2{font-size:26px}
}
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def shot(src, alt):
    return (f'<figure class="sk-shot"><img src="{src}" alt="{esc(alt)}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(alt)}</figcaption></figure>')


# ══════════════════════════════ SECTIONS ══════════════════════════════════
HERO = f'''<section class="sk sk-hero"><div class="sk-hero-grid">
<div>
  <h1 class="sk-h1">Skip the Applications.<span class="l2">Get a Confirmed Interview Time.</span></h1>
  <p>Employers post their open jobs to a job fair in your city. We match you to the ones that fit and
  invite you to request an interview at a time you choose. The employer confirms it, and you meet them
  in person, on video, or by phone.</p>
  <span class="sk-free">Always 100% free for job seekers.</span>
  <form method="get" action="/job-fair-calendar" role="search" aria-label="Find a job fair by city">
    <span class="sk-find" id="findlbl">Find the next job fair in your city</span>
    <div class="sk-search">
      <input type="text" name="search" autocomplete="off" placeholder="Search by city" aria-labelledby="findlbl">
      <button type="submit">Search</button>
    </div>
  </form>
  <a class="sk-under" href="/job-fairs-near-me">Browse job fairs near you</a>
</div>
<div class="sk-map">
  <p class="cap">The whole path, end to end</p>
  <ol><li>Register</li><li>Get matched</li><li>Pick your time</li><li>Confirmed</li></ol>
  <div class="split"><span>Video</span><span>Phone</span><span>In person</span><span>Their link</span></div>
</div>
</div></section>'''

rows = "".join(
    f'<a class="sk-row" href="/job-fairs/{slug}">'
    f'<span class="d">{d}<span>{t}</span></span>'
    f'<span class="t">{title}</span>'
    f'<span class="c"><span class="sk-chip {chip}">{typ}</span></span>'
    f'<span class="go">View</span></a>'
    for d, md, t, title, slug, typ, chip in EVENTS)

BOARD = f'''<section class="sk sk-sec sk-sec--warm" id="upcoming"><div class="sk-in">
<span class="sk-eyebrow">Upcoming Job Fairs</span>
<h2 class="sk-h2">Job Fairs Open for Registration Right Now</h2>
<p class="sk-lead">Every job fair is a city, a date, and a hiring type. Employers post their jobs ahead of
the day, matching opens as soon as they do, and it stays open right up until the job fair starts.</p>
<div class="sk-board">{rows}</div>
<div class="sk-boardfoot">
  <a class="sk-btn" href="/job-fair-calendar">View all job fairs</a>
  <a class="sk-btn sk-btn--ghost" href="/job-fairs-near-me">Browse by city</a>
</div>
</div></section>'''

stations = ""
for num, eyebrow, h3, paras, img, alt, link in STATIONS:
    body = "".join(f'<p class="sk-p">{p}</p>' for p in paras)
    cta = f'<a class="sk-link" href="{link[1]}">{link[0]}</a>' if link else ""
    stations += (f'<div class="sk-station"><div><span class="sk-num">{num}</span></div>'
                 f'<div class="sk-station-body"><span class="sk-eyebrow">{eyebrow}</span>'
                 f'<h3 class="sk-h3">{h3}</h3>{body}{shot(img, alt)}{cta}</div></div>')

branches = "".join(
    f'<div class="sk-branch"><h3>{t}</h3><p>{b}</p>{shot(img, alt)}</div>'
    for t, b, img, alt in FORMATS)

PATH = f'''<section class="sk sk-sec sk-sec--warm" id="how-it-works"><div class="sk-path">
<div class="sk-center" style="margin-bottom:44px">
  <span class="sk-eyebrow">How JobFairX Works</span>
  <h2 class="sk-h2">One Path From Registering to Sitting in an Interview</h2>
  <p class="sk-lead">Four steps, in order, and then one fork. Nothing else to learn.</p>
</div>
{stations}
<div class="sk-fork"><div><span class="sk-forkmark"><span></span></span></div>
<div class="sk-station-body">
  <span class="sk-eyebrow">Where the path splits</span>
  <h3 class="sk-h3">Every Employer Chooses Where Your Interview Happens</h3>
  <p class="sk-p">A job fair is a city and a date, not a place. Each employer decides how they interview,
  so two employers at the same job fair can meet you in completely different ways. Your interview details
  always name which one, and carry whatever that format needs: the address, the number, or the link.</p>
  <div class="sk-branches">{branches}</div>
</div></div>
</div></section>'''

TOOLS_S = f'''<section class="sk sk-sec" id="your-interviews"><div class="sk-in">
<span class="sk-eyebrow">Your Dashboard</span>
<h2 class="sk-h2">You Always Know Where Every Interview Stands</h2>
<p class="sk-lead">Requests, confirmed interviews and finished ones sit in three tabs with a live count on
each. Nothing is a mystery and nothing needs chasing.</p>
<ul class="sk-checks">{"".join(f"<li>{t}</li>" for t in TOOLS)}</ul>
{shot(f"{IMG}/tools-tabs.png", "The three interview tabs in the JobFairX app, showing a live count of upcoming, pending and past interviews.")}
<div class="sk-panel"><h3>If an employer does not reply</h3>
<p>Employers follow up directly with the candidates they want to move forward, so there is no result to go
and check here. Not every employer replies, and no reply is not a decision you need to chase. The strongest
next step is registering for another job fair, because your profile is already done.</p></div>
</div></section>'''

COST = f'''<section class="sk sk-sec sk-sec--warm" id="what-it-costs"><div class="sk-in">
<div class="sk-center"><span class="sk-eyebrow">Before You Start</span>
<h2 class="sk-h2">Free for Job Seekers, Always</h2>
<p class="sk-lead">Employers pay to hire at the job fair. You never do. There is nothing to buy, nothing to
subscribe to, and no upgrade that gets you seen faster.</p></div>
<div class="sk-cost">
<div><h3>What you need</h3><ul class="sk-checks">
<li>A free account and a profile you build once</li>
<li>A job fair in a city within about 20 miles of you</li>
<li>A 30-minute slot for each interview you request</li>
<li>A camera and microphone, only if the employer you matched with chose a video interview</li></ul></div>
<div><h3>What you never pay for</h3><ul class="sk-checks">
<li>Registering for a job fair</li>
<li>Getting matched to open jobs</li>
<li>Requesting and attending interviews</li>
<li>Rescheduling or cancelling an interview</li></ul></div>
</div></div></section>'''

FAQ_S = ('<section class="sk sk-sec" id="faq"><div class="sk-in" style="max-width:820px">'
         '<div class="sk-center"><h2 class="sk-h2">Frequently Asked Questions</h2></div>'
         + "".join(f'<details class="sk-faq"><summary>{esc(q)}</summary><div>{esc(a)}</div></details>'
                   for q, a in FAQ)
         + '<div class="sk-center" style="margin-top:26px">'
           '<a class="sk-link" href="/job-seeker-faqs">View all FAQs</a></div></div></section>')

CLOSE = ('<section class="sk sk-close"><h2>Interview With Employers Hiring in Your City</h2>'
         '<p>Pick your city, find the next job fair, and register free.</p>'
         '<a class="sk-btn" href="/job-fairs-near-me">Browse job fairs near you</a></section>')

# ── added after the BestHire teardown: the three things a first-time seeker
#    needs before the story starts, and the two content blocks the whole
#    category carries and we had none of.
TRUST = ("""<section class="sk sk-trust"><ul class="sk-in">
<li>Always 100% free for job seekers</li>
<li>No application step, ever</li>
<li>Employers usually respond within 72 hours</li>
<li>Local to your city, verified within about 20 miles</li>
<li>Five kinds of job fair</li>
</ul></section>""")

DEFINITION = """<section class="sk sk-sec" id="what-it-is"><div class="sk-in" style="max-width:780px">
<span class="sk-eyebrow">The short version</span>
<h2 class="sk-h2">A Job Fair Where the Employers Come to You</h2>
<p class="sk-lead">A JobFairX job fair is a dated hiring event for one city and one kind of work.
Employers who want to hire in that city post their open jobs to it. You register free, and instead of
sending applications, you get matched to the jobs you fit and invited to request an interview at a
time you choose. The employer accepts, and accepting is the booking. Every interview is one to one
with an employer, and each employer decides whether yours happens in person, on video, or by phone.</p>
</div></section>"""

TYPES = [
 ("Healthcare", "Nursing, allied health, medical assisting and therapy roles.", "healthcare",
  "bg-teal-50 text-teal-700 border-teal-200"),
 ("Diversity", "Employers hiring across every industry with inclusive hiring goals.", "diversity",
  "bg-orange-50 text-orange-700 border-orange-200"),
 ("Veteran", "Employers hiring veterans and recently separated service members.", "veterans",
  "bg-red-50 text-red-700 border-red-200"),
 ("Technology", "Engineering, product and data roles at every experience level.", "technology",
  "bg-blue-50 text-blue-700 border-blue-200"),
 ("Entry-Level", "Early-career roles for recent graduates and career changers.", "entryLevel",
  "bg-sky-50 text-sky-700 border-sky-200"),
]

TYPES_S = ('<section class="sk sk-sec" id="hiring-types"><div class="sk-in">'
  '<div class="sk-center"><span class="sk-eyebrow">Which job fair is yours</span>'
  '<h2 class="sk-h2">Five Kinds of Job Fair, One in Your City</h2>'
  '<p class="sk-lead">Every job fair is built around one kind of hiring, so the employers in the room '
  'are the ones hiring for the work you actually do.</p></div>'
  '<div class="sk-types">'
  + "".join(f'<a class="sk-type" href="/job-fair-calendar">'
            f'<span class="sk-chip {chip}">{name}</span><span>{desc}</span></a>'
            for name, desc, slug, chip in TYPES)
  + '</div></div></section>')

PREP = """<section class="sk sk-sec" id="prepare"><div class="sk-in" style="max-width:820px">
<span class="sk-eyebrow">Before your interview</span>
<h2 class="sk-h2">Turning Up Prepared Is Most of It</h2>
<p class="sk-lead">Your interview is one employer, one to one, in a 30-minute slot. A little
preparation goes a long way in that time.</p>
<ul class="sk-checks" style="grid-template-columns:1fr">
<li>Read the job you matched with again, and the employer's own description of the role</li>
<li>Have two or three examples of your work ready, with what you did and what changed because of it</li>
<li>Write down what you want to ask them, because you will have time to ask</li>
<li>Check your interview details the day before for the address, the number, or the link</li>
<li>If yours is a video call, open the device check from your Interviews tab before the day</li>
<li>If yours is in person, read the employer's arrival note and plan for traffic and parking</li>
</ul></div></section>"""

# ══════════════════════════════ ASSEMBLE ══════════════════════════════════
HEAD = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="assets/seeker-home/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="assets/seeker-home/app.css?v=1" rel="stylesheet">
    <link href="assets/seeker-home/page.css?v=1" rel="stylesheet">
    <title>{TITLE}</title>
    <meta name="description" content="{DESC}">
    <meta name="fo-verify" content="5df63e6a-79e6-4d4f-89dc-342a42b5e8a7">
    <link rel="canonical" href="{CANON}">
    <meta property="og:title" content="{TITLE}">
    <meta property="og:description" content="{DESC}">
    <meta property="og:image" content="{OGIMG}">
    <meta property="og:url" content="{CANON}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{TITLE}">
    <meta name="twitter:description" content="{DESC}">
    <meta name="twitter:image" content="{OGIMG}">
    {ORG_LD}
    {FAQ_LD}
    <style>{CSS}</style>
  </head>
  <body>'''

MOBILE_SEARCH = ('<div class="sk py-16 px-5 lg:hidden"><p class="text-2xl text-center font-bold text-gray-900 mb-6">'
                 'Find a Job Fair Today</p>'
                 '<form method="get" action="/job-fair-calendar" role="search" aria-label="Find a job fair by city" class="sk-search">'
                 '<input type="text" name="search" autocomplete="off" placeholder="Search by city" aria-label="Search by city">'
                 '<button type="submit">Search</button></form></div>')

# The live page clears its fixed header with this wrapper; without it the nav
# sits on top of the H1.
BODY = (HERO + TRUST + DEFINITION + BOARD + TYPES_S + PATH + TOOLS_S + PREP + COST
        + FAQ_S + FARM + MOBILE_SEARCH + CLOSE)
html = (HEAD + NAV + '<div class="pt-[65px] lg:pt-[60px]">' + BODY + "</div>"
        + FOOT + "</body>\n</html>\n")

# ══════════════════════════════ GUARDS ════════════════════════════════════
need("title frozen", html, f"<title>{TITLE}</title>", 1)
need("canonical frozen", html, f'<link rel="canonical" href="{CANON}">', 1)
need("og:title frozen", html, f'<meta property="og:title" content="{TITLE}">', 1)
need("verification token", html, "5df63e6a-79e6-4d4f-89dc-342a42b5e8a7", 1)
need("city links 349 live + 3 Wisconsin", html, "/job-fairs-near-me/", 352)
need("single h1", html, "<h1", 1)
need("FAQPage schema", html, '"@type":"FAQPage"', 1)
need("no Event schema on a listing page", html, '"@type":"Event"', 0)

v = [m.start() for m in re.finditer(r"[Vv]irtual", html)]
bad = [i for i in v if "virtual.jobfairx.com" not in html[max(0, i - 40):i + 40]]
if bad:
    print(f"ABORT [virtual]: {len(bad)} outside the permitted app host")
    for i in bad[:4]:
        print("   ", re.sub(r"\s+", " ", html[max(0, i - 90):i + 90]))
    sys.exit(1)
log.append(("virtual = app host only", len(v)))

for banned in ("No Zoom, no downloads", "Invite-only Interviews", "That is all it takes to be seen",
               "PLACEHOLDER", "Baylor Scott", "Nike", "Alicia Barrett"):
    if banned in html:
        print(f"ABORT [banned]: {banned!r} present")
        sys.exit(1)
log.append(("banned strings absent", 7))

for cls in ("animate-pulse", "animate-bounce", "animate-spin"):
    if cls in html:
        print(f"ABORT [motion]: {cls}")
        sys.exit(1)
log.append(("no motion", 3))

for m in re.finditer(r"<(h[1-3])\b[^>]*>(.*?)</\1>", html, re.S):
    if "—" in m.group(2) or "&mdash;" in m.group(2):
        print(f"ABORT [em dash in heading]: {re.sub(r'<[^>]+>', '', m.group(2))[:70]!r}")
        sys.exit(1)
log.append(("no em dashes in headings", 1))

for _, _, _, _, img, _, _ in STATIONS:
    if not os.path.exists(f"{W}/{img}"):
        print(f"ABORT [asset missing]: {img}")
        sys.exit(1)
for _, _, img, _ in FORMATS:
    if not os.path.exists(f"{W}/{img}"):
        print(f"ABORT [asset missing]: {img}")
        sys.exit(1)
log.append(("product screenshots present", len(STATIONS) + len(FORMATS)))

open(OUT, "w", encoding="utf-8").write(html)
print(f"WROTE {OUT}  {len(html):,} bytes")
for label, n in log:
    print(f"  ok  {label}  ({n})")
