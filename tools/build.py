"""Make every page load in about one round trip.

Run from the repo root after editing assets/css/, assets/js/site.js or page text:  python3 tools/build.py

  1. Inlines assets/css/site.css, assets/css/sections.css and assets/js/site.js into each page, so the browser
     needs nothing else before it can paint (the page itself is the only blocking request).
  2. Cuts the Sourcerer serif down to exactly the characters each page uses, as WOFF2,
     and preloads those files so the serif arrives alongside the HTML.
  3. Cuts Inter (body text) and Geist Mono (labels) down to every character any page can show,
     once for the whole site, so all pages share (and cache) the same two small files. Serving
     the type ourselves is what makes Mac, Windows, Linux, iOS and Android all look the same.

Sources stay where they are; the build rewrites the marked blocks in each page in place, so
it is safe to run as often as you like.
"""
import hashlib, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
try:
    import brotli  # noqa: F401
except ImportError:
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'vendor'))
from fontTools import subset
from fontTools.ttLib import TTFont

PAGES = ['index', 'about', 'contact', 'press', 'listen', 'privacy', 'accessibility', 'credits', '404']
FACES = {  # face key -> (source file, weight, style)
    'regular': ('assets/fonts/sourcerer-regular.woff', 400, 'normal'),
    'italic': ('assets/fonts/sourcerer-italic.woff', 400, 'italic'),
    'bold': ('assets/fonts/sourcerer-bold.woff', 700, 'normal'),
}
# Faces each page sets in the serif (found by checking computed styles on every element)
USES = {'index': ['regular', 'italic', 'bold']}
OUT = 'assets/fonts/sub'
# Sans and mono, shared by every page: (key, source, family, style, preload)
SHARED = [
    ('sans', 'assets/fonts/inter-variable.woff2', 'Inter', 'normal', True),
    ('sans-italic', 'assets/fonts/inter-variable-italic.woff2', 'Inter', 'italic', False),
    ('mono', 'assets/fonts/geist-mono-variable.woff2', 'Geist Mono', 'normal', True),
]
SHARED_EXTRA = set('–—‘’“”…·×→←↗↘↑↓°±²³µ€£©®™−≈≤≥✓')
# Arial (Windows, Mac), Liberation Sans / Arimo (Linux) and Helvetica stretched to Inter's size,
# so text barely moves in the moment before Inter arrives.
FALLBACK = ('  @font-face { font-family: "Inter fallback"; src: local("Arial"), local("ArialMT"), local("Liberation Sans"), '
            'local("Arimo"), local("Helvetica"); size-adjust: 107.4%; ascent-override: 90.2%; descent-override: 22.5%; '
            'line-gap-override: 0%; }')


def page_chars(src):
    """Every character the page could show: its text, attributes and script strings, plus ASCII."""
    text = html.unescape(re.sub(r'<[^>]+>', ' ', src)) + ' ' + html.unescape(src)
    chars = {c for c in text if ord(c) >= 0x20}
    chars |= {chr(c) for c in range(0x20, 0x7f)}
    chars |= set('–—‘’“”…·×→←↗°')
    return ''.join(sorted(chars))


SAFETY = set('0123456789 .,:;!?\'"()[]-–—‘’“”…&%/+')


def serif_chars(page):
    """The characters each face really sets on the page, read from computed styles in a headless
    browser after the page's scripts have run (so drawn charts and hidden panels count too).
    Returns None when Playwright isn't available; the build then falls back to page_chars()."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    js = """() => { const o = {regular: '', italic: '', bold: ''};
      for (const e of document.querySelectorAll('body *')) {
        const t = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.data).join('');
        if (!t.trim()) continue;
        const s = getComputedStyle(e);
        if (!/Sourcerer/.test(s.fontFamily.split(',')[0])) continue;
        o[s.fontStyle === 'italic' ? 'italic' : (+s.fontWeight >= 600 ? 'bold' : 'regular')] += t;
      } return o; }"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        out = {}
        for theme in ('light', 'dark'):
            for w in (390, 1280):
                pg = b.new_page(viewport={'width': w, 'height': 900}, color_scheme=theme)
                pg.goto('file://' + os.path.join(ROOT, page + '.html'))
                pg.wait_for_timeout(600)
                for k, v in pg.evaluate(js).items():
                    out[k] = out.get(k, '') + v
                pg.close()
        b.close()
    return {k: ''.join(sorted(set(v) | SAFETY)) for k, v in out.items()}


def make_subset(face, chars, page):
    src = FACES[face][0]
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['kern', 'liga', 'calt', 'onum', 'lnum', 'tnum', 'case']
    opts.hinting = False
    opts.desubroutinize = True
    opts.name_IDs = []
    opts.notdef_outline = True
    font = subset.load_font(src, opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, f'_{page}-{face}.woff2')
    subset.save_font(font, tmp, opts)
    data = open(tmp, 'rb').read()
    name = f'{page}-{face}.{hashlib.sha1(data).hexdigest()[:8]}.woff2'
    os.replace(tmp, os.path.join(OUT, name))
    return name, len(data)


def make_shared(key, src, chars):
    """One subset of a variable face for the whole site (axes kept, so every weight still works)."""
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['kern', 'liga', 'calt', 'ccmp', 'locl', 'mark', 'mkmk', 'rvrn', 'case',
                            'tnum', 'lnum', 'pnum', 'frac', 'numr', 'dnom', 'sups', 'subs']
    opts.hinting = False
    opts.desubroutinize = True
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6]
    opts.notdef_outline = True
    font = subset.load_font(src, opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, f'_{key}.woff2')
    subset.save_font(font, tmp, opts)
    data = open(tmp, 'rb').read()
    name = f'{key}.{hashlib.sha1(data).hexdigest()[:8]}.woff2'
    os.replace(tmp, os.path.join(OUT, name))
    return name, len(data)


def block(s, start, end, new):
    """Replace the text between two marker strings (inclusive), or fail loudly."""
    a = s.index(start); b = s.index(end, a) + len(end)
    return s[:a] + new + s[b:]


def minify_css(css):
    """Comments and spare whitespace out; the readable source stays in assets/css/."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    return css.replace(';}', '}').strip()


def inline_css(s, href):
    path = href
    css = minify_css(open(path, encoding='utf-8').read())
    tag = f'<style data-src="{path}">\n{css}\n</style>'
    if f'<style data-src="{path}">' in s:
        return re.sub(r'<style data-src="' + re.escape(path) + r'">.*?</style>', lambda m: tag, s, count=1, flags=re.S)
    m = re.search(r'<link rel="stylesheet" href="' + re.escape(path) + r'(\?v=\d+)?">', s)
    if not m:
        return s
    return s[:m.start()] + tag + s[m.end():]


def inline_js(s, path):
    js = open(path, encoding='utf-8').read().strip()
    tag = f'<script data-src="{path}">\n{js}\n</script>'
    if f'<script data-src="{path}">' in s:
        return re.sub(r'<script data-src="' + re.escape(path) + r'">.*?</script>', lambda m: tag, s, count=1, flags=re.S)
    m = re.search(r'<script src="' + re.escape(path) + r'(\?v=\d+)?" defer></script>', s)
    if not m:
        return s
    return s[:m.start()] + tag + s[m.end():]


def main():
    keep = set()
    texts = {}
    # 1. inline the shared CSS and JS, and write the pages so the browser-based checks below read current styles
    for page in PAGES:
        fn = page + '.html'
        if not os.path.exists(fn):
            continue
        s = open(fn, encoding='utf-8').read()
        s = inline_css(s, 'assets/css/site.css')
        s = inline_css(s, 'assets/css/sections.css')
        s = inline_js(s, 'assets/js/site.js')
        open(fn, 'w', encoding='utf-8').write(s)
        texts[page] = s

    # 2. Inter and Geist Mono: one subset each for the whole site
    chars = set(SHARED_EXTRA)
    for s in texts.values():
        chars |= set(page_chars(s))
    chars = ''.join(sorted(chars))
    shared = []
    for key, src, fam, style, preload in SHARED:
        name, size = make_shared(key, src, chars)
        keep.add(name)
        shared.append((key, name, fam, style, preload))
        print(f'{key}: {size / 1024:.1f} KB ({len(chars)} characters, shared by every page)')

    # 3. per page: the serif subsets where used, then the @font-face rules and preloads
    for page, s in texts.items():
        fn = page + '.html'
        root = '/' if page == '404' else ''          # the 404 page is served at any depth
        ff, pre, report = [FALLBACK], [], []
        for key, name, fam, style, preload in shared:
            ff.append(f'  @font-face {{ font-family: "{fam}"; src: url("{root}{OUT}/{name}") format("woff2"); '
                      f'font-weight: 100 900; font-style: {style}; font-display: swap; }}')
            if preload:
                pre.append(f'<link rel="preload" href="{root}{OUT}/{name}" as="font" type="font/woff2" crossorigin>')
        faces = USES.get(page, [])
        if faces:
            live = serif_chars(page)
            pchars = page_chars(s)
            for face in faces:
                name, size = make_subset(face, live[face] if live else pchars, page)
                keep.add(name)
                _, w, st = FACES[face]
                ff.append(f'  @font-face {{ font-family: "Sourcerer"; src: url("{root}{OUT}/{name}") format("woff2"); '
                          f'font-weight: {w}; font-style: {st}; font-display: swap; }}')
                pre.append(f'<link rel="preload" href="{root}{OUT}/{name}" as="font" type="font/woff2" crossorigin>')
                report.append(f'{face} {size / 1024:.1f} KB')
        fonts = '  /* @fonts: written by tools/build.py (Inter and Geist Mono shared; serif subset to this page) */\n' + '\n'.join(ff) + '\n  /* @fonts:end */'
        if '/* @fonts:' in s:
            s = block(s, "  /* @fonts:", "/* @fonts:end */", fonts)
        else:
            s = s.replace('<style', '<style>\n' + fonts + '\n</style>\n<style', 1)
        pre_html = '<!-- @preload -->\n' + '\n'.join(pre) + '\n<!-- @preload:end -->'
        if '<!-- @preload -->' in s:
            s = block(s, '<!-- @preload -->', '<!-- @preload:end -->', pre_html)
        else:
            s = re.sub(r'(<meta name="viewport"[^>]*>\n)', lambda m: m.group(1) + pre_html + '\n', s, count=1)
        if report:
            print(f'{fn}: serif ' + ', '.join(report))
        open(fn, 'w', encoding='utf-8').write(s)
    for f in os.listdir(OUT) if os.path.isdir(OUT) else []:
        if f not in keep:
            os.remove(os.path.join(OUT, f))


if __name__ == '__main__':
    main()
