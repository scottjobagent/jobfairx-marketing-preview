#!/usr/bin/env python3
"""Build hero-fix-preview.html — every employer page that shares the small-hero
component, in live markup, with the fix applied and a current/fixed toggle.

Source of truth: pages/*.html, the server-rendered HTML of each live URL,
fetched 31 Aug 2026, plus the page's own compiled stylesheet
(_app/immutable/assets/app.bb701d17.css — one build serves all of them).

Scope was established by sweeping all 26 core employer URLs in sitemap.xml for
the class string `text-3xl font-medium lg:font-semibold`. Exactly five pages
carry it. Every other employer page already has a real hero size
(host-an-event 46px, job-postings 52px, bundles 44px, about-us 52px,
resources 48px, job-posting-pricing 60px), and the 1,760 programmatic
/employer/job-fairs/* pages do not use this component at all.

Contract, same as build-employer-faq.py: every replacement asserts its match
count and aborts loudly on drift. Nothing is guessed.

Each changed element keeps its ORIGINAL class string in data-oc="", so the
toggle flips the real page between current and fixed with no second copy of
the markup.
"""
import re, sys, base64

W    = "/Users/scottl./Desktop/jobfairx-marketing"
CSS  = f"{W}/assets/live-capture/hero-fix-aug31/css-app.bb701d17.css"
LOGO = "/Users/scottl./Desktop/jobfairx-marketing/assets/employer-home/jobfairx-logo.png"
OUT  = f"{W}/employer-hero-fix-preview.html"

log = []


def sub(s, label, old, new, count=1):
    n = s.count(old)
    if n != count:
        print(f"ABORT [{label}]: {n} matches, expected {count}")
        sys.exit(1)
    log.append((label, n))
    return s.replace(old, new)


def swap(s, label, old_cls, new_cls, count=1):
    """class="OLD"  ->  class="NEW" data-oc="OLD"  so the toggle can flip it."""
    return sub(s, label,
               f'class="{old_cls}"',
               f'class="{new_cls}" data-oc="{old_cls}"',
               count)


# ── the change, in one place ─────────────────────────────────────────────────
HALO_OLD = ("absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[450px] "
            "bg-blue-600/10 blur-[140px] rounded-full pointer-events-none hidden lg:block")
HALO_NEW = "jfx-halo pointer-events-none hidden lg:block"

# text-3xl (30px/36px) stays for mobile; the desktop step is added on top of it,
# so phones render byte-identically to today.
H_OLD = "text-3xl font-medium lg:font-semibold"
H_NEW = ("text-3xl lg:text-[44px] font-medium lg:font-semibold "
         "lg:leading-[1.05] lg:tracking-[-0.03em]")

EY_OLD = ("text-[12px] font-bold lg:text-center text-[#2563eb] uppercase "
          "tracking-[0.14em] mb-2 lg:mb-4")
EY_NEW = ("text-[12px] lg:text-[14px] font-bold lg:text-center text-[#2563eb] uppercase "
          "tracking-[0.14em] mb-2 lg:mb-4")

WHITE = "bg-white relative overflow-hidden"
GRAD  = "bg-gradient-to-b from-white to-slate-50 relative overflow-hidden"

# key, nav label, source file, hero <section> padding prefix, band beneath?,
# headline class prefixes present on that page, eyebrow present?
PAGES = [
    ("calendar",  "Calendar",   "employer_hiring-event-calendar.html",
     "pt-[20px] lg:pt-[60px] lg:pb-[48px] ", True,
     ["hidden lg:block text-slate-900 lg:mb-4 max-w-3xl mx-auto ",
      "lg:hidden text-slate-900 lg:mb-4 max-w-3xl mx-auto "], True),

    ("healthcare", "Healthcare", "employer_healthcare-hiring-event-calendar.html",
     "pt-[20px] lg:pt-[60px] lg:pb-[48px] ", True,
     ["text-slate-900 lg:mb-4 max-w-3xl mx-auto "], True),

    ("pricing",   "Pricing",    "employer_hiring-event-pricing.html",
     "pt-[40px] pb-[36px] lg:pt-[60px] lg:pb-[48px] ", False,
     ["text-slate-900 mb-4 flex gap-1.5 max-w-3xl justify-center mx-auto "], True),

    ("faq",       "FAQ",        "employer_hiring-event-faq.html",
     "pt-[40px] pb-[36px] lg:pt-[60px] lg:pb-[48px] ", True,
     ["text-slate-900 mb-4 max-w-3xl mx-auto "], False),

    ("contact",   "Contact",    "employer_contact.html",
     "pt-[40px] lg:pt-[60px] lg:pb-[48px] ", False,
     ["text-slate-900 mb-4 max-w-3xl mx-auto "], False),
]


def clean(s):
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    s = re.sub(r'\s+data-svelte-h="svelte-[a-z0-9]+"', '', s)
    s = s.replace(' data-sveltekit-preload-data="hover"', '')
    s = re.sub(r'<!--\s*HTML_TAG_(START|END)\s*-->', '', s)
    m = re.search(r'<body[^>]*>(.*)</body>', s, re.S)
    if not m:
        print("ABORT: no <body>")
        sys.exit(1)
    return m.group(1)


logo_uri = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()
built = {}

for key, label, fname, pad, has_band, heads, has_eyebrow in PAGES:
    s = clean(open(f"{W}/assets/live-capture/hero-fix-aug31/{fname}", encoding="utf-8").read())

    # 1. hero background: only pages with a slate-50 band underneath need the
    #    gradient. Pricing and Contact flow into white already.
    if has_band:
        s = swap(s, f"{key}: hero bg -> gradient", pad + WHITE, pad + GRAD)
    else:
        log.append((f"{key}: hero bg unchanged (no band beneath)", 0))

    # 2. halo off top-centre
    s = swap(s, f"{key}: halo off-centre", HALO_OLD, HALO_NEW)

    # 3. eyebrow 12 -> 14px on desktop
    if has_eyebrow:
        s = swap(s, f"{key}: eyebrow 12->14px",
                 f"hidden lg:block {EY_OLD}", f"hidden lg:block {EY_NEW}")

    # 4. headline desktop step
    for i, pre in enumerate(heads):
        s = swap(s, f"{key}: headline{'' if len(heads) == 1 else f' #{i+1}'}",
                 pre + H_OLD, pre + H_NEW)

    n = s.count('src="/jobfairx-logo.png"')
    s = s.replace('src="/jobfairx-logo.png"', f'src="{logo_uri}"')
    log.append((f"{key}: logo inlined", n))
    s = s.replace('href="/employer', 'data-href="/employer')   # inert in preview
    built[key] = s

# ── stylesheet ───────────────────────────────────────────────────────────────
css = open(CSS, encoding="utf-8").read()
nff = len(re.findall(r'@font-face\s*{[^}]*}', css))
css = re.sub(r'@font-face\s*{[^}]*}', '', css)     # self-hosted TTFs are CSP-blocked
log.append(("local @font-face blocks removed", nff))

needed = ["lg\\:text-\\[44px\\]", "lg\\:leading-\\[1\\.05\\]", "lg\\:tracking-\\[-0\\.03em\\]",
          "lg\\:text-\\[14px\\]", "from-white", "to-slate-50", "bg-gradient-to-b"]
missing = [c.replace("\\", "") for c in needed if c not in css]
print("Not in the production stylesheet — Tailwind must generate these:")
for c in missing:
    print("   ", c)

SHIM = """
/* preview shim: the production build only ships utilities the source uses, so
   the new ones do not exist in app.bb701d17.css yet. Tailwind generates them
   at build time once the class strings land in the components. */
.jfx-halo{position:absolute;top:-140px;right:4%;width:780px;height:430px;
  background:rgba(37,99,235,.10);filter:blur(150px);border-radius:9999px}
@media (min-width:1024px){
  .lg\\:text-\\[44px\\]{font-size:44px}
  .lg\\:leading-\\[1\\.05\\]{line-height:1.05}
  .lg\\:tracking-\\[-0\\.03em\\]{letter-spacing:-.03em}
  .lg\\:text-\\[14px\\]{font-size:14px}
}
.from-white{--tw-gradient-from:#fff;--tw-gradient-to:rgb(255 255 255 / 0);
  --tw-gradient-stops:var(--tw-gradient-from),var(--tw-gradient-to)}
.to-slate-50{--tw-gradient-to:#f8fafc}
"""

CHROME = """
/* The site is a light-only marketing page and the artifact host paints its own
   ground in the viewer's theme, so commit to light explicitly. */
html,body{background:#fff;color-scheme:light}
.jfx-page{background:#fff;display:none}
.jfx-page.on{display:block}

/* preview chrome - not part of the site */
#jfx-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;z-index:99999;
  display:flex;align-items:center;gap:9px;padding:7px 9px;border-radius:999px;
  background:rgba(15,23,42,.94);backdrop-filter:blur(10px);max-width:calc(100vw - 24px);
  box-shadow:0 8px 30px rgba(15,23,42,.35);font-family:Inter,system-ui,sans-serif}
#jfx-bar .grp{display:flex;gap:2px;background:rgba(255,255,255,.10);border-radius:999px;padding:3px}
#jfx-bar button{border:0;cursor:pointer;font:600 12px/1 Inter,system-ui,sans-serif;
  color:#cbd5e1;background:transparent;padding:8px 12px;border-radius:999px;white-space:nowrap}
#jfx-bar button:hover{color:#fff}
#jfx-bar button[aria-pressed="true"]{background:#fff;color:#0f172a}
#jfx-bar button:focus-visible{outline:2px solid #60a5fa;outline-offset:2px}
#jfx-bar .lbl{color:#94a3b8;font:600 10px/1 Inter,system-ui,sans-serif;
  letter-spacing:.14em;text-transform:uppercase;padding-left:5px}
#jfx-note{position:fixed;right:14px;bottom:18px;z-index:99999;max-width:355px;
  font-family:Inter,system-ui,sans-serif}
#jfx-note summary{cursor:pointer;list-style:none;display:inline-block;float:right;
  background:#2563eb;color:#fff;font:600 11px/1 Inter,sans-serif;letter-spacing:.06em;
  padding:9px 13px;border-radius:999px;box-shadow:0 6px 20px rgba(37,99,235,.35)}
#jfx-note summary::-webkit-details-marker{display:none}
#jfx-note[open] summary{float:none;margin-bottom:8px}
#jfx-note .card{clear:both;background:#fff;border:1px solid #e2e8f0;border-radius:12px;
  padding:15px 17px;box-shadow:0 12px 40px rgba(15,23,42,.18);font-size:12px;line-height:1.6;
  color:#334155;max-height:64vh;overflow:auto}
#jfx-note h4{margin:12px 0 7px;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#64748b}
#jfx-note h4:first-child{margin-top:0}
#jfx-note ul{margin:0;padding-left:16px}
#jfx-note li{margin-bottom:6px}
#jfx-note code{background:#f1f5f9;padding:1px 4px;border-radius:3px;font-size:11px;
  font-family:ui-monospace,Menlo,monospace;word-break:break-word}
@media (max-width:900px){#jfx-note{display:none}}
"""

JS = """
(function(){
  var mode='after', page='calendar';
  function apply(){
    document.querySelectorAll('[data-oc]').forEach(function(el){
      if(!el.dataset.nc) el.dataset.nc = el.getAttribute('class');
      el.setAttribute('class', mode==='before' ? el.dataset.oc : el.dataset.nc);
    });
    document.querySelectorAll('.jfx-page').forEach(function(p){
      p.classList.toggle('on', p.id==='jfx-'+page);
    });
    document.querySelectorAll('#jfx-bar button').forEach(function(b){
      var on = (b.dataset.mode && b.dataset.mode===mode) || (b.dataset.page && b.dataset.page===page);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('#jfx-bar button');
    if(b){
      if(b.dataset.mode) mode=b.dataset.mode;
      if(b.dataset.page){ page=b.dataset.page; window.scrollTo(0,0); }
      apply(); return;
    }
    if(e.target.closest('#jfx-note')) return;
    var a = e.target.closest('a');
    if(a) e.preventDefault();               // preview: links stay put
  });
  document.addEventListener('keydown', function(e){
    if(e.key==='b'||e.key==='B'){ mode = (mode==='after'?'before':'after'); apply(); }
  });
  apply();
})();
"""

tabs = "".join(f'<button data-page="{k}">{lbl}</button>'
               for k, lbl, *_ in PAGES)

BAR = f"""
<div id="jfx-bar">
  <span class="lbl">Page</span><div class="grp">{tabs}</div>
  <span class="lbl">View</span>
  <div class="grp">
    <button data-mode="before">Current</button>
    <button data-mode="after">Fixed</button>
  </div>
</div>
<details id="jfx-note">
  <summary>WHAT CHANGED</summary>
  <div class="card">
    <h4>Scope</h4>
    <ul>
      <li>All 26 core employer URLs were swept for <code>text-3xl font-medium lg:font-semibold</code>.
          <b>Exactly these five carry it.</b> Every other employer page already has a real hero
          (host-an-event 46px, job-postings 52px, bundles 44px, about-us 52px, resources 48px).
          The 1,760 <code>/employer/job-fairs/*</code> pages don't use this component.</li>
    </ul>
    <h4>Applied</h4>
    <ul>
      <li><b>Headline.</b> <code>text-3xl</code> &rarr;
          <code>text-3xl lg:text-[44px] lg:leading-[1.05] lg:tracking-[-0.03em]</code>.
          Desktop only &mdash; mobile renders byte-identically to today.</li>
      <li><b>Eyebrow.</b> 12px &rarr; 14px on desktop, matching the home page.
          Calendar, Healthcare, Pricing. FAQ and Contact have no eyebrow.</li>
      <li><b>Halo.</b> The 900&times;450 <code>bg-blue-600/10 blur-[140px]</code> circle moves off
          top-centre to the right, the way the home page's does. All five.</li>
      <li><b>Hero background.</b> <code>bg-white</code> &rarr;
          <code>bg-gradient-to-b from-white to-slate-50</code> on Calendar, Healthcare and FAQ,
          so the hero melts into the grey band instead of butting against it.
          <b>Pricing and Contact are unchanged</b> &mdash; no band beneath them, so they never
          read as recessed.</li>
    </ul>
    <h4>Not changed</h4>
    <ul>
      <li>No copy edits. No CTA added to the heroes. No left-alignment. Those are design
          calls, not defect fixes.</li>
    </ul>
    <h4>Preview caveats</h4>
    <ul>
      <li>Static clone: scripts stripped, so search, filters and the FAQ accordion don't run,
          and links are inert on purpose.</li>
      <li>Inter loads from Google Fonts here; the live site self-hosts it.</li>
      <li>A shim supplies four utilities the production CSS doesn't contain yet
          (<code>lg:leading-[1.05]</code>, <code>lg:tracking-[-0.03em]</code>,
          <code>lg:text-[14px]</code>, <code>to-slate-50</code>). Tailwind generates them for
          real once the class strings are in the components.</li>
    </ul>
  </div>
</details>
"""

body = "".join(
    f'<div class="jfx-page{" on" if k == "calendar" else ""}" id="jfx-{k}">{built[k]}</div>'
    for k, *_ in PAGES)

html = f"""<meta charset="utf-8">
<title>Employer Hero Fix Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap">
<style>
{css}
</style>
<style>{SHIM}</style>
<style>{CHROME}</style>
{body}
{BAR}
<script>{JS}</script>
"""

open(OUT, "w", encoding="utf-8").write(html)
print("\nEdits applied:")
for label, n in log:
    print(f"  {n:>3}  {label}")
print(f"\nWrote {OUT}  ({len(html)/1024:.0f} KB)")
