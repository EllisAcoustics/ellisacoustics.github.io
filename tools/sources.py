"""Noise-source icons for the frequency ruler, drawn as technical line schematics.

All share a 40 x 34 viewBox with a thin uniform stroke in currentColor, so they read
like figures in a paper rather than cartoons. Animated parts carry classes that the
page's CSS animates: .spin (rotate about a hub), .wheel, .wind (dashed flow),
.down (downwash), .srot (rotor seen edge-on), .lift (rotor disc in perspective),
.pushprop, .cargo (sway), .pulse (sound pulse), .note and .head.

Placement on the ruler: x = log2(Hz / 63) / 8 across 63 Hz to 16 kHz."""

COMMON = ('viewBox="0 0 40 34" fill="none" stroke="currentColor" stroke-width="0.8" '
          'stroke-linecap="round" stroke-linejoin="round" overflow="visible"')


def wheel(cx, cy, r, spokes=5):
    import math
    pts = ''.join(f'M{cx} {cy}L{cx + r * 0.78 * math.cos(2 * math.pi * k / spokes - math.pi / 2):.2f} '
                  f'{cy + r * 0.78 * math.sin(2 * math.pi * k / spokes - math.pi / 2):.2f}' for k in range(spokes))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<g class="wheel" style="transform-origin:{cx}px {cy}px">'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.78:.2f}" stroke-width="0.5"/>'
            f'<path d="{pts}" stroke-width="0.5"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="0.55" fill="currentColor" stroke="none"/>')


def pulse(x, y):
    """Sound pulse: three arcs rippling forward from a point."""
    arcs = ''.join(f'<path class="pulse p{i}" d="M{x + 1.4} {y - 3}A3.4 3.4 0 0 1 {x + 1.4} {y + 3}" '
                   f'style="transform-origin:{x}px {y}px"/>' for i in (1, 2, 3))
    return f'<g stroke-width="0.6">{arcs}</g>'


def pulse_left(x, y):
    """The same sound pulse, rippling backwards."""
    arcs = ''.join(f'<path class="pulse p{i}" d="M{x - 1.4} {y - 3}A3.4 3.4 0 0 0 {x - 1.4} {y + 3}" '
                   f'style="transform-origin:{x}px {y}px"/>' for i in (1, 2, 3))
    return f'<g stroke-width="0.6">{arcs}</g>'


def gust(d, delay=0.0, w=0.5, dur=None):
    """A gust of moving air: a short dash travels along a curling path and loops without a seam
    (pathLength is 100 and the dash pattern repeats every 100)."""
    st = f'animation-delay:{delay:.2f}s' + (f';animation-duration:{dur}s' if dur else '')
    return f'<path class="gust" d="{d}" pathLength="100" stroke-width="{w}" style="{st}"/>'


def turbine():
    blade = 'M20 12L20.6 9.4L20.3 1L19.8 1L19.5 9.4Z'
    return (f'<svg {COMMON}><title>Next-generation wind turbine</title>'
            + gust('M-1 8C3 7.2 6 8.8 9 8C11 7.4 11.4 5.8 10 5.6C8.8 5.5 8.8 7 10.2 7.2', 0)
            + gust('M-2 13C2 12.2 5 13.8 8.5 13C10.6 12.5 11 10.9 9.6 10.7C8.4 10.6 8.4 12.1 9.8 12.3', 0.6)
            + gust('M-1 18C3 17.2 6 18.8 9 18C11 17.4 11.4 15.8 10 15.6C8.8 15.5 8.8 17 10.2 17.2', 1.2)
            + gust('M30 10C33 9.4 35 11.2 38 10.4C40 9.8 40.4 8.2 39 8.1', 0.3)
            + gust('M30.5 16C33.5 15.4 35.5 17.2 38.5 16.4C40.5 15.8 40.9 14.2 39.5 14.1', 0.9) +
            '<path d="M19.35 33L19.75 13H20.25L20.65 33Z"/>'                                     # tapered tower
            '<path d="M15.5 33H24.5" stroke-width="0.6"/>'                                        # ground
            f'<g class="spin" style="transform-origin:20px 12px"><path d="{blade}"/>'
            f'<path d="{blade}" transform="rotate(120 20 12)"/><path d="{blade}" transform="rotate(240 20 12)"/></g>'
            '<circle cx="20" cy="12" r="1.05" fill="var(--paper)"/></svg>')


def ashp():
    fins = ''.join(f'M{x:.1f} 17V29.5' for x in [24 + 1.15 * i for i in range(7)])
    blade = 'M13.5 23.5C14.6 22.2 15.6 20.6 15.1 18.4C14.2 19 13.6 21 13.5 23.5Z'
    note = lambda x, y, cls: (f'<g class="note {cls}" stroke-width="0.6"><ellipse cx="{x}" cy="{y}" rx="0.95" ry="0.7" '
                              f'transform="rotate(-20 {x} {y})" fill="currentColor" stroke="none"/>'
                              f'<path d="M{x + 0.85} {y - 0.2}V{y - 3.8}L{x + 2.2} {y - 3.1}"/></g>')
    return (f'<svg {COMMON}><title>Air-source heat pump</title>'
            '<rect x="4" y="14.5" width="30" height="17.5" rx="0.8"/>'
            '<circle cx="13.5" cy="23.25" r="6.4"/>'
            '<circle cx="13.5" cy="23.25" r="4.3" stroke-width="0.45"/>'
            '<path d="M7.1 23.25H19.9M13.5 16.85V29.65" stroke-width="0.45"/>'                    # fan guard
            f'<g class="spin fast" style="transform-origin:13.5px 23.5px" stroke-width="0.6"><path d="{blade}"/>'
            f'<path d="{blade}" transform="rotate(120 13.5 23.5)"/><path d="{blade}" transform="rotate(240 13.5 23.5)"/></g>'
            f'<path d="{fins}" stroke-width="0.45"/>'
            '<path d="M7 32V33.5M31 32V33.5"/>'
            # Small songbird perched on the casing, drawn as a plain silhouette outline
            '<g class="bird" stroke-width="0.7">'
            '<path d="M24.6 11.6L21.6 10.6L24.4 12.6"/>'                                          # tail
            '<path d="M24.4 12.6Q26.4 14.4 29.2 13.2Q30.6 12.4 30.4 10.8"/>'                      # belly
            '<path d="M24.6 11.6Q26.6 10.2 29 10.2"/>'                                            # back
            '<path d="M26.6 14.1L26.4 14.5M28 13.8L28 14.5" stroke-width="0.5"/>'                # legs
            '<g class="head" style="transform-origin:29.4px 10.8px">'
            '<path d="M29 10.2Q29.6 8.2 31.2 8.4Q32.4 8.7 32.3 9.9L33.8 10.2L32 10.6Q31.4 11.4 30.4 10.8"/>'
            '<circle cx="31.2" cy="9.3" r="0.28" fill="currentColor" stroke="none"/></g>'
            '</g>'
            f'{note(35, 7, "n1")}{note(33.4, 5, "n2")}'
            '</svg>')


def evtol():
    """Passenger multicopter eVTOL in side view: an egg-shaped two-seat cabin with a wrap-around
    windscreen, four raised arms ending in motor pods and rotors (far pair drawn lighter), skid
    landing gear, and rotor downwash curling away underneath."""
    def rotor(cx, cy, r, far=False):
        o = ' opacity="0.45"' if far else ''
        return (f'<g{o}><ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.18:.2f}" stroke-width="0.35" stroke-dasharray="0.8 0.8"/>'
                f'<g class="srot" style="transform-origin:{cx}px {cy}px"><path d="M{cx - r} {cy}H{cx + r}" stroke-width="0.7"/></g>'
                f'<rect x="{cx - 0.9}" y="{cy + 0.25}" width="1.8" height="1.6" rx="0.45" stroke-width="0.55"/></g>')
    cabin = 'M12.6 20.4C12.6 15.6 15.8 12.9 20.6 12.9C25.6 12.9 28.6 15.8 28.6 20.2C28.6 23.7 26.1 25.3 20.6 25.3C15.1 25.3 12.6 23.8 12.6 20.4Z'
    return (f'<svg {COMMON}><title>Passenger multicopter eVTOL</title>'
            + gust('M5 12.5C4.6 15 5.4 17 4.4 19C3.8 20.2 2.4 20 2.6 18.8', 0)
            + gust('M35 12.5C35.4 15 34.6 17 35.6 19C36.2 20.2 37.6 20 37.4 18.8', 0.4)
            + rotor(9, 8.6, 4.6, True) + rotor(31, 8.6, 4.6, True) +
            '<path d="M15.6 14.6L9 10.4M25.6 14.6L31 10.4" stroke-width="0.6" opacity="0.45"/>'      # far arms
            f'<path d="{cabin}" fill="var(--paper)"/>'
            '<path d="M21.4 13.7C25.2 14 27.4 16.6 27.7 19.9H21.4Z" stroke-width="0.5"/>'          # windscreen
            '<path d="M22.6 14.9C24.4 15.3 25.6 16.6 26 18.2" stroke-width="0.35" opacity="0.6"/>'  # glint
            '<path d="M17.4 13.6V24.8M13.2 21.6H28.2" stroke-width="0.4"/>'                          # door, belt line
            '<path d="M14.4 16L5 11.6M26.8 16L35 11.6" stroke-width="0.8"/>'                        # near arms
            + rotor(5, 9.6, 4.8) + rotor(35, 9.6, 4.8) +
            '<path d="M16.2 25L14.8 29.4M25 25L26.4 29.4" stroke-width="0.6"/>'                      # struts
            '<path d="M11.2 29.4H19.4M22.2 29.4H30.4" stroke-width="0.8"/>'                          # skids
            '</svg>')

def ev():
    """Modern electric fastback in side view, facing right."""
    body = ('M3.6 23.6V21.2Q3.8 19.4 5.6 18.9L9.6 17.9Q13.8 12.6 19.4 12.4Q23.4 12.4 26.6 15.2L29 17.1'
            'Q34.6 17.7 36 19.2Q36.6 20.2 36.5 23.6H33.6A3.8 3.8 0 0 0 26.2 23.6H14.6A3.8 3.8 0 0 0 7.2 23.6Z')
    return (f'<svg {COMMON}><title>Electric car</title>'
            f'<path d="{body}"/>'
            '<path d="M11.4 17.7Q14.8 13.6 19.4 13.5Q22.8 13.5 25.4 15.6L26.8 17.1Z" stroke-width="0.55"/>'   # glasshouse
            '<path d="M19.2 13.6V17.4M19.2 17.4V22.8" stroke-width="0.45"/>'                        # B-pillar, door
            '<path d="M34.2 19.4H36" stroke-width="0.5"/>'                                          # light
            '<path d="M22.6 18.6L21.6 20.3H22.9L21.9 22" stroke-width="0.55"/>'                     # small bolt
            f'{wheel(10.9, 23.6, 3.2)}{wheel(29.9, 23.6, 3.2)}{pulse(37.2, 20.6)}{pulse_left(2.6, 20.6)}</svg>')


def drone():
    """Heavy-lift quadcopter in side view (T150-style) carrying a cargo box."""
    return (f'<svg {COMMON}><title>Cargo drone</title>'
            + gust('M3 11.5C2.6 14 3.4 16 2.4 18C1.8 19.2 0.4 19 0.6 17.8', 0)
            + gust('M7 11.5C7.4 14 6.6 16 7.6 18C8.2 19.2 9.6 19 9.4 17.8', 0.5)
            + gust('M33 11.5C32.6 14 33.4 16 32.4 18C31.8 19.2 30.4 19 30.6 17.8', 0.25)
            + gust('M37 11.5C37.4 14 36.6 16 37.6 18C38.2 19.2 39.6 19 39.4 17.8', 0.75) +
            '<g class="srot" style="transform-origin:5px 6.6px"><path d="M0.4 6.6H9.6" stroke-width="0.8"/></g>'
            '<g class="srot" style="transform-origin:35px 6.6px"><path d="M30.4 6.6H39.6" stroke-width="0.8"/></g>'
            '<path d="M5 7V9.2M35 7V9.2" stroke-width="0.6"/>'
            '<rect x="3.6" y="9.2" width="2.8" height="1.8" rx="0.4"/><rect x="33.6" y="9.2" width="2.8" height="1.8" rx="0.4"/>'
            '<path d="M6.4 10.1H14.2M25.8 10.1H33.6" stroke-width="0.7"/>'                          # arms
            '<rect x="14.2" y="8" width="11.6" height="4.6" rx="1.6"/>'                             # body
            '<path d="M16.2 12.6L13.6 18M23.8 12.6L26.4 18M11.8 18H15.4M24.6 18H28.2" stroke-width="0.7"/>'
            '<g class="cargo" style="transform-origin:20px 12.6px">'
            '<path d="M18 12.6L16.4 21M22 12.6L23.6 21" stroke-width="0.5"/>'
            '<rect x="14.6" y="21" width="10.8" height="8.6" rx="0.6"/>'
            '<path class="sym-med" d="M20 23.1V27.5M17.8 25.3H22.2" stroke-width="1.1"/>'
            '<path class="sym-food" d="M18 23.1V27.6M17.3 23.1V24.4Q17.3 25.2 18 25.2Q18.7 25.2 18.7 24.4V23.1'
            'M22 27.6V23.1Q23.2 24 22.5 25.8" stroke-width="0.6"/>'
            '</g></svg>')


def scooter():
    """E-scooter with a chunky battery deck."""
    return (f'<svg {COMMON}><title>E-scooter</title>'
            '<path d="M3.2 25.4A4.8 4.8 0 0 1 11.6 23.6" stroke-width="0.7"/>'                       # rear fender
            '<rect x="11.6" y="23" width="16.8" height="4.2" rx="1"/>'                               # battery deck
            '<path d="M20.6 23.7L19.6 25.1H21L20 26.5" stroke-width="0.55"/>'                        # bolt
            '<path d="M32 27.4L27.9 7.6L29.4 7.3L33.5 27.1Z"/>'                                     # stem
            '<path d="M28.4 25L31 24.8" stroke-width="0.7"/>'
            '<path d="M24.8 7.3H32.4" stroke-width="1.1"/>'                                         # handlebar
            f'{wheel(8, 27.4, 3.6)}{wheel(32.6, 27.4, 3.6)}{pulse(36.4, 17)}{pulse_left(2.4, 19)}</svg>')


# Source name, characteristic frequency (Hz) used for placement, drawing
SOURCES = [
    ('Next-generation wind turbine', 100, turbine),
    ('Air-source heat pump', 200, ashp),
    ('Passenger multicopter eVTOL', 400, evtol),
    ('Electric car', 1000, ev),
    ('Cargo drone', 2500, drone),
    ('E-scooter', 5000, scooter),
]
