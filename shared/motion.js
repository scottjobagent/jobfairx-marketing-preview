/* ==========================================================================
   JobFairX Marketing — shared motion layer
   Vanilla, no dependencies, no build step. Everything is transform/opacity
   only, driven by a single rAF loop, so it stays on the compositor.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mark the document as script-capable straight away. base.css only hides
  // [data-reveal] under `.js`, so if this file never runs the page still
  // renders fully instead of staying blank.
  document.documentElement.classList.add('js');

  /* ---------- 1. scroll reveal --------------------------------------------
     Stagger comes from a --i custom property set in markup, so the CSS owns
     the timing and JS only toggles a class. */
  function initReveal() {
    var items = document.querySelectorAll('[data-reveal]');
    if (!items.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);           // reveal once, never re-hide
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 2. pointer parallax -----------------------------------------
     One rAF loop for every layer. Each layer declares a depth; we lerp toward
     the pointer so it glides instead of snapping. Translation only — the
     research was unanimous that perspective-skewing product UI reads dated. */
  function initParallax() {
    var layers = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
    if (!layers.length || reduced) return;
    if (window.matchMedia('(pointer: coarse)').matches) return;  // no hover on touch

    var tx = 0, ty = 0, cx = 0, cy = 0, running = false;
    var LERP = 0.08;

    function onMove(e) {
      // -1..1 from viewport centre
      tx = (e.clientX / window.innerWidth - 0.5) * 2;
      ty = (e.clientY / window.innerHeight - 0.5) * 2;
      if (!running) { running = true; requestAnimationFrame(tick); }
    }

    function tick() {
      cx += (tx - cx) * LERP;
      cy += (ty - cy) * LERP;
      for (var i = 0; i < layers.length; i++) {
        var el = layers[i];
        var d = parseFloat(el.getAttribute('data-parallax')) || 0;
        el.style.transform = 'translate3d(' + (-cx * d).toFixed(2) + 'px,' +
                                              (-cy * d).toFixed(2) + 'px,0)';
      }
      if (Math.abs(tx - cx) > 0.001 || Math.abs(ty - cy) > 0.001) {
        requestAnimationFrame(tick);
      } else {
        running = false;
      }
    }

    window.addEventListener('pointermove', onMove, { passive: true });
  }

  /* ---------- 3. sticky nav state -----------------------------------------
     A sentinel above the nav tells us when we've left the top, and sentinels
     inside each section tell the nav which theme it is currently sitting on,
     so it can invert without hardcoding scroll offsets. */
  function initNav() {
    var nav = document.querySelector('[data-nav]');
    if (!nav) return;

    var top = document.createElement('div');
    top.style.cssText = 'position:absolute;top:0;height:1px;width:1px;';
    document.body.prepend(top);

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        nav.classList.toggle('is-stuck', !e[0].isIntersecting);
      }).observe(top);

      // theme inversion: whichever themed section owns the nav band
      var sections = document.querySelectorAll('[data-theme]');
      var band = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          nav.setAttribute('data-on', e.target.getAttribute('data-theme'));
        });
      }, { rootMargin: '-32px 0px -95% 0px' });
      sections.forEach(function (s) { band.observe(s); });
    }

    // mobile drawer
    var toggle = document.querySelector('[data-nav-toggle]');
    var drawer = document.querySelector('[data-nav-drawer]');
    if (toggle && drawer) {
      toggle.addEventListener('click', function () {
        var open = drawer.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
      });
      drawer.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          drawer.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
          document.body.style.overflow = '';
        }
      });
    }
  }

  /* ---------- 4. tab groups (interview formats, capability grid) ---------- */
  function initTabs() {
    document.querySelectorAll('[data-tabs]').forEach(function (group) {
      var tabs = group.querySelectorAll('[data-tab]');
      var panes = group.querySelectorAll('[data-pane]');

      function select(key) {
        tabs.forEach(function (t) {
          var on = t.getAttribute('data-tab') === key;
          t.classList.toggle('is-active', on);
          t.setAttribute('aria-selected', String(on));
          t.tabIndex = on ? 0 : -1;
        });
        panes.forEach(function (p) {
          p.classList.toggle('is-active', p.getAttribute('data-pane') === key);
        });
      }

      tabs.forEach(function (t, i) {
        t.addEventListener('click', function () { select(t.getAttribute('data-tab')); });
        t.addEventListener('keydown', function (e) {
          var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
          if (!d) return;
          e.preventDefault();
          var next = tabs[(i + d + tabs.length) % tabs.length];
          next.focus(); select(next.getAttribute('data-tab'));
        });
      });
    });
  }

  /* ---------- 5. sticky journey ------------------------------------------
     The 7 steps scroll while one visual stays pinned; whichever step is in
     the middle band owns the visual. */
  function initJourney() {
    var root = document.querySelector('[data-journey]');
    if (!root || !('IntersectionObserver' in window)) return;
    var steps = root.querySelectorAll('[data-step]');
    var shots = root.querySelectorAll('[data-shot]');
    if (!steps.length) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var k = e.target.getAttribute('data-step');
        steps.forEach(function (s) { s.classList.toggle('is-active', s === e.target); });
        shots.forEach(function (s) { s.classList.toggle('is-active', s.getAttribute('data-shot') === k); });
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (s) { io.observe(s); });
  }

  /* ---------- 6. stat count-up -------------------------------------------
     The final value is already in the HTML. We animate FROM a lower number up
     to the value we read out of the DOM, never toward a JS-held constant — a
     failed script then shows the real figure rather than a zero. */
  function initCounters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length || reduced || !('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var el = e.target;
        var text = el.textContent;
        var m = text.match(/([\d,.]+)/);
        if (!m) return;
        var target = parseFloat(m[1].replace(/,/g, ''));
        if (!isFinite(target)) return;
        var decimals = (m[1].split('.')[1] || '').length;
        var start = performance.now(), dur = 900;

        var done = false;
        function settle() {
          if (done) return;
          done = true;
          el.textContent = text;           // land exactly on the authored value
        }

        function frame(now) {
          if (done) return;
          var p = Math.min(1, (now - start) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          var val = (target * eased).toFixed(decimals);
          if (!decimals) val = Math.round(target * eased).toLocaleString();
          el.textContent = text.replace(m[1], val);
          if (p < 1) requestAnimationFrame(frame);
          else settle();
        }
        requestAnimationFrame(frame);

        // Hard guard. If rAF stalls — background tab, throttling, a headless
        // renderer where performance.now() doesn't advance — the number must
        // still end up correct rather than frozen on a fake-precise midpoint
        // like "475,059+". A wrong statistic is worse than no animation.
        setTimeout(settle, dur + 400);
      });
    }, { threshold: 0.5 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 7. annotated screenshots ------------------------------------
     Pins and captions are paired by a shared data-anno value. Hovering or
     focusing either side lights both, so the association works with a mouse,
     a keyboard and a screen reader — not just on hover. */
  function initAnno() {
    document.querySelectorAll('.anno').forEach(function (fig) {
      var pins = fig.querySelectorAll('.anno__pin');
      var keys = fig.querySelectorAll('.anno__key li');
      if (!pins.length) return;

      function light(key, on) {
        pins.forEach(function (p) {
          if (p.getAttribute('data-anno') === key) p.classList.toggle('is-on', on);
        });
        keys.forEach(function (k) {
          if (k.getAttribute('data-anno') === key) k.classList.toggle('is-on', on);
        });
      }

      function bind(el) {
        var key = el.getAttribute('data-anno');
        if (!key) return;
        ['mouseenter', 'focus'].forEach(function (e) {
          el.addEventListener(e, function () { light(key, true); });
        });
        ['mouseleave', 'blur'].forEach(function (e) {
          el.addEventListener(e, function () { light(key, false); });
        });
        // touch: tap a pin to pin its caption open
        el.addEventListener('click', function () {
          var already = el.classList.contains('is-on');
          pins.forEach(function (p) { p.classList.remove('is-on'); });
          keys.forEach(function (k) { k.classList.remove('is-on'); });
          if (!already) light(key, true);
        });
      }

      pins.forEach(bind);
      keys.forEach(bind);

      // wire each caption to its pin for assistive tech
      pins.forEach(function (p) {
        var key = p.getAttribute('data-anno');
        var li = fig.querySelector('.anno__key li[data-anno="' + key + '"]');
        if (!li) return;
        if (!li.id) li.id = 'anno-' + Math.random().toString(36).slice(2, 8);
        p.setAttribute('aria-describedby', li.id);
      });
    });
  }

  function init() {
    initReveal(); initParallax(); initNav();
    initTabs(); initJourney(); initCounters(); initAnno();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
