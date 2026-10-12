"""Six minimal line icons of the noise sources, drawn for the frequency ruler.

All share a 40 x 34 viewBox, 1.25 stroke, currentColor, round caps. Animated parts
carry classes that the page's CSS animates (.spin, .prop, .ring, .wheel, .wind,
.note, .head)."""

COMMON = 'viewBox="0 0 40 34" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" overflow="visible"'


def rotor(cx, cy, r, ring=None, cls="prop"):
    """Two-blade rotor seen from above, spinning about its hub, with an optional air ring."""
    ring_svg = (f'<circle class="ring" cx="{cx}" cy="{cy}" r="{ring}" stroke-width="0.6" stroke-dasharray="1 1.8" '
                f'style="transform-origin:{cx}px {cy}px"/>') if ring else ''
    return (f'{ring_svg}<g class="{cls}" style="transform-origin:{cx}px {cy}px">'
            f'<path d="M{cx - r} {cy}H{cx + r}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="0.9" fill="currentColor" stroke="none"/>')


def wheel(cx, cy, r):
    s = r * 0.866
    return (f'<g class="wheel" style="transform-origin:{cx}px {cy}px">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<path d="M{cx} {cy - r}V{cy + r}M{cx - s:.2f} {cy - r / 2:.2f}L{cx + s:.2f} {cy + r / 2:.2f}'
            f'M{cx - s:.2f} {cy + r / 2:.2f}L{cx + s:.2f} {cy - r / 2:.2f}" stroke-width="0.9"/></g>')


def turbine():
    blade = 'M20 12C21.3 9 21.1 4.2 20 1C19.1 4.2 18.9 9 20 12Z'
    return (f'<svg {COMMON}><title>Next-generation wind turbine</title>'
            '<path class="wind" d="M1 7H7M0 13H6M1 19H7M33 7H39M34 13H40M33 19H39" stroke-width="1" stroke-dasharray="2 3"/>'
            '<path d="M19.3 33L19.8 13.5M20.7 33L20.2 13.5M16 33H24"/>'
            f'<g class="spin" style="transform-origin:20px 12px"><path d="{blade}"/>'
            f'<path d="{blade}" transform="rotate(120 20 12)"/><path d="{blade}" transform="rotate(240 20 12)"/></g>'
            '<circle cx="20" cy="12" r="1.3" fill="currentColor" stroke="none"/></svg>')


def ashp():
    fan = ''.join(f'<path d="M13.5 23.5L13.5 19" transform="rotate({a} 13.5 23.5)"/>' for a in (0, 120, 240))
    note = lambda x, y, cls: (f'<g class="note {cls}"><ellipse cx="{x}" cy="{y}" rx="1.25" ry="0.95" '
                              f'transform="rotate(-20 {x} {y})" fill="currentColor" stroke="none"/>'
                              f'<path d="M{x + 1.1} {y - 0.3}V{y - 4.6}L{x + 2.8} {y - 3.7}" stroke-width="1"/></g>')
    return (f'<svg {COMMON}><title>Air-source heat pump</title>'
            '<rect x="4" y="15" width="30" height="17" rx="1.5"/>'
            '<circle cx="13.5" cy="23.5" r="6"/>'
            f'<g class="spin fast" style="transform-origin:13.5px 23.5px">{fan}</g>'
            '<path d="M23.5 19.5H30.5M23.5 22.5H30.5M23.5 25.5H30.5M23.5 28.5H30.5" stroke-width="1"/>'
            '<path d="M7.5 32V33.6M30.5 32V33.6"/>'
            # Songbird perched on the top edge
            '<g class="bird">'
            '<path d="M24.2 11.2L21.8 9.4"/>'                                   # tail
            '<ellipse cx="27.2" cy="11.8" rx="3.3" ry="2.4"/>'                    # body
            '<path d="M25.6 11.6Q27.2 10.6 28.7 12" stroke-width="1"/>'           # wing
            '<path d="M26.4 14.1V15M28.1 14.1V15" stroke-width="1"/>'             # legs
            '<g class="head" style="transform-origin:29.6px 10.6px">'
            '<circle cx="30.4" cy="9.3" r="1.75"/>'
            '<path d="M32.1 8.9L34 9.3L32.1 9.8"/>'
            '<circle cx="30.9" cy="8.9" r="0.35" fill="currentColor" stroke="none"/></g>'
            '</g>'
            f'{note(35.5, 6, "n1")}{note(33.5, 4, "n2")}'
            '</svg>')


def evtol():
    props = ''.join(rotor(x, 8.6, 2.8, ring=3.4) for x in (5.5, 13, 27, 34.5))
    pylons = 'M5.5 9.6V13M13 9.6V13M27 9.6V13M34.5 9.6V13'
    return (f'<svg {COMMON}><title>Fixed-wing eVTOL aircraft</title>'
            '<ellipse cx="20" cy="19" rx="2.3" ry="12.5"/>'
            '<rect x="2" y="13.5" width="36" height="3" rx="1.3"/>'
            '<rect x="13" y="28" width="14" height="2" rx="1"/>'
            f'<path d="{pylons}" stroke-width="0.8"/>'
            f'{props}</svg>')


def ev():
    body = ('M3.5 24V20Q3.8 17.8 8 17.2L12.4 12.8Q13.8 11.6 16 11.6H25Q27.2 11.6 28.9 13.2L33 17.1'
            'Q36.2 17.6 36.5 20V24H33.4A4 4 0 0 0 25.6 24H14.9A4 4 0 0 0 7.1 24Z')
    return (f'<svg {COMMON}><title>Electric car</title>'
            f'<path d="{body}"/>'
            '<path d="M13.6 16.9L16.4 13.6H24.6L27.6 16.9ZM20.4 13.6V16.9" stroke-width="1"/>'
            '<path d="M21.6 18.8L20.3 21H21.9L20.6 23.2" stroke-width="0.9"/>'   # small bolt: electric
            f'{wheel(11, 24, 3.2)}{wheel(29.5, 24, 3.2)}</svg>')


def drone():
    arms = 'M20 17L11 8M20 17L29 8M20 17L11 26M20 17L29 26'
    rotors = ''.join(rotor(x, y, 4.4, ring=5.4) for x, y in ((11, 8), (29, 8), (11, 26), (29, 26)))
    return (f'<svg {COMMON}><title>Drone</title>'
            f'<path d="{arms}"/>'
            '<rect x="16.6" y="13.6" width="6.8" height="6.8" rx="1.6"/>'
            f'{rotors}</svg>')


def scooter():
    return (f'<svg {COMMON}><title>E-scooter</title>'
            '<path class="wind" d="M0 18H4M1 22H4.5" stroke-width="1" stroke-dasharray="2 2.5"/>'
            '<path d="M4.6 25.6A4.2 4.2 0 0 1 11.6 24.4"/>'                        # rear fender
            '<path d="M10.5 26.1H27.5L32 27"/>'                                     # deck
            '<path d="M32 27L28 7.5M24.8 7.5H31"/>'                                  # stem and bar
            f'{wheel(8, 27.5, 3.5)}{wheel(32, 27.5, 3.5)}</svg>')


# Source name, characteristic frequency (Hz) used for placement, drawing
SOURCES = [
    ('Next-generation wind turbine', 100, turbine),
    ('Air-source heat pump', 200, ashp),
    ('Fixed-wing eVTOL aircraft', 400, evtol),
    ('Electric car', 1000, ev),
    ('Drone', 2500, drone),
    ('E-scooter', 5000, scooter),
]
