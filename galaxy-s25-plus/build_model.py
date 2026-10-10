"""Build the Galaxy S25+ model from params.py and export it.

    python build_model.py

Writes to output/:
    galaxy_s25plus.step      phone body plus feature markers, for Shapr3D
    galaxy_s25plus_body.stl  phone body only, for test prints

The body is the outer shape a case has to fit around: the slab, the camera
rings and the keys. Openings (ports, mics, flash, SIM tray, screen, selfie
camera) are thin separate marker bodies sitting on the surface, so offsetting
the body to make a case doesn't push plugs into the ports.

Origin is the centre of the phone. +X points to the button side, +Y to the
top, +Z out of the screen.
"""

from pathlib import Path

import cadquery as cq

import params as p

OUT = Path(__file__).parent / "output"
MARKER = 0.2  # thickness of the marker bodies
OVERLAP = 0.1  # how far rings and keys sink into the slab so they fuse cleanly

L, W, T = p.LENGTH, p.WIDTH, p.THICKNESS
EDGE_RADIUS = (T - p.SIDE_FLAT_HEIGHT) / 2


def x_center(from_side, size):
    return W / 2 - from_side - size / 2


def y_center(from_top, size):
    return L / 2 - from_top - size / 2


def z_center(feature):
    return feature.get("from_back", T / 2) - T / 2


def slab():
    return (
        cq.Workplane("XY")
        .workplane(offset=-T / 2)
        .rect(W, L)
        .extrude(T)
        .edges("|Z")
        .fillet(p.CORNER_RADIUS)
        .edges("not |Z")
        .fillet(EDGE_RADIUS)
    )


def camera_ring(cam):
    d, h = cam["diameter"], cam["protrusion"]
    return (
        cq.Workplane("XY")
        .workplane(offset=-T / 2 + OVERLAP)
        .center(x_center(cam["from_side"], d), y_center(cam["from_top"], d))
        .circle(d / 2)
        .extrude(-(h + OVERLAP))
        .faces("<Z")
        .edges()
        .fillet(min(0.3, h / 2))
    )


def key(k):
    depth = k["protrusion"] + OVERLAP
    return (
        cq.Workplane("XY")
        .box(depth, k["length"], k["height"])
        .faces(">X")
        .edges()
        .fillet(min(k["protrusion"], k["height"] / 2) * 0.8)
        .translate((W / 2 - OVERLAP + depth / 2, y_center(k["from_top"], k["length"]), z_center(k)))
    )


def body():
    shape = slab()
    for cam in p.CAMERAS:
        shape = shape.union(camera_ring(cam))
    for k in p.KEYS:
        shape = shape.union(key(k))
    return shape


def pad(plane, width, height, thickness=MARKER):
    wp = cq.Workplane(plane)
    wp = wp.slot2D(width, height) if width > height else wp.circle(width / 2)
    return wp.extrude(thickness)


def edge_opening(o, end):
    """Marker for an opening on the top (end=1) or bottom (end=-1) edge."""
    origin = (x_center(o["from_side"], o["width"]), end * L / 2, z_center(o))
    return pad(cq.Plane(origin, (1, 0, 0), (0, end, 0)), o["width"], o["height"])


def flash():
    f = p.FLASH
    d = f["diameter"]
    origin = (x_center(f["from_side"], d), y_center(f["from_top"], d), -T / 2)
    return pad(cq.Plane(origin, (1, 0, 0), (0, 0, -1)), d, d)


def screen():
    b = p.SCREEN_BORDER
    w, h = W - 2 * b["sides"], L - b["top"] - b["bottom"]
    return (
        cq.Workplane("XY")
        .workplane(offset=T / 2)
        .center(0, (b["bottom"] - b["top"]) / 2)
        .rect(w, h)
        .extrude(MARKER / 2)
        .edges("|Z")
        .fillet(max(p.CORNER_RADIUS - b["sides"], 0.5))
    )


def selfie_camera():
    c = p.SELFIE_CAMERA
    d = c["diameter"]
    return pad(cq.Plane((0, y_center(c["from_top"], d), T / 2), (1, 0, 0), (0, 0, 1)), d, d)


def markers():
    for o in p.BOTTOM_OPENINGS:
        yield f"{o['id']}_bottom_{o['name']}", edge_opening(o, -1)
    for o in p.TOP_OPENINGS:
        yield f"{o['id']}_top_{o['name']}", edge_opening(o, 1)
    yield f"{p.FLASH['id']}_flash", flash()
    yield f"{p.SCREEN_BORDER['id']}_screen", screen()
    yield f"{p.SELFIE_CAMERA['id']}_selfie_camera", selfie_camera()


def main():
    OUT.mkdir(exist_ok=True)
    phone = body()

    asm = cq.Assembly(name="galaxy_s25plus")
    asm.add(phone, name="phone_body", color=cq.Color(0.25, 0.25, 0.28))
    for name, shape in markers():
        color = cq.Color(0.1, 0.3, 0.8) if name.endswith("_screen") else cq.Color(1.0, 0.45, 0.0)
        asm.add(shape, name=name, color=color)
    asm.export(str(OUT / "galaxy_s25plus.step"))
    cq.exporters.export(phone, str(OUT / "galaxy_s25plus_body.stl"), tolerance=0.01, angularTolerance=0.1)

    bb = phone.val().BoundingBox()
    print(f"phone body envelope: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm (incl. keys and camera rings)")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
