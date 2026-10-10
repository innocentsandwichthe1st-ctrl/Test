"""Samsung Galaxy S25+ dimensions, in millimetres.

Each value is tagged:
    SPEC   Samsung's published spec
    CASE   from a fitted S25+ case STL (built from Samsung's 3D models): centres
           about +/-0.2 mm; sizes are the case opening minus its 0.25 mm clearance
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
# The case mesh contains its designer's phone outline as an explicit contour: 75.80 x 158.40, R 8.25 arcs.
CORNER_RADIUS = 8.25  # A4 CASE, seen from the front
SIDE_FLAT_HEIGHT = 5.5  # A5 GUESS, flat strip of the side frame between the rounded edges

# B: rear cameras (top to bottom) and flash
# Positions CASE (centres 13.00 from the button side, 12.90 / 29.85 / 46.80 from the top);
# diameter CASE (16.00 mm hole less 0.25 clearance a side). Protrusion is GUESS: published figures disagree
# (~1.25 mm from PhoneArena's "~8.55 mm with camera", 1.8 mm leaked for the base S25).
CAMERAS = [
    dict(id="B1", from_top=5.15, from_side=5.25, diameter=15.5, protrusion=1.5),
    dict(id="B2", from_top=22.10, from_side=5.25, diameter=15.5, protrusion=1.5),
    dict(id="B3", from_top=39.05, from_side=5.25, diameter=15.5, protrusion=1.5),
]
FLASH = dict(id="B4", from_top=18.70, from_side=24.85, diameter=5.5)  # CASE, centre 27.60 / 21.45, 6.00 mm hole

# C: pill-shaped keys on the button side. from_top is to the top end of the key;
# height is across the phone's thickness; protrusion is how far the key sticks out.
# Centres CASE: volume 38.35, power 63.30 mm from the top, 3.9 mm above the back glass (0.25 toward
# the screen from mid-thickness). Sizes are GUESS from the case openings (22.5 x 5.0 and 13.5 x 5.0 at
# their narrowest) less a ~1 mm margin all round; protrusion GUESS.
KEYS = [
    dict(id="C1", name="volume", from_top=28.10, length=20.5, height=2.8, protrusion=0.6, from_back=3.9),
    dict(id="C2", name="power", from_top=57.55, length=11.5, height=2.8, protrusion=0.6, from_back=3.9),
]

# D, E: openings on the bottom and top edges, measured from the button side.
# Each is a slot with rounded ends (a circle when width == height), centred on
# the thickness unless it has from_back (back glass to the opening's centre).
# Centres are CASE; sizes are GUESS (the case cuts are oversized for plugs and sound).
BOTTOM_OPENINGS = [
    dict(id="D1", name="usb_c", from_side=33.45, width=8.9, height=3.2),  # centred; case cut 12.6 x 6.4
    dict(id="D2", name="speaker", from_side=17.60, width=8.8, height=0.8, from_back=3.7),  # centre 22.0; case slot 9.3 x 1.3
    dict(id="D3", name="mic", from_side=44.54, width=1.0, height=1.0),  # centre 45.04; case hole 1.25
    dict(id="D4", name="sim_tray", from_side=52.0, width=16.0, height=2.6),  # GUESS: the case has no cut for it
]
TOP_OPENINGS = [  # two holes on the top edge, case holes 1.2 mm
    dict(id="E1", name="hole_1", from_side=19.50, width=1.0, height=1.0, from_back=3.8),  # centre 20.0
    dict(id="E2", name="hole_2", from_side=23.50, width=1.0, height=1.0, from_back=3.8),  # centre 24.0
]

# F: front, only needed if the case covers the screen
# CALC from Samsung's 169.1 mm full-rectangle diagonal and 1440 x 3120 pixels: active area 70.86 x 153.54 mm.
# Measured from the body edge to the first lit pixel; the top/bottom split of the 4.86 mm total is assumed even.
SCREEN_BORDER = dict(id="F1", sides=2.47, top=2.43, bottom=2.43)  # CALC
SELFIE_CAMERA = dict(id="F2", from_top=5.0, diameter=3.6)  # GUESS, centred side to side
