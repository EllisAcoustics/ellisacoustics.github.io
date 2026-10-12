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







def pulse(x, y, cls="pulse"):
    """Sound pulse: three arcs rippling out from a point (the vehicle's warning sound)."""
    arcs = ''.join(f'<path class="{cls} p{i}" d="M{x + 1.4} {y - 3}A3.4 3.4 0 0 1 {x + 1.4} {y + 3}" '
                   f'style="transform-origin:{x}px {y}px"/>' for i in (1, 2, 3))
    return f'<g stroke-width="0.9">{arcs}</g>'


def evtol():
    """Fixed-wing eVTOL in side view, facing right: high wing, V-tail, pusher propeller."""
    fuselage = ('M37 17.2Q36 14.2 31.4 13.5L22 12.9Q15 12.7 9.2 14.3L5.6 15.6Q4.6 16.3 5.6 16.9L9.4 17.8'
                'Q16.4 19.8 24 20.3L31.4 20.1Q36.1 19.5 37 17.2Z')
    return (f'<svg {COMMON}><title>Fixed-wing eVTOL aircraft</title>'
            '<path class="wind" d="M-4 14.4H1M-5 16.4H1.4M-4 18.4H1" stroke-width="0.9" stroke-dasharray="1.6 2.4"/>'
            f'<path d="{fuselage}"/>'
            '<path d="M29 13.4Q31.8 13.5 33.6 15.2L28.6 15.3Z" stroke-width="0.9"/>'               # canopy
            '<path d="M13 12.3Q20.5 10.6 29 11.5Q20.5 11.6 13 12.3Z" stroke-width="0.9"/>'           # high wing
            '<path d="M9.4 14.2L5 5.6L6.9 5.4L12.2 13.6"/>'                                          # V-tail
            '<path d="M10.8 13.8L8.6 8.4" stroke-width="0.9"/>'
            '<path d="M16.8 20.1V21.4M31.6 20.1V21.4" stroke-width="0.9"/>'                          # gear struts
            '<ellipse cx="16.8" cy="22.2" rx="2.4" ry="0.95"/><ellipse cx="31.6" cy="22.2" rx="2" ry="0.9"/>'
            '<path d="M5.2 16.3L3.6 16.3" stroke-width="1.2"/>'                                       # spinner
            '<g class="pushprop" style="transform-origin:3.4px 16.3px"><path d="M3.4 11.6V21" stroke-width="1.2"/></g>'
            '</svg>')


def drone():
    """Heavy-lift quadcopter in side view (T150-style) carrying a cargo box."""
    return (f'<svg {COMMON}><title>Cargo drone</title>'
            '<path class="down" d="M2.5 11.5V17M7.5 11.5V17M32.5 11.5V17M37.5 11.5V17" stroke-width="0.8" stroke-dasharray="1.6 2"/>'
            '<g class="srot" style="transform-origin:5px 6.4px"><path d="M0.4 6.4H9.6" stroke-width="1.1"/></g>'
            '<g class="srot" style="transform-origin:35px 6.4px"><path d="M30.4 6.4H39.6" stroke-width="1.1"/></g>'
            '<path d="M5 7V9M35 7V9"/>'                                                               # rotor masts
            '<rect x="3.4" y="9" width="3.2" height="2" rx="0.6"/><rect x="33.4" y="9" width="3.2" height="2" rx="0.6"/>'
            '<path d="M6.6 10H14M26 10H33.4"/>'                                                        # arms
            '<rect x="14" y="7.8" width="12" height="5" rx="2"/>'                                      # body
            '<path d="M16 12.8L13.4 18.2M24 12.8L26.6 18.2M11.6 18.2H15.4M24.6 18.2H28.4"/>'           # legs, skids
            '<g class="cargo" style="transform-origin:20px 12.8px">'
            '<path d="M18 12.8L16.4 21M22 12.8L23.6 21" stroke-width="0.8"/>'                          # slings
            '<rect x="14.4" y="21" width="11.2" height="9" rx="1"/>'
            '<path class="sym-med" d="M20 23.2V27.8M17.7 25.5H22.3" stroke-width="1.4"/>'
            '<path class="sym-food" d="M17.9 23.1V27.9M17.1 23.1V24.5Q17.1 25.4 17.9 25.4Q18.7 25.4 18.7 24.5V23.1'
            'M22.1 27.9V23.1Q23.4 24.1 22.6 26" stroke-width="0.85"/>'
            '</g></svg>')


def ev():
    body = ('M3.5 24V20Q3.8 17.8 8 17.2L12.4 12.8Q13.8 11.6 16 11.6H25Q27.2 11.6 28.9 13.2L33 17.1'
            'Q36.2 17.6 36.5 20V24H33.4A4 4 0 0 0 25.6 24H14.9A4 4 0 0 0 7.1 24Z')
    return (f'<svg {COMMON}><title>Electric car</title>'
            f'<path d="{body}"/>'
            '<path d="M13.6 16.9L16.4 13.6H24.6L27.6 16.9ZM20.4 13.6V16.9" stroke-width="1"/>'
            '<path d="M21.6 18.8L20.3 21H21.9L20.6 23.2" stroke-width="0.9"/>'
            f'{wheel(11, 24, 3.2)}{wheel(29.5, 24, 3.2)}{pulse(37.2, 20.2)}</svg>')


def scooter():
    """E-scooter with a chunky battery deck."""
    return (f'<svg {COMMON}><title>E-scooter</title>'
            '<path class="wind" d="M-2 17H2M-1 20.5H2.5" stroke-width="1" stroke-dasharray="2 2.5"/>'
            '<path d="M3.2 25.4A4.8 4.8 0 0 1 11.6 23.6"/>'                                           # rear fender
            '<rect x="11.6" y="23" width="16.8" height="4.2" rx="1.6"/>'                               # battery deck
            '<path d="M20.6 23.6L19.4 25.2H21.2L20 26.7" stroke-width="0.9"/>'                         # bolt
            '<path d="M31.9 27.4L27.8 7.6L29.5 7.3L33.6 27.1Z"/>'                                     # stem
            '<path d="M28.4 25L30.9 24.8"/>'                                                           # deck to stem
            '<path d="M24.8 7.3H32.4" stroke-width="1.5"/>'                                           # handlebar
            f'{wheel(8, 27.4, 3.6)}{wheel(32.6, 27.4, 3.6)}{pulse(36.4, 17)}</svg>')


# Source name, characteristic frequency (Hz) used for placement, drawing
SOURCES = [
    ('Next-generation wind turbine', 100, turbine),
    ('Air-source heat pump', 200, ashp),
    ('Fixed-wing eVTOL aircraft', 400, evtol),
    ('Electric car', 1000, ev),
    ('Cargo drone', 2500, drone),
    ('E-scooter', 5000, scooter),
]
