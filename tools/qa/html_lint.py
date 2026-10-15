"""Static checks on every page: well-formed HTML, unique ids, resolvable links and images,
alt text, heading order. No browser needed.  Run: python3 tools/qa/html_lint.py"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VOID={'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
SVGVOID=set()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.errs=[]; s.ids={}; s.refs=[]; s.imgs=[]; s.heads=[]; s.insvg=0; s.cur=None; s.htext=''
    def handle_starttag(s,t,a):
        a=dict(a); ln=s.getpos()[0]
        if t=='svg': s.insvg+=1
        if 'id' in a:
            s.ids.setdefault(a['id'],[]).append(ln)
        for k in ('href','src','srcset','poster'):
            if k in a and a[k] is not None: s.refs.append((t,k,a[k],ln))
        if t=='img': s.imgs.append((a,ln))
        if re.fullmatch(r'h[1-6]',t): s.cur=(t,ln); s.htext=''
        if t in VOID: return
        if s.insvg and t!='svg' and False: pass
        s.stack.append((t,ln))
    def handle_startendtag(s,t,a):
        a=dict(a); ln=s.getpos()[0]
        if 'id' in a: s.ids.setdefault(a['id'],[]).append(ln)
        for k in ('href','src'):
            if k in a and a[k] is not None: s.refs.append((t,k,a[k],ln))
        if t=='img': s.imgs.append((a,ln))
    def handle_endtag(s,t):
        ln=s.getpos()[0]
        if t in VOID: return
        if re.fullmatch(r'h[1-6]',t) and s.cur: s.heads.append((s.cur[0],s.cur[1],s.htext.strip()[:60])); s.cur=None
        if t=='svg': s.insvg-=1
        if not s.stack: s.errs.append(f'L{ln}: stray </{t}>'); return
        if s.stack[-1][0]==t: s.stack.pop(); return
        # implicit closes allowed for p/li
        names=[x[0] for x in s.stack]
        if t in names:
            while s.stack and s.stack[-1][0]!=t:
                o=s.stack.pop()
                if o[0] not in ('p','li','option','tr','td','th','thead','tbody','dt','dd'): s.errs.append(f'L{ln}: </{t}> closes unclosed <{o[0]}> from L{o[1]}')
            s.stack.pop()
        else: s.errs.append(f'L{ln}: stray </{t}>')
    def handle_data(s,d):
        if s.cur: s.htext+=d
def exists(url, page):
    u=urlparse(url)
    if u.scheme in ('http','https','mailto','tel','data','javascript') or url.startswith('//'): return None
    path=unquote(u.path)
    if path=='' : return True
    if path in ('./','/'): path='index.html'
    p=os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
    for c in (p, p+'.html', os.path.join(p,'index.html')):
        if os.path.isfile(c): return True
    return False
for f in sorted(x for x in os.listdir(ROOT) if x.endswith('.html')):
    src=open(os.path.join(ROOT,f)).read()
    p=P(); p.feed(src)
    print('=====',f)
    for e in p.errs[:20]: print('  TAG',e)
    for t,ln in p.stack: print('  UNCLOSED',t,'L',ln)
    for i,l in p.ids.items():
        if len(l)>1: print('  DUP-ID',i,l)
    for t,k,v,ln in p.refs:
        vals=[x.strip().split(' ')[0] for x in v.split(',')] if k=='srcset' else [v]
        for v2 in vals:
            if v2.startswith('#'):
                if v2[1:] and v2[1:] not in p.ids: print('  BAD-ANCHOR',v2,'L',ln)
                continue
            r=exists(v2,f)
            if r is False: print('  MISSING',k,v2,'L',ln)
    for a,ln in p.imgs:
        if 'alt' not in a: print('  IMG-NO-ALT L',ln,a.get('src'))
        if 'width' not in a or 'height' not in a: print('  IMG-NO-DIMS L',ln,a.get('src'))
    print('  HEADINGS:',' > '.join(f"{h}" for h,_,_ in p.heads))
