"""Opens every page in headless Chromium (light and dark, desktop and phone widths) and fails
on console errors, failed requests or horizontal overflow.
Needs the site served on :8765 (make serve).  Run: python3 tools/qa/smoke.py"""
import json, sys
from playwright.sync_api import sync_playwright
PAGES=['index.html','about.html','contact.html','press.html','listen.html','privacy.html','accessibility.html','credits.html']
WIDTHS=[320,360,390,768,1024,1440,1920]
OVF=r"""() => {
  const W = document.documentElement.clientWidth, out = [];
  const sw = document.documentElement.scrollWidth;
  document.querySelectorAll('body *').forEach((e) => {
    if (e.closest('#intro, .visually-hidden, [aria-hidden="true"] svg, .marquee')) return;
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return;
    const r = e.getBoundingClientRect(); if (!r.width) return;
    if (r.right > W + 1 || r.left < -1) {
      // ignore children clipped by an overflow:hidden ancestor
      let p = e.parentElement, clipped = false;
      while (p && p !== document.body) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { const pr = p.getBoundingClientRect(); if (pr.right <= W + 1 && pr.left >= -1) { clipped = true; break; } } p = p.parentElement; }
      if (!clipped) out.push(e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).join('.') : '') + ` [${Math.round(r.left)}..${Math.round(r.right)}]`);
    }
  });
  return { sw, W, out: out.slice(0, 8) };
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for pg_name in PAGES:
        for w in WIDTHS:
            for scheme in (['light','dark'] if w in (390,1440) else ['light']):
                ctx=b.new_context(viewport={'width':w,'height':900},color_scheme=scheme,reduced_motion='reduce')
                pg=ctx.new_page(); errs=[]; bad=[]
                pg.on('pageerror', lambda e: errs.append('JS: '+str(e)))
                pg.on('console', lambda m: m.type in ('error','warning') and errs.append(m.type+': '+m.text))
                pg.on('response', lambda r: r.status>=400 and bad.append(f'{r.status} {r.url}'))
                pg.on('requestfailed', lambda r: bad.append('FAILED '+r.url))
                pg.goto('http://localhost:8765/'+pg_name, wait_until='networkidle'); pg.wait_for_timeout(300)
                # scroll to the bottom to trigger lazy content
                pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(400)
                o=pg.evaluate(OVF)
                if o['sw']>o['W'] or o['out'] or errs or bad:
                    print(f'{pg_name} {w} {scheme}: scrollW={o["sw"]} vw={o["W"]}', o['out'], errs[:5], bad[:5])
                ctx.close()
    b.close()
print('done')
