"""Samsung Galaxy S25+ dimensions, in millimetres.

Each value is tagged:
    SPEC   Samsung's published spec
    PHOTO  measured from a photo of the real phone, about +/-1 mm
    CALC   worked out from other published figures
    GUESS  placeholder until it's measured on the real phone
    MEAS   measured on the real phone with calipers

The IDs (A1, B2, ...) match the measurement sheet, page 1 of
output/galaxy_s25plus_print_sheets.pdf.

Hold the phone upright with the screen facing you:
    top          the end with the selfie camera
    button side  the long side with the volume and power keys (your right)

Every position is the distance from the named edge to the NEAREST edge of the
feature, which is what calipers measure directly. The scripts work out centres.
"""

# A: body
LENGTH = 158.4  # A1 SPEC, top to bottom
WIDTH = 75.8  # A2 SPEC, side to side
THICKNESS = 7.3  # A3 SPEC, screen to back glass, not counting the cameras
# A leaked CAD dummy gave 158.44 x 75.79 x 7.35, so expect the real phone within ~0.05 mm of the spec.
CORNER_RADIUS = 9.3  # A4 PHOTO, seen from the front; Samsung's corners are a smooth "squircle", this is the equivalent arc
SIDE_FLAT_HEIGHT = 5.5  # A5 GUESS, flat strip of the side frame between the rounded edges

# B: rear cameras (top to bottom) and flash
# Positions and diameters are PHOTO. Protrusion is GUESS: published figures disagree
# (~1.25 mm from PhoneArena's "~8.55 mm with camera", 1.8 mm leaked for the base S25).
CAMERAS = [
    dict(id="B1", from_top=6.4, from_side=5.9, diameter=15.0, protrusion=1.5),
    dict(id="B2", from_top=23.3, from_side=5.9, diameter=15.0, protrusion=1.5),
    dict(id="B3", from_top=40.2, from_side=5.9, diameter=15.0, protrusion=1.5),
]
FLASH = dict(id="B4", from_top=20.0, from_side=25.5, diameter=4.5)  # PHOTO

# C: keys on the button side. from_top is to the top end of the key; height is
# across the phone's thickness; protrusion is how far the key sticks out.
KEYS = [
    dict(id="C1", name="volume", from_top=37.0, length=22.0, height=2.4, protrusion=0.6),  # GUESS
    dict(id="C2", name="power", from_top=64.0, length=12.0, height=2.4, protrusion=0.6),  # GUESS
]

# D, E: openings on the bottom and top edges, measured from the button side.
# Each is a slot with rounded ends (a circle when width == height), centred on
# the thickness unless it has from_back (back glass to the opening's centre).
BOTTOM_OPENINGS = [
    dict(id="D1", name="usb_c", from_side=33.45, width=8.9, height=3.2),  # GUESS
    dict(id="D2", name="speaker", from_side=9.0, width=12.0, height=1.2),  # GUESS
    dict(id="D3", name="mic", from_side=45.5, width=1.0, height=1.0),  # GUESS
    dict(id="D4", name="sim_tray", from_side=52.0, width=16.0, height=2.6),  # GUESS
]
TOP_OPENINGS = [
    dict(id="E1", name="mic", from_side=50.0, width=1.0, height=1.0),  # GUESS
]

# F: front, only needed if the case covers the screen
# CALC from Samsung's 169.1 mm full-rectangle diagonal and 1440 x 3120 pixels: active area 70.86 x 153.54 mm.
# Measured from the body edge to the first lit pixel; the top/bottom split of the 4.86 mm total is assumed even.
SCREEN_BORDER = dict(id="F1", sides=2.47, top=2.43, bottom=2.43)  # CALC
SELFIE_CAMERA = dict(id="F2", from_top=5.0, diameter=3.6)  # GUESS, centred side to side
