#!/usr/bin/env python3
"""Build employer-faq.html from the captured live FAQ page.

Source of truth: assets/live-capture/faq-live-dom.html — the server-rendered
HTML of https://jobfairx.com/employer/hiring-event-faq, captured 24 Aug 2026
(scripts stripped at capture). Same contract as build-employer-pricing.py:
every replacement asserts its match count and aborts loudly on drift.

The live accordion ships only the question buttons server-side; the answers
hydrate client-side. Section 4 injects the answer panels using the live page's
own answer texts (read from its FAQ JSON-LD) and the exact expanded-item markup
captured from the hydrated live page (border-blue-200 bg-blue-50/40 container,
rotated chevron, px-5/pb-4 panel with text-sm slate-600 copy). Items toggle
independently, as on live.

Scott's updates, 24 Aug (audit approved in chat):
  - no "virtual" anywhere in copy (titles, metas, intro, Q1/Q2 questions,
    footer links); the two virtual.jobfairx.com Sign In URLs are the real
    login domain and stay
  - Q1 answer covers in-person / video / phone instead of video-only
  - new question 2: "Where do interviews take place?"
A floating, toggleable DEV NOTE (bottom-right pill, clearly marked
prototype-only) lists every delta so the developer applying this to production
does not have to diff the page. Remove it before production.
"""
import re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/faq-live-dom.html"
OUT = f"{W}/employer-faq.html"
s = open(SRC, encoding="utf-8").read()
orig = len(s)
log = []

def sub(label, old, new, count=1, regex=False, flags=0):
    global s
    if regex:
        s2, n = re.subn(old, new, s, flags=flags)
    else:
        n = s.count(old); s2 = s.replace(old, new) if n == count else s
    if n != count or count == 0:
        print(f"ABORT [{label}]: {n} matches, expected {count}"); sys.exit(1)
    s = s2; log.append((label, n))

# ── 1. De-frameworkise ───────────────────────────────────────────────────────
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "",
    count=len(re.findall(r'data-svelte-h', s)), regex=True)
sub("strip sveltekit body attr", ' data-sveltekit-preload-data="hover"', "")
sub("strip svelte comment markers", r'<!--\s*HTML_TAG_START\s*-->\s*<!--\s*HTML_TAG_END\s*-->', "",
    count=len(re.findall(r'HTML_TAG_START', s)), regex=True)

# ── 2. Localise assets (shared with the other employer clones) ───────────────
sub("app css",  '../_app/immutable/assets/app.029f5d9e.css', 'assets/employer-home/app.css?v=2')
sub("page css", '../_app/immutable/assets/6.2102846a.css', 'assets/employer-home/page.css?v=2')
sub("favicon", 'href="../favicon.png"', 'href="assets/employer-home/favicon.png"')
n = s.count('/jobfairx-logo.png')
sub("logo", '/jobfairx-logo.png', 'assets/employer-home/jobfairx-logo.png', count=n)

# ── 3. No "virtual" anywhere in copy ─────────────────────────────────────────
sub("title / og / twitter titles",
    "Virtual Hiring Event FAQ for Employers | JobFairX",
    "Hiring Event FAQ for Employers | JobFairX", count=3)
sub("meta / og / twitter descriptions",
    "Get answers to common questions about JobFairX virtual hiring events.",
    "Get answers to common questions about JobFairX hiring events.", count=3)
sub("intro line", "Everything you need to know about our virtual hiring events.",
    "Everything you need to know about our hiring events.")
sub("Q1 question", "How do JobFairX virtual job fairs work?",
    "How do JobFairX hiring events work?")
sub("Q2 question", "What types of targeted virtual job fairs do you host?",
    "What types of targeted hiring events do you host?")
sub("footer employers link", "Virtual Hiring Event Platform</a>", "Hiring Event Platform</a>")
sub("footer seekers link", "Virtual Job Fair Calendar</a>", "Job Fair Calendar</a>")
n_virtual = len(re.findall(r'virtual', s, flags=re.I))
if n_virtual != 2:
    print(f"ABORT [virtual sweep]: {n_virtual} remain, expected 2 (login URLs only)"); sys.exit(1)
log.append(("virtual sweep: only the 2 login URLs remain", 2))

# ── 4. Inject the answer panels (live texts; Q1 updated per the audit) ───────
ANSWERS = [
 ("How do JobFairX hiring events work?",
  "Employers post their open jobs and candidates request interviews through the platform. "
  "You review candidate profiles, confirm interviews before the event begins, and interview "
  "candidates in person at your address, on JobFairX video, or by phone. Video interviews run "
  "directly inside JobFairX, no Zoom, no downloads, no external software required."),
 ("What types of targeted hiring events do you host?",
  "JobFairX hosts targeted hiring events designed to connect employers with specific candidate "
  "audiences, including Technology, Healthcare, Entry-level, Diversity, and Veteran hiring events. "
  "Browse upcoming events on our employer calendar to find the right fit for your open roles."),
 ("Are candidates local to the city where the event is held?",
  "Yes, candidates are verified to be within approximately 20 miles of the event city, so "
  "you're connecting with local, relevant talent."),
 ("How are candidates sourced?",
  "JobFairX maintains a database of over 3+ million job seekers actively looking for new "
  "opportunities. Candidates are sourced and continually added through targeted digital marketing, "
  "social media advertising, job distribution across major platforms, email campaigns, and organic search."),
 ("How does candidate matching and interviewing work?",
  "Once you post your open jobs, candidate matching activates immediately and you will start "
  "receiving interview requests within a few hours. Job seekers whose background and interests "
  "align with your roles are invited to request interviews. You'll receive a notification for each "
  "request and a summary email every morning at 9:00 AM. You can review candidate résumés before "
  "accepting or declining. You can also enable automatic interview scheduling to accept requests "
  "automatically and save time."),
 ("How are candidates prepared for interviews?",
  "Candidates receive pre-event preparation materials, including interview tips, technical "
  "requirements, and platform tutorials, along with guidance on presenting themselves "
  "professionally. They also receive automated emails and SMS leading up to their scheduled "
  "interview to ensure high attendance rates."),
 ("How many interviews can I expect?",
  "It depends on your plan. Starter employers (1 job per event) average around 20 interviews. "
  "Growth employers (up to 3 jobs) average around 60. Pro employers (up to 6 jobs) typically see "
  "100+. <a href=\"/employer/hiring-event-pricing\" class=\"text-blue-600 hover:text-blue-500 underline\">View packages</a>"),
 ("What happens after the hiring event?",
  "You receive a post-event report with recruiter notes, interview records, and résumés. Your "
  "access doesn't expire, you can continue scheduling follow-up interviews and communicating with "
  "candidates through the platform for as long as you need."),
 ("How do I register, and when should I sign up?",
  "Visit the JobFairX employer calendar, select an upcoming event, and reserve your spot. We "
  "recommend registering at least one week in advance, so candidate matching can begin, and "
  "interview requests can start coming in."),
]

def panel(text):
    return ('<div class="px-5 lg:px-6 pb-4 lg:pb-5" hidden>'
            f'<p class="text-sm text-slate-600 leading-relaxed">{text}</p></div>')

for q, a in ANSWERS:
    pat = (r'(<span class="text-base lg:font-semibold text-left">' + re.escape(q)
           + r'</span>.*?</button>)\s*</div>')
    sub(f"answer panel: {q[:34]}", pat, r'\1 ' + panel(a) + '</div>',
        regex=True, flags=re.S)

# ── 5. New question 2: Where do interviews take place? ───────────────────────
NEW_Q = "Where do interviews take place?"
NEW_A = ("You choose. When you set up your jobs, you select your interview location: in person at "
         "your address, on JobFairX video with nothing to install, or by phone. It never changes the price.")
ITEM = ('<div class="flex flex-col rounded-xl border w-full transition-all duration-200 '
        'border-slate-200 bg-white hover:border-slate-300">'
        '<button class="flex lg:items-center space-x-5 justify-between cursor-pointer w-full py-4 px-5 lg:px-6 lg:py-5">'
        f'<span class="text-base lg:font-semibold text-left">{NEW_Q}</span> '
        '<svg class="h-2 lg:h-auto flex-shrink-0 transform transition-all duration-300 ease-in-out mt-1" '
        'width="12" height="8" viewBox="0 0 21 13" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M3.33403 0.296875L10.9903 7.95312L18.6465 0.296875L20.9903 2.64062L10.9903 12.6406L0.990278 2.64062L3.33403 0.296875Z" fill="#6B7280"></path></svg>'
        '</button> ' + panel(NEW_A) + '</div>')
q1_end = s.find('</div>', s.find('How do JobFairX hiring events work?'))  # panel close
q1_end = s.find('</div>', q1_end + 1) + len('</div>')                     # item close
i2 = s.find('What types of targeted hiring events do you host?')
if not (0 < q1_end <= i2):
    print("ABORT [new question]: insertion point after Q1 not found before Q2"); sys.exit(1)
s = s[:q1_end] + ' ' + ITEM + s[q1_end:]
log.append(("new question 2 inserted", 1))

# ── 6. Dev note (prototype-only, remove before production) ───────────────────
DEV_NOTE = """<div id="dev-note" style="position:fixed;right:16px;bottom:16px;z-index:80;font-family:inherit">
<button id="dev-note-pill" style="background:#0f172a;color:#fff;border:0;border-radius:999px;padding:9px 16px;font-size:12.5px;font-weight:600;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)">Dev note: what changed</button>
<div id="dev-note-panel" hidden style="position:absolute;right:0;bottom:44px;width:330px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px 16px;box-shadow:0 12px 40px rgba(15,23,42,.18);font-size:12.5px;line-height:1.55;color:#334155">
<b style="color:#0f172a">Prototype note, remove before production.</b>
Changes vs the live FAQ page:
<ul style="margin:8px 0 0;padding-left:18px;list-style:disc">
<li>Remove the word "virtual" from all copy, everywhere it appears on the live page: tab title, search/social tags and descriptions, intro line, the Q1 and Q3 questions ("job fairs" becomes "hiring events"), and both footer links (now "Hiring Event Platform" and "Job Fair Calendar"). Apply the same wording to the FAQ schema (JSON-LD); this static copy omits scripts.</li>
<li>Q1 answer now covers in-person, video, and phone interviews (was video-only)</li>
<li>NEW question 2: "Where do interviews take place?"</li>
<li>The Sign In link is the login web address and stays unchanged</li>
</ul></div></div>"""

# ── 7. Accordion + drawer + dev-note behavior ────────────────────────────────
JS = """<script>
(function () {
  "use strict";
  var OPEN = ["border-blue-200", "bg-blue-50/40", "shadow-sm"];
  var CLOSED = ["border-slate-200", "bg-white", "hover:border-slate-300"];
  var list = document.querySelectorAll(".max-w-3xl.mx-auto.flex.flex-col.gap-4 > div");
  list.forEach(function (item) {
    var btn = item.querySelector("button");
    var panel = item.querySelector("div[hidden], div[data-open]");
    if (!btn || !panel) return;
    btn.addEventListener("click", function () {
      var opening = !panel.hasAttribute("data-open");
      if (opening) { panel.removeAttribute("hidden"); panel.setAttribute("data-open", "1"); }
      else { panel.setAttribute("hidden", ""); panel.removeAttribute("data-open"); }
      OPEN.forEach(function (c) { item.classList.toggle(c, opening); });
      CLOSED.forEach(function (c) { item.classList.toggle(c, !opening); });
      btn.querySelector("svg").classList.toggle("rotate-180", opening);
    });
  });
  var drawer = document.querySelector("div.fixed.right-0.w-full.bg-white");
  var burger = document.querySelector("header button");
  if (drawer && burger) {
    burger.addEventListener("click", function () { drawer.classList.remove("translate-x-full"); });
    var closeBtn = drawer.querySelector('button[aria-label="Close menu"]');
    if (closeBtn) closeBtn.addEventListener("click", function () { drawer.classList.add("translate-x-full"); });
  }
  var pill = document.getElementById("dev-note-pill");
  var np = document.getElementById("dev-note-panel");
  if (pill && np) pill.addEventListener("click", function () {
    if (np.hasAttribute("hidden")) np.removeAttribute("hidden"); else np.setAttribute("hidden", "");
  });
})();
</script>"""
sub("dev note + behavior script", "</body>", DEV_NOTE + "\n" + JS + "\n</body>")

# ── 8. Provenance comment ────────────────────────────────────────────────────
s = s.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!--\n"
  "  employer-faq.html — JobFairX employer FAQ page, cloned from the live DOM of\n"
  "  https://jobfairx.com/employer/hiring-event-faq (captured 24 Aug 2026) with\n"
  "  Scott's 24 Aug updates applied: no virtual in copy, Q1 answer covers\n"
  "  in-person/video/phone, new question 2 (Where do interviews take place?).\n"
  "  Answer panels injected from the live page's FAQ JSON-LD; accordion, drawer,\n"
  "  and the removable dev-note toggle reinstated with a small inline script.\n-->\n", 1)

open(OUT, "w", encoding="utf-8").write(s)
print(f"{'label':<44} matches")
for l, n in log: print(f"  {l:<42} {n}")
print(f"\nchars {orig:,} -> {len(s):,}  ({len(s)-orig:+,})")
