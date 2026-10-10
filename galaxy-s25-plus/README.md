# Galaxy S25+ reference model

A parametric model of the Samsung Galaxy S25+ to design an enclosed case around
in Shapr3D. All dimensions live in [`params.py`](params.py), each tagged with
where it came from: `SPEC` (Samsung's published length, width and thickness),
`PHOTO` (measured from a photo of the real phone, about ±1 mm), `CALC` (worked
out from published figures), `GUESS` (placeholder) or `MEAS` (calipers).
Don't design the final case until the `PHOTO` and `GUESS` values are `MEAS`.

## Files

| File | What it is |
| --- | --- |
| `output/galaxy_s25plus.step` | Phone body plus feature markers. Import this into Shapr3D. |
| `output/galaxy_s25plus_body.stl` | Phone body only, for a quick test print. |
| `output/galaxy_s25plus_print_sheets.pdf` | Measurement sheet, corner gauge and 1:1 check templates. |

In the STEP file, `phone_body` is the outer shape the case has to fit around:
the slab, camera rings and keys. Ports, mics, the flash, the SIM tray, the
screen area and the selfie camera are thin orange and blue marker bodies on the
surface. You can use them as references, push/pull them into cutters, or delete
them. They're kept off the body so offsetting the body for the case's inner
wall doesn't put plugs into the ports.

Origin is the centre of the phone: +X toward the button side, +Y toward the top,
+Z out of the screen.

## Measuring

1. Print the PDF at 100% / "Actual size" and check each page's 100 mm bar with
   the calipers. If your printer shrinks the page and has no "Actual size"
   option (common when printing from a phone), measure the bar and run
   `python make_print_sheets.py --printer-scale 0.953` (bar length / 100).
   That writes a separate PDF drawn bigger to make up for the shrink.
2. Fill in page 1. Every position is from the named edge to the nearest edge
   of the feature, which is what calipers measure directly.
3. Use page 2 for the corner radius (A4).
4. Once the numbers are in `params.py`, rebuild. Then check the outline on
   page 3 and the camera and key positions on page 4 against the real phone.

## Rebuilding

```
pip install -r requirements.txt
python build_model.py
python make_print_sheets.py
```
