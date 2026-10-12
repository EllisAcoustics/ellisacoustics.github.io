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


def turbine():
    blade = 'M20 12L20.6 9.4L20.3 1L19.8 1L19.5 9.4Z'
    return (f'<svg {COMMON}><title>Next-generation wind turbine</title>'
            '<path class="wind" d="M1 8H7.5M0 13H6.5M1 18H7.5M32.5 8H39M33.5 13H40M32.5 18H39" '
            'stroke-width="0.5" stroke-dasharray="1.6 2.4"/>'
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
    """Fixed-wing eVTOL: side view rolled 45 degrees toward the viewer, so the top of the
    high wing faces us. Booms on the wing carry four lift rotors (horizontal discs seen in
    perspective); a pusher propeller sits at the tail."""
    # Geometry: fuselage axis tail (6, 13.5) -> nose (34, 18.3); wing root C = (20.6, 16);
    # half-span vector w = (-4.43, 10.6) (near tip down-left, far tip up-right).
    def lift(cx, cy):
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="3" ry="1.9" stroke-width="0.4" stroke-dasharray="0.7 0.9"/>'
                f'<g transform="translate({cx} {cy}) scale(1 0.63)"><g class="lift">'
                f'<path d="M-2.8 0H2.8" stroke-width="0.75"/></g></g>'
                f'<circle cx="{cx}" cy="{cy}" r="0.45" fill="currentColor" stroke="none"/>')
    fuselage = ('M6.2 12.7Q11 11.6 21 13.2L31.8 15.6Q35.4 16.6 35 18.4Q34.4 19.9 30.6 19.6'
                'L19.8 18.6Q10.4 17.4 6.2 14.6Q5.2 13.7 6.2 12.7Z')
    wing = 'M22.3 16.3L17.2 26.8L15.2 26.4L18.9 15.7L24 5.2L26 5.6Z'
    return (f'<svg {COMMON}><title>Fixed-wing eVTOL aircraft</title>'
            '<path class="wind" d="M4.4 12H0.2M4.6 13.6H0M4.4 15.2H0.6" stroke-width="0.45" stroke-dasharray="1.2 1.8"/>'
            f'<path d="{fuselage}" fill="var(--paper)"/>'
            '<path d="M29.4 15.2Q32.6 15.6 34.4 17.2" stroke-width="0.5"/>'                       # canopy
            '<path d="M9.2 13.1L5.4 6.6L6.6 6.3L11 13.3M10.6 13.4L9.6 8.4L10.6 8.2L12.2 13.6" stroke-width="0.65"/>'  # V-tail
            f'<path d="{wing}" fill="var(--paper)"/>'                                               # high wing over fuselage
            '<path d="M13.7 21.1L22.7 22.6M18.5 9.4L27.5 10.9" stroke-width="0.7"/>'               # booms
            + lift(13.7, 21.1) + lift(22.7, 22.6) + lift(18.5, 9.4) + lift(27.5, 10.9) +
            '<g class="pushprop" style="transform-origin:5.6px 13.6px"><path d="M6.1 10L5.1 17.2" stroke-width="0.8"/></g>'
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
            f'{wheel(10.9, 23.6, 3.2)}{wheel(29.9, 23.6, 3.2)}{pulse(37.2, 20.6)}</svg>')


def drone():
    """Heavy-lift quadcopter in side view (T150-style) carrying a cargo box."""
    return (f'<svg {COMMON}><title>Cargo drone</title>'
            '<path class="down" d="M2.5 11.5V17M7.5 11.5V17M32.5 11.5V17M37.5 11.5V17" stroke-width="0.45" stroke-dasharray="1.2 1.6"/>'
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
            '<path class="wind" d="M-2 17H2M-1 20.5H2.5" stroke-width="0.5" stroke-dasharray="1.6 2"/>'
            '<path d="M3.2 25.4A4.8 4.8 0 0 1 11.6 23.6" stroke-width="0.7"/>'                       # rear fender
            '<rect x="11.6" y="23" width="16.8" height="4.2" rx="1"/>'                               # battery deck
            '<path d="M20.6 23.7L19.6 25.1H21L20 26.5" stroke-width="0.55"/>'                        # bolt
            '<path d="M32 27.4L27.9 7.6L29.4 7.3L33.5 27.1Z"/>'                                     # stem
            '<path d="M28.4 25L31 24.8" stroke-width="0.7"/>'
            '<path d="M24.8 7.3H32.4" stroke-width="1.1"/>'                                         # handlebar
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
