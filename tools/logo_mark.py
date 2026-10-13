def mark(cls=""):
    blade = "M42 12L42.4 10.4L42.1 7.8L41.7 10.4Z"
    return (f'<svg class="{cls}" viewBox="-13 0 61 32" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">'
            # distant turbine (lighter)
            '<g opacity="0.5" stroke-width="0.8"><path d="M36.5 22.4Q41.5 19.6 47 21.2"/>'
            '<path d="M41.85 21L41.95 12H42.05L42.15 21Z"/>'
            f'<g class="mk-spin" style="transform-origin:42px 12px"><path d="{blade}"/>'
            f'<path d="{blade}" transform="rotate(120 42 12)"/><path d="{blade}" transform="rotate(240 42 12)"/></g></g>'
            # house
            '<path d="M5 30V17.5L14 10L23 17.5V30"/><path d="M3 19L14 9.6L25 19"/>'
            '<path d="M11.8 30V24.2H16.2V30" stroke-width="1"/><rect x="17.6" y="20" width="3" height="3" stroke-width="0.9"/>'
            # air-source heat pump in the garden
            '<rect x="26.5" y="23.5" width="8" height="6.5" rx="0.6"/><circle cx="29.6" cy="26.75" r="2" stroke-width="0.9"/>'
            '<g class="mk-fan" style="transform-origin:29.6px 26.75px" stroke-width="0.7">'
            '<path d="M29.6 26.75V25.2M29.6 26.75L30.95 27.5M29.6 26.75L28.25 27.5"/></g>'
            '<path d="M32.6 25V28.6" stroke-width="0.8"/>'
            # songbird perched on the heat pump, chirping
            '<g stroke-width="0.6"><path d="M30.6 22.2Q31.4 23.4 32.8 22.9Q33.6 22.5 33.4 21.6"/>'
            '<path d="M30.6 22.2Q31.6 21.3 33.1 21.4"/><path d="M30.6 22.2L29.5 21.7"/>'
            '<path d="M33.1 21.4Q33.4 20.4 34.2 20.6Q34.8 20.8 34.6 21.4L35.4 21.5L34.5 21.8Q34.2 22.1 33.4 21.6"/>'
            '<path d="M31.8 23.2V23.5M32.6 23.1V23.5" stroke-width="0.4"/></g>'
            '<g class="mk-note" stroke-width="0.5"><ellipse cx="36.4" cy="18.6" rx="0.55" ry="0.4" fill="currentColor" stroke="none"/>'
            '<path d="M36.9 18.5V16.4L37.7 16.8"/></g>'
            # drone overhead with parcel
            '<path d="M24.5 4.6H29.5M33.5 4.6H38.5" class="mk-rotor"/>'
            '<path d="M27 4.6V6.4H36V4.6" stroke-width="1"/><rect x="29.5" y="5.6" width="4" height="2.2" rx="0.8" stroke-width="1"/>'
            '<rect x="30" y="9" width="3" height="2.6" stroke-width="0.9"/><path d="M31.5 7.8V9" stroke-width="0.7"/>'
            # e-scooter to the left of the house
            '<circle cx="-10" cy="28" r="1.9" stroke-width="1"/><circle cx="-1.6" cy="28" r="1.9" stroke-width="1"/>'
            '<rect x="-8.6" y="25.6" width="5.6" height="1.6" rx="0.6" stroke-width="1"/>'
            '<path d="M-1.6 28L-3.4 19.6M-5 19.6H-1.8" stroke-width="1"/>'
            # ground
            '<path d="M-12 30H47"/>'
            '</svg>')
