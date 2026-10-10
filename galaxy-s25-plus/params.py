"""Samsung Galaxy S25+ dimensions, in millimetres.

Each value is tagged:
    SPEC   Samsung's published spec
    GUESS  placeholder until it's measured on the real phone
    MEAS   measured on the real phone

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
CORNER_RADIUS = 11.0  # A4 GUESS, seen from the front
SIDE_FLAT_HEIGHT = 5.5  # A5 GUESS, flat strip of the side frame between the rounded edges

# B: rear cameras (top to bottom) and flash
CAMERAS = [
    dict(id="B1", from_top=7.0, from_side=7.5, diameter=12.0, protrusion=1.5),  # GUESS
    dict(id="B2", from_top=22.0, from_side=7.5, diameter=12.0, protrusion=1.5),  # GUESS
    dict(id="B3", from_top=37.0, from_side=7.5, diameter=12.0, protrusion=1.5),  # GUESS
]
FLASH = dict(id="B4", from_top=10.5, from_side=24.0, diameter=5.0)  # GUESS

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
SCREEN_BORDER = dict(id="F1", sides=2.0, top=2.0, bottom=2.0)  # GUESS, black border around the display
SELFIE_CAMERA = dict(id="F2", from_top=5.0, diameter=3.6)  # GUESS, centred side to side
