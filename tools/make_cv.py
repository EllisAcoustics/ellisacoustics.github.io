"""Build cv/Max-Ellis-CV.pdf from the live page's print layout.

Run from the repo root after editing index.html:
    python3 -m http.server 8765 &   # then
    python3 tools/make_cv.py
The page is rendered in light mode with reduced motion, so the intro, drone and
animations are skipped and every logo and label is shown."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(color_scheme='light', reduced_motion='reduce')
        pg = await ctx.new_page()
        await pg.goto('http://localhost:8765/index.html')
        await pg.evaluate("document.documentElement.setAttribute('data-theme','light')")
        # the animated dot of the i is placed for screen sizes; print the name as plain text
        await pg.evaluate("document.querySelector('.name [aria-hidden]').textContent = 'Max Ellis'")
        await pg.wait_for_timeout(600)
        await pg.emulate_media(media='print')
        await pg.pdf(path='cv/Max-Ellis-CV.pdf', format='A4', print_background=True,
                     prefer_css_page_size=True, display_header_footer=True,
                     header_template='<span></span>',
                     footer_template='<div style="width:100%;font:8px ui-monospace,monospace;color:#6B6A64;padding:0 14mm;display:flex;justify-content:space-between">'
                                     '<span>Max Ellis — CV</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
        await b.close()

asyncio.run(main())
