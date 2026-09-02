#!/usr/bin/env python3
"""Build employer-pricing.html from the captured live pricing page.

Source of truth: assets/live-capture/pricing-live-dom.html — the server-rendered
HTML of https://jobfairx.com/employer/hiring-event-pricing, captured 24 Aug 2026
(scripts stripped at capture; the SSR carried no modulepreloads, iframes, or
origin-trial metas). Same contract as build-employer-home.py: every replacement
asserts its match count and aborts loudly if the live page drifts.

EXACT CLONE — zero copy changes by design (Scott, 24 Aug: clone it exactly as it
is; his updates land later as explicit steps in this builder).

One thing the static capture cannot carry is the page's client JS. Section 3
reinstates it with a dependency-free script that drives the captured markup:
package-card selection, the Events stepper, Total/savings, cart links, and the
mobile drawer. All numbers and ids come from the live page's own SvelteKit data
payload (all three bundle ladders, package ids), and the behavior was verified
against the live stepper on 24 Aug 2026 — selecting a tier resets the count to 1,
the selected card's header price shows the bundle per-event rate at bundle
counts, valid counts are 1-4 plus the 8 bundle rungs, and Reserve navigates to
the live cart with bundle=<id> at bundle counts or pkg+qty otherwise. Nothing is
invented.
"""
import re, sys

W = "/Users/scottl./Desktop/jobfairx-marketing"
SRC = f"{W}/assets/live-capture/pricing-live-dom.html"
OUT = f"{W}/employer-pricing.html"
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

# ── 1. De-frameworkise ───────────────────────────────────────────────────────
sub("strip data-svelte-h", r'\s+data-svelte-h="svelte-[a-z0-9]+"', "",
    count=len(re.findall(r'data-svelte-h', s)), regex=True)
sub("strip sveltekit body attr", ' data-sveltekit-preload-data="hover"', "")
sub("strip svelte comment markers", "<!-- HTML_TAG_START --><!-- HTML_TAG_END -->", "")

# ── 2. Localise assets (all already on disk from the employer-home build) ────
sub("app css",  '../_app/immutable/assets/app.029f5d9e.css', 'assets/employer-home/app.css?v=2')
sub("page css", '../_app/immutable/assets/6.2102846a.css', 'assets/employer-home/page.css?v=2')
sub("favicon", 'href="../favicon.png"', 'href="assets/employer-home/favicon.png"')
n = s.count('/jobfairx-logo.png')
sub("logo", '/jobfairx-logo.png', 'assets/employer-home/jobfairx-logo.png', count=n)

# ── 2b. Scott's updates, 24 Aug 2026 ─────────────────────────────────────────
# Headline + sub, given verbatim in chat. The live page hides "Flexible" on
# mobile (span.hidden lg:block); Scott specified one headline with no viewport
# caveat, so it now reads in full at every width.
sub("headline (full at all widths)",
    '<span class="hidden lg:block">Flexible</span> Hiring Event Packages</h1>',
    'Flexible Hiring Event Packages</h1>')
sub("hero sub",
    r'>Choose the package that fits your hiring goals, budget, and schedule so you can start finding candidates right\s*away\.</p>',
    '>Register for a hiring event, post your jobs, and select in-person or video interviews. AI Candidate Matching starts immediately.</p>',
    regex=True)

# Card bullet "In-person or video interviews" between the scheduled-interviews
# and recruiter-seats bullets, all three tiers (Scott, 24 Aug, confirmed).
# Markup cloned from the cards' own bullets.
IPV_LI = ('<li class="flex items-start gap-2.5 text-slate-700">'
  '<div class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0 mt-0.5">'
  '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" '
  'stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="text-blue-600">'
  '<path d="M20 6 9 17l-5-5"></path></svg></div> '
  '<span class="font-medium leading-snug text-[16px]">In-person or video interviews</span> </li>')
for tier in ["20+", "60+", "100+"]:
    anchor = f'<span class="font-medium leading-snug text-[16px]">{tier} scheduled candidate interviews</span> </li>'
    sub(f"in-person/video bullet ({tier})", anchor, anchor + IPV_LI)

# All Packages Include: the dashboard item (the one whose claim the report,
# auto-accept, and follow-up items already cover) becomes the interview-location
# item, keeping the grid at eight. Scott approved the swap 24 Aug; wording is
# the fuller phone-inclusive variant recommended to him.
sub("includes: dashboard -> interview location",
    ">Employer dashboard to manage events, dispositions, notes, and analytics</span>",
    ">In-person, video, or phone interviews</span>")

# No "virtual" anywhere in copy (Scott, 24 Aug: "It should not say virtual
# anywhere"). The two virtual.jobfairx.com Sign In URLs are the product's real
# login domain, not copy, and stay.
sub("title / og / twitter titles",
    "Virtual Hiring Event Pricing for Employers | JobFairX",
    "Hiring Event Pricing for Employers | JobFairX", count=3)
sub("meta / og / twitter descriptions",
    "See JobFairX pricing for virtual hiring events:",
    "See JobFairX pricing for hiring events:", count=3)
sub("closing CTA", "successfully hired through our virtual events.",
    "successfully hired through our hiring events.")
sub("footer employers link", "Virtual Hiring Event Platform</a>", "Hiring Event Platform</a>")
sub("footer seekers link", "Virtual Job Fair Calendar</a>", "Job Fair Calendar</a>")
n_virtual = len(re.findall(r'virtual', s, flags=re.I))
if n_virtual != 2:
    print(f"ABORT [virtual sweep]: {n_virtual} occurrences remain, expected 2 (login URLs only)")
    sys.exit(1)
log.append(("virtual sweep: only the 2 login URLs remain", 2))

# ── 3. Reinstate the page's client behavior (data from the live payload) ─────
JS = """<script>
(function () {
  "use strict";
  // Live SvelteKit payload, jobfairx.com/employer/hiring-event-pricing, 24 Aug 2026.
  // bundles: eventCount -> [actualPerEvent, totalSavings]
  var TIERS = [
    { pkg: "job-fair-starter-1", base: 495, bundles: { 5: [470, 125], 10: [445, 500], 15: [420, 1125], 25: [395, 2500], 40: [365, 5200], 50: [345, 7500], 75: [320, 13125], 100: [297, 19800] } },
    { pkg: "job-fair-exhibitor-1", base: 895, bundles: { 5: [850, 225], 10: [805, 900], 15: [760, 2025], 25: [715, 4500], 40: [655, 9600], 50: [620, 13750], 75: [575, 24000], 100: [537, 35800] } },
    { pkg: "job-fair-sponsor-1", base: 1495, bundles: { 5: [1420, 375], 10: [1345, 1500], 15: [1270, 3375], 25: [1195, 7500], 40: [1095, 16000], 50: [1045, 22500], 75: [970, 39375], 100: [897, 59800] } }
  ];
  var STEPS = [1, 2, 3, 4, 5, 10, 15, 25, 40, 50, 75, 100];
  var SEL_ON = ["border-blue-500", "shadow-[0_0_60px_-10px_rgba(59,130,246,0.3)]"];
  var SEL_OFF = ["border-slate-200", "hover:border-slate-300", "hover:shadow-xl"];

  var cards = document.querySelectorAll("#pricing [role='button']");
  if (cards.length !== 3) return;
  var block = cards[1].querySelector(".border-t.border-slate-200.pt-4");
  var check = cards[1].querySelector(".absolute.top-4.right-4");
  var sel = 1, qty = 1;

  function fmt(n) { return "$" + n.toLocaleString("en-US"); }
  function bundleFor(t, q) { return TIERS[t].bundles[q] || null; }
  function spanByLabel(root, label) {
    var spans = root.querySelectorAll("span");
    for (var i = 0; i < spans.length; i++) if (spans[i].textContent.trim() === label) return spans[i].nextElementSibling;
    return null;
  }
  function setStep(btn, on) {
    btn.disabled = !on;
    btn.classList.toggle("text-slate-600", on);
    btn.classList.toggle("hover:bg-slate-200", on);
    btn.classList.toggle("text-slate-300", !on);
    btn.classList.toggle("cursor-not-allowed", !on);
  }

  function render() {
    cards.forEach(function (card, i) {
      var isSel = i === sel;
      SEL_ON.forEach(function (c) { card.classList.toggle(c, isSel); });
      SEL_OFF.forEach(function (c) { card.classList.toggle(c, !isSel); });
      var b = isSel ? bundleFor(i, qty) : null;
      card.querySelector(".tracking-tight").textContent = fmt(b ? b[0] : TIERS[i].base);
    });
    var target = cards[sel];
    if (check.parentNode !== target) target.insertBefore(check, target.firstChild);
    if (block.parentNode !== target) target.insertBefore(block, target.querySelector(".button-bar"));
    var b = bundleFor(sel, qty);
    block.querySelector(".font-bold.text-lg").textContent = qty;
    spanByLabel(block, "Total").textContent = fmt(b ? b[0] * qty : TIERS[sel].base * qty);
    var chip = block.querySelector(".bg-emerald-50");
    chip.classList.toggle("invisible", !b);
    chip.querySelector("span").textContent = "You save " + fmt(b ? b[1] : 0);
    var btns = block.querySelectorAll("button");
    var idx = STEPS.indexOf(qty);
    setStep(btns[0], idx > 0);
    setStep(btns[1], idx < STEPS.length - 1);
  }

  block.addEventListener("click", function (e) {
    var btn = e.target.closest("button");
    if (!btn || btn.disabled) return;
    var plus = btn.querySelectorAll("path").length === 2;
    var idx = STEPS.indexOf(qty) + (plus ? 1 : -1);
    if (idx >= 0 && idx < STEPS.length) { qty = STEPS[idx]; render(); }
    e.stopPropagation();
  });

  cards.forEach(function (card, i) {
    card.addEventListener("click", function (e) {
      if (e.target.closest(".button-bar")) {
        var b = i === sel ? bundleFor(i, qty) : null;
        var p = new URLSearchParams();
        if (b) p.set("bundle", TIERS[i].pkg.replace(/-1$/, "-" + qty));
        else { p.set("pkg", TIERS[i].pkg); p.set("qty", String(i === sel ? qty : 1)); }
        p.set("skipEvent", "1");
        p.set("returnTo", "/employer/hiring-event-pricing#pricing");
        window.location.assign("https://jobfairx.com/employer/cart?" + p.toString());
        return;
      }
      if (i !== sel && !e.target.closest("#pricing .border-t button")) { sel = i; qty = 1; render(); }
    });
  });

  // Mobile drawer
  var drawer = document.querySelector("div.fixed.right-0.w-full.bg-white");
  var burger = document.querySelector("header button");
  if (drawer && burger) {
    burger.addEventListener("click", function () { drawer.classList.remove("translate-x-full"); });
    var closeBtn = drawer.querySelector('button[aria-label="Close menu"]');
    if (closeBtn) closeBtn.addEventListener("click", function () { drawer.classList.add("translate-x-full"); });
  }
})();
</script>"""
sub("client behavior script", "</body>", JS + "\n</body>")

# ── 4. Provenance comment ────────────────────────────────────────────────────
s = s.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n<!--\n"
  "  employer-pricing.html — JobFairX employer pricing page, an exact clone of\n"
  "  https://jobfairx.com/employer/hiring-event-pricing (captured 24 Aug 2026)\n"
  "  with Scott's headline + sub applied (24 Aug). All other copy verbatim.\n"
  "  Framework hydration attrs and tracking scripts removed;\n"
  "  stylesheets, logo, and favicon shared with assets/employer-home/. The\n"
  "  package selector, Events stepper, cart links, and mobile drawer are\n"
  "  reinstated with a small inline script using the live page's own data.\n-->\n", 1)

open(OUT, "w", encoding="utf-8").write(s)
print(f"{'label':<38} matches")
for l, n in log: print(f"  {l:<36} {n}")
print(f"\nchars {orig:,} -> {len(s):,}  ({len(s)-orig:+,})")
