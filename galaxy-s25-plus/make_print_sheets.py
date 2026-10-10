"""Make the printable measuring sheets from params.py.

    python make_print_sheets.py

Writes output/galaxy_s25plus_print_sheets.pdf:
    page 1  measurement sheet to fill in with calipers
    page 2  corner radius gauge (1:1)
    page 3  outline check: the model's outline at 1:1
    page 4  back template: cut out and lay on the back to check the cameras

Pages are US Letter with everything kept inside the A4 area, so they print at
1:1 on either. Print at 100% / "Actual size" and check the 100 mm bar.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

import params as p

OUT = Path(__file__).parent / "output"
PAGE_W, PAGE_H = 215.9, 279.4
LINE = 0.25  # pt, thin enough to line edges up against

SHEET = [
    ("Body", [
        ("A1", "Length, top to bottom (spec 158.4)", ["mm"]),
        ("A2", "Width, side to side (spec 75.8)", ["mm"]),
        ("A3", "Thickness, not at the cameras (spec 7.3)", ["mm"]),
        ("A4", "Corner radius, seen from the front (page 2)", ["mm"]),
        ("A5", "Height of the flat strip on the side frame", ["mm"]),
    ]),
    ("Rear cameras and flash", [
        ("B1", "Top lens", ["top → ring", "btn side → ring", "ring Ø", "sticks out"]),
        ("B2", "Middle lens", ["top → ring", "btn side → ring", "ring Ø", "sticks out"]),
        ("B3", "Bottom lens", ["top → ring", "btn side → ring", "ring Ø", "sticks out"]),
        ("B4", "Flash", ["top → flash", "btn side → flash", "Ø"]),
    ]),
    ("Keys (button side)", [
        ("C1", "Volume key", ["top → key", "length", "height", "sticks out"]),
        ("C2", "Power key", ["top → key", "length", "height", "sticks out"]),
    ]),
    ("Bottom edge", [
        ("D1", "USB-C port", ["btn side → port", "width", "height"]),
        ("D2", "Speaker grille", ["btn side → grille", "grille width", "hole Ø"]),
        ("D3", "Microphone hole", ["btn side → hole", "Ø"]),
        ("D4", "SIM tray (note if it's on the top)", ["btn side → tray", "length", "height"]),
    ]),
    ("Top edge and other side", [
        ("E1", "Microphone hole", ["btn side → hole", "Ø"]),
        ("E2", "Anything else on the top edge?", ["notes"]),
        ("G1", "Anything on the long side without keys?", ["notes"]),
    ]),
    ("Front (only if the case covers the screen)", [
        ("F1", "Black border around the screen", ["sides", "top", "bottom"]),
        ("F2", "Selfie camera hole", ["top → hole", "Ø"]),
    ]),
]


def new_page(pdf_pages, title, lines):
    fig = plt.figure(figsize=(PAGE_W / 25.4, PAGE_H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_W)
    ax.set_ylim(0, PAGE_H)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(16, 262, title, fontsize=14, weight="bold", va="top")
    for i, line in enumerate(lines):
        ax.text(16, 254 - i * 4.6, line, fontsize=8, va="top")
    pdf_pages.append(fig)
    return ax


def scale_bar(ax, x=16, y=18):
    ax.plot([x, x + 100], [y, y], color="k", lw=0.8)
    for i in range(11):
        h = 3 if i % 5 == 0 else 1.6
        ax.plot([x + 10 * i, x + 10 * i], [y, y + h], color="k", lw=0.6)
    ax.text(x + 104, y, "must measure exactly 100 mm - if not, reprint at 100% / Actual size", fontsize=7, va="center")


def rounded_rect(cx, cy, w, h, r, n=60):
    """Closed outline of a rounded rectangle as x, y arrays."""
    corners = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    xs, ys = [], []
    for ox, oy, start in corners:
        t = np.radians(np.linspace(start, start + 90, n))
        xs.extend(cx + ox + r * np.cos(t))
        ys.extend(cy + oy + r * np.sin(t))
    return np.array(xs + xs[:1]), np.array(ys + ys[:1])


def measurement_sheet(pages):
    ax = new_page(pages, "Galaxy S25+ measurement sheet", [
        "Hold the phone upright, screen facing you. Top = the selfie-camera end. Button side = the long side with the keys.",
        "\"top → ring\" = from the top edge to the NEAREST edge of the ring. Same idea for every \"→\". All values in mm.",
        "Sticks out: measure across the phone over the ring (or key), then subtract A3 (or A2). Measure twice, write both if they differ.",
    ])
    y = 236
    for section, rows in SHEET:
        ax.text(16, y, section, fontsize=9, weight="bold", va="center")
        y -= 7
        for rid, label, fields in rows:
            ax.text(16, y, rid, fontsize=8, weight="bold", va="center")
            ax.text(25, y, label, fontsize=8, va="center")
            width = 84 if fields == ["notes"] else 24
            for i, field in enumerate(fields):
                x0 = 112 + i * 23.5
                ax.plot([x0, x0 + width - 3], [y - 1.5, y - 1.5], color="0.4", lw=0.5)
                ax.text(x0, y - 3.2, field, fontsize=5.5, color="0.35", va="top")
            y -= 9
        y -= 2


def corner_gauge(pages):
    ax = new_page(pages, "Corner radius gauge (A4)", [
        "1. Lay the phone screen-down, one long side on line Y, the bottom edge on line X, pushed snugly into the corner.",
        "2. Look straight down at the corner. Arcs smaller than the phone's corner show in the gap; bigger ones hide under the phone.",
        "3. The corner radius is between the largest arc you can still see and the next size up. A 0.5 mm error here only moves",
        "    the corner of the case by 0.2 mm. Or take a photo straight down and send it to Claude.",
    ])
    x0, y0 = 60, 55
    ax.plot([x0, x0 + 110], [y0, y0], color="k", lw=LINE)
    ax.plot([x0, x0], [y0, y0 + 150], color="k", lw=LINE)
    ax.text(x0 + 112, y0, "X", fontsize=10, weight="bold", va="center")
    ax.text(x0, y0 + 152, "Y", fontsize=10, weight="bold", ha="center")
    colors = ["#d62728", "#1f77b4", "#2ca02c", "#9467bd"]
    for i, r in enumerate(range(5, 17)):
        t = np.radians(np.linspace(180, 270, 120))
        c = colors[i % len(colors)]
        ax.plot(x0 + r + r * np.cos(t), y0 + r + r * np.sin(t), color=c, lw=LINE)
        # leader from where the arc meets line X out to a readable label
        label_x = x0 - 10 + i * 6.5
        ax.plot([x0 + r, x0 + r, label_x], [y0, y0 - 3, y0 - 12], color=c, lw=LINE)
        ax.text(label_x, y0 - 13, str(r), fontsize=7, color=c, ha="center", va="top")
    ax.text(x0 - 14, y0 - 15, "radius, mm", fontsize=7, ha="right", va="center")
    ax.text(x0 + 38, y0 + 75, "phone goes here\n(screen down)", fontsize=9, color="0.6", ha="center")
    scale_bar(ax)


def outline_check(pages):
    ax = new_page(pages, "Outline check (A1, A2, A4)", [
        "Lay the phone screen-down inside the outline. It should just cover the solid line all the way round and leave the",
        "dashed line (0.5 mm outside) visible. Solid line showing at the corners = the phone's corners are rounder than the model.",
    ])
    cx, cy = PAGE_W / 2, 137
    ax.plot(*rounded_rect(cx, cy, p.WIDTH, p.LENGTH, p.CORNER_RADIUS), color="k", lw=LINE)
    ax.plot(*rounded_rect(cx, cy, p.WIDTH + 1, p.LENGTH + 1, p.CORNER_RADIUS + 0.5), color="0.3", lw=LINE, ls=(0, (4, 3)))
    ax.text(cx, cy, f"{p.LENGTH} x {p.WIDTH} mm\ncorner radius {p.CORNER_RADIUS} mm", fontsize=8, color="0.5", ha="center", va="center")
    scale_bar(ax)


def back_template(pages):
    ax = new_page(pages, "Back template (B1-B4, C1-C2)", [
        "Cut along the outline. Lay it on the back of the phone with the edges lined up and press gently round each camera:",
        "every ring should sit inside its circle. Hold it against the button side to check the key marks. Note what's off and by how much.",
    ])
    cx, cy = PAGE_W / 2, 137
    left = cx - p.WIDTH / 2  # the button side, seen from the back
    top = cy + p.LENGTH / 2
    ax.plot(*rounded_rect(cx, cy, p.WIDTH, p.LENGTH, p.CORNER_RADIUS), color="k", lw=LINE)
    for item in p.CAMERAS + [p.FLASH]:
        d = item["diameter"]
        x, y = left + item["from_side"] + d / 2, top - item["from_top"] - d / 2
        t = np.linspace(0, 2 * np.pi, 120)
        ax.plot(x + d / 2 * np.cos(t), y + d / 2 * np.sin(t), color="k", lw=LINE)
        ax.text(x, y, item["id"], fontsize=6, ha="center", va="center")
    for k in p.KEYS:
        y1 = top - k["from_top"]
        ax.fill([left - 3, left, left, left - 3], [y1, y1, y1 - k["length"], y1 - k["length"]], color="0.75", lw=0)
        ax.text(left - 4, y1 - k["length"] / 2, k["id"], fontsize=6, ha="right", va="center")
    ax.text(left - 4, cy - 40, "button\nside", fontsize=7, ha="right", va="center", color="0.4")
    ax.text(cx, top + 3, "top", fontsize=7, ha="center", color="0.4")
    scale_bar(ax)


def main():
    OUT.mkdir(exist_ok=True)
    pages = []
    measurement_sheet(pages)
    corner_gauge(pages)
    outline_check(pages)
    back_template(pages)
    path = OUT / "galaxy_s25plus_print_sheets.pdf"
    with PdfPages(path) as pdf:
        for fig in pages:
            pdf.savefig(fig)
            plt.close(fig)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
