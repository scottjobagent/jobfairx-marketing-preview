#!/usr/bin/env python3
"""Build employer-footer-live.html + seeker-footer-live.html.

Each is the LIVE page (fetched Sep 1) as a visual clone — scripts stripped,
stylesheets and images inlined, YouTube embeds replaced with their poster
frames — with ONE addition: the finalized JobFairX wordmark trace inserted
into the real footer, between the link grid and the copyright bar. Nothing
else about the footer is touched.

Trace spec (locked Sep 1): base rgb(30,56,110), highlight rgba(96,165,250,.62),
width 1, dasharray L L, 5s lap on cubic-bezier(.44,0,.56,1), offset
accumulates; X pulse clipped to x1005-1185 over last 12% of lap, peak .85;
bottom fade mask; off under prefers-reduced-motion.
"""
import re, base64, sys

WORD = open("../jobfairx-word.pathd").read().strip()

def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

IMGS = {
    "/_app/immutable/assets/diversity.af0ced6e.png": "diversity.af0ced6e.png",
    "/_app/immutable/assets/entry-level.ac5531c3.png": "entry-level.ac5531c3.png",
    "/_app/immutable/assets/healthcare.d1574504.png": "healthcare.d1574504.png",
    "/_app/immutable/assets/review-confirm-mobile.f43ed302.png": "review-confirm-mobile.f43ed302.png",
    "/_app/immutable/assets/review-confirm.4d17b17e.png": "review-confirm.4d17b17e.png",
    "/_app/immutable/assets/tech.b663863c.png": "tech.b663863c.png",
    "/_app/immutable/assets/veteran.4e121597.png": "veteran.4e121597.png",
    "/_app/immutable/assets/companies.3017771d.png": "companies.3017771d.png",
    "/_app/immutable/assets/mobile-companies.ee028fce.png": "mobile-companies.ee028fce.png",
    "/jobfairx-logo.png": "jobfairx-logo.png",
}

MARK = """
<div class="jfxmark" aria-hidden="true">
  <svg viewBox="-4 -10 1256 244" role="presentation">
    <path class="jfx-base" d="__W__" fill="transparent" stroke-width="1"
      stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10"/>
    <path id="jfx-lit" d="__W__" fill="transparent" stroke-width="1"
      stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10"/>
    <clipPath id="jfx-xclip"><rect x="1005" y="-10" width="180" height="244"/></clipPath>
    <path id="jfx-xsnap" d="__W__" fill="transparent" stroke-width="1.2" opacity="0"
      clip-path="url(#jfx-xclip)" stroke-linecap="butt" stroke-linejoin="miter"/>
  </svg>
</div>
""".replace("__W__", WORD)

MARK_CSS = """
<style>
.jfxmark{position:relative;padding:56px 8px 0;
  -webkit-mask-image:linear-gradient(0deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 100%);
  mask-image:linear-gradient(0deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 100%)}
.jfxmark svg{display:block;width:100%;height:auto}
.jfx-base{stroke:rgb(30,56,110)}
#jfx-lit{stroke:rgba(96,165,250,.62)}
#jfx-xsnap{stroke:rgba(147,197,253,.9)}
</style>
"""

MARK_JS = """
<script>
(function(){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var lit=document.getElementById('jfx-lit');
  var xsnap=document.getElementById('jfx-xsnap');
  if(!lit)return;
  var L=lit.getTotalLength();
  lit.setAttribute('stroke-dasharray',L+' '+L);
  function bez(x1,y1,x2,y2){function f(t,a,b){return 3*t*(1-t)*(1-t)*a+3*t*t*(1-t)*b+t*t*t}
    return function(x){var lo=0,hi=1,t=x;for(var i=0;i<24;i++){f(t,x1,x2)<x?lo=t:hi=t;t=(lo+hi)/2}return f(t,y1,y2)}}
  var ease=bez(.44,0,.56,1);
  var DUR=5000, laps=0, t0=performance.now();
  function frame(now){
    var u=(now-t0)/DUR;
    if(u>=1){laps+=Math.floor(u);t0=now-(u%1)*DUR;u=u%1}
    lit.setAttribute('stroke-dashoffset',String(L-(laps+ease(Math.max(u,.001)))*L));
    var xo=u>.88?Math.sin((u-.88)/.12*Math.PI):0;
    xsnap.setAttribute('opacity',String(xo*.85));
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  document.addEventListener('click',function(e){
    var a=e.target.closest('a');if(a)e.preventDefault();
  });
})();
</script>
"""

ANCHOR = '<div class="pt-8 pb-12 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">'

def build(src, css_files, out, title):
    s = open(src, encoding="utf-8").read()
    n0 = len(s)

    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<link[^>]*rel="modulepreload"[^>]*>', '', s)
    s = re.sub(r'\s(?:srcset|imagesrcset|imagesizes)="[^"]*"', '', s)

    css = ""
    for c in css_files:
        t = open(c, encoding="utf-8").read()
        t = re.sub(r'@font-face\s*{[^}]*}', '', t)
        css += t + "\n"
    s = re.sub(r'<link[^>]*\.css[^>]*>', '', s)

    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family='
             'Inter:wght@300;400;500;600;700;800&display=swap">')
    inject = f"{fonts}<style>{css}</style>{MARK_CSS}"
    assert "</head>" in s
    s = s.replace("</head>", inject + "</head>", 1)

    for path, f in IMGS.items():
        if path in s:
            s = s.replace(path, data_uri(f, "image/png"))
    s = re.sub(r'<link[^>]*rel="icon"[^>]*>', '', s)

    def yt_repl(m):
        tag = m.group(0)
        vid = re.search(r'embed/([A-Za-z0-9_-]{6,})', tag)
        cls = re.search(r'class="([^"]*)"', tag)
        if not vid: return ""
        try: uri = data_uri(f"yt-{vid.group(1)}.jpg", "image/jpeg")
        except FileNotFoundError: return ""
        return (f'<img class="{cls.group(1) if cls else ""}" src="{uri}" '
                f'alt="video" style="object-fit:cover">')
    s = re.sub(r'<iframe[^>]*youtube[^>]*>\s*</iframe>', yt_repl, s)
    s = re.sub(r'<iframe[^>]*>\s*</iframe>', '', s)

    n = s.count(ANCHOR)
    assert n == 1, f"{out}: footer anchor count {n}"
    s = s.replace(ANCHOR, MARK + ANCHOR)

    assert "</body>" in s
    s = s.replace("</body>", MARK_JS + "</body>", 1)
    s = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', s, count=1)

    open(out, "w", encoding="utf-8").write(s)
    print(f"{out}: {n0//1024}KB -> {len(s)//1024}KB")

build("employer-live.html", ["app.c26c23f8.css", "HowItWorks.39bbff2d.css"],
      "employer-footer-live.html", "Employer Footer Live Preview")
build("seeker-live.html", ["app.c26c23f8.css", "2.557b8e8a.css"],
      "seeker-footer-live.html", "Seeker Footer Live Preview")
