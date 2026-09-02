#!/usr/bin/env python3
"""Build employer-event-detail.html from the captured live DOM of the Dallas
Technology event page (jobfairx.com/employer/job-fairs/texas/dallas/743231932652847104,
captured 24 Aug 2026), with the interview-format messaging applied.

Same contract as build-employer-home.py: every replacement must match exactly once.
The testimonial QUOTE mentioning "a virtual event" is deliberately untouched —
quotes are people's words, not site copy.
"""
import re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/event-detail-live-dom.html"
OUT = f"{W}/employer-event-detail.html"
s = open(SRC, encoding="utf-8").read()
orig = len(s)
log = []

def sub(label, old, new, count=1, regex=False):
    global s
    if regex:
        s2, n = re.subn(old, new, s)
    else:
        n = s.count(old); s2 = s.replace(old, new) if n == count else s
    if n != count or count == 0:
        print(f"ABORT [{label}]: {n} matches, expected {count}"); sys.exit(1)
    s = s2; log.append((label, n))

# ── de-frameworkise ──────────────────────────────────────────────────────────
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "", count=len(re.findall(r'data-svelte-h', s)), regex=True)
s = s.replace(' data-sveltekit-preload-data="hover"', ""); log.append(("strip sveltekit body attr", 1))
sub("strip origin-trial metas", r'<meta http-equiv="origin-trial"[^>]*>', "", count=len(re.findall(r'origin-trial', s)), regex=True)

# ── localise assets ──────────────────────────────────────────────────────────
sub("app css",  re.escape('../../../../_app/immutable/assets/app.029f5d9e.css'), 'assets/employer-home/app.css?v=2', regex=True)
sub("page css", re.escape('../../../../_app/immutable/assets/6.2102846a.css'), 'assets/employer-home/page.css?v=2', regex=True)
sub("favicon", 'https://jobfairx.com/favicon.png', 'assets/employer-home/favicon.png')
n = s.count('/jobfairx-logo.png'); sub("logo", '/jobfairx-logo.png', 'assets/employer-home/jobfairx-logo.png', count=n)
sub("recruiter img", '/_app/immutable/assets/recruiter.63204f89.jpg', 'assets/employer-home/recruiter.63204f89.jpg')
for nm in ["tech-hero.28296e64.png","tech.d1d87547.jpg","dell.fcaf3f08.png","ibm.82b54423.png",
           "cisco.fa39b3db.png","oracle.1d9b4d5c.png","hp.ec4178bd.png","salesforce.a4bedb40.png",
           "intuit.83c04601.png","paypal.ac4d3340.png","servicenow.d4a63bb9.png","vmware.9227be68.png",
           "adobe.659bbc06.png","capital-one.fb621c52.png","infosys.41dbb667.png","cognizant.2bb7b687.png",
           "accenture.2e8a4602.png","cdw.fa9a45f8.png"]:
    cnt = s.count(f'/_app/immutable/assets/{nm}')
    sub(f"img {nm}", f'/_app/immutable/assets/{nm}', f'assets/event-detail/{nm}', count=cnt)

# ── head / SEO ───────────────────────────────────────────────────────────────
sub("title", "For Employers: Technology Dallas, TX  Virtual Job Fair",
    "For Employers: Technology Dallas, TX Hiring Event", count=s.count("For Employers: Technology Dallas, TX  Virtual Job Fair"))
sub("meta descriptions", "Recruit smart tech people at JobFairX's Dallas, TX virtual job fair.",
    "Recruit smart tech people at JobFairX's Dallas, TX hiring event. Interview in person or on video.",
    count=s.count("Recruit smart tech people at JobFairX's Dallas, TX virtual job fair."))

# ── hero ─────────────────────────────────────────────────────────────────────
sub("hero pill", ">Dallas, TX · Virtual Technology Hiring Event</span>",
    ">Dallas, TX · Technology Hiring Event</span>")
sub("hero sub (mention)", ">Meet engineers, developers, and data talent in live interviews. Skip the sourcing and start hiring.<",
    ">Meet engineers, developers, and data talent in live interviews, in person or on video. Skip the sourcing and start hiring.<")

# ── event-day step (same block as homepage) ──────────────────────────────────

# ── video walkthrough: subtext -> what-you'll-see bullets (Scott-approved) ───
CHECK = '<span style="color:#186a3b;margin-right:8px">&#10003;</span>'
sub("walkthrough bullets",
    '<p class="text-[16px] text-[#4a4a4a] leading-[1.55]">A quick walkthrough of the platform.</p>',
    '<div class="text-[16px] text-[#4a4a4a]" style="line-height:2.1">'
    + CHECK + 'Interviews in person, on video, or by phone<br>'
    + CHECK + 'How matched candidates request interview times<br>'
    + CHECK + 'One dashboard for every interview and candidate</div>')

# ── results intro (site copy; the testimonial QUOTE below it stays verbatim) ─
sub("results intro", "who've used our virtual events to hire", "who've used our hiring events to hire")

# ── pricing: mirror the shipped employer-pricing.html treatment ──────────────
# (commits 9ef298f/3a378bf on the preview repo, Scott-approved): each tier card
# gains an "In-person or video interviews" bullet after the scheduled-interviews
# line, and All Packages Include gains a standalone "In-person, video, or phone
# interviews" item after Auto-accept. The unlimited-interviews bullet stays
# clean — the format has its own line now. Markup copied verbatim from the
# deployed pricing page (same live template family, classes identical).
CARD_FMT_LI = ('<li class="flex items-start gap-2.5 text-slate-700"><div class="w-5 h-5 rounded-full bg-blue-100 flex '
 'items-center justify-center flex-shrink-0 mt-0.5"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '
 'class="text-blue-600"><path d="M20 6 9 17l-5-5"></path></svg></div> '
 '<span class="font-medium leading-snug text-[16px]">In-person or video interviews</span> </li>')
for cnt in ["20+", "60+", "100+"]:
    anchor = f">{cnt} scheduled candidate interviews</span> </li>"
    sub(f"card format bullet ({cnt})", anchor, anchor + CARD_FMT_LI)
AUTOACCEPT = '<span class="text-slate-600 text-sm leading-relaxed">Auto-accept interview requests or review each one individually</span> </div>'
ALLPKG_FMT = ('<div class="flex items-start gap-3"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
 'class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"><path d="M20 6 9 17l-5-5"></path></svg> '
 '<span class="text-slate-600 text-sm leading-relaxed">In-person, video, or phone interviews</span> </div>')
sub("all-packages format item", AUTOACCEPT, AUTOACCEPT + ALLPKG_FMT)

# ── final CTA ────────────────────────────────────────────────────────────────
sub("final CTA h2", ">Secure your spot for the Dallas Technology virtual hiring event</h2>",
    ">Secure your spot for the Dallas Technology hiring event</h2>")

# ── footer ───────────────────────────────────────────────────────────────────
sub("footer employers link", r"(</span>\s*)Virtual Hiring Event Platform(\s*</a>)", r"\1Hiring Event Platform\2", regex=True)


# ── SECTION SURGERY (#1 #2 #6 #10) ───────────────────────────────────────────
# The live page's How-It-Works and Messaging sections are scroll-pinned by JS the
# static build cannot carry (they rendered 12k/44k px tall). Replace them with the
# homepage's proven static sections — which now carry step 1 (Interview Settings),
# the request→accept step, the Video chip, Analytics, and Automations — and
# reorder the page so its unique proof (testimonials, Past Companies) sits above
# the shared explainer. FAQ becomes native <details> with the live site's answers.

home = open(f"{W}/employer-home.html", encoding="utf-8").read()
def span_of(src, probe, tag="section"):
    i = src.find(probe)
    if i == -1: print(f"ABORT [span {probe[:30]}]: probe not found"); sys.exit(1)
    st = src.rfind(f"<{tag}", 0, i)
    en = src.find(f"</{tag}>", i) + len(f"</{tag}>")
    return st, en

# ── Built-in Tools bento: authored HERE now (home no longer carries it). ────
# Moved verbatim from build-employer-home.py when Scott removed the section
# from the homepage (24 Aug). CHECK is defined above (walkthrough bullets).
ICON_MSG  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>'
ICON_LIST = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/><path d="M13 6h8"/><path d="M13 12h8"/><path d="M13 18h8"/></svg>'
ICON_ZAP  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 3 14h7l-1 8 10-12h-7z"/></svg>'

def _tinput(v):
    return f'<div style="border:1px solid #e2e8f0;border-radius:8px;padding:8px 11px;font-size:13px;color:#0f172a">{v}</div>'
def _chip(t, green):
    if green: return f'<span style="background:#dcfce7;color:#186a3b;border-radius:999px;padding:3px 10px;font-size:11px;font-weight:600;white-space:nowrap">{t}</span>'
    return f'<span style="background:#f1f5f9;color:#475569;border-radius:999px;padding:3px 10px;font-size:11px;font-weight:600;white-space:nowrap">{t}</span>'
def _trow(name, job, st, green, last=False):
    b = "" if last else "border-bottom:1px solid #f0eeea;"
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;padding:9px 0;{b}">'
            f'<span style="min-width:0"><b style="color:#0f172a;font-size:13px">{name}</b>'
            f'<span style="color:#94a3b8;font-size:12px"> &middot; {job}</span></span>{_chip(st, green)}</div>')
def _preset(name, on, last=False):
    b = "" if last else "border-bottom:1px solid #f0eeea;"
    tog = ('<span style="display:inline-flex;align-items:center;gap:6px;color:#186a3b;font-size:12px;font-weight:600">'
           '<span style="width:26px;height:14px;border-radius:999px;background:#186a3b;position:relative;display:inline-block">'
           '<span style="position:absolute;right:1.5px;top:1.5px;width:11px;height:11px;border-radius:50%;background:#fff"></span></span>On</span>'
           if on else '<span style="color:#94a3b8;font-size:12px;font-weight:600">Off</span>')
    return f'<div style="display:flex;justify-content:space-between;align-items:center;padding:9px 0;{b}"><span style="color:#0f172a;font-size:13px">{name}</span>{tog}</div>'

BENTO = (
'<section id="built-in-tools" class="py-12 min-[901px]:py-24 bg-[#f8f7f4]">'
'<style>'
'#built-in-tools .bt-grid{display:grid;grid-template-columns:1fr;gap:24px}'
'#built-in-tools .bt-hero{display:grid;grid-template-columns:1fr}'
'#built-in-tools .bt-card{background:#fff;border:1px solid #e8e6e3;border-radius:16px;'
'box-shadow:0 8px 32px rgba(0,0,0,0.04);transition:transform .2s,box-shadow .2s}'
'#built-in-tools .bt-card:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(15,23,42,0.08)}'
'#built-in-tools .bt-crop{margin-top:22px}'
'@media (min-width:901px){'
'#built-in-tools .bt-grid{grid-template-columns:repeat(3,1fr)}'
'#built-in-tools .bt-hero{grid-template-columns:1fr 560px}'
'#built-in-tools .bt-crop{height:280px;overflow:hidden}'
'}'
'@media (prefers-reduced-motion:reduce){#built-in-tools .bt-card{transition:none}'
'#built-in-tools .bt-card:hover{transform:none}}'
'</style>'
'<div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">'
# header
'<div style="text-align:center;margin-bottom:56px">'
'<div class="text-[12px] font-bold uppercase tracking-[0.14em] text-[#2563eb]" style="margin-bottom:14px">Built-in Tools</div>'
'<h2 class="text-3xl lg:text-4xl font-semibold text-slate-900 tracking-[-0.02em]" style="margin-bottom:14px">Message, schedule, and track candidates in one place</h2>'
'<p class="text-[17px] text-slate-600" style="max-width:680px;margin:0 auto">Candidate messaging, interview scheduling, response tracking, and automations &mdash; built into every JobFairX event.</p>'
'</div>'
# hero — scheduling
'<div class="bt-card bt-hero" style="overflow:hidden">'
'<div style="padding:44px 48px;display:flex;flex-direction:column;justify-content:center">'
'<div class="text-[12px] font-bold uppercase tracking-[0.14em] text-[#2563eb]" style="margin-bottom:12px">Interview Scheduling</div>'
'<h3 class="text-lg lg:text-2xl font-semibold text-slate-900 leading-tight" style="margin-bottom:12px">Interview candidates before and after the event</h3>'
'<p class="text-base text-slate-600 leading-[1.55]" style="margin-bottom:16px">Propose interview times, reschedule when plans change, and schedule follow-up interviews after the event.</p>'
'<div class="text-[15px] text-slate-700" style="line-height:2.1">'
+ CHECK + 'Suggest multiple interview times<br>'
+ CHECK + 'Reschedule interviews with one click<br>'
+ CHECK + 'Schedule follow-up interviews after the event</div>'
'<a href="/employer/cart?returnTo=%2Femployer" class="inline-block text-[15px] font-semibold text-brand hover:underline" style="margin-top:18px">Register for an event <span aria-hidden="true">&rarr;</span></a>'
'</div>'
'<div style="background:#f4f6fa;padding:34px;display:flex;align-items:center;justify-content:center">'
'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:20px 22px;width:100%;max-width:400px;box-shadow:0 4px 14px rgba(15,23,42,0.08)">'
'<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:12px">Schedule with Maya Rodriguez</div>'
'<div style="display:flex;gap:8px;margin-bottom:8px"><div style="flex:1.4">' + _tinput("05/28/2026") + '</div><div style="flex:1">' + _tinput("11:00 AM") + '</div></div>'
'<div style="display:flex;gap:8px;margin-bottom:10px"><div style="flex:1.4">' + _tinput("06/03/2026") + '</div><div style="flex:1">' + _tinput("9:00 AM") + '</div></div>'
'<div style="font-size:13px;font-weight:600;color:#2563eb;margin-bottom:12px">+ Suggest multiple times</div>'
'<div style="border:1px solid #f0eeea;border-radius:8px;padding:10px 12px;font-size:12.5px;color:#64748b;line-height:1.55;margin-bottom:14px">Hi Maya, thank you for your interest in our open Project Engineer role. Are you available to interview on either of the proposed times?</div>'
'<div style="display:flex;gap:10px;justify-content:flex-end;align-items:center">'
'<span style="font-size:13px;color:#475569;padding:7px 14px">Cancel</span>'
'<span style="font-size:13px;font-weight:600;color:#fff;background:#2563eb;border-radius:999px;padding:7px 18px">Send</span></div>'
'</div></div></div>'
# row 2
'<div class="bt-grid" style="margin-top:24px">'
# messaging card
'<div class="bt-card" style="padding:28px">'
'<div style="width:26px;height:26px;border-radius:50%;background:#dbeafe;color:#2563eb;display:inline-flex;align-items:center;justify-content:center;margin-bottom:14px">' + ICON_MSG + '</div>'
'<h3 class="text-lg font-semibold text-slate-900 leading-tight" style="margin-bottom:8px">Stay connected with candidates</h3>'
'<p class="text-[14px] text-slate-600 leading-[1.55]" style="margin:0">Start conversations, answer questions, and keep candidates engaged from registration to interview.</p>'
'<div class="bt-crop"><div style="border:1px solid #e8e6e3;border-radius:14px;padding:14px 16px">'
'<div style="font-size:13px;margin-bottom:10px"><b style="color:#0f172a">Tamara Williams</b><span style="color:#94a3b8;font-size:12px"> &middot; Registered Nurse &middot; Nashville, TN</span></div>'
'<div style="background:#2563eb;color:#fff;border-radius:10px 10px 3px 10px;padding:8px 11px;font-size:12.5px;line-height:1.5;margin-bottom:7px">Hi Tamara &mdash; your interview is confirmed for tomorrow at 2pm. Talk soon!</div>'
'<div style="background:#f1f5f9;color:#334155;border-radius:10px 10px 10px 3px;padding:8px 11px;font-size:12.5px;line-height:1.5">Confirmed, thank you! Looking forward to it.</div>'
'<div style="font-size:10.5px;color:#94a3b8;margin-top:7px">Delivered &middot; 9:15 AM</div>'
'</div></div></div>'
# tracking card — strings verified against the app
'<div class="bt-card" style="padding:28px">'
'<div style="width:26px;height:26px;border-radius:50%;background:#dbeafe;color:#2563eb;display:inline-flex;align-items:center;justify-content:center;margin-bottom:14px">' + ICON_LIST + '</div>'
'<h3 class="text-lg font-semibold text-slate-900 leading-tight" style="margin-bottom:8px">Track every interview response</h3>'
'<p class="text-[14px] text-slate-600 leading-[1.55]" style="margin:0">Monitor interview requests, candidate confirmations, and pending responses in one place.</p>'
'<div class="bt-crop"><div style="border:1px solid #e8e6e3;border-radius:14px;padding:12px 16px">'
'<div style="font-size:12px;font-weight:700;color:#0f172a;margin-bottom:4px">Candidates awaiting your response</div>'
+ _trow("Andre Diaz","Registered Nurse","Awaiting your response",False)
+ _trow("Sanjay Iyer","Software Engineer","Confirmed",True)
+ _trow("Riley Foster","Security Officer","Awaiting your response",False)
+ _trow("Aaliyah Lee","Account Executive","Confirmed",True,last=True)
+ '</div></div></div>'
# automations card
'<div class="bt-card" style="padding:28px">'
'<div style="width:26px;height:26px;border-radius:50%;background:#dbeafe;color:#2563eb;display:inline-flex;align-items:center;justify-content:center;margin-bottom:14px">' + ICON_ZAP + '</div>'
'<h3 class="text-lg font-semibold text-slate-900 leading-tight" style="margin-bottom:8px">Message every candidate without touching your keyboard</h3>'
'<p class="text-[14px] text-slate-600 leading-[1.55]" style="margin:0">Preset automations message candidates as they move through your hiring process &mdash; personalized with merge fields, scoped per job or event.</p>'
'<div class="bt-crop"><div style="border:1px solid #e8e6e3;border-radius:14px;padding:10px 16px">'
'<div style="font-size:12px;font-weight:700;color:#0f172a;padding:4px 0 2px">My automations</div>'
+ _preset("Message new candidates",True)
+ _preset("Missed interview follow-up",True)
+ _preset("Post-interview follow-up",False,last=True)
+ '<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px 10px;font-size:12px;color:#475569;line-height:1.5;margin-top:8px">Hi <span style="color:#2563eb;font-family:ui-monospace,monospace">{CANDIDATE_FIRSTNAME}</span>, thanks for requesting an interview for the <span style="color:#2563eb;font-family:ui-monospace,monospace">{JOB_TITLE}</span> role&hellip;</div>'
'<div style="font-size:11px;color:#94a3b8;margin-top:8px">5 presets &middot; On/Off per job</div>'
'</div></div></div>'
'</div></div></section>')

# pieces from the built homepage
h_st, h_en = span_of(home, "Hiring Events Built Around Interviews")
HOW = home[h_st:h_en]
MSG = BENTO

# ── Localize the imported sections to this event (Dallas Technology) ─────────
# The homepage stays the canonical generic version; the event page carries the
# same sections with a down-funnel H2, condensed step copy, and mock data
# re-skinned to the event's vertical and metro — the same pattern the live
# site uses on its event pages. Scoped to the extracted section strings so
# counts can't collide with the rest of the page.
def loc(section, label, old, new, count=1):
    n = section.count(old)
    if n != count:
        print(f"ABORT [loc {label}]: {n} matches, expected {count}"); sys.exit(1)
    log.append((f"loc {label}", n))
    return section.replace(old, new)

HOW = loc(HOW, "H2 down-funnel",
    ">Hiring Events Built Around Interviews</h2>",
    ">Register once, interview all day</h2>")
HOW = loc(HOW, "step-1 body condensed",
    ">Set your screening questions and interview settings. Candidate matching activates automatically once your\n            jobs are posted.</p>",
    ">Post your jobs and set your screening questions. Candidate matching activates automatically.</p>")
HOW = loc(HOW, "step-2 body condensed",
    ">Matched candidates request interview times. Accept requests individually, or enable auto-accept to confirm\n          interviews automatically.</p>",
    ">AI-matched candidates request an interview time &mdash; you accept, decline, or propose another. Auto-accept confirms instantly and pauses when your slots fill.</p>")
HOW = loc(HOW, "step-3 body condensed",
    ">Meet candidates in person at your address, on JobFairX video with nothing to install, or by phone. Whatever you choose, the schedule, resumes, and notes are right there in the same place.</p>",
    ">Meet candidates in person at your Dallas address, on JobFairX video, or by phone &mdash; schedule, resumes, and notes in the same place.</p>")
HOW = loc(HOW, "step-4 body condensed",
    ">Gain complete visibility into your hiring metrics with a comprehensive event report that consolidates your team&rsquo;s input. Track which team member interviewed each candidate, review yes, no, or maybe outcomes, and identify no-shows. You can seamlessly advance your pipeline by messaging candidates or scheduling next-round interviews directly from the dashboard.</p>",
    ">Requests, scheduled, completed, and your Yes/Maybe/No ratings for this event &mdash; ready the moment it ends.</p>")
# step-1 mock: tech screener + the Dallas address the product's own dashboard uses
HOW = loc(HOW, "screener -> tech",
    ">Do you have an active RN license in Texas?</div>",
    ">How many years of software engineering experience do you have?</div>")
HOW = loc(HOW, "address -> Dallas", ">1201 Peachtree St NE</div>", ">2200 Ross Ave</div>")
HOW = loc(HOW, "suite -> 400", ">Suite 300</div>", ">Suite 400</div>")
# review table (current-app mock): the two Registered Nurse rows go tech for
# the Dallas Technology page; Tamara also renames (she is the bento's Senior
# Network Engineer on this page — one person, one role).
def loc_first(section, label, old, new):
    if section.count(old) < 1:
        print(f"ABORT [loc {label}]: 0 matches"); sys.exit(1)
    log.append((f"loc {label}", 1))
    return section.replace(old, new, 1)
HOW = loc_first(HOW, "rev row1 name", ">Tamara Williams</b>", ">Dana Whitfield</b>")
HOW = loc_first(HOW, "rev row1 role", ">Registered Nurse</span>", ">DevOps Engineer</span>")
HOW = loc(HOW, "rev row4 role", ">Registered Nurse</span>", ">QA Engineer</span>")

# ── bento: same localization for this event. Card copy stays; the H2 goes
# down-funnel (approved #11 string) and mock personas go tech, reusing the
# HOW table's Dallas personas so the same candidates recur across the page.
MSG = loc(MSG, "bento H2 down-funnel",
    ">Message, schedule, and track candidates in one place</h2>",
    ">Fill your interview calendar before event day.</h2>")
MSG = loc(MSG, "chat persona -> tech",
    " &middot; Registered Nurse &middot; Nashville, TN</span>",
    " &middot; Senior Network Engineer &middot; Dallas, TX</span>")
MSG = loc(MSG, "modal role -> tech",
    "our open Project Engineer role", "our open IT Support Technician role")
MSG = loc(MSG, "trow2 role", " &middot; Software Engineer</span>", " &middot; Data Analyst</span>")
MSG = loc(MSG, "trow1 role", " &middot; Registered Nurse</span>", " &middot; Software Engineer</span>")
MSG = loc(MSG, "trow3 role", " &middot; Security Officer</span>", " &middot; IT Support Technician</span>")
MSG = loc(MSG, "trow4 role", " &middot; Account Executive</span>", " &middot; Network Engineer</span>")
MSG = loc(MSG, "trow1 name", ">Andre Diaz</b>", ">Marcus Bell</b>")
MSG = loc(MSG, "trow2 name", ">Sanjay Iyer</b>", ">Priya Nair</b>")
MSG = loc(MSG, "trow3 name", ">Riley Foster</b>", ">Devon Clarke</b>")
MSG = loc(MSG, "trow4 name", ">Aaliyah Lee</b>", ">Elena Vasquez</b>")

# spans in the event page
s3a, _ = span_of(s, "Hiring Events Built Around Interviews")
_, s4b = span_of(s, "Candidate Messaging")
res_a, res_b = span_of(s, "Results from Top Tech Teams")
faq_a, faq_b = span_of(s, "Frequently Asked Questions")
pr_a, pr_b = span_of(s, "Starter")
gap = s[pr_b:faq_a]                        # [All Packages Include][Past Companies] both live here
pc = gap.find("Past Companies")
split = gap.rfind('<div class="lg:my-16 my-8">', 0, pc)
if split == -1: print("ABORT [gap split]: Past Companies boundary not found"); sys.exit(1)
ALLPKG = gap[:split]                       # stays glued to pricing
PASTCO = gap[split:]                       # moves up with the testimonials
TESTI = s[res_a:res_b]
PRICING = s[pr_a:pr_b]

FAQ_ITEMS = [
 ("Are candidates local to the city where the event is held?",
  "Yes. Candidates are verified to be within approximately 20 miles of the event city, so you’re connecting with local, relevant talent."),
 ("How are candidates sourced?",
  "JobFairX has a database of more than 3 million job seekers, with over 2,200 new registrations each day. Candidates register for specific events by city and date. Once you post your jobs, we match your roles with registered candidates and invite qualified matches to request an interview."),
 ("How are candidates prepared for interviews?",
  "Candidates receive pre-event preparation materials, including interview tips and technical requirements, along with guidance on presenting themselves professionally. They also receive automated emails and SMS leading up to their scheduled interview to ensure high attendance rates."),
]
FAQ = ('<section class="bg-white py-12 lg:py-[90px]"><div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[820px]">'
 '<h2 class="text-3xl lg:text-4xl font-semibold text-slate-900 tracking-[-0.02em] text-center" style="margin-bottom:34px">Frequently Asked Questions</h2>'
 + "".join(
   '<details class="border-b border-slate-200" style="padding:4px 0">'
   f'<summary class="text-[17px] font-semibold text-slate-900" style="cursor:pointer;padding:16px 4px;list-style-position:outside">{q}</summary>'
   f'<p class="text-[15px] text-slate-600 leading-relaxed" style="padding:0 4px 18px;margin:0">{a}</p></details>'
   for q, a in FAQ_ITEMS)
 + '</div></section>')

# cut testimonials, past companies, pricing, faq from their old positions (back to front)
s = s[:faq_a] + s[faq_b:]
s = s[:pr_a] + s[pr_a + len(PRICING) + len(gap):]
s = s[:res_a] + s[res_b:]
# replace the two broken sections with home HOW + MSG
s3a2, _ = span_of(s, "Hiring Events Built Around Interviews")
_, s4b2 = span_of(s, "Candidate Messaging")
s = s[:s3a2] + s[s4b2:]
# insert, after the video section, the new order:
v_a, v_b = span_of(s, "See How JobFairX Works")
s = s[:v_b] + TESTI + PASTCO + HOW + MSG + PRICING + ALLPKG + FAQ + s[v_b:]
log.append(("section surgery: rebuild + reorder + native FAQ", 1))

# ── #10: unsplash headshots -> initials circles ──────────────────────────────
def initials(alt):
    parts = alt.split(); return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()
heads = re.findall(r'<img[^>]*src="https://images\.unsplash\.com[^"]*"[^>]*alt="([^"]*)"[^>]*>', s)
for alt in heads:
    ini = initials(alt)
    pat = re.compile(r'<img[^>]*src="https://images\.unsplash\.com[^"]*"[^>]*alt="' + re.escape(alt) + r'"[^>]*>')
    rep = (f'<span role="img" aria-label="{alt}" class="inline-flex items-center justify-center rounded-full" '
           f'style="width:48px;height:48px;background:#e4edfd;color:#1d4ed8;font-weight:700;font-size:15px;flex:none">{ini}</span>')
    s, n = pat.subn(rep, s, count=1)
    if n != 1: print(f"ABORT [headshot {alt[:30]}]"); sys.exit(1)
log.append((f"headshots -> initials ({len(heads)})", len(heads)))
if len(heads) != 3: print(f"ABORT: expected 3 unsplash headshots, saw {len(heads)}"); sys.exit(1)


s = s.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!--\n  employer-event-detail.html — event detail page (Dallas Technology), rebuilt from the\n"
  "  live DOM of jobfairx.com/employer/job-fairs/texas/dallas/743231932652847104\n"
  "  (captured 24 Aug 2026) with interview-format messaging applied. The YouTube embed\n"
  "  is preserved. Testimonial quotes are verbatim and deliberately unedited.\n-->\n", 1)

open(OUT, "w", encoding="utf-8").write(s)
for l, n in log[-14:]: print(f"  ok  {l} ({n})")
print(f"chars {orig:,} -> {len(s):,}")
