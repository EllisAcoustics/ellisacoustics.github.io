/* ==========================================================================
   ellisacoustics.github.io: shared behaviour
   The theme itself is set by a tiny inline script in each page's <head>, so
   the page never flashes the wrong colours. This file adds the switch, keeps
   the tab icon and browser bar in step with it, and says hello in the console.
   ========================================================================== */
(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');

  // Tab icon and browser bar follow the theme, including the visitor's own choice from the switch
  const syncChrome = () => {
    const dark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('meta[name="theme-color"]').forEach((m) => m.setAttribute('content', dark ? '#0B0B0C' : '#F7F6F2'));
    document.querySelectorAll('link[rel="icon"][type="image/svg+xml"]').forEach((l) => l.setAttribute('href', dark ? 'favicon.svg' : 'favicon-light.svg'));
    if (toggle) toggle.setAttribute('aria-checked', dark ? 'true' : 'false');
    // SVG <animate> colour sequences cannot read CSS variables, so they take the theme's viridis steps here
    const cs = getComputedStyle(root);
    document.querySelectorAll('animate[data-vr]').forEach((a) => a.setAttribute('values', a.dataset.vr.split(';').map((i) => cs.getPropertyValue('--vr' + i).trim()).join(';')));
  };
  if (toggle) toggle.addEventListener('click', () => window.__setTheme && window.__setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  new MutationObserver(syncChrome).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  syncChrome();

  // Pages start loading the moment a link is hovered, pressed or focused, so a click feels instant.
  // Chromium gets a speculation rule (its prefetch survives into the navigation); others a plain prefetch.
  const PAGE = /^\/(index|about|contact|press|listen|privacy|accessibility|credits)?(\.html)?$/;
  let spec = false;
  try { spec = HTMLScriptElement.supports && HTMLScriptElement.supports('speculationrules'); } catch (e) {}
  const warmed = new Set([location.pathname.replace(/\.html$/, '')]);
  const warm = (e) => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.origin !== location.origin || !PAGE.test(a.pathname)) return;
    const path = a.pathname.replace(/\.html$/, '');
    if (warmed.has(path)) return;
    warmed.add(path);
    const url = a.origin + a.pathname;
    if (spec) {
      const rule = document.createElement('script');
      rule.type = 'speculationrules';
      rule.textContent = JSON.stringify({ prefetch: [{ source: 'list', urls: [url] }] });
      document.head.appendChild(rule);
    } else {
      const link = document.createElement('link');
      link.rel = 'prefetch'; link.href = url;
      document.head.appendChild(link);
    }
  };
  ['pointerover', 'touchstart', 'focusin'].forEach((t) => document.addEventListener(t, warm, { passive: true, capture: true }));

  // Even line lengths: no wrapped line of text is shorter than 80% of the longest line in its block
  // (in a paragraph of more than six lines, its last line). CSS text-wrap: balance does most of this;
  // browsers stop balancing after about six lines and are sometimes loose, so a block that still fails
  // gets the measure (and, if need be, a hair of word spacing) that evens it out. Trial widths are laid
  // out on a hidden copy in an isolated sandbox, so the page itself never reflows while searching, and
  // a block only changes its number of lines when it is well below the screen (no visible shift).
  // Screen only: the printed CV keeps its own measure.
  const SEL = 'p, li, figcaption, dd, dt, blockquote, h1, h2, h3, h4, td, th, summary';
  let painted = false;   // before the first paint a block may change its number of lines; after it, only off screen
  const lineWidths = (el) => {
    const rg = document.createRange(); rg.selectNodeContents(el);
    const L = [];
    for (const q of rg.getClientRects()) {
      if (q.width < 0.5 || q.height < 4) continue;
      const k = q.top + q.height / 2, l = L.find((x) => Math.abs(x.k - k) < q.height * 0.45);
      if (!l) L.push({ k, a: q.left, b: q.right }); else { l.a = Math.min(l.a, q.left); l.b = Math.max(l.b, q.right); }
    }
    return L.sort((x, y) => x.k - y.k).map((x) => x.b - x.a);
  };
  const ratio = (ws) => (ws.length < 2 ? 1 : (ws.length > 6 ? ws[ws.length - 1] : Math.min(...ws)) / Math.max(...ws));
  const even = (ws) => ratio(ws) >= 0.8;
  const flowsText = (el) => {
    if (el.closest('svg, nav, #intro, .courier, .no-bal')) return false;
    const cs = getComputedStyle(el);
    if (cs.display.startsWith('inline') || cs.whiteSpace === 'nowrap') return false;
    if (parseFloat(cs.borderLeftWidth) > 0 || !/rgba\(.*, 0\)|transparent/.test(cs.backgroundColor)) return false;   // boxes keep their size
    return [...el.children].every((c) => c.tagName === 'BR' || getComputedStyle(c).display.startsWith('inline'));
  };
  const TYPE = ['font-family', 'font-size', 'font-weight', 'font-style', 'font-stretch', 'font-variant', 'font-feature-settings',
    'font-variation-settings', 'font-optical-sizing', 'font-kerning', 'line-height', 'letter-spacing', 'word-spacing', 'text-transform',
    'hyphens', '-webkit-hyphens', 'white-space', 'vertical-align', 'padding-left', 'padding-right', 'margin-left', 'margin-right', 'display'];
  let box;
  const sandbox = () => {
    if (!box) {
      box = document.createElement('div'); box.setAttribute('aria-hidden', 'true');
      box.style.cssText = 'position:fixed;left:-10000px;top:0;width:0;height:0;overflow:hidden;visibility:hidden;contain:strict;pointer-events:none';
      document.body.appendChild(box);
    }
    return box;
  };
  const copyOf = (el) => {   // a typographically identical copy, every inline run carrying its own computed type
    const c = el.cloneNode(true), src = [el, ...el.querySelectorAll('*')], dst = [c, ...c.querySelectorAll('*')];
    src.forEach((s, i) => { const cs = getComputedStyle(s), d = dst[i]; d.removeAttribute('id'); d.removeAttribute('class');
      TYPE.forEach((k) => d.style.setProperty(k, cs.getPropertyValue(k))); });
    c.style.cssText += ';position:absolute;left:0;top:0;margin:0;padding:0;border:0;box-sizing:content-box;text-wrap:wrap;max-width:none;display:block';
    sandbox().appendChild(c);
    return c;
  };
  const search = (el, ws, mayReflow) => {
    const n = ws.length, cs = getComputedStyle(el);
    const C = el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const c = copyOf(el);
    const at = (t) => { c.style.width = t + 'px'; return lineWidths(c); };
    let best = { r: ratio(at(C)), t: 0, sp: 0 };
    const counts = mayReflow ? [n, n - 1, n + 1] : [n];   // near the screen, the number of lines never changes
    for (const sp of [0, 0.05, -0.03, 0.1]) {             // width first; then a hair of word spacing (about a pixel) moves one word across a break
      c.style.wordSpacing = sp ? sp + 'em' : cs.wordSpacing;
      for (const m of counts) {
        if (m < 2) continue;
        const floor = C * (m > n ? 0.8 : 0.6);            // never pinch the column much narrower than its layout
        let lo = floor, hi = C;                           // narrowest measure that still fits m lines
        if (at(hi).length > m) continue;
        while (hi - lo > 1.5) { const mid = (lo + hi) / 2; if (at(mid).length <= m) hi = mid; else lo = mid; }
        for (let i = 0; i < 10; i++) {                    // and a range of wider ones, keeping the most even
          const t = hi + (C - hi) * i / 10, w = at(t);
          if (w.length === m && ratio(w) > best.r + 0.005) best = { r: ratio(w), t, sp };
        }
        if (best.r >= 0.8) break;
      }
      if (best.r >= 0.8) break;
    }
    c.remove();
    if (!best.t) return null;
    const pad = cs.boxSizing === 'border-box' ? parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) : 0;
    return { w: best.t + pad, sp: best.sp, center: cs.textAlign === 'center' };
  };
  const apply = (el, res) => {
    el.classList.toggle('bal', !!res); el.classList.toggle('bal-c', !!(res && res.center));
    if (res) el.style.setProperty('--bal-w', res.w + 'px'); else el.style.removeProperty('--bal-w');
    el.style.wordSpacing = res && res.sp ? res.sp + 'em' : '';
  };
  const balance = (el) => {
    apply(el, null);
    if (!el.offsetWidth || !flowsText(el)) return;
    const ws = lineWidths(el);
    if (even(ws)) return;
    apply(el, search(el, ws, !painted || el.getBoundingClientRect().top > innerHeight + 200));
  };
  if (matchMedia('screen').matches) {
    // one pass over the page in idle time once fonts are in, reading in batches and writing in batches;
    // hidden text (drawers, pop-ups) is balanced when it is first shown
    const idle = window.requestIdleCallback || ((f) => setTimeout(() => f({ timeRemaining: () => 8 }), 1));
    const io = 'IntersectionObserver' in window && new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { io.unobserve(e.target); balance(e.target); } }));
    let first = true;
    const run = () => {
      const all = [...document.querySelectorAll(SEL)];
      all.forEach((el) => { if (el.classList.contains('bal')) apply(el, null); });
      const queue = [];
      all.forEach((el) => {                                // one read pass: which blocks need help
        if (!el.offsetWidth) { if (io) io.observe(el); return; }
        if (!flowsText(el)) return;
        const r = el.getBoundingClientRect();
        if (first && r.top < innerHeight && r.bottom > 0) return;   // on screen at load: done before first paint, or left to the browser (never a visible shift)
        const ws = lineWidths(el);
        if (!even(ws)) queue.push([el, ws, r.top > innerHeight + 200]);
      });
      const step = (d) => {
        const done = [];
        while (queue.length && (d.timeRemaining() > 4 || !done.length)) { const [el, ws, far] = queue.shift(); done.push([el, search(el, ws, far)]); }
        done.forEach(([el, res]) => apply(el, res));       // writes together, after the reads
        if (queue.length) idle(step);
      };
      if (queue.length) idle(step);
      first = false;
    };
    // Text on screen at load is balanced right now, before the first paint, if the fonts are already in
    // (they are preloaded); otherwise it keeps the browser's balancing so nothing moves after it is drawn.
    if (!document.fonts || document.fonts.status === 'loaded') {
      document.querySelectorAll(SEL).forEach((el) => {
        if (!el.offsetWidth) return;
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) balance(el);
      });
    }
    requestAnimationFrame(() => { painted = true; });
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => idle(run));
    let lastW = innerWidth, t;
    addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { if (innerWidth !== lastW) { lastW = innerWidth; run(); } }, 150); });
    window.__balance = balance;   // for text that is swapped in later
  }

  // The illustrated machines spin their fans, rotors and wheels with SVG animation, which CSS cannot pause;
  // visitors who ask for less motion get them still.
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) document.querySelectorAll('svg.craft').forEach((v) => v.pauseAnimations && v.pauseAnimations());

  // Tile labels show on hover only, one at a time, and never stay pinned open.
  // On touch screens a tap stands in for hover: that tile's label shows alone, then fades by itself.
  const TILES = '.itile, .vol-tile, .org-tile, .icon-tile, .int';
  let tapT;
  document.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse') return;
    const t = e.target.closest && e.target.closest(TILES);
    document.querySelectorAll('.tap-hover').forEach((x) => { if (x !== t) x.classList.remove('tap-hover'); });
    clearTimeout(tapT);
    if (t) { t.classList.add('tap-hover'); tapT = setTimeout(() => t.classList.remove('tap-hover'), 2500); }
  }, { passive: true });

  // For the developers who open the console
  try {
    console.log(
      '%c▁▂▃▅▇█▇▅▃▂▁▂▃▅▇▅▃▂▁  Max Ellis · psychoacoustics\n%cHand-built: no frameworks, no trackers, no cookies. The CV PDF is printed from these pages.\nLooking for someone who can hear the future? ellisacoustics.github.io/contact',
      'font: 600 13px ui-monospace, monospace; color: #3FAE3A',
      'font: 12px ui-monospace, monospace; color: inherit'
    );
  } catch (e) {}
})();
