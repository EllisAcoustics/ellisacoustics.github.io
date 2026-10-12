"""Convert uploaded logos to the site's single ink colour on transparency.

mode "alpha": the logo's shape comes from its transparency (white or coloured
              logos on a transparent background).
mode "dark":  the logo's shape comes from how dark each pixel is (logos on a
              white background, or logos whose white parts should become holes).
crop:         optional (left, top, right, bottom) box applied before trimming.
"""
import os, sys
from PIL import Image, ImageChops

INK = (0x1A, 0x1A, 0x18)

def mono(src, dst, mode, crop=None, gain=1.6, max_size=(320, 112)):
    im = Image.open(src).convert('RGBA')
    if crop:
        im = im.crop(crop)
    r, g, b, a = im.split()
    if mode == 'alpha':
        ink = a
    else:
        lum = Image.merge('RGB', (r, g, b)).convert('L')
        ink = ImageChops.invert(lum).point(lambda v: min(255, int(v * gain)))
        ink = ImageChops.multiply(ink, a)
    ink = ink.point(lambda v: 0 if v < 12 else v)
    ink = ink.crop(ink.getbbox())
    out = Image.new('RGBA', ink.size, INK + (0,))
    out.putalpha(ink)
    out.thumbnail(max_size, Image.LANCZOS)
    out.save(dst, optimize=True)
    return out.size

JOBS = [
    # Organisation logos (logos/)
    ('logos/originals/defra-square-logo.jpg', 'logos/defra.png', 'dark', None),
    ('logos/originals/nc-logo-white.png', 'logos/noise-consultants.png', 'alpha', (0, 0, 210, 56)),  # circle + "Noise Consultants" only
    ('logos/originals/dyson.png', 'logos/dyson.png', 'dark', None),
    ('logos/originals/HEAD Acoustic PNG 1.png', 'logos/head-acoustics.png', 'alpha', None),
    ('logos/originals/635154aa7d0a29b74a04207a_Joby.png', 'logos/joby-aviation.png', 'alpha', None),
    ('logos/originals/Arcani_logo_v2_white.png', 'logos/arcani.png', 'alpha', None),
    ('logos/originals/Logo-NASA-500x416.jpg', 'logos/nasa.png', 'dark', None),
    ('logos/originals/NNP_logo_M_C-scaled-1-1024x512.jpg', 'logos/noise-network-plus.png', 'alpha', None),
    ('logos/originals/6cC0RRGY_400x400.png', 'logos/young-acousticians-network.png', 'dark', None),
    # Software logos (software/)
    ('software/originals/FME.png', 'software/fme.png', 'alpha', None),
    ('software/originals/REAPER_logo.png', 'software/reaper.png', 'dark', None),
    ('software/originals/maxresdefault.jpg', 'software/artemis.png', 'dark', (0, 0, 1280, 475)),  # the A mark only, no wordmark
]

if __name__ == '__main__':
    only = set(sys.argv[1:])
    for src, dst, mode, crop in JOBS:
        if only and dst not in only:
            continue
        print(f'{src:55} -> {dst} {mono(src, dst, mode, crop, gain=2.2 if "REAPER" in src else 1.6, max_size=(160, 160) if dst.startswith("software/") else (320, 112))}')
