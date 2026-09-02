#!/usr/bin/env python3
"""Build employer-home.html from the captured live DOM of jobfairx.com/employer.

Source of truth: assets/live-capture/employer-live-dom.html (rendered DOM, Aug 23 2026).
Every replacement asserts its anchor matches exactly once, so a drift in the
live page fails loudly instead of silently shipping the old copy.
"""
import re, sys, html

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/employer-live-dom.html"
OUT = f"{W}/employer-home.html"
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

# ───────────────────────────── 1. De-frameworkise ──────────────────────────
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "", count=170, regex=True)
sub("strip sveltekit body attr", ' data-sveltekit-preload-data="hover"', "")
sub("strip svelte comment markers", r"<!-- HTML_TAG_START --><!-- HTML_TAG_END -->", "", regex=True)
sub("strip origin-trial metas", r'<meta http-equiv="origin-trial"[^>]*>', "", count=2, regex=True)

# ───────────────────────────── 2. Localise assets ──────────────────────────
# Version the stylesheet URLs so a CSS change can never be masked by a stale browser/CDN cache.
CSS_V = "v=2"
sub("app css", './_app/immutable/assets/app.029f5d9e.css', f'assets/employer-home/app.css?{CSS_V}')
sub("page css", './_app/immutable/assets/6.2102846a.css', f'assets/employer-home/page.css?{CSS_V}')
sub("favicon", 'https://jobfairx.com/favicon.png', 'assets/employer-home/favicon.png')
sub("logo", '/jobfairx-logo.png', 'assets/employer-home/jobfairx-logo.png', count=2)
for nm in ["healthcare.d1574504.png","diversity.af0ced6e.png","veteran.4e121597.png",
           "tech.b663863c.png","entry-level.ac5531c3.png","home.d6a75ca2.jpg","recruiter.63204f89.jpg"]:
    sub(f"img {nm}", f'/_app/immutable/assets/{nm}', f'assets/employer-home/{nm}')
# Font Awesome is a pro CDN asset with an integrity hash; keep it (it is what the live page uses).

# ───────────────────────────── 3. Head / SEO ───────────────────────────────
sub("title", "<title>Virtual Hiring Event Platform for Employers | JobFairX\n</title>",
    "<title>Hiring Event Platform for Employers | JobFairX</title>")
DESC_OLD = "JobFairX is the virtual hiring event platform where pre-screened candidates book interviews with your team — 20–100+ interviews in a day, flat rate. Book a demo."
DESC_NEW = "Hiring events where pre-screened candidates book interviews with your team, in person, on video, or by phone. 20–100+ interviews in a day, flat rate. Register for an event."
sub("meta description x3", DESC_OLD, DESC_NEW, count=3)
sub("og/twitter title x2", 'content="Virtual Hiring Event Platform for Employers | JobFairX\n"',
    'content="Hiring Event Platform for Employers | JobFairX"', count=2)

# ───────────────────────────── 4. Hero ─────────────────────────────────────
# <h1> is the small uppercase eyebrow on the live page; the big headline is a div.
sub("H1 eyebrow", ">The Virtual Hiring Event Platform for Employers</h1>",
    ">The Hiring Event Platform for Employers</h1>")
sub("hero headline (mention 1 of 4)",
    r'>Hire faster with<br class="hidden lg:block"> interview-ready<br class="hidden lg:block"> candidates</div>',
    r'>Hire faster with<br class="hidden lg:block"> in&#8209;person and video<br class="hidden lg:block"> interviews</div>', regex=True)
# supporting line: carries "interview-ready candidates" down from the old headline. Phone is NOT here by decision.
sub("hero supporting copy",
    r"Join upcoming hiring events and connect with candidates across healthcare, technology, veterans, entry-level,\s*and diversity hiring\.</p>",
    "Interview-ready candidates, matched to your open roles. Join upcoming hiring events across healthcare, technology, veterans, entry-level, and diversity hiring.</p>", regex=True)

# ── 4b. Hero video: restore the embed the iframe-strip removed ───────────────
# The live hero's right column is this card with a YouTube embed inside; the
# capture dropped all iframes. Same video the live event pages embed.
sub("hero video embed",
    '<div class="relative rounded-2xl bg-white border border-slate-200 shadow-xl overflow-hidden max-w-2xl mx-auto"></div>',
    '<div class="relative rounded-2xl bg-white border border-slate-200 shadow-xl overflow-hidden max-w-2xl mx-auto" style="aspect-ratio:16/9">'
    '<iframe src="https://www.youtube.com/embed/QuRalPnpPLA?rel=0" title="See how JobFairX works" '
    'class="w-full h-full border-0 block" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
    'sandbox="allow-scripts allow-same-origin" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen loading="lazy"></iframe></div>')

# ───────────────────────────── 5. How It Works — Set up ────────────────────
# Scott 24 Aug (v2): step 1 stays EXACTLY the live site's version — heading,
# body, and the upcoming-events visual. Registration comes first; the format
# story moved to the Event day step below.

# ───────────────────────────── 6. How It Works — Event day ─────────────────
# Scott 24 Aug (v2): the format statement is this step's heading now, and the
# Interview Settings panel (section 6b) replaces the video-call mock here.
# The call mock and its Video chip are gone from the page.
sub("event-day H3 (mention 2 of 4)", ">Interview on JobFairX</h3>", ">Interview in person, video, or phone</h3>")
EV_OLD = ">Log in and interview candidates directly on JobFairX. No external links or downloads required.</p>"
EV_NEW = (">Meet candidates in person at your address, on JobFairX video with nothing to install, or by phone. "
          "Whatever you choose, the schedule, resumes, and notes are right there in the same place.</p>")
sub("event-day body (mention 3 of 4)", EV_OLD, EV_NEW)


# ─────────── 6b. Event-day visual: call mock -> Interview Settings panel ─────
# Scott 24 Aug (v2): the panel now illustrates the Event day step's format
# heading; step 1 keeps the live upcoming-events visual. Every field exists in
# the product (setup-flow-v3 / edit-post-v3). In-Person selected per priority.
i = s.find("Aisha Rahman")
st = s.rfind('<div class="w-full max-w-[560px]', 0, i)
depth = 0; j = st
for m in re.finditer(r"<div\b|</div>", s[st:]):
    depth += 1 if m.group(0) == "<div" else -1
    if depth == 0:
        j = st + m.end(); break
if st == -1 or j <= st:
    print("ABORT [step1 visual]: span not found"); sys.exit(1)

ICON_PIN   = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_VIDEO = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m22 8-6 4 6 4V8Z"/><rect width="14" height="12" x="2" y="6" rx="2" ry="2"/></svg>'
ICON_PHONE = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'

PANEL = (
 '<div class="w-full max-w-[560px] h-[420px] max-lg:h-auto max-lg:min-h-[280px] mx-auto overflow-hidden box-border bg-white border border-[#e8e6e3] rounded-[14px] shadow-[0_8px_32px_rgba(0,0,0,0.04)] flex flex-col">'
 '<div style="padding:18px 24px 14px;border-bottom:1px solid #f0eeea">'
 '<div class="text-[15px] font-semibold text-[#0f172a]">Interview settings</div>'
 '<div class="text-[12.5px] text-slate-500" style="margin-top:3px">Choose how your team interviews at this event.</div>'
 '</div>'
 '<div style="padding:18px 24px 0;flex:1;overflow:hidden">'
 '<div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:8px">Interview format <span class="text-[#dc2626]">*</span></div>'
 '<div style="display:inline-flex;border:1px solid #e2e8f0;border-radius:9999px;padding:4px;gap:4px;background:#fff">'
 '<span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:7px 16px;border-radius:9999px;background:#2563eb;color:#fff">' + ICON_PIN + 'In-Person</span>'
 '<span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:500;padding:7px 16px;border-radius:9999px;color:#334155">' + ICON_VIDEO + 'Video</span>'
 '<span style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:500;padding:7px 16px;border-radius:9999px;color:#334155">' + ICON_PHONE + 'Phone</span>'
 '</div>'
 '<div style="margin-top:18px">'
 '<div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:6px">Interview address <span class="text-[#dc2626]">*</span></div>'
 '<div style="display:flex;gap:8px">'
 '<div style="flex:2;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a">1201 Peachtree St NE</div>'
 '<div style="flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#94a3b8">Suite 300</div>'
 '</div></div>'
 '<div style="margin-top:14px">'
 '<div class="text-[12px] font-semibold text-slate-700" style="margin-bottom:6px">How to attend</div>'
 '<div style="border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a;line-height:1.5">Visitor parking is behind Building A. Check in with the receptionist on the 2nd floor.</div>'
 '</div>'
 '<div style="margin-top:16px;border-top:1px solid #f0eeea;padding-top:12px">'
 '<div class="text-[12px] font-semibold text-slate-700">Screening questions</div>'
 '<div style="display:flex;gap:8px;margin-top:8px;align-items:center">'
 '<div style="flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:9px 12px;font-size:13px;color:#0f172a">Do you have an active RN license in Texas?</div>'
 '<span style="font-size:12px;font-weight:600;color:#2563eb;white-space:nowrap">+ Add</span>'
 '</div></div>'
 '</div></div>'
)
removed = j - st
s = s[:st] + PANEL + s[j:]
log.append((f"event-day visual -> Interview Settings ({removed} chars out)", 1))


# ── 6b2. Set-up visual: live event list -> NEW calendar design (exact code) ──
# Scott 24 Aug: the launching calendar redesign (page-events.html) is the
# step-1 screenshot now. assets/live-capture/setup-cal-fragment.html is the
# EXACT markup+CSS lifted from the deployed page-events.html (rules scoped
# under #jfx-cal, tokens inlined from shared/base.css, hrefs stripped, rows
# verbatim: Dallas/Nashville/Norfolk Live + Chicago Starts soon). Desktop
# renders the table scaled to the frame; <=820px uses the design's own
# mobile card rules. Regenerate via the extraction script in git history.
CAL = open(f"{W}/assets/live-capture/setup-cal-fragment.html", encoding="utf-8").read()
i = s.find("Apr 17")
st = s.rfind('<div class="w-full max-w-[560px]', 0, i)
depth = 0; j = st
for m in re.finditer(r"<div\b|</div>", s[st:]):
    depth += 1 if m.group(0) == "<div" else -1
    if depth == 0:
        j = st + m.end(); break
if st == -1 or j <= st or i == -1:
    print("ABORT [setup calendar visual]: span not found"); sys.exit(1)
removed = j - st
s = s[:st] + CAL + s[j:]
log.append((f"set-up visual -> new calendar design ({removed} chars out, {len(CAL)} in)", 1))


# ── 6b3. Review & confirm visual: live table -> current app view (Scott) ─────
# Replicates Scott's screenshot of the live application (24 Aug): five columns
# incl. Requested time, Accept/Decline/Reschedule button group (app blue
# #0044b3), and the "Proposed · awaiting candidate" state with Cancel. Data
# verbatim from the screenshot. Scaled table on desktop; simple stack <=820px.
BTNS = ('<span class="jr-btns" style="display:inline-flex;border:1px solid #d5d9e0;border-radius:8px;overflow:hidden;white-space:nowrap;justify-self:start;background:#fff">'
 '<span style="background:#0044b3;color:#fff;padding:8px 14px;font-size:13px;font-weight:700">Accept</span>'
 '<span style="padding:8px 12px;font-size:13px;font-weight:600;color:#14161a;border-left:1px solid #d5d9e0">Decline</span>'
 '<span style="padding:8px 12px;font-size:13px;font-weight:600;color:#14161a;border-left:1px solid #d5d9e0">Reschedule</span></span>')
def _prop(t):
    return ('<span style="justify-self:start"><span style="font-size:13px;font-weight:700;color:#0044b3">Proposed &middot; awaiting candidate</span>'
     '&nbsp;&nbsp;<span style="font-size:12.5px;color:#565b66;text-decoration:underline">Cancel</span>'
     f'<span style="display:block;font-size:13px;color:#33322e;margin-top:3px">{t}</span></span>')
def _name(n):
    return (f'<span><b style="display:block;color:#14161a;font-weight:600;font-size:14.5px">{n}</b>'
     '<span style="font-size:12px"><span style="color:#0044b3;text-decoration:underline">View resume</span>'
     '&nbsp;&nbsp;<span style="color:#0044b3;text-decoration:underline">Message</span></span></span>')
def _cell(t, sz="14px"):
    return f'<span style="color:#33322e;font-size:{sz}">{t}</span>'
def _jr(name, job, locn, time, action, last=False):
    b = "" if last else "border-bottom:1px solid #f0eeea;"
    return (f'<div class="jr" style="padding:14px 0;{b}">'
     + _name(name) + _cell(job) + _cell(locn) + _cell(time, "13px") + action + '</div>')

REVIEW = (
 '<div id="jfx-rev" class="w-full max-w-[560px] h-[420px] max-lg:h-auto max-lg:min-h-[280px] mx-auto overflow-hidden box-border '
 'bg-white border border-[#e8e6e3] rounded-[14px] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" style="padding:16px 20px">'
 '<style>'
 '#jfx-rev .jfx-rev-scale{width:824px;transform:scale(.61);transform-origin:top left;margin-top:64px}'
 '#jfx-rev .jr,#jfx-rev .jh{display:grid;grid-template-columns:150px 120px 95px 150px 245px;column-gap:16px;align-items:center}'
 '#jfx-rev .jh{padding:10px 0;border-bottom:1px solid #e6e3dd;font-size:12px;color:#565b66}'
 '@media (max-width:820px){'
 '#jfx-rev .jfx-rev-scale{width:auto;transform:none;margin:0}'
 '#jfx-rev .jh{display:none}'
 '#jfx-rev .jr{grid-template-columns:minmax(0,1fr);row-gap:4px;padding:12px 0}'
 '#jfx-rev .jr-btns{margin-top:4px}'
 '}'
 '</style>'
 '<div class="jfx-rev-scale">'
 '<div style="display:flex;align-items:center;gap:9px;margin-bottom:8px">'
 '<span style="color:#565b66;font-size:13px">&#8963;</span>'
 '<span style="width:18px;height:18px;border-radius:50%;background:#a3161d;color:#fff;font-size:12px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;flex:none">!</span>'
 '<span style="font-size:17px;font-weight:700;color:#14161a">Candidates awaiting your response (4)</span></div>'
 '<div class="jh"><span>Name</span><span>Desired job</span><span>Desired location</span><span>Requested time</span><span>Action</span></div>'
 + _jr("Tamara Williams", "Registered Nurse", "Dallas, TX", "9:00 AM - 9:30 AM PDT", BTNS)
 + _jr("Marcus Johnson", "Web Developer", "Remote", "9:30 AM - 10:00 AM PDT", BTNS)
 + _jr("Priya Patel", "Frontend Developer", "Remote", "2:00 PM - 2:30 PM PDT", _prop("2:00 PM - 2:30 PM PDT"))
 + _jr("Jordan Lee", "Registered Nurse", "Dallas, TX", "3:00 PM - 3:30 PM PDT", _prop("3:00 PM - 3:30 PM PDT"), last=True)
 + '</div></div>')

i = s.find("Candidates awaiting your response")
st = s.rfind('<div class="w-full max-w-[560px]', 0, i)
depth = 0; j = st
for m in re.finditer(r"<div\b|</div>", s[st:]):
    depth += 1 if m.group(0) == "<div" else -1
    if depth == 0:
        j = st + m.end(); break
if st == -1 or j <= st or i == -1:
    print("ABORT [review visual]: span not found"); sys.exit(1)
removed = j - st
s = s[:st] + REVIEW + s[j:]
log.append((f"review visual -> current app table ({removed} chars out, {len(REVIEW)} in)", 1))



# ── 6c. Sticky nav (#3) ──────────────────────────────────────────────────────
sub("sticky nav",
    '<header class="w-full bg-white/95 backdrop-blur-md border-b border-slate-200 transition-all duration-300">',
    '<header class="w-full bg-white/95 backdrop-blur-md border-b border-slate-200 transition-all duration-300" style="position:sticky;top:0;z-index:60">')

# ── 6d. Mechanic rewrite in Review & confirm (#5) ────────────────────────────
# Scott 24 Aug: the ENTIRE Review & confirm step stays exactly as the live
# site has it today — heading, body, and table mock. The earlier H3
# replacement and the added Auto-accept chip are removed; the capture flows
# through untouched so the developer sees production's own step verbatim.

# ── 6e. Step 4 -> Analytics (#4a) ────────────────────────────────────────────
# Scott's copy, 24 Aug (v3 — "applicants" -> "candidates" per the vocab law).
sub("step-4 body",
    ">Candidate feedback, resumes, notes, and messages are automatically organized during the event, allowing your\n          team to review candidates and take next steps.</p>",
    ">Gain complete visibility into your hiring metrics with a comprehensive event report that consolidates "
    "your team&rsquo;s input. Track which team member interviewed each candidate, review yes, no, or maybe outcomes, "
    "and identify no-shows. You can seamlessly advance your pipeline by messaging candidates or scheduling next-round interviews directly from the dashboard.</p>")
i = s.find("Your event report is ready")
v = s.find('class="w-full max-w-[560px]', i)
v = s.rfind("<div", 0, v + 10)
d = 0; j = v
for m in re.finditer(r"<div\b|</div>", s[v:]):
    d += 1 if m.group(0) == "<div" else -1
    if d == 0:
        j = v + m.end(); break
# App-faithful mock (Scott, 24 Aug): one week filtered, Day granularity, both
# default metrics as two lines in the app's exact colors (#0044b3 / #b8730f),
# all seven dates labeled, stat row = the app's four cards. Daily values sum
# to the stat row (22 scheduled, 19 completed, 3 missed); attendance shown as
# 86%, deliberately consistent with the 84% show-rate claim (the prototype's
# 66% demo figure would undercut it).
ANALYTICS = (
 '<div class="w-full max-w-[560px] h-[420px] max-lg:h-auto max-lg:min-h-[280px] mx-auto overflow-hidden box-border bg-white border border-[#e8e6e3] rounded-[14px] p-5 shadow-[0_18px_48px_-12px_rgba(0,0,0,0.18),0_4px_12px_rgba(0,0,0,0.05)] flex flex-col">'
 '<div class="flex items-center justify-between" style="flex-wrap:wrap;gap:6px;margin-bottom:8px">'
 '<span class="text-[14px] font-bold text-[#1a1a1a] tracking-[-0.01em]">Interviews over time</span>'
 '<span class="text-[11px] text-slate-500 border border-slate-200 rounded-md" style="padding:3px 8px;white-space:nowrap">05/11/2026 &ndash; 05/17/2026 &#9662;</span></div>'
 '<div class="flex items-center justify-between" style="flex-wrap:wrap;gap:6px;margin-bottom:6px">'
 '<span style="display:inline-flex;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;font-size:10.5px;white-space:nowrap">'
 '<span style="padding:3px 9px;color:#475569">Event day</span>'
 '<span style="padding:3px 9px;background:#0044b3;color:#fff;font-weight:600;border-left:1px solid #e2e8f0">Day</span>'
 '<span style="padding:3px 9px;color:#475569;border-left:1px solid #e2e8f0">Week</span>'
 '<span style="padding:3px 9px;color:#475569;border-left:1px solid #e2e8f0">Month</span></span>'
 '<span style="font-size:10.5px;color:#475569;display:inline-flex;gap:11px;align-items:center;white-space:nowrap">'
 '<span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#0044b3;margin-right:5px"></span>Interviews scheduled</span>'
 '<span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#b8730f;margin-right:5px"></span>Interviews completed</span></span></div>'
 '<div style="flex:1;min-height:0;display:flex;align-items:center">'
 '<svg viewBox="0 0 520 170" style="width:100%;height:100%" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
 '<text x="18" y="16" font-size="9" fill="#94a3b8" text-anchor="end">6</text>'
 '<text x="18" y="53" font-size="9" fill="#94a3b8" text-anchor="end">4</text>'
 '<text x="18" y="90" font-size="9" fill="#94a3b8" text-anchor="end">2</text>'
 '<text x="18" y="127" font-size="9" fill="#94a3b8" text-anchor="end">0</text>'
 '<line x1="26" y1="13" x2="516" y2="13" stroke="#eef2f7"/><line x1="26" y1="50" x2="516" y2="50" stroke="#eef2f7"/><line x1="26" y1="87" x2="516" y2="87" stroke="#eef2f7"/>'
 '<line x1="26" y1="124" x2="516" y2="124" stroke="#e2e8f0" stroke-width="2"/>'
 '<polyline points="40,87 112,87 184,68 256,68 328,50 400,68 472,87" fill="none" stroke="#b8730f" stroke-width="2.5"/>'
 '<g fill="#b8730f"><circle cx="40" cy="87" r="3.5"/><circle cx="112" cy="87" r="3.5"/><circle cx="184" cy="68" r="3.5"/><circle cx="256" cy="68" r="3.5"/><circle cx="328" cy="50" r="3.5"/><circle cx="400" cy="68" r="3.5"/><circle cx="472" cy="87" r="3.5"/></g>'
 '<polyline points="40,87 112,68 184,50 256,68 328,31 400,68 472,87" fill="none" stroke="#0044b3" stroke-width="2.5"/>'
 '<g fill="#0044b3"><circle cx="40" cy="87" r="3.5"/><circle cx="112" cy="68" r="3.5"/><circle cx="184" cy="50" r="3.5"/><circle cx="256" cy="68" r="3.5"/><circle cx="328" cy="31" r="3.5"/><circle cx="400" cy="68" r="3.5"/><circle cx="472" cy="87" r="3.5"/></g>'
 '<text x="40" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 11</text>'
 '<text x="112" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 12</text>'
 '<text x="184" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 13</text>'
 '<text x="256" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 14</text>'
 '<text x="328" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 15</text>'
 '<text x="400" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 16</text>'
 '<text x="472" y="142" font-size="9" fill="#64748b" text-anchor="middle">May 17</text></svg></div>'
 '<div class="text-center border-t border-[#f0eeea]" style="display:grid;grid-template-columns:repeat(4,1fr);margin-top:8px;padding-top:12px">'
 '<div><b class="block text-[20px] text-[#1a1a1a]" style="font-variant-numeric:tabular-nums">22</b><span style="font-size:10.5px;color:#64748b">Interviews scheduled</span></div>'
 '<div><b class="block text-[20px] text-[#1a1a1a]" style="font-variant-numeric:tabular-nums">86%</b><span style="font-size:10.5px;color:#64748b">Attendance rate</span></div>'
 '<div><b class="block text-[20px] text-[#1a1a1a]" style="font-variant-numeric:tabular-nums">3</b><span style="font-size:10.5px;color:#64748b">Missed interviews</span></div>'
 '<div><b class="block text-[20px]" style="color:#186a3b;font-variant-numeric:tabular-nums">11</b><span style="font-size:10.5px;color:#64748b">Marked yes</span></div>'
 '</div></div>')
removed = j - v
s = s[:v] + ANALYTICS + s[j:]
log.append((f"step-4 visual -> analytics mock ({removed} chars out)", 1))
# H3 swap AFTER the block above — the analytics locator finds the old heading.
sub("step-4 H3 (Scott's copy)",
    ">Your event report is ready the moment the event ends</h3>",
    ">Post-Event Reporting</h3>")


# ── 6f. Built-in Tools section REMOVED from the homepage (Scott, 24 Aug) ─────
# The live scroll-pinned messaging section is cut and nothing replaces it: the
# tools story lives on the event page only (its localized bento is authored in
# build-event-detail.py). How It Works and All Packages Include carry the
# capability mentions on this page.
_msec_i = s.find("Candidate Messaging")
_msec_a = s.rfind("<section", 0, _msec_i)
_msec_b = s.find("</section>", _msec_i) + len("</section>")
if _msec_a == -1 or _msec_b <= _msec_a:
    print("ABORT [tools removal]: messaging section span not found"); sys.exit(1)
s = s[:_msec_a] + s[_msec_b:]
log.append((f"messaging section removed ({_msec_b-_msec_a} chars out)", 1))


# ── 6g. CTA bands — REMOVED (Scott, 24 Aug: take the two dark bands off the
# homepage). The insertion step is deleted rather than commented so the build
# log no longer mentions bands; restore from git history if ever wanted back.


# ───────────────────────────── 7. Pricing: format bullet + includes item ────
# Mirrors the shipped employer-pricing.html treatment (preview commits
# 9ef298f/3a378bf) and the event page: each tier card gains an "In-person or
# video interviews" bullet after the scheduled-interviews line, and All
# Packages Include gains a standalone "In-person, video, or phone interviews"
# item after Auto-accept. The unlimited-interviews bullet stays as captured —
# the format has its own line now (this remains format mention 4 of 4).
CARD_FMT_LI = ('<li class="flex items-start gap-2.5 text-slate-700"><div class="w-5 h-5 rounded-full bg-blue-100 flex '
 'items-center justify-center flex-shrink-0 mt-0.5"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" '
 'class="text-blue-600"><path d="M20 6 9 17l-5-5"></path></svg></div> '
 '<span class="font-medium leading-snug text-[16px]">In-person or video interviews</span> </li>')
for _cnt in ["20+", "60+", "100+"]:
    _anchor = f">{_cnt} scheduled candidate interviews</span> </li>"
    sub(f"card format bullet ({_cnt})", _anchor, _anchor + CARD_FMT_LI)
AUTOACCEPT = '<span class="text-slate-600 text-sm leading-relaxed">Auto-accept interview requests or review each one individually</span> </div>'
ALLPKG_FMT = ('<div class="flex items-start gap-3"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" '
 'class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"><path d="M20 6 9 17l-5-5"></path></svg> '
 '<span class="text-slate-600 text-sm leading-relaxed">In-person, video, or phone interviews</span> </div>')
sub("all-packages format item", AUTOACCEPT, AUTOACCEPT + ALLPKG_FMT)

# ───────────────────────────── 8. Final CTA + footer ───────────────────────
sub("final CTA sub", ">Join upcoming virtual hiring events and meet candidates matched to your open jobs.</p>",
    ">Join upcoming hiring events and meet candidates matched to your open jobs.</p>")
sub("footer employers link", r"(</span>\s*)Virtual Hiring Event Platform</a>", r"\1Hiring Event Platform</a>", regex=True)

# ───────────────────────────── 8b. Font paths in the localised CSS ────────
# app.css ships font urls as ../../../fonts/Inter/ (domain-root-relative on the live
# SvelteKit build). From assets/employer-home/ that is one level too many.
_css_p = f"{W}/assets/employer-home/app.css"
_css = open(_css_p, encoding="utf-8").read()
_css2 = _css.replace("url(../../../fonts/Inter/", "url(../../fonts/Inter/")
if _css2 != _css:
    open(_css_p, "w", encoding="utf-8").write(_css2); log.append(("app.css font paths -> ../../fonts", _css.count("url(../../../fonts/Inter/")))

# ── 8d. Review & confirm visual: real prototype screenshot (Scott, 25 Aug) ───
# Scott: the DOM mock had too much white space and too-small text. Replaced
# with captures of the actual event-lobby prototype (lobby-v3-healthcare,
# ?method=video, default pre-event state, Not yet interviewed tab). v2 (Scott,
# 25 Aug brief): ONE unified window, 2 awaiting rows with Accept/Decline/
# Reschedule + divider + "Upcoming interviews (2)" (retitled from "Candidates
# with upcoming interviews", location column hidden there per the brief), dev
# chrome removed, capture.py neutralisation applied (minus the Tamar rule so
# Tamara Williams, the fictional name used across this page, stays). Mobile
# variant hides the Desired job / Desired location columns so the buttons fit.
# Files: assets/product/review-confirm.png (836x1269 css @2x),
#        assets/product/review-confirm-mobile.png (584x1229 css @2x).
if s.count('<div id="jfx-rev"') != 1:
    print("ABORT [review visual]: jfx-rev anchor not unique"); sys.exit(1)
_ra = s.find('<div id="jfx-rev"')
_rd = 0; _rb = _ra
for _m in re.finditer(r"<div\b|</div>", s[_ra:]):
    _rd += 1 if _m.group(0) == "<div" else -1
    if _rd == 0:
        _rb = _ra + _m.end(); break
if _ra == -1 or _rb <= _ra:
    print("ABORT [review visual]: span walk failed"); sys.exit(1)
_ALT_D = ("One application window from the event lobby. Candidates awaiting your response lists two "
 "candidates with their requested times and Accept, Decline, and Reschedule buttons; below a "
 "divider, Upcoming interviews lists two candidates with confirmed times and Reschedule and Cancel options.")
_ALT_M = ("One application window from the event lobby: two candidates awaiting your response with "
 "Accept, Decline, and Reschedule buttons, and two confirmed upcoming interviews.")
_RIMG = ('<div class="w-full max-w-[560px] mx-auto">'
 f'<img src="assets/product/review-confirm.png?v=2" alt="{_ALT_D}" width="824" height="609" '
 'class="hidden lg:block w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy">'
 f'<img src="assets/product/review-confirm-mobile.png?v=2" alt="{_ALT_M}" width="584" height="651" '
 'class="lg:hidden w-full h-auto rounded-[14px] border border-[#e8e6e3] shadow-[0_8px_32px_rgba(0,0,0,0.04)]" loading="lazy">'
 '</div>')
s = s[:_ra] + _RIMG + s[_rb:]
log.append((f"review visual -> prototype screenshots ({_rb-_ra} chars out, {len(_RIMG)} in)", 1))

# ── 8e. All Packages Include: 9 -> 8 items (Scott, 25 Aug) ───────────────────
# The format item made the list nine and orphaned one item in the grid. Scott
# wanted eight; the dashboard item goes, same call as the pricing page (the
# post-event report covers its claim, auto-accept and follow-ups imply it),
# which also makes this list identical to the pricing page's eight.
_dash = '<span class="text-slate-600 text-sm leading-relaxed">Employer dashboard to manage events, dispositions, notes, and analytics</span>'
if s.count(_dash) != 1:
    print("ABORT [includes drop]: dashboard span not unique"); sys.exit(1)
_di2 = s.find(_dash)
_da2 = s.rfind('<div class="flex items-start gap-3">', 0, _di2)
_db2 = s.find('</div>', _di2) + len('</div>')
if not (0 < _da2 < _di2 < _db2):
    print("ABORT [includes drop]: item bounds not found"); sys.exit(1)
s = s[:_da2] + s[_db2:]
log.append((f"includes: drop dashboard item ({_db2-_da2} chars)", 1))

# ── 8c. The Difference section: UNTOUCHED — matches the live site verbatim. ──
# A cost-model redesign (option C) shipped here 24-25 Aug and Scott reverted it
# 25 Aug ("update it back to what the live site has"). The researched variants
# live in COST-PER-HIRE-CLAIM.md and the session memory if they return.

# ── 8f. Review-only view toggle (Scott, 25 Aug): desktop <-> mobile design ──
# A dedicated mobile design exists at employer-home-mobile.html (built by
# build-employer-home-mobile.py FROM this page's output). The floating pill
# lets the developer flip between both. Prototype-only, remove for production.
TOGGLE = ('<div id="view-toggle" title="Prototype view toggle, remove before production" '
 'style="position:fixed;left:16px;bottom:16px;z-index:80;background:#0f172a;border-radius:999px;'
 'padding:6px 8px;display:flex;gap:4px;align-items:center;box-shadow:0 4px 14px rgba(0,0,0,.25);'
 'font-size:12.5px;font-weight:600;font-family:inherit">'
 '<span style="color:#fff;background:#2563eb;border-radius:999px;padding:5px 12px">Desktop</span>'
 '<a href="mobile-view.html?page=employer-home-mobile.html" '
 'style="color:#cbd5e1;padding:5px 12px;text-decoration:none">Mobile</a></div>')
sub("view toggle", "</body>", TOGGLE + "\n</body>")

# ── 8g. Reschedule / follow-ups section (Scott, 26 Aug) ──────────────────────
# Replaces the live site's scroll-pinned "Built-in Tools / Candidate Messaging
# and Interview Scheduling" block, which section 6f removed from this page.
# Scott chose this layout ("Option A") from rendered mocks and then cut the
# supporting paragraph, because the three points below already say it.
#
# HEADLINE: no <br>. An explicit break here produced a phantom line box and the
# heading rendered on THREE lines at every size down to 32px. Left to wrap
# naturally at lg:text-[40px] it breaks after "and", which is the break Scott
# marked up. Verified by counting client rects, not by eye. Do not re-add a <br>.
#
# BACKGROUND: brand navy (bg-brand-dark, #00245b). Scott chose this from a
# three-way comparison on 26 Aug. The reason is structural, not decorative:
# from this section down the page was white, white, white, white (Reschedule,
# Hiring Teams, Pricing, closing CTA), so the alternation flatlined for the
# whole bottom half. This is the only dark band in the body; the footer is the
# only other dark surface. A slate-50 tint was tried and rejected: How It Works
# directly above is also slate-50, so it erased the boundary above while fixing
# the one below. Dark separates on both sides and the pale poster reads better
# against it. No border needed.
#
# JS: this adds the page's ONLY script (7 lines) so the poster can hand off to
# the real 1:04 file. EMPLOYER-HOME-DEV-NOTES.md is updated accordingly, and it
# is a one-line swap to the YouTube embed once the tutorial is uploaded.
TUT_DIR = "developer-tutorial-reschedule"
TUT_POSTER = f"{TUT_DIR}/thumbnail.jpg"
TUT_MP4 = f"{TUT_DIR}/jobfairx-01-reschedule-candidate-1080p.mp4"

def _tut_item(title, body):
    return (
        '<li class="flex items-start gap-3">'
        '<span class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0" style="margin-top:2px;">'
        '<svg class="w-3 h-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
        'stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg>'
        '</span><span>'
        f'<span class="block text-[17px] font-semibold text-white leading-snug">{title}</span>'
        f'<span class="block text-base text-slate-300 leading-relaxed">{body}</span>'
        '</span></li>'
    )

TUT_ITEMS = "".join([
    _tut_item("Choose the interview format", "Video, in person, or phone."),
    _tut_item("Propose multiple times", "Give candidates clear options to select from."),
    _tut_item("Keep everyone prepared", "Confirmation messages, reminders, and guidance."),
])

TUT_STYLE = (
 '<style>'
 '.jfx-tut{position:relative;border-radius:16px;overflow:hidden;'
 'box-shadow:0 18px 48px -12px rgba(15,23,42,.28),0 4px 12px rgba(0,0,0,.06)}'
 '.jfx-tut img,.jfx-tut video{display:block;width:100%;height:auto}'
 '.jfx-tut-scrim{position:absolute;left:0;right:0;bottom:0;height:26%;pointer-events:none;'
 'background:linear-gradient(to top,rgba(10,20,40,.80) 0%,rgba(10,20,40,.34) 55%,rgba(10,20,40,0) 100%)}'
 '.jfx-tut-play{position:absolute;left:67%;top:47%;transform:translate(-50%,-50%);width:74px;height:74px;'
 'border-radius:999px;background:#fff;border:0;cursor:pointer;display:flex;align-items:center;'
 'justify-content:center;box-shadow:0 8px 26px rgba(15,23,42,.3)}'
 '.jfx-tut-play:hover{background:#f1f5f9}'
 '.jfx-tut-play:focus-visible{outline:3px solid #2563eb;outline-offset:3px}'
 '.jfx-tut-bar{position:absolute;left:22px;right:22px;bottom:20px;pointer-events:none}'
 '.jfx-tut-track{height:4px;border-radius:999px;background:rgba(255,255,255,.35);overflow:hidden}'
 '.jfx-tut-fill{height:100%;width:9%;background:#fff;border-radius:999px}'
 '.jfx-tut-time{color:#fff;font-size:13px;font-weight:600;margin-bottom:8px;letter-spacing:.02em}'
 '@media (max-width:1023px){.jfx-tut-play{left:50%}}'
 '</style>'
)

TUT_SECTION = (
 '<section class="bg-brand-dark py-12 lg:py-[90px]">'
 '<div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1180px]">'
 '<div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">'
 '<div>'
 '<p class="text-xs lg:text-sm font-bold uppercase tracking-[0.12em] text-blue-400 mb-5">Unlimited interviews with every candidate</p>'
 '<h2 class="text-[30px] lg:text-[40px] font-semibold text-white tracking-[-0.02em] leading-tight mb-8">'
 'Reschedule interviews and schedule follow-ups anytime</h2>'
 f'<ul class="list-none pl-0 space-y-5">{TUT_ITEMS}</ul>'
 '</div>'
 '<div class="jfx-tut" id="jfx-tut">'
 f'<img src="{TUT_POSTER}" width="2560" height="1440" loading="lazy" '
 'alt="Employer tutorial: reschedule an interview. Propose a new time, change the format, or set up a '
 'follow-up. The JobFairX reschedule form is shown with Video, In-Person and Phone format options, an '
 'interview address, how-to-attend notes and a message to the candidate.">'
 '<div class="jfx-tut-scrim"></div>'
 '<button type="button" class="jfx-tut-play" id="jfx-tut-play" '
 'aria-label="Play the reschedule tutorial, 1 minute 4 seconds">'
 '<svg width="26" height="26" viewBox="0 0 24 24" fill="#2563eb" xmlns="http://www.w3.org/2000/svg" '
 'style="margin-left:4px" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></button>'
 '<div class="jfx-tut-bar"><div class="jfx-tut-time">1:04</div>'
 '<div class="jfx-tut-track"><div class="jfx-tut-fill"></div></div></div>'
 '</div>'
 '</div></div></section> '
)

TUT_SCRIPT = (
 '<script>(function(){var w=document.getElementById("jfx-tut");if(!w)return;'
 'document.getElementById("jfx-tut-play").addEventListener("click",function(){'
 'w.innerHTML=\'<video controls autoplay playsinline poster="POSTER" '
 'style="display:block;width:100%;height:auto"><source src="MP4" type="video/mp4"></video>\';});})();</script>'
).replace("POSTER", TUT_POSTER).replace("MP4", TUT_MP4)

RESULTS_ANCHOR = ('<section class="bg-white py-12 lg:py-[90px]"><div class="container mx-auto px-4 sm:px-6 lg:px-8 '
                  'max-w-[1180px]"><div class="text-center"><div class="inline-block text-sm font-bold text-brand '
                  'uppercase tracking-[0.12em] mb-3.5">Hiring Event Results</div>')
sub("8g reschedule section", RESULTS_ANCHOR, TUT_SECTION + RESULTS_ANCHOR)
sub("8g reschedule styles", "</head>", TUT_STYLE + "</head>")
sub("8g reschedule script", "</body>", TUT_SCRIPT + "\n</body>")

# ── 8h. Hero headline + subcopy (Scott, 26 Aug, from his marked-up screenshot) ──
# Replaces the copy set by the earlier hero step. Verbatim from Scott:
#   headline  "Meet interview-ready candidates at hiring events built to hire."
#   subcopy   "Post the roles you need to fill, meet candidates matched to your
#              openings, and interview them in person, by video, or by phone."
# Line breaks match the three lines in his screenshot; they are lg-only, so the
# phone wraps naturally.
#
# NOTE for the record: this changes the documented four-mention interview-format
# ladder. The hero previously said "in-person and video" with phone deliberately
# held back until the Event day step. Scott's copy puts all three formats in the
# hero. Prose register is correct (prepositions, not the bare pill labels).
sub("8h hero headline",
    '>Hire faster with<br class="hidden lg:block"> in&#8209;person and video<br class="hidden lg:block"> interviews</div>',
    '>Meet interview&#8209;ready<br class="hidden lg:block"> candidates at hiring<br class="hidden lg:block"> events built to hire.</div>')

sub("8h hero subcopy",
    "Interview-ready candidates, matched to your open roles. Join upcoming hiring events across healthcare, technology, veterans, entry-level, and diversity hiring.</p>",
    "Post the roles you need to fill, meet candidates matched to your openings, and interview them in person, by video, or by phone.</p>")

# ───────────────────────────── 9. Provenance comment ───────────────────────
s = s.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!--\n  employer-home.html — JobFairX employer homepage, rebuilt from the live DOM of\n"
  "  https://jobfairx.com/employer (captured 23 Aug 2026) with the interview-format\n"
  "  messaging applied. Static file: framework hydration attrs and tracking scripts\n"
  "  removed; stylesheets and images localised under assets/employer-home/.\n-->\n", 1)

open(OUT, "w", encoding="utf-8").write(s)
print(f"{'label':<40} matches")
for l, n in log: print(f"  {l:<38} {n}")
print(f"\nchars {orig_len:,} -> {len(s):,}  ({len(s)-orig_len:+,})")
