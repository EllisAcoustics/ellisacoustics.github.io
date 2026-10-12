import sys, os
from PIL import Image, ImageChops
INK = (0x1A, 0x1A, 0x18)
src_dir, out_dir = sys.argv[1], sys.argv[2]
mapping = {
  'defra-square-logo.jpg': 'defra',
  'nc-logo-white.png': 'noise-consultants',
  'dyson.png': 'dyson',
  'HEAD Acoustic PNG 1.png': 'head-acoustics',
  '635154aa7d0a29b74a04207a_Joby.png': 'joby-aviation',
  'Arcani_logo_v2_white.png': 'arcani',
  'Logo-NASA-500x416.jpg': 'nasa',
  'NNP_logo_M_C-scaled-1-1024x512.jpg': 'noise-network-plus',
  '6cC0RRGY_400x400.png': 'young-acousticians-network',
}
for name, slug in mapping.items():
    im = Image.open(os.path.join(src_dir, name)).convert('RGBA')
    r, g, b, a = im.split()
    transparent_bg = im.getpixel((0, 0))[3] < 10
    if transparent_bg:
        ink = a
    else:
        lum = Image.merge('RGB', (r, g, b)).convert('L')
        ink = ImageChops.invert(lum).point(lambda v: min(255, int(v * 1.6)))
        ink = ImageChops.multiply(ink, a)
    ink = ink.point(lambda v: 0 if v < 12 else v)
    bbox = ink.getbbox()
    ink = ink.crop(bbox)
    out = Image.new('RGBA', ink.size, INK + (0,))
    out.putalpha(ink)
    out.thumbnail((320, 112), Image.LANCZOS)
    out.save(os.path.join(out_dir, slug + '.png'), optimize=True)
    print(f'{name:40} -> {slug}.png {out.size}')
