"""WCAG 2.2 AA colour-contrast audit of all visible text, in light and dark mode.
Needs the site served on :8765 (make serve).  Run: python3 tools/qa/contrast.py"""
from playwright.sync_api import sync_playwright
CON=r"""() => {
  const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const parse = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const L = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const bgOf = (e) => { let base = null; const layers = []; for (let n = e; n; n = n.parentElement) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; } } let out = layers.length && layers[layers.length-1].a>=1 ? layers.pop() : parse(getComputedStyle(document.body).backgroundColor);
    while (layers.length) { const c = layers.pop(); out = { r: c.r*c.a+out.r*(1-c.a), g: c.g*c.a+out.g*(1-c.a), b: c.b*c.a+out.b*(1-c.a), a:1 }; } return out; };
  const res = [], seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const e = t.parentElement; if (!e || seen.has(e)) continue; seen.add(e);
    if (e.closest('#intro, .visually-hidden, script, style, [aria-hidden="true"], .print-only, svg title')) continue;
    const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    let op = 1; for (let n = e; n; n = n.parentElement) op *= +getComputedStyle(n).opacity; if (op < 0.5) continue;
    if (cs.webkitTextFillColor && cs.webkitTextFillColor.includes('0, 0, 0, 0')) continue; // gradient text
    let fg = parse(e.tagName === 'text' || e.closest('svg') ? cs.fill : cs.color); if (!fg) continue;
    const bg = bgOf(e);
    if (fg.a < 1) fg = { r: fg.r*fg.a+bg.r*(1-fg.a), g: fg.g*fg.a+bg.g*(1-fg.a), b: fg.b*fg.a+bg.b*(1-fg.a) };
    const l1 = L(fg), l2 = L(bg), ratio = (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
    const size = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
    const need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
    if (ratio < need) res.push(`${ratio.toFixed(2)} < ${need}  ${e.tagName.toLowerCase()}.${(typeof e.className==='string'?e.className:'')}  "${t.textContent.trim().slice(0,40)}"  ${cs.color}`);
  }
  return [...new Set(res)];
}"""
OTHER=r"""() => {
  const o = [];
  document.querySelectorAll('[tabindex]').forEach((e) => { if (+e.getAttribute('tabindex') > 0) o.push('tabindex>0: ' + e.outerHTML.slice(0, 80)); });
  document.querySelectorAll('[aria-hidden="true"] a[href], [aria-hidden="true"] button, [aria-hidden="true"] [tabindex="0"], [aria-hidden="true"] input').forEach((e) => { if (!e.closest('#intro')) o.push('focusable in aria-hidden: ' + e.outerHTML.slice(0, 80)); });
  ['main', 'header', 'footer', 'nav', 'h1'].forEach((t) => { if (!document.querySelector(t)) o.push('missing ' + t); });
  if (document.querySelectorAll('h1').length > 1) o.push('multiple h1');
  if (!document.documentElement.lang) o.push('no lang');
  document.querySelectorAll('a[target="_blank"]').forEach((a) => { if (!/noopener/.test(a.rel)) o.push('blank without noopener ' + a.href); });
  return o;
}"""
def names(pg):
    cdp=pg.context.new_cdp_session(pg); tree=cdp.send('Accessibility.getFullAXTree')['nodes']; out=[]
    for n in tree:
        if n.get('ignored'): continue
        role=n.get('role',{}).get('value'); name=(n.get('name') or {}).get('value','')
        if role in ('link','button','switch','radio','slider','checkbox','img','image','textbox','combobox','listitem') and not str(name).strip():
            if role=='listitem': continue
            out.append(f"{role} with no name (backend {n.get('backendDOMNodeId')})")
    return out
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ['index.html','about.html','contact.html','press.html','listen.html','privacy.html','accessibility.html','credits.html']:
        for scheme in ('light','dark'):
            pg=b.new_page(viewport={'width':1280,'height':900},color_scheme=scheme,reduced_motion='reduce')
            pg.goto('http://localhost:8765/'+f); pg.wait_for_timeout(500)
            c=pg.evaluate(CON)
            print(f'== {f} {scheme}: {len(c)} contrast issues'); [print('   ',x) for x in c[:25]]
            if scheme=='light':
                for x in pg.evaluate(OTHER)+names(pg): print('   ',x)
            pg.close()
    b.close()
