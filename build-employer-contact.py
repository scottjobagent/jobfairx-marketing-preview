#!/usr/bin/env python3
"""Build employer-contact.html from the captured live contact page.

Source of truth: assets/live-capture/contact-live-dom.html — the server-rendered
HTML of https://jobfairx.com/employer/contact, captured 1 Sep 2026 (curl; the
client scripts, Cloudflare email obfuscation and reCAPTCHA badge are stripped
here). Same contract as build-employer-faq.py: every replacement asserts its
match count and aborts loudly on drift. Edit this builder, never the output.

What changes vs live (the 1 Sep 2026 design audit, 18 findings, 0 refuted):
  layout   body moves into the page column every other page uses (the hero's own
           `container mx-auto px-6 lg:px-8 max-w-7xl`), the contact channels
           become one bordered white card under the hero (rendered once, not a
           desktop + mobile pair), and the form sits in a bordered white card;
           Submit is left-aligned with the fields at the site's primary width,
           full-width on mobile; the CTA band uses the FAQ/pricing button grammar
  hero     untouched apart from the mobile bottom padding the siblings carry
  form     inputs get real types, inputmode, autocomplete, required; labels in
           sentence case; the optional field is marked; Submit is enabled and
           validates on click (errors linked with aria-invalid/aria-describedby,
           summary in a polite live region); reCAPTCHA badge replaced by the
           permitted attribution line
  copy     one expectation line under Submit ({{placeholder}} until Scott
           confirms the reply time); FAQ and job-seeker routes; PST -> PT;
           page title on the family pattern; meta description on live vocabulary
Everything new is authored with page CSS (assets/employer-contact/contact.css)
or inline styles — no bare Tailwind utilities in new markup. Live chrome
(header, footer) is untouched. A removable dev-note pill lists the deltas.
"""
import re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/contact-live-dom.html"
OUT = f"{W}/employer-contact.html"
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

def sub_in(text, label, old, new, count=1):
    n = text.count(old)
    if n != count:
        print(f"ABORT [{label}]: {n} matches, expected {count}"); sys.exit(1)
    log.append((label, n))
    return text.replace(old, new)

# ── 1. De-frameworkise ───────────────────────────────────────────────────────
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "",
    count=len(re.findall(r'data-svelte-h', s)), regex=True)
sub("strip sveltekit body attr", ' data-sveltekit-preload-data="hover"', "")
sub("strip data-fg tracing attrs", r'\s+data-fg[a-z0-9-]*="[^"]*"', "",
    count=len(re.findall(r' data-fg[a-z0-9-]*="', s)), regex=True)
sub("strip scripts (recaptcha, cf email-decode, inline)", r'<script\b.*?</script>', "",
    count=3, regex=True, flags=re.S)

# ── 2. Localise assets (shared with the other employer clones) ───────────────
sub("app css + page css",
    '<link href="../_app/immutable/assets/app.c26c23f8.css" rel="stylesheet">',
    '<link href="assets/employer-home/app.css?v=2" rel="stylesheet">\n'
    '<link href="assets/employer-contact/contact.css?v=1" rel="stylesheet">')
sub("favicon", 'href="../favicon.png"', 'href="assets/employer-home/favicon.png"')
sub("logo", '/jobfairx-logo.png', 'assets/employer-home/jobfairx-logo.png', count=2)

# ── 3. Head: family title pattern, live-vocabulary description ───────────────
TITLE_OLD = "Contact JobFairX | Employer Support"
TITLE_NEW = "Contact Employer Support for Hiring Events | JobFairX"
sub("title / og / twitter titles", TITLE_OLD, TITLE_NEW, count=3)
DESC_OLD = ("Have questions about JobFairX hiring events? Contact our team to learn how employers "
            "can meet candidates and hire top talent through our hiring events.")
DESC_NEW = ("Contact the JobFairX employer team about event registration, pricing and packages, "
            "private hiring events, or technical support. Email info@jobfairx.com.")
assert len(DESC_NEW) <= 160, len(DESC_NEW)
sub("meta / og / twitter descriptions", DESC_OLD, DESC_NEW, count=3)

# ── 4. Hero: the siblings' mobile bottom padding, nothing else ───────────────
sub("hero mobile pb-[36px] (pricing's exact class string)",
    '<section class="pt-[40px] lg:pt-[60px] lg:pb-[48px] bg-white relative overflow-hidden">',
    '<section class="pt-[40px] pb-[36px] lg:pt-[60px] lg:pb-[48px] bg-white relative overflow-hidden">')

# ── 5. Body: carve out the live rail + form block ────────────────────────────
BODY_START = '<div class="px-4 lg:px-0 lg:max-w-7xl mx-auto border-gray-300 my-12 lg:my-16">'
CTA_START = '<section class="bg-slate-50 py-[80px] lg:py-[100px] relative overflow-hidden border-t border-slate-200">'
b0 = s.find(BODY_START); b1 = s.find(CTA_START)
if s.count(BODY_START) != 1 or s.count(CTA_START) != 1 or not (0 < b0 < b1):
    print("ABORT [body block]: anchors not unique / ordered"); sys.exit(1)
block = s[b0:b1]
f0 = block.find('<form method="POST">'); f1 = block.find('</form>')
if block.count('<form method="POST">') != 1 or block.count('</form>') != 1 or not (0 < f0 < f1):
    print("ABORT [form span]: not found once"); sys.exit(1)
form_inner = block[f0 + len('<form method="POST">'):f1]
rail = block[:f0]                       # desktop rail only (before the form)
icons = re.findall(r'<svg[^>]*class="lucide lucide-(?:mail|phone|map-pin|clock) [^"]*"[^>]*>.*?</svg>', rail, re.S)
if len(icons) != 4:
    print(f"ABORT [rail icons]: {len(icons)} found, expected 4"); sys.exit(1)
ICON_MAIL, ICON_PHONE, ICON_PIN, ICON_CLOCK = icons
log.append(("body block carved (rail icons reused)", 1))

# ── 6. Form: semantics, sentence case, optional marker, enabled Submit ───────
f = form_inner
f = sub_in(f, "asterisks red-500 -> red-600", 'class="text-red-500">*</span>', 'class="text-red-600">*</span>', count=8)
for old, new in [("Phone Number <span", "Phone number <span"), ("Business Email <span", "Business email <span"),
                 ("Company Size <span", "Company size <span"), ("Job Title <span", "Job title <span")]:
    f = sub_in(f, f"label sentence case: {old.split(' <')[0]}", old, new)
f = sub_in(f, "optional marker on message", 'How can we help you? </label>',
           'How can we help you? <span style="font-weight:400;color:#64748b">(optional)</span></label>')
f = sub_in(f, "firstName semantics", '<input id="firstName" name="firstName" type="text" class="',
           '<input id="firstName" name="firstName" type="text" autocomplete="given-name" required aria-required="true" class="')
f = sub_in(f, "lastName semantics", '<input id="lastName" name="lastName" type="text" class="',
           '<input id="lastName" name="lastName" type="text" autocomplete="family-name" required aria-required="true" class="')
f = sub_in(f, "phone semantics", '<input id="phoneNumber" name="phoneNumber" type="text" class="',
           '<input id="phoneNumber" name="phoneNumber" type="tel" inputmode="tel" autocomplete="tel" required aria-required="true" class="')
f = sub_in(f, "email semantics", '<input id="Email" name="Email" type="text" class="',
           '<input id="Email" name="Email" type="email" inputmode="email" autocomplete="email" required aria-required="true" class="')
f = sub_in(f, "company semantics", '<input id="company" name="company" type="text" class="',
           '<input id="company" name="company" type="text" autocomplete="organization" required aria-required="true" class="')
for sel in ["companySize", "jobTitle", "subject"]:
    f = sub_in(f, f"{sel} required", f'<select id="{sel}" name="{sel}" class="',
               f'<select id="{sel}" name="{sel}" required aria-required="true" class="')
f = sub_in(f, "select placeholder: company size", '>Company size...</option>', '>Select...</option>')
f = sub_in(f, "select placeholder: job title", '>Job title...</option>', '>Select...</option>')
f = sub_in(f, "select placeholder: subject", '>Select a subject...</option>', '>Select...</option>')
SUBMIT_OLD = '<button disabled class="button-primary button mt-4 lg:mt-8 lg:mx-auto" type="submit">Submit</button>'
SUBMIT_NEW = (
  '<div class="jfx-submit"><button class="button-primary button" type="submit">Submit</button> '
  '<p class="jfx-help">You\'ll hear back from a real person by email {{reply time: not yet confirmed}}.</p></div> '
  '<p class="jfx-note" id="jfx-note" hidden></p> '
  '<p class="jfx-legal">This site is protected by reCAPTCHA and the Google '
  '<a href="https://policies.google.com/privacy">Privacy Policy</a> and '
  '<a href="https://policies.google.com/terms">Terms of Service</a> apply.</p>')
f = sub_in(f, "submit row (enabled, left-aligned, expectation line, reCAPTCHA attribution)", SUBMIT_OLD, SUBMIT_NEW)
form_inner = f

# ── 7. New body: channels card + form card inside the shared page column ─────
def channel(icon, label, value_html):
    return (f'<div class="jfx-channel">{icon} <div><p class="jfx-ch-label">{label}</p> {value_html}</div></div>')

NEW_BODY = (
  '<section class="jfx-body"><div class="container mx-auto px-6 lg:px-8 max-w-7xl">'
  '<h2 class="sr-only">Contact details</h2> '
  '<div class="jfx-card jfx-channels">'
  + channel(ICON_MAIL, "Email", '<a href="mailto:info@jobfairx.com" class="jfx-link">info@jobfairx.com</a>') + ' '
  + channel(ICON_PHONE, "Phone", '<a href="tel:+17022690808" class="jfx-link">(702) 269-0808</a>') + ' '
  + channel(ICON_PIN, "Mailing address", '<p class="jfx-ch-value">JobFairX, LLC<br>209 S Stephanie St. STE B #144<br>Henderson, Nevada 89012</p>') + ' '
  + channel(ICON_CLOCK, "Support hours", '<p class="jfx-ch-value">Monday – Friday<br>5:00 AM – 5:00 PM PT</p>')
  + '</div> '
  '<h2 class="sr-only">Contact form</h2> '
  '<div class="jfx-card jfx-formcard"><form method="POST" novalidate>' + form_inner + '</form></div> '
  '<p class="jfx-aside">Looking for a quick answer? Most questions about registration, pricing, and interviews are '
  'covered in the <a href="/employer/hiring-event-faq">Hiring Event FAQ</a>. Looking for a job? This form is for '
  'employers. Job seekers can find upcoming events on the <a href="/job-fair-calendar">job fair calendar</a>.</p>'
  '</div></section> ')
s = s[:b0] + NEW_BODY + s[b1:]
log.append(("new body injected", 1))

# ── 8. CTA band: FAQ/pricing button grammar ──────────────────────────────────
CTA_A = '<a href="/employer/hiring-event-calendar" class="button button-primary">'
a0 = s.find(CTA_A)
a1 = s.find('</a>', a0) + 4
old_btn = s[a0:a1]
if a0 < 0 or s.count(CTA_A) != 1 or 'Browse Events' not in old_btn or 'lucide-calendar-days' not in old_btn:
    print("ABORT [cta primary]: anchor drift"); sys.exit(1)
ARROW = ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="cta-arrow">'
         '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>')
s = s[:a0] + ('<a href="/employer/hiring-event-calendar" class="button button-primary" style="min-width:224px">Browse Events\n        '
              + ARROW + '</a>') + s[a1:]
log.append(("cta primary: trailing arrow, faq pill width", 1))
sub("cta secondary -> button-primary-inverted",
    '<a href="/employer/hiring-event-pricing" class="button button-secondary">View Pricing</a>',
    '<a href="/employer/hiring-event-pricing" class="button button-primary-inverted" style="min-width:224px">View Pricing</a>')

# ── 9. Dev note (prototype-only, remove before production) ───────────────────
DEV_NOTE = """<div id="dev-note" style="position:fixed;right:16px;bottom:16px;z-index:80;font-family:inherit">
<button id="dev-note-pill" style="background:#0f172a;color:#fff;border:0;border-radius:999px;padding:9px 16px;font-size:12.5px;font-weight:600;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)">Dev note: what changed</button>
<div id="dev-note-panel" hidden style="position:absolute;right:0;bottom:44px;width:340px;max-height:70vh;overflow:auto;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px 16px;box-shadow:0 12px 40px rgba(15,23,42,.18);font-size:12.5px;line-height:1.55;color:#334155">
<b style="color:#0f172a">Prototype note, remove before production.</b>
Changes vs the live contact page:
<ul style="margin:8px 0 0;padding-left:18px;list-style:disc">
<li><b>Page column.</b> The body now uses the same container as the hero, header and CTA band (content on 112 to 1328 at 1440px), instead of overhanging it by 32px on each side.</li>
<li><b>Cards.</b> Contact channels are one bordered white card under the hero (rendered once; the desktop and mobile copies are gone). The form sits in a bordered white card, the same surface the FAQ, pricing, bundles and calendar pages use.</li>
<li><b>Submit.</b> Enabled and blue at all times, left-aligned with the fields at 200px min-width (full-width on mobile). Validates on click: first invalid field is focused, each error is linked with aria-invalid and aria-describedby, a polite live region announces the count. Errors keep the live wording ("First name is required").</li>
<li><b>Inputs.</b> Email is type=email, phone is type=tel, with inputmode and autocomplete; required and aria-required on the eight required fields; 16px control text below 1024px so iOS does not zoom. Labels in sentence case; the message field is marked (optional); select placeholders unified to "Select...".</li>
<li><b>reCAPTCHA.</b> Hide the floating badge (it covers the right edge of inputs on phones) and print the permitted attribution line under Submit instead. Apply the same on the event page form.</li>
<li><b>Copy.</b> One expectation line under Submit; the reply time is a {{placeholder}} until confirmed. FAQ and job-seeker routes under the form. Hours read PT instead of PST. Title on the family pattern; meta description on live vocabulary.</li>
<li><b>CTA band.</b> Browse Events carries the trailing arrow the FAQ and pricing bands use; View Pricing uses the site's inverted primary; both 224px so they stack evenly on mobile.</li>
<li><b>Hero.</b> Unchanged except the mobile bottom padding (pb-[36px]) the FAQ and pricing heroes already have.</li>
<li><b>Not decided here.</b> Field count (nine fields, eight required), whether the phone line is staffed, the reply time, and a job-seeker support address are Scott's calls.</li>
</ul></div></div>"""

# ── 10. Drawer + validation + dev-note behaviour ─────────────────────────────
JS = """<script>
(function () {
  "use strict";
  var drawer = document.querySelector("div.fixed.right-0.w-full.bg-white");
  var burger = document.querySelector("header button");
  if (drawer && burger) {
    burger.addEventListener("click", function () { drawer.classList.remove("translate-x-full"); });
    var closeBtn = drawer.querySelector('button[aria-label="Close menu"]');
    if (closeBtn) closeBtn.addEventListener("click", function () { drawer.classList.add("translate-x-full"); });
  }
  var form = document.querySelector(".jfx-formcard form");
  if (form) {
    var fields = Array.prototype.slice.call(form.querySelectorAll("input, select, textarea"));
    var live = document.createElement("p");
    live.className = "sr-only"; live.setAttribute("aria-live", "polite"); form.appendChild(live);
    var note = document.getElementById("jfx-note");
    function labelOf(f) {
      var l = form.querySelector('label[for="' + f.id + '"]');
      return l ? l.textContent.replace("*", "").replace("(optional)", "").trim() : "This field";
    }
    function clear(f) {
      var e = document.getElementById(f.id + "-error"); if (e) e.parentNode.removeChild(e);
      f.removeAttribute("aria-invalid"); f.removeAttribute("aria-describedby");
      f.classList.remove("jfx-invalid"); f.style.borderColor = "";
    }
    function setError(f, msg) {
      clear(f); if (!msg) return;
      var p = document.createElement("p"); p.className = "jfx-error"; p.id = f.id + "-error"; p.textContent = msg;
      f.parentNode.insertBefore(p, f.nextSibling);
      f.setAttribute("aria-invalid", "true"); f.setAttribute("aria-describedby", p.id);
      f.classList.add("jfx-invalid"); f.style.borderColor = "#dc2626";
    }
    function check(f) {
      var v = (f.value || "").trim();
      if (f.required && !v) return labelOf(f) + " is required";
      if (f.type === "email" && v && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v)) return labelOf(f) + " is invalid";
      return "";
    }
    fields.forEach(function (f) {
      f.addEventListener("blur", function () { setError(f, check(f)); });
      f.addEventListener("input", function () { if (f.getAttribute("aria-invalid")) setError(f, check(f)); });
      f.addEventListener("change", function () { if (f.getAttribute("aria-invalid")) setError(f, check(f)); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = fields.filter(function (f) { var m = check(f); setError(f, m); return !!m; });
      if (bad.length) {
        live.textContent = bad.length + (bad.length === 1 ? " field needs" : " fields need") + " attention";
        if (note) note.setAttribute("hidden", "");
        bad[0].focus();
      } else {
        live.textContent = "Design preview only. Nothing was sent.";
        if (note) { note.textContent = "Design preview only. Nothing was sent."; note.removeAttribute("hidden"); }
      }
    });
  }
  var pill = document.getElementById("dev-note-pill");
  var np = document.getElementById("dev-note-panel");
  if (pill && np) pill.addEventListener("click", function () {
    if (np.hasAttribute("hidden")) np.removeAttribute("hidden"); else np.setAttribute("hidden", "");
  });
})();
</script>"""
sub("dev note + behaviour script", "</body>", DEV_NOTE + "\n" + JS + "\n</body>")

# ── 11. Provenance comment ───────────────────────────────────────────────────
s = s.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!--\n"
  "  employer-contact.html — JobFairX employer contact page, cloned from the live\n"
  "  server-rendered HTML of https://jobfairx.com/employer/contact (captured 1 Sep\n"
  "  2026) with the 1 Sep design-audit fixes applied: body inside the shared page\n"
  "  column, channels card + form card, enabled left-aligned Submit, input\n"
  "  semantics, reCAPTCHA attribution line, FAQ/pricing CTA grammar. Generated by\n"
  "  build-employer-contact.py; edit the builder, not this file.\n-->\n", 1)

# ── 12. Guards ───────────────────────────────────────────────────────────────
checks = {
  "virtual only in the 2 login URLs": len(re.findall(r'virtual', s, re.I)) == 2,
  "no Cloudflare email obfuscation left": '__cf_email__' not in s and 'email-protection' not in s,
  "no tracing attrs": ' data-fg' not in s,
  "exactly one script (ours)": s.count('<script') == 1,
  "no disabled submit": '<button disabled' not in s,
  "no em dash in rendered copy": '—' not in re.sub(r'<[^>]+>', '', s),
  "exactly one h1": s.count('<h1') == 1,
  "no 'Book a demo'": 'Book a demo' not in s,
  "rail rendered once": s.count('Mailing address') == 1 and s.count('Mailing Address') == 0,
}
bad = [k for k, ok in checks.items() if not ok]
if bad:
    print("ABORT [guards]:", bad); sys.exit(1)

open(OUT, "w", encoding="utf-8").write(s)
print(f"{'label':<64} matches")
for l, n in log: print(f"  {l:<62} {n}")
print(f"\nchars {orig:,} -> {len(s):,}  ({len(s)-orig:+,})  guards ok: {len(checks)}")
