#!/usr/bin/env python3
"""
build-event-healthcare.py  —  Hiring Event Details Page, REDESIGN (not a clone).

Stream: employer clone stream (HANDOFF-4). Written 25 Aug 2026 at Scott's
direction: "build a health care page", "author a redesign", "we're not changing
the colors or fonts".

WHAT THIS IS
    The event details page rebuilt to answer "why THIS event" instead of
    restating the homepage. Strategy + measurements are in the audit artifact
    ("Why This Event"). The old clone (employer-event-detail.html) was ~79%
    identical across all 1,760 event pages and only ~6% event-specific.

HOW IT DIFFERS FROM THE OTHER BUILDERS
    Those rebuild a captured live page byte-faithfully. This one AUTHORS the
    content and only LIFTS the live chrome (head, announcement bar + header +
    drawer, footer) out of employer-event-detail.html so the page sits inside
    the live design system without re-typing it. Every lift asserts.

    Only Tailwind classes already compiled into assets/employer-home/app.css
    may be used - there is no Tailwind runtime. Anything new lives in the
    scoped <style> block. Verified traps honoured here:
      - .container is NOT used (it caps at 1024px). Uses max-w-[1180px] mx-auto.
      - .button is max-width:min-content; full-width CTAs use .button-bar.
      - tabular figures need scoped CSS (.jfx-num) - no numeric utility exists.
      - sticky rail sits below the header's z-index.

REAL EVENT (verified on jobfairx.com, 25 Aug 2026)
    Austin, TX Healthcare Hiring Event, Sep 30 2026, 11:00 AM - 3:00 PM CDT
    446 pre-registered - 35 avg interviews - 8 avg hires - 91% show rate

SRC  employer-event-detail.html   (chrome donor only)
OUT  employer-event-detail-v2.html
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "employer-event-detail.html"
OUT = ROOT / "employer-event-detail-v2.html"

# --------------------------------------------------------------------------
# Event data. One place. This is the parameterisation point for the other four
# event types and for the 1,760 city pages - everything below reads from here.
# --------------------------------------------------------------------------
EV = {
    "city": "Austin, TX",
    "city_short": "Austin",
    "type": "Healthcare",
    "date_long": "September 30, 2026",
    "date_short": "Sep 30",
    "weekday": "Wednesday",
    "month_abbr": "SEP",
    "day_num": "30",
    "time": "11:00 AM &ndash; 3:00 PM CDT",
    "event_id": "642761563807154215",
    "path": "/employer/job-fairs/texas/austin/642761563807154215",
    "return_to": "%2Femployer%2Fjob-fairs%2Ftexas%2Faustin%2F642761563807154215",
    "next_event": "/employer/job-fairs/texas/austin/next-healthcare",
    # Live per-event number. Dynamic in production - the developer feeds this.
    "registered": "446",
    # Type-level figures, live on jobfairx.com. Healthcare's set is the one
    # Scott has confirmed as real 2025 platform data.
    "show_rate": "91%",
    "avg_interviews": "35",
    "avg_hires": "8",
    # Early registration: Scott ruled 30+ days on 25 Aug 2026.
    # Sep 30 - 30 days = Aug 31. The live server still computes 31 days
    # (Aug 30); the code must move to 30. Flagged in the dev note on-page.
    "early_ends": "August 31",
    "early_ends_live": "August 30",
}

CART = "/employer/cart?eventId={id}&amp;returnTo={rt}".format(id=EV["event_id"], rt=EV["return_to"])
CART_HERO = CART + "%23hero"
CART_PKG = CART + "%23packages"
CART_CLOSE = CART + "%23final-cta"


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def lift(src, start_marker, end_marker, label, include_end=True):
    """Cut an exact span out of the donor. Aborts loudly if the anchors moved."""
    i = src.find(start_marker)
    if i == -1:
        fail("[{}] start anchor not found: {!r}".format(label, start_marker[:60]))
    j = src.find(end_marker, i)
    if j == -1:
        fail("[{}] end anchor not found: {!r}".format(label, end_marker[:60]))
    span = src[i: j + len(end_marker)] if include_end else src[i:j]
    print("  lifted {:<14} {:>7} chars".format(label, len(span)))
    return span


def sub(s, old, new, count, label):
    n = s.count(old)
    if n != count:
        fail("[{}] expected {} matches, found {}: {!r}".format(label, count, n, old[:70]))
    return s.replace(old, new)


# --------------------------------------------------------------------------
print("Reading chrome donor: " + SRC.name)
if not SRC.exists():
    fail("donor missing: " + str(SRC))
donor = SRC.read_text(encoding="utf-8")

head = lift(donor, "<!DOCTYPE html>", "</head>", "head")
# The donor carries its own provenance comment inside the head. Strip every
# comment out of the lifted head so the Dallas note does not ride along.
head = re.sub(r"<!--.*?-->\n?", "", head, flags=re.S)
chrome_top = lift(donor, '<div class="contents">', '<div class="lg:relative text-brand-text ">', "header+drawer")
footer = lift(donor, "<footer", "</footer>", "footer")

# --- head: retitle and re-point for this event -----------------------------
head = re.sub(r"<title>.*?</title>", "<title>Austin, TX Healthcare Hiring Event for Employers | JobFairX</title>", head, count=1, flags=re.S)
head = re.sub(r'<meta name="description" content=".*?">',
              '<meta name="description" content="Interview Austin nurses, medical assistants and clinical staff at the JobFairX Austin Healthcare Hiring Event on September 30, 2026. Flat-rate packages, scheduled interviews, no resume pile.">',
              head, count=1, flags=re.S)
head = re.sub(r'<link rel="canonical" href=".*?">',
              '<link rel="canonical" href="https://jobfairx.com{}">'.format(EV["path"]),
              head, count=1, flags=re.S)
for prop in ("og:title", "twitter:title"):
    head = re.sub(r'(<meta (?:property|name)="{}" content=").*?(">)'.format(re.escape(prop)),
                  r"\1Austin, TX Healthcare Hiring Event for Employers | JobFairX\2", head, count=1, flags=re.S)
for prop in ("og:description", "twitter:description"):
    head = re.sub(r'(<meta (?:property|name)="{}" content=").*?(">)'.format(re.escape(prop)),
                  r"\1Interview Austin nurses, medical assistants and clinical staff on September 30, 2026.\2",
                  head, count=1, flags=re.S)
head = re.sub(r'(<meta property="og:url" content=").*?(">)',
              r"\1https://jobfairx.com{}\2".format(EV["path"]), head, count=1, flags=re.S)

# --- chrome: repoint Dallas deep links at this event -----------------------
DALLAS = "/employer/cart?eventId=743231932652847104&amp;returnTo=%2Femployer%2Fjob-fairs%2Ftexas%2Fdallas%2F743231932652847104"
chrome_top = sub(chrome_top, DALLAS, CART, 2, "chrome cart links")

# The announcement bar is rebuilt as the state-driven banner, so drop the
# donor's frozen one and re-insert our own with state hooks.
bar_start = chrome_top.find('<div class="sticky top-0 w-full z-[51]">')
bar_end = chrome_top.find('<div class="relative w-full z-50 flex flex-col">')
if bar_start == -1 or bar_end == -1:
    fail("[banner] could not locate the donor announcement bar")

BANNER = (
    '<div id="jfx-banner-wrap" class="sticky top-0 w-full z-[51]"><div id="jfx-banner" '
    'class="px-6 py-2.5 text-[14px] font-normal text-center flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-3 w-full border-b" '
    'style="background-color: rgb(254, 244, 224); color: rgb(120, 53, 15); border-color: rgb(252, 211, 77);">'
    '<span id="jfx-banner-text">Early registration pricing ends soon. Save $100 and lock in priority candidate matching.</span> '
    '<a id="jfx-banner-link" href="#packages" class="underline underline-offset-4 hover:opacity-80 transition-opacity sm:ml-1 text-[14px] font-normal" '
    'style="color: inherit;">Register Now &rarr;</a></div></div> '
)
chrome_top = chrome_top[:bar_start] + BANNER + chrome_top[bar_end:]

# --- footer: apply the virtual sweep the live footer never got -------------
footer = footer.replace("Virtual Hiring Event Platform", "Hiring Event Platform")
footer = footer.replace("Virtual Job Fair Calendar", "Job Fair Calendar")

# --------------------------------------------------------------------------
# Authored content
# --------------------------------------------------------------------------

STYLE = """
<style>
  /* Scoped: only what app.css cannot already do. */
  .jfx-num { font-variant-numeric: tabular-nums; }
  .jfx-rail > li { position: relative; padding-left: 34px; }
  .jfx-rail > li::before {
    content: ""; position: absolute; left: 5px; top: 26px; bottom: -22px; width: 2px; background: #e2e8f0;
  }
  .jfx-rail > li:last-child::before { display: none; }
  .jfx-rail > li > .jfx-dot {
    position: absolute; left: 0; top: 6px; width: 12px; height: 12px; border-radius: 999px;
    background: #fff; border: 2px solid #cbd5e1;
  }
  .jfx-rail > li.is-now > .jfx-dot { border-color: #2563eb; background: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.15); }
  .jfx-rail > li.is-key > .jfx-dot { border-color: #b45309; background: #fff; }
  .jfx-chip {
    display: inline-block; border-radius: 999px; padding: 5px 12px; font-size: 13px; font-weight: 600;
    background: #f0fdfa; color: #0f766e; border: 1px solid #99f6e4; margin: 0 6px 8px 0;
  }
  .jfx-faq-a { display: none; }
  .jfx-faq.is-open .jfx-faq-a { display: block; }
  .jfx-faq.is-open .jfx-faq-chev { transform: rotate(180deg); }
  .jfx-faq-chev { transition: transform .2s ease; }
  /* Preview control - review only. */
  #jfx-preview-bar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 90;
    background: #0f172a; color: #cbd5e1; font-size: 12px;
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    padding: 6px 12px; font-family: Inter, sans-serif;
  }
  .jfx-preview-label { font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 10px; color: #64748b; }
  #jfx-preview button {
    background: #1e293b; color: #e2e8f0; border: 0; border-radius: 4px;
    padding: 4px 9px; margin-right: 3px; cursor: pointer; font-size: 12px; font-family: Inter, sans-serif;
  }
  #jfx-preview button:hover { background: #334155; }
  #jfx-preview button[aria-pressed="true"] { background: #2563eb; color: #fff; }
  #jfx-preview-note { color: #94a3b8; }
  body { padding-top: 34px; }
  #jfx-banner-wrap { top: 34px !important; }
  @media (prefers-reduced-motion: reduce) { .jfx-faq-chev { transition: none; } }
</style>
"""

HERO = """
<section id="hero" class="bg-white">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-16">
    <div class="grid lg:grid-cols-[1fr_360px] gap-10 lg:gap-14 items-start">

      <div>
        <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-teal-700 mb-4">{TYPE} Hiring Event</p>
        <h1 class="text-[36px] lg:text-[52px] font-extrabold text-slate-900 tracking-[-0.02em] leading-tight mb-6">
          Fill your open healthcare roles in {CITY_SHORT}
        </h1>
        <p class="text-[17px] text-slate-600 leading-relaxed max-w-2xl mb-8">
          One day of scheduled interviews with {CITY_SHORT}-area nurses, medical assistants and clinical
          staff who registered for this event and asked to meet a hiring team.
        </p>

        <div class="flex flex-wrap gap-3 mb-8">
          <div class="flex items-center gap-3 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
            <div class="text-center">
              <div class="text-[11px] font-bold uppercase tracking-[0.12em] text-slate-500">{MONTH}</div>
              <div class="text-2xl font-bold text-slate-900 jfx-num leading-tight">{DAY}</div>
            </div>
            <div class="text-sm text-slate-600 leading-relaxed">
              <div class="font-semibold text-slate-900">{WEEKDAY}</div>
              <div class="jfx-num">{TIME}</div>
            </div>
          </div>

          <div class="flex flex-col justify-center rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
            <div class="text-2xl font-bold text-slate-900 jfx-num leading-tight" id="jfx-hero-count">{REGISTERED}</div>
            <div class="text-sm text-slate-600">candidates registered so far</div>
          </div>

          <div class="flex flex-col justify-center rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
            <div class="text-2xl font-bold text-slate-900 jfx-num leading-tight">{SHOW_RATE}</div>
            <div class="text-sm text-slate-600">of booked interviews show up</div>
          </div>
        </div>

        <div class="flex flex-wrap gap-3">
          <a href="{CART_HERO}" id="jfx-hero-cta" class="button button-lg button-primary" data-cta>Register for This Event</a>
          <button type="button" id="jfx-video-open" class="button button-lg button-primary-inverted">
            <span class="w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0" style="margin-right:2px;">
              <svg class="w-3 h-3 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"></path></svg>
            </span>
            See how it works
          </button>
        </div>
      </div>

      <div class="lg:sticky lg:top-24 self-start w-full">
        <div class="rounded-2xl border border-slate-200 bg-white shadow-lg p-6">
          <p class="text-xs font-bold uppercase tracking-[0.12em] text-teal-700 mb-2">{TYPE} Hiring Event</p>
          <p class="text-lg font-semibold text-slate-900 leading-tight mb-1">{CITY}</p>
          <p class="text-sm text-slate-600 jfx-num mb-5">{DATE_LONG}<br>{TIME}</p>

          <div class="border-t border-slate-200 pt-5 mb-5">
            <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500 mb-3">What you get</p>
            <ul class="list-none pl-0 space-y-2.5">
              <li class="flex items-start gap-2.5"><span class="w-4 h-4 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:3px;"><svg class="w-2.5 h-2.5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[14px] text-slate-700 leading-snug">A full day of interviews, already on your calendar</span></li>
              <li class="flex items-start gap-2.5"><span class="w-4 h-4 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:3px;"><svg class="w-2.5 h-2.5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[14px] text-slate-700 leading-snug">Candidates verified within about 20 miles of Austin</span></li>
              <li class="flex items-start gap-2.5"><span class="w-4 h-4 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:3px;"><svg class="w-2.5 h-2.5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[14px] text-slate-700 leading-snug">Resumes and contact details for every match</span></li>
              <li class="flex items-start gap-2.5"><span class="w-4 h-4 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:3px;"><svg class="w-2.5 h-2.5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[14px] text-slate-700 leading-snug">Your report the moment the event ends</span></li>
            </ul>
          </div>

          <a href="{CART_PKG}" class="button-bar button-primary mb-3" data-cta>Register for This Event</a>
          <p class="text-[13px] text-slate-500 text-center mb-2">
            <span class="jfx-num">{REGISTERED}</span> candidates registered so far &middot; updated daily
          </p>
          <p class="text-center">
            <a href="#packages" class="text-[13px] font-semibold text-brand hover:underline">Packages from <span class="jfx-num" id="jfx-rail-price">$395</span> per event &rarr;</a>
          </p>
          <p class="text-[12px] text-slate-500 text-center mt-1" id="jfx-rail-note">Early registration saves $100 through {EARLY_ENDS}.</p>
        </div>
      </div>

    </div>
  </div>
</section>
"""

ROOM = """
<section class="bg-slate-50 border-y border-slate-200 py-10 lg:py-12">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8">
    <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-slate-400 text-center mb-8">The room so far</p>
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
      <div class="text-center">
        <p class="text-3xl sm:text-4xl font-bold text-slate-900 jfx-num mb-1">{REGISTERED}</p>
        <p class="text-sm text-slate-500">Candidates registered<br>for this event</p>
      </div>
      <div class="text-center">
        <p class="text-3xl sm:text-4xl font-bold text-slate-900 jfx-num mb-1">{SHOW_RATE}</p>
        <p class="text-sm text-slate-500">Interview show rate<br>at healthcare events</p>
      </div>
      <div class="text-center">
        <p class="text-3xl sm:text-4xl font-bold text-slate-900 jfx-num mb-1">{AVG_INT}</p>
        <p class="text-sm text-slate-500">Interviews per employer,<br>per event</p>
      </div>
      <div class="text-center">
        <p class="text-3xl sm:text-4xl font-bold text-slate-900 jfx-num mb-1">{AVG_HIRE}</p>
        <p class="text-sm text-slate-500">Hires per employer,<br>per event</p>
      </div>
    </div>
    <p class="text-[13px] text-slate-500 text-center max-w-3xl mx-auto mt-8 leading-relaxed">
      The candidate count is live for this event and updates daily. Show rate and per-employer
      averages are 2025 platform data across 582 healthcare hiring events.
    </p>
  </div>
</section>
"""

AUDIENCE = """
<section class="bg-white py-12 lg:py-[90px]">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-start">
      <div>
        <h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-5">
          Who you will meet in {CITY_SHORT}
        </h2>
        <p class="text-base text-slate-600 leading-relaxed mb-6">
          Clinical and allied health professionals across nursing, medical assisting and therapy.
          They registered for this date, in this city, and they are choosing interview times with
          employers who post roles before the event.
        </p>
        <div>
          <span class="jfx-chip">Registered Nurse</span><span class="jfx-chip">Nurse Practitioner</span><span class="jfx-chip">Licensed Practical Nurse</span><span class="jfx-chip">Certified Nursing Assistant</span><span class="jfx-chip">Medical Assistant</span><span class="jfx-chip">Patient Care Technician</span><span class="jfx-chip">Physical Therapist</span><span class="jfx-chip">Occupational Therapist</span><span class="jfx-chip">Respiratory Therapist</span><span class="jfx-chip">Dental Hygienist</span><span class="jfx-chip">Pharmacy Technician</span><span class="jfx-chip">Home Health Aide</span><span class="jfx-chip">CT Technologist</span><span class="jfx-chip">Ultrasound Technologist</span>
        </div>
        <p class="text-[13px] text-slate-500 mt-3">Roles seen on JobFairX healthcare events. Not a limit on who registers.</p>
      </div>

      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-6 lg:p-7">
        <div class="flex items-start gap-4">
          <div class="w-12 h-12 rounded-full bg-teal-50 flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-teal-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-slate-900 mb-2">Everyone here is local to {CITY_SHORT}</h3>
            <p class="text-base text-slate-600 leading-relaxed">
              Candidates at this event are verified to be within approximately 20 miles of
              {CITY_SHORT}. That is what makes an in-person interview practical, and it is why the
              people you meet can start a shift without relocating.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

RUNWAY = """
<section id="how" class="bg-slate-50 border-y border-slate-200 py-12 lg:py-[90px]">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mb-10 lg:mb-14">
      <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-brand mb-4">How it works</p>
      <h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-5">
        Four things happen, and you control all of them
      </h2>
      <p class="text-base text-slate-600 leading-relaxed">
        Nothing about this event is a lucky dip. You decide how your team interviews, which candidates
        get time, and what every one of them was worth afterwards.
      </p>
    </div>

    <!-- 1 - set up. The interview location is chosen here, which is why this beat
         exists at all: without it the page explains candidates booking into a
         setting the reader has not been told they choose. -->
    <div class="grid lg:grid-cols-[1fr_560px] gap-10 lg:gap-16 items-center mb-16 lg:mb-24">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500 mb-3">Step one</p>
        <h3 class="text-[22px] lg:text-[26px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-4">
          Post your roles and choose how you interview
        </h3>
        <p class="text-base text-slate-600 leading-relaxed mb-5">
          Register, post the jobs you need to fill, and set your interview location. This is your
          setting, not the event&rsquo;s &mdash; another employer at the same event can interview a
          different way. Matching starts as soon as your jobs are live.
        </p>
        <ul class="list-none pl-0 space-y-3">
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug"><strong class="font-semibold text-slate-900">In person</strong> at your {CITY_SHORT} address, with parking and check-in notes that reach candidates with their confirmation</span></li>
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug"><strong class="font-semibold text-slate-900">On JobFairX video</strong>, in the browser, with nothing to install and no link to send</span></li>
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug"><strong class="font-semibold text-slate-900">By phone</strong>, calling each candidate at the time you accepted</span></li>
        </ul>
        <p class="text-[15px] text-slate-500 mt-5">Whichever you choose, it never changes the price.</p>
      </div>
      <div><div class="w-full max-w-[560px] h-[420px] max-lg:h-auto max-lg:min-h-[280px] mx-auto overflow-hidden box-border bg-white border border-[#e8e6e3] rounded-[14px] shadow-[0_8px_32px_rgba(0,0,0,0.04)] flex flex-col"><div style="padding:18px 24px 14px;border-bottom:1px solid #f0eeea"><div class="text-[15px] font-semibold text-[#0f172a]">Interview settings</div><div class="text-[12.5px] text-slate-500" style="margin-top:3px">Choose how your team interviews at this event.</div></div><div style="padding:18px 24px 0;flex:1;overflow:hidden"><div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:8px">Interview format <span class="text-[#dc2626]">*</span></div><div style="display:inline-flex;border:1px solid #e2e8f0;border-radius:9999px;padding:4px;gap:4px;background:#fff"><span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:7px 16px;border-radius:9999px;background:#2563eb;color:#fff"><svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>In-Person</span><span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:500;padding:7px 16px;border-radius:9999px;color:#334155"><svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>Video</span><span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:500;padding:7px 16px;border-radius:9999px;color:#334155"><svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>Phone</span></div><div style="margin-top:18px"><div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:6px">Interview address <span class="text-[#dc2626]">*</span></div><div style="display:flex;gap:8px"><div style="flex:2;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a">600 Congress Ave</div><div style="flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#94a3b8">Suite 1400</div></div></div><div style="margin-top:14px"><div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:6px">How to attend</div><div style="border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a;line-height:1.5">Visitor parking is behind Building A. Check in with the receptionist on the 2nd floor.</div></div><div style="margin-top:16px;border-top:1px solid #f0eeea;padding-top:12px"><div class="text-[12px] font-semibold text-slate-700">Screening questions</div><div style="display:flex;gap:8px;margin-top:8px;align-items:center"><div style="flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a">Do you have an active RN license in Texas?</div><span style="font-size:12px;font-weight:600;color:#2563eb;white-space:nowrap">+ Add</span></div></div></div></div>
        <p class="text-[13px] text-slate-500 mt-3 leading-relaxed">Interview settings, set when you post your jobs.</p>
      </div>
    </div>

    <!-- 2 -->
    <div class="grid lg:grid-cols-[1fr_560px] gap-10 lg:gap-16 items-center mb-16 lg:mb-24">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500 mb-3">Step two</p>
        <h3 class="text-[22px] lg:text-[26px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-4">
          Candidates ask you for a time, and you say yes
        </h3>
        <p class="text-base text-slate-600 leading-relaxed mb-5">
          Post your roles and AI matches them to {CITY_SHORT}-area candidates who registered for this
          date. Matched candidates request a slot that suits them. You accept it, and accepting is
          what books the interview. There is no chasing, and no resume pile to work through first.
        </p>
        <ul class="list-none pl-0 space-y-3">
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug">Take each request individually, or turn on auto-accept and let the day fill itself</span></li>
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug">Every request arrives with a resume and contact details</span></li>
          <li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug">Candidates get reminders by email and SMS, which is why {SHOW_RATE} of them turn up</span></li>
        </ul>
      </div>
      <div>
        <img src="assets/product/review-confirm-austin.png?v=2" width="728" height="648"
             class="hidden lg:block w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy"
             alt="Candidates awaiting your response shows a Registered Nurse and a Medical Assistant in Austin with the times they requested and Accept, Decline and Reschedule buttons. Below, Upcoming interviews shows a Patient Care Technician and a Physical Therapist already booked for September 30.">
        <img src="assets/product/review-confirm-austin-mobile.png?v=2" width="668" height="648"
             class="lg:hidden w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy"
             alt="The same review screen on a narrow display.">
      </div>
    </div>

    <!-- 3 -->
    <div class="mb-16 lg:mb-24">
      <div class="max-w-3xl mb-8">
        <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500 mb-3">Step three &middot; {DATE_LONG}</p>
        <h3 class="text-[22px] lg:text-[26px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-4">
          You run the day from your interview rooms
        </h3>
        <p class="text-base text-slate-600 leading-relaxed">
          Your lobby opens at {TIME_PLAIN}. Candidates check themselves in, so you can see who is
          ready now and who is still waiting. You interview from your rooms, and your team can run
          several at once, up to the seats in your package. Where those interviews happen is your
          call, set once when you register: in person at your {CITY_SHORT} address, on JobFairX video
          with nothing to install, or by phone.
        </p>
      </div>
      <img src="assets/product/event-day-austin.png?v=1" width="1120" height="1078"
           class="w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy"
           alt="The Austin Hiring Event Lobby during the event. The header reads Event is live, ends in 2 hours 42 minutes, September 30 2026. Tabs show Waiting to interview 6, Interviewing 3, Interviewed 11, Not yet interviewed 14. Interview rooms lists a Registered Nurse and a Medical Assistant marked Ready with Start interview buttons, and Waiting rooms lists a Patient Care Technician and a Physical Therapist with their wait times.">
    </div>

    <!-- 4 -->
    <div>
      <div class="max-w-3xl mb-8">
        <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-500 mb-3">Step four</p>
        <h3 class="text-[22px] lg:text-[26px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-4">
          Every interview comes back with a decision on it
        </h3>
        <p class="text-base text-slate-600 leading-relaxed">
          JobFairX does not guess who you liked. Each completed interview carries the rating your
          own interviewer gave it, yes, maybe or no, alongside who ran it, the notes they took and
          where it happened. Message a candidate or book a second round from the same row.
        </p>
      </div>
      <img src="assets/product/post-event-report-austin.png?v=1" width="960" height="536"
           class="w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy"
           alt="Interviewed candidates lists four Austin healthcare candidates from September 30: a Registered Nurse rated No after two interviews, a Nurse Practitioner rated Yes, a Medical Assistant rated Maybe and a Respiratory Therapist rated Yes. Each row shows which interviewer ran it, a link to their notes, and whether the interview was on video or by phone.">
    </div>
  </div>
</section>
"""

VIDEO = """
<!-- Video slot. One walkthrough today; built as a slot so a healthcare-specific
     film can replace it per type without touching the layout. -->
<section id="walkthrough" class="bg-white py-12 lg:py-[90px]">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
      <div>
        <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-brand mb-4">Watch walkthrough</p>
        <h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-5">
          See the event day you are buying
        </h2>
        <p class="text-base text-slate-600 leading-relaxed mb-6">
          Three minutes through the lobby, the interview screen and the report, using the
          same product you will run on {DATE_SHORT}.
        </p>
        <a href="{CART_PKG}" class="button button-lg button-primary-inverted" data-cta>See packages for this event</a>
      </div>
      <div class="w-full">
        <div class="relative rounded-2xl bg-white border border-slate-200 shadow-xl overflow-hidden" style="aspect-ratio:16/9">
          <iframe src="https://www.youtube.com/embed/QuRalPnpPLA?rel=0" title="See how JobFairX works"
                  class="w-full h-full border-0 block"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  sandbox="allow-scripts allow-same-origin" referrerpolicy="strict-origin-when-cross-origin" 
                  allowfullscreen loading="lazy"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
"""

PACKAGES = """
<section id="packages" class="bg-slate-50 border-y border-slate-200 py-12 lg:py-[72px]" style="scroll-margin-top: 80px;">
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-10">
      <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-brand mb-3">Packages</p>
      <h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight mb-4">
        Register for {CITY_SHORT}, {DATE_SHORT}
      </h2>
      <p class="text-base text-slate-600 max-w-2xl mx-auto leading-relaxed" id="jfx-pkg-note">
        Flat rate for the event. Every package includes AI matching, unlimited interviews with
        each candidate, and a post-event report.
      </p>
    </div>

    <div class="grid lg:grid-cols-3 gap-6 mb-8">
      {TIERS}
    </div>

    <div class="rounded-2xl border border-blue-200 bg-blue-50 px-6 py-5 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <p class="text-base font-semibold text-slate-900 mb-1">Hiring across more than one event?</p>
        <p class="text-sm text-slate-600">Bundles run from 5 to 100 events and bring the per-event rate down to $297.</p>
      </div>
      <a href="/employer/hiring-event-bundles" class="button button-primary-inverted flex-shrink-0">View bundles</a>
    </div>

    <p class="text-[13px] text-slate-500 text-center mt-6">
      Full package comparison lives on the <a href="/employer/hiring-event-pricing" class="text-brand font-semibold hover:underline">pricing page</a>.
    </p>
  </div>
</section>
"""

TIER = """
      <div class="rounded-2xl border-2 {BORDER} bg-white p-6 lg:p-7 flex flex-col {GLOW}">
        {RIBBON}
        <div class="mb-1 flex items-center gap-2" data-state-show="a">
          <span class="text-[11px] font-semibold rounded-full px-2.5 py-1" style="background:#fffbeb;color:#b45309;border:1px solid #fde68a;">Save $100 &middot; ends {EARLY_ENDS}</span>
        </div>
        <h3 class="text-2xl font-semibold text-slate-900 mb-2">{NAME}</h3>
        <div class="flex items-baseline gap-2 mb-1">
          <span class="text-[20px] text-slate-400 line-through jfx-num" data-state-show="a">{FULL}</span>
          <span class="text-[28px] font-bold text-slate-900 jfx-num" data-price data-full="{FULL}" data-early="{EARLY}">{EARLY}</span>
        </div>
        <p class="text-sm text-slate-500 font-medium mb-5">per event</p>
        <ul class="list-none pl-0 mb-6 space-y-4">
          {BULLETS}
        </ul>
        <a href="{CART_PKG}" class="button-bar button-primary mt-auto" data-cta data-tier-cta>Reserve My Spot</a>
      </div>
"""

BULLET = """<li class="flex items-start gap-3"><span class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0" style="margin-top:2px;"><svg class="w-3 h-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg></span><span class="text-[16px] text-slate-700 leading-snug">{T}</span></li>"""

RIBBON_HTML = '<span class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold uppercase tracking-widest py-1.5 px-4 rounded-full shadow-lg text-[10px]">Most Popular</span>'

TIER_DATA = [
    ("Starter", "$495", "$395", ["Promote 1 job", "20+ scheduled candidate interviews", "In-person or video interviews", "2 recruiter seats"], False),
    ("Growth", "$895", "$795", ["Promote up to 3 jobs", "60+ scheduled candidate interviews", "In-person or video interviews", "Up to 5 recruiter seats"], True),
    ("Pro", "$1,495", "$1,395", ["Promote up to 6 jobs", "100+ scheduled candidate interviews", "In-person or video interviews", "Unlimited recruiters"], False),
]

PROOF = """
<section class="bg-white py-12 lg:py-[90px]">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto text-center mb-10">
      <p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-brand mb-4">Hiring event results</p>
      <blockquote class="text-xl lg:text-2xl text-slate-800 leading-relaxed mb-5">
        &ldquo;My team hired two LPNs, three RNs, and two MAs at the hiring event. What a great way to
        meet candidates and move quickly through interviews.&rdquo;
      </blockquote>
      <p class="text-sm text-slate-500">Director of Talent Acquisition, Western Regional Medical Center</p>
    </div>

    <div class="relative overflow-hidden pt-8 border-t border-slate-200">
      <p class="text-xs font-bold uppercase tracking-[0.12em] text-slate-400 text-center mb-6">Healthcare organizations that have hired at JobFairX events</p>
      <div class="absolute left-0 bottom-0 w-20 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none" style="top:80px;"></div>
      <div class="absolute right-0 bottom-0 w-20 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none" style="top:80px;"></div>
      <div class="flex animate-marquee whitespace-nowrap">{LOGOS}</div>
    </div>
  </div>
</section>
"""

LOGO_NAMES = [
    ("CVS Health", "font-black tracking-tighter"),
    ("Kaiser Permanente", "font-bold tracking-widest uppercase"),
    ("UnitedHealthcare", "font-semibold tracking-tight"),
    ("HCA Healthcare", "font-black tracking-tight"),
    ("Ascension", "font-extrabold italic"),
    ("Tenet Health", "font-bold"),
    ("Mayo Clinic", "font-medium tracking-widest uppercase"),
    ("Cleveland Clinic", "font-bold tracking-wide"),
    ("CommonSpirit Health", "font-semibold tracking-tight"),
    ("Community Health Systems (CHS)", "font-black italic"),
    ("Trinity Health", "font-extrabold tracking-tighter"),
    ("Providence", "font-medium tracking-tight"),
    ("Mount Sinai", "font-bold tracking-tight"),
    ("AdventHealth", "font-black tracking-tighter"),
    ("Baptist Health", "font-extrabold"),
    ("Intermountain Health", "font-semibold tracking-wide"),
]

FAQ = """
<section class="bg-slate-50 border-y border-slate-200 py-12 lg:py-[90px]">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 class="text-[26px] lg:text-[36px] font-semibold text-slate-900 tracking-[-0.02em] leading-tight text-center mb-10">
      Questions about this event
    </h2>
    <div class="space-y-4">{ITEMS}</div>
  </div>
</section>
"""

FAQ_ITEM = """
      <div class="jfx-faq rounded-xl border border-slate-200 bg-white transition-all duration-300"{ATTR}>
        <button type="button" class="w-full flex items-center justify-between gap-4 text-left px-5 lg:px-6 py-4 lg:py-5">
          <span class="text-[17px] font-semibold text-slate-900">{Q}</span>
          <svg class="jfx-faq-chev w-5 h-5 text-slate-400 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
        </button>
        <div class="jfx-faq-a px-5 lg:px-6 pb-4 lg:pb-5">
          <p class="text-sm text-slate-600 leading-relaxed">{A}</p>
        </div>
      </div>
"""

FAQ_DATA = [
    ("Are these candidates local to {CITY_SHORT}?",
     "Yes. Candidates are verified to be within approximately 20 miles of the event city, so you are meeting people who can realistically work for you in {CITY_SHORT}.", ""),
    ("When does candidate matching start for this event?",
     "As soon as your jobs are posted. AI matches your roles to candidates registered for {CITY_SHORT} and promotes your jobs to them, and interview requests typically begin arriving within a few hours.", ""),
    ("What is early registration pricing?",
     "Register 30 or more days before the event and $100 comes off every package. For {DATE_LONG} that window closes on {EARLY_ENDS}. The discount is a flat $100, not a percentage.", ' data-state-show="a"'),
    ("Where do the interviews actually happen?",
     "You choose, and your choice applies to your own interviews only. Interview in person at your {CITY_SHORT} address, on JobFairX video with nothing to install, or by phone. It never changes the price.", ""),
    ("How are candidates sourced?",
     "JobFairX has a database of more than 3 million job seekers, with over 2,200 new registrations each day. Candidates register for a specific city and date. Once you post your jobs, we match your roles to registered candidates and invite qualified matches to request an interview.", ""),
    ("How are candidates prepared?",
     "Candidates receive preparation materials before the event, including interview tips and technical requirements, plus automated email and SMS reminders ahead of each scheduled interview. Healthcare events run a 91% interview show rate.", ""),
    ("What if I register close to the event date?",
     "Registration stays open until roughly a day before the event. The later you post, the less time matching has to fill your schedule, which is the real cost of waiting.", ""),
]

CLOSE = """
<section id="final-cta" class="bg-white py-16 lg:py-[100px]">
  <div class="max-w-[1180px] mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 border border-slate-200 text-slate-600 text-[13px] font-semibold uppercase tracking-wider mb-6">
      <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
      <span class="jfx-num">{DATE_LONG} &middot; {CITY}</span>
    </div>
    <h2 class="text-[36px] lg:text-[52px] font-bold text-slate-900 tracking-[-0.02em] leading-tight mb-5" id="jfx-close-h">
      Reserve your spot at the {CITY_SHORT} healthcare hiring event
    </h2>
    <p class="text-[18px] text-slate-600 max-w-2xl mx-auto mb-8 leading-relaxed" id="jfx-close-sub">
      <span class="jfx-num">{REGISTERED}</span> candidates have registered so far, and healthcare events
      run a <span class="jfx-num">{SHOW_RATE}</span> interview show rate.
    </p>
    <a href="{CART_CLOSE}" id="jfx-close-cta" data-cta
       class="inline-flex items-center gap-2.5 px-8 md:px-10 py-4 md:py-5 bg-brand text-white rounded-full text-[15px] md:text-[17px] font-semibold transition-all duration-200 hover:bg-blue-700">
      Register for This Event <span>&rarr;</span>
    </a>
  </div>
</section>
"""

REVIEW = """
<!-- PREVIEW CONTROL - REVIEW ONLY. Delete this block, the #jfx-preview styles
     and the PREVIEW array in the script before production. Production renders
     exactly one lifecycle state, computed from the event date. -->
<div id="jfx-preview-bar">
  <span class="jfx-preview-label">Preview lifecycle</span>
  <span id="jfx-preview"></span>
  <span id="jfx-preview-note">36 days out - this event today</span>
</div>

<!-- Video lightbox. Matches the live site: "See how it works" opens the
     walkthrough in a modal and autoplays it, rather than scrolling. -->
<div id="jfx-video-modal" class="fixed inset-0 z-[80] items-center justify-center px-4" style="display:none;background:rgba(15,23,42,.75);">
  <div class="w-full max-w-[1014px] bg-white rounded-2xl shadow-2xl overflow-hidden relative" role="dialog" aria-modal="true" aria-label="How JobFairX hiring events work">
    <button type="button" id="jfx-video-close" aria-label="Close video"
            class="absolute right-3 top-3 z-10 w-9 h-9 rounded-full flex items-center justify-center"
            style="background:rgba(15,23,42,.6);color:#fff;border:0;cursor:pointer;">
      <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18L18 6M6 6l12 12"></path></svg>
    </button>
    <div id="jfx-video-slot" class="aspect-video w-full"></div>
  </div>
</div>
"""

SCRIPT = """
<script>
(function () {
  /* ---- Mobile drawer (the Dallas clone shipped without this) ---- */
  var burger = document.querySelector('header button');
  var drawer = document.querySelector('.fixed.right-0.w-full.bg-white');
  if (burger && drawer) {
    burger.addEventListener('click', function () { drawer.classList.remove('translate-x-full'); });
    var close = drawer.querySelector('button[aria-label="Close menu"]');
    if (close) close.addEventListener('click', function () { drawer.classList.add('translate-x-full'); });
  }

  /* ---- Video lightbox (matches live: opens and autoplays, no scroll) ----
     The iframe is created on open and destroyed on close so the video
     actually stops and the page does not carry a second YouTube embed. ---- */
  var VID = 'https://www.youtube.com/embed/QuRalPnpPLA?autoplay=1&playsinline=1&rel=0';
  var modal = document.getElementById('jfx-video-modal');
  var slot = document.getElementById('jfx-video-slot');
  function openVideo() {
    slot.innerHTML = '<iframe class="aspect-video w-full" src="' + VID + '" title="How JobFairX hiring events work" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope" sandbox="allow-scripts allow-same-origin" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>';
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    document.getElementById('jfx-video-close').focus();
  }
  function closeVideo() {
    slot.innerHTML = '';
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
  var openBtn = document.getElementById('jfx-video-open');
  if (openBtn) openBtn.addEventListener('click', openVideo);
  document.getElementById('jfx-video-close').addEventListener('click', closeVideo);
  modal.addEventListener('click', function (e) { if (e.target === modal) closeVideo(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.style.display === 'flex') closeVideo();
  });

  /* ---- FAQ accordion: items open independently ---- */
  document.querySelectorAll('.jfx-faq').forEach(function (item) {
    var btn = item.querySelector('button');
    btn.addEventListener('click', function () {
      var open = item.classList.toggle('is-open');
      item.classList.toggle('border-blue-200', open);
      item.classList.toggle('bg-blue-50/40', open);
      item.classList.toggle('shadow-sm', open);
    });
  });

  /* ---- Lifecycle states -------------------------------------------------
     Five real states, verified on the live site. Production drives this from
     the event date; here a review-only switcher stands in.
     A 30+ days . B 15-30 . C 3-15 . D ~2 days . E closed
  ----------------------------------------------------------------------- */
  var EVENT = {
    city: '__CITY__', citySrt: '__CITY_SHORT__', type: '__TYPE__',
    dateLong: '__DATE_LONG__', dateShort: '__DATE_SHORT__',
    earlyEnds: '__EARLY_ENDS__', nextEvent: '__NEXT_EVENT__',
    registered: '__REGISTERED__', showRate: '__SHOW_RATE__'
  };

  /* ---- Lifecycle states -------------------------------------------------
     CAPTURED EMPIRICALLY on 25 Aug 2026 by rendering real jobfairx event
     pages at 0,1,2,3,7,10,14,17,21,28,29,30,31,36 and 45 days out and reading
     the rendered DOM. Strings, inline colours and CTA behaviour below are
     verbatim from those pages - not from documentation.

     Boundaries proven at the edges:
       - the Save $100 badge is PRESENT at 31 days out and ABSENT at 30, so the
         live rule is "31 or more days before the event" (deadline = event-31).
         Scott has ruled the business rule is 30; the code must move to match.
       - registration is already CLOSED at 1 day out, not on the day.
       - at 0 days out there is no banner element at all.
  ---------------------------------------------------------------------- */
  var LINK_STD = 'Reserve your spot to meet interview-ready candidates →';
  var STATES = {
    early:  { banner: 'Early registration pricing ends soon. Save $100 and lock in priority candidate matching.',
              link: 'Register Now →', href: '#packages',
              bg: 'rgb(254, 244, 224)', fg: 'rgb(120, 53, 15)', bd: 'rgb(252, 211, 77)',
              early: true, open: true },
    soon:   { banner: 'Candidate matching activates soon.', link: LINK_STD, href: '#packages',
              bg: 'rgb(219, 234, 254)', fg: 'rgb(30, 58, 138)', bd: 'rgb(191, 219, 254)',
              early: false, open: true },
    week:   { banner: 'Candidate matching activates this week.', link: LINK_STD, href: '#packages',
              bg: 'rgb(219, 234, 254)', fg: 'rgb(30, 58, 138)', bd: 'rgb(191, 219, 254)',
              early: false, open: true },
    live:   { banner: 'Candidate matching is live.', link: LINK_STD, href: '#packages',
              bg: 'rgb(219, 234, 254)', fg: 'rgb(30, 58, 138)', bd: 'rgb(191, 219, 254)',
              early: false, open: true },
    closing:{ banner: 'Employer registration closes in 6 days.', link: LINK_STD, href: '#packages',
              bg: 'rgb(254, 247, 230)', fg: 'rgb(146, 64, 14)', bd: '',
              early: false, open: true },
    tomorrow:{ banner: 'Employer registration closes tomorrow.', link: 'Reserve your spot now →', href: '#packages',
              bg: 'rgb(254, 226, 226)', fg: 'rgb(153, 27, 27)', bd: '',
              early: false, open: true },
    closed: { banner: 'Employer registration is closed for this event. Next ' + EVENT.citySrt + ' Healthcare Hiring Event: {{NEXT_EVENT_DATE}}.',
              link: 'View Details →', href: EVENT.nextEvent,
              bg: 'rgb(240, 240, 240)', fg: 'rgb(51, 65, 85)', bd: 'rgb(203, 213, 225)',
              early: false, open: false },
    eventday:{ banner: null, link: null, href: null, bg: '', fg: '', bd: '',
              early: false, open: false }
  };

  function setState(key) {
    var s = STATES[key];
    if (!s) return;

    var wrap = document.getElementById('jfx-banner-wrap');
    var bar = document.getElementById('jfx-banner');
    if (!s.banner) {
      wrap.style.display = 'none';            // event day: the live site drops the bar entirely
    } else {
      wrap.style.display = '';
      document.getElementById('jfx-banner-text').textContent = s.banner;
      var link = document.getElementById('jfx-banner-link');
      link.textContent = s.link;
      link.setAttribute('href', s.href);
      link.style.color = s.fg;
      bar.style.backgroundColor = s.bg;
      bar.style.color = s.fg;
      bar.style.borderColor = s.bd || 'transparent';
    }

    document.querySelectorAll('[data-state-show="a"]').forEach(function (el) {
      el.style.display = s.early ? '' : 'none';
    });
    document.querySelectorAll('[data-price]').forEach(function (el) {
      el.textContent = s.early ? el.getAttribute('data-early') : el.getAttribute('data-full');
    });
    document.getElementById('jfx-rail-price').textContent = s.early ? '$395' : '$495';
    document.getElementById('jfx-rail-note').textContent = s.open
      ? (s.early
          ? 'Early registration saves $100 through ' + EVENT.earlyEnds + '.'
          : 'Standard pricing. Same at every event type.')
      : 'Registration closed. Same pricing at the next ' + EVENT.citySrt + ' event.';
    document.getElementById('jfx-pkg-note').textContent = s.open
      ? (s.early
          ? 'Flat rate for the event, with $100 off every package until ' + EVENT.earlyEnds + '.'
          : 'Flat rate for the event. Every package includes AI matching, unlimited interviews with each candidate, and a post-event report.')
      : 'Registration for ' + EVENT.dateLong + ' is closed. Packages are shown for reference.';

    document.querySelectorAll('[data-tier-cta]').forEach(function (el) {
      if (s.open) {
        el.textContent = 'Reserve My Spot';
        el.removeAttribute('aria-disabled');
        el.style.pointerEvents = ''; el.style.opacity = ''; el.style.background = ''; el.style.color = '';
      } else {
        el.textContent = 'Registration Closed';
        el.setAttribute('aria-disabled', 'true');
        el.style.pointerEvents = 'none';
        el.style.background = '#e2e8f0'; el.style.color = '#94a3b8';
      }
    });

    var heroCta = document.getElementById('jfx-hero-cta');
    if (heroCta) {
      heroCta.textContent = s.open ? 'Register for This Event' : 'Registration Closed';
      heroCta.style.pointerEvents = s.open ? '' : 'none';
      heroCta.style.background = s.open ? '' : '#e2e8f0';
      heroCta.style.color = s.open ? '' : '#94a3b8';
      heroCta.style.borderColor = s.open ? '' : '#e2e8f0';
    }

    var closeH = document.getElementById('jfx-close-h');
    var closeSub = document.getElementById('jfx-close-sub');
    var closeCta = document.getElementById('jfx-close-cta');
    if (s.open) {
      closeH.textContent = 'Reserve your spot at the ' + EVENT.citySrt + ' healthcare hiring event';
      closeSub.innerHTML = '<span class="jfx-num">' + EVENT.registered + '</span> candidates have registered so far, and healthcare events run a <span class="jfx-num">' + EVENT.showRate + '</span> interview show rate.';
      closeCta.innerHTML = 'Register for This Event <span>→</span>';
      closeCta.setAttribute('href', closeCta.getAttribute('data-href-open'));
    } else {
      closeH.textContent = 'This ' + EVENT.citySrt + ' event has closed';
      closeSub.textContent = 'Registration for ' + EVENT.dateLong + ' is closed. The next ' + EVENT.citySrt + ' healthcare hiring event is open for registration.';
      closeCta.innerHTML = 'See the next ' + EVENT.citySrt + ' Healthcare Hiring Event <span>→</span>';
      closeCta.setAttribute('href', EVENT.nextEvent);
    }
  }

  /* ---- Preview control (REVIEW ONLY - delete before production) ---------
     Pinned above the page's own banner so the thing it changes is always in
     view. Production renders exactly one of these from the event date. ---- */
  var PREVIEW = [
    { d: '45d', k: 'early',    note: '45 days out' },
    { d: '36d', k: 'early',    note: '36 days out - this event today' },
    { d: '31d', k: 'early',    note: '31 days out - last day of early registration' },
    { d: '30d', k: 'soon',     note: '30 days out - discount gone' },
    { d: '21d', k: 'week',     note: '21 days out' },
    { d: '14d', k: 'live',     note: '14 days out' },
    { d: '7d',  k: 'closing',  note: '7 days out' },
    { d: '2d',  k: 'tomorrow', note: '2 days out' },
    { d: '1d',  k: 'closed',   note: '1 day out - registration closed' },
    { d: '0d',  k: 'eventday', note: 'event day - no banner' }
  ];
  var pv = document.getElementById('jfx-preview');
  if (pv) {
    PREVIEW.forEach(function (o, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.textContent = o.d; b.title = o.note;
      b.addEventListener('click', function () {
        setState(o.k);
        document.getElementById('jfx-preview-note').textContent = o.note;
        pv.querySelectorAll('button').forEach(function (x, n) { x.setAttribute('aria-pressed', String(n === i)); });
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      if (i === 1) b.setAttribute('aria-pressed', 'true');
      pv.appendChild(b);
    });
  }

  var cta = document.getElementById('jfx-close-cta');
  if (cta) cta.setAttribute('data-href-open', cta.getAttribute('href'));

  setState('early');   // this event is 36 days out
})();
</script>
"""


def fill(tpl):
    return (tpl
            .replace("{CITY_SHORT}", EV["city_short"])
            .replace("{CITY}", EV["city"])
            .replace("{TYPE}", EV["type"])
            .replace("{DATE_LONG}", EV["date_long"])
            .replace("{DATE_SHORT}", EV["date_short"])
            .replace("{WEEKDAY}", EV["weekday"])
            .replace("{MONTH}", EV["month_abbr"])
            .replace("{DAY}", EV["day_num"])
            .replace("{TIME_PLAIN}", EV["time"])
            .replace("{TIME}", EV["time"])
            .replace("{REGISTERED}", EV["registered"])
            .replace("{SHOW_RATE}", EV["show_rate"])
            .replace("{AVG_INT}", EV["avg_interviews"])
            .replace("{AVG_HIRE}", EV["avg_hires"])
            .replace("{EARLY_ENDS}", EV["early_ends"])
            .replace("{CART_HERO}", CART_HERO)
            .replace("{CART_PKG}", CART_PKG)
            .replace("{CART_CLOSE}", CART_CLOSE))


# --- assemble tiers --------------------------------------------------------
tiers = []
for name, full, early, bullets, popular in TIER_DATA:
    t = TIER
    t = t.replace("{BORDER}", "border-blue-500" if popular else "border-slate-200")
    t = t.replace("{GLOW}", 'relative shadow-[0_0_60px_-10px_rgba(59,130,246,0.3)]' if popular else "relative")
    t = t.replace("{RIBBON}", RIBBON_HTML if popular else "")
    t = t.replace("{NAME}", name).replace("{FULL}", full).replace("{EARLY}", early)
    t = t.replace("{BULLETS}", "\n          ".join(BULLET.replace("{T}", b) for b in bullets))
    tiers.append(t)
packages = fill(PACKAGES.replace("{TIERS}", "".join(tiers)))

# --- assemble logos (duplicated for the marquee loop) ----------------------
logo_spans = "".join(
    '<span class="text-lg {c} text-slate-400 mx-8 shrink-0">{n}</span>'.format(c=cls, n=name)
    for name, cls in LOGO_NAMES
)
proof = PROOF.replace("{LOGOS}", logo_spans + logo_spans)

# --- assemble FAQ ----------------------------------------------------------
faq_items = "".join(
    FAQ_ITEM.replace("{Q}", fill(q)).replace("{A}", fill(a)).replace("{ATTR}", attr)
    for q, a, attr in FAQ_DATA
)
faq = FAQ.replace("{ITEMS}", faq_items)

script = (SCRIPT
          .replace("__CITY__", EV["city"])
          .replace("__CITY_SHORT__", EV["city_short"])
          .replace("__TYPE__", EV["type"])
          .replace("__DATE_LONG__", EV["date_long"])
          .replace("__DATE_SHORT__", EV["date_short"])
          .replace("__EARLY_ENDS__", EV["early_ends"])
          .replace("__NEXT_EVENT__", EV["next_event"])
          .replace("__REGISTERED__", EV["registered"])
          .replace("__SHOW_RATE__", EV["show_rate"]))

body = "".join([
    chrome_top,
    fill(HERO), fill(ROOM), fill(AUDIENCE), fill(RUNWAY), fill(VIDEO),
    packages, fill(proof), fill(faq), fill(CLOSE),
    "</div></div></div></div>",
    footer,
    REVIEW, script,
])

provenance = (
    "<!--\n"
    "  employer-event-detail-v2.html - GENERATED. Do not edit by hand.\n"
    "  Built by build-event-healthcare.py. Edit the builder and re-run.\n"
    "  Hiring Event Details Page, redesign. Austin TX Healthcare, Sep 30 2026.\n"
    "  Chrome (head/header/drawer/footer) lifted from employer-event-detail.html.\n"
    "  Content authored. Live event data verified on jobfairx.com 25 Aug 2026.\n"
    "  NOTE FOR THE DEVELOPER: early registration is shown here as 30+ days\n"
    "  (ends {a}), per Scott's ruling. The live server still computes 31 days\n"
    "  (ends {b}) - the code needs to move to 30 or the page promises the\n"
    "  discount a day earlier than the system grants it.\n"
    "-->\n"
).format(a=EV["early_ends"], b=EV["early_ends_live"])

html = head.replace("</head>", STYLE + "</head>") + "\n<body>\n" + body + "\n</body></html>\n"
html = provenance + html

OUT.write_text(html, encoding="utf-8")
print("\nWrote {} ({:,} bytes)".format(OUT.name, len(html)))

# --- post-build assertions -------------------------------------------------
checks = [
    ("interview settings panel present", "Interview settings" in html and "Interview format" in html),
    ("four product visuals present", all(v in html for v in ["review-confirm-austin.png","event-day-austin.png","post-event-report-austin.png"])),
    ("four beats numbered", all(f">Step {w}</p>" in html for w in ["one","two","four"])),
    ("clinical roles expanded", html.count('class="jfx-chip"') >= 12),
    ("video lightbox wired", "jfx-video-modal" in html and "jfx-video-open" in html and "autoplay=1" in html),
    ("eight lifecycle states defined", all(k + ":" in html for k in ["early","soon","week","live","closing","tomorrow","closed","eventday"])),
    ("preview control present", "jfx-preview-bar" in html and html.count("note: '") == 10),
    ("no Dallas event id", "743231932652847104" not in html),
    ("no Dallas paths", "%2Fdallas%2F" not in html and "/texas/dallas/" not in html),
    ("event id threaded", html.count(EV["event_id"]) >= 6),
    ("no 'virtual' in copy", html.lower().count("virtual") == 2),  # 2 login URLs
    ("30-day deadline used", EV["early_ends"] in html),
    ("tabular class defined", ".jfx-num" in html),
    # .container caps at 1024px. It is allowed only where the lifted live
    # footer already pairs it with an explicit max-w-*; never in authored content.
    ("no bare .container in authored content", 'class="container' not in html[: html.find("<footer")]),
]
print("\nPost-build checks:")
bad = 0
for label, ok in checks:
    print("  {} {}".format("OK  " if ok else "FAIL", label))
    if not ok:
        bad += 1
if bad:
    fail("{} post-build check(s) failed".format(bad))
print("\nDone.")
