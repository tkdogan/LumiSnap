# HDR field guide assets

Used by [the student guide](../../guide.html). These are local site assets; no
external image host or font is required.

## Editable diagrams

- `capture-setup.svg`: camera position, view hemisphere, eye height and sensor orientation.
- `exposure-strategy.svg`: conceptual usable ranges and exposure overlap.
- `measurement-methods.svg`: spot luminance, vertical eye illuminance and horizontal workplane illuminance.
- `processing-workflow.svg`: merge, lens correction, calibration, validation and analysis.
- `sample-calibration.svg`: actual portrait capture with editable target annotations.
- `meter-identification.svg`: recognizable Konica Minolta T-10A and LS-150
  instrument drawings, their units, how to position them and their role in HDR work.

Open an SVG directly in Illustrator or Inkscape. Labels are live Arial text;
geometry consists of vector paths, shapes and named groups. The photograph in
`sample-calibration.svg` is an embedded raster image; its markers and text are
editable vectors. No text is outlined. All SVGs are self-contained.
The same six SVGs are packaged in `lumisnap-editable-diagrams.zip` for download.

The optional generator is [`tools/build-tutorial-diagrams.py`](../../tools/build-tutorial-diagrams.py)
(Python 3 with Pillow).
Editing an SVG directly is sufficient; rerunning the generator replaces it.

The meter silhouettes are original schematic drawings based on Konica Minolta's
[T-10A](https://www.konicaminolta.com/instruments/download/catalog/light/pdf/t10a_catalog_eng.pdf)
and [LS-150](https://sensing.konicaminolta.us/wp-content/uploads/ls150_catalog_eng_compressed.pdf)
brochures. Standard configurations are shown, without optional adapters. Display
readings are illustrative and are not paired measurements or a lux-to-cd/m²
conversion. Manufacturer product photographs are not included in the site assets.

## Example photographs and provenance

The originals remain unchanged in the sibling `LumiSnapDev` repository:

- `sample/Fisheye HDR Photos/IMG_0418.JPG` through `IMG_0428.JPG`.
  Canon EOS 6D Mark II, 8 mm, f/4, ISO 200; Sep. 30, 2026,
  10:12:19–10:13:18 according to EXIF (timezone unverified).
  The 11 actual exposure times are in `exposures.json`.
- `sample/Portrait HDR Photos/3X6A2043.JPG`.
  Canon EOS R5, RF24–105 mm at 24 mm, f/5.6, ISO 100, 1/10 s;
  Oct. 5, 2026, 16:45:53 according to EXIF (timezone unverified).
  Orientation is applied to make the web copy upright.
- The associated `Portrait HDR Luminance Measurements.pdf` supplies five
  readings: A 67, B 165, C 77, D 415, E 65 cd/m². It records 4:30 pm,
  Oct. 5, 2026. The timestamps differ; these are illustrative course notes,
  not a verified simultaneous calibration of this frame. Target positions
  have been redrawn approximately. The sheet identifies the course as
  ARCH5611 and credits mtc237, Harry Turghan and EZ Wang for the shared
  photographs and measurements. The original sheet is retained in the
  development repository.

The camera JPEG WebP images above are resized display copies with metadata removed,
not HDR files or measurement inputs. They have no applied creative edits or added
tonal processing. The iPhone HDR display copies described below use explicit tone
mapping and false-colour rendering.
The fisheye series spans log2(1.3 / 0.02) ≈ 6.02 stops between exposure endpoints.
Its frame spacing is uneven, people move, and highlight validity has not been
established. It is presented as an example to inspect, not as an ideal capture.

The example photographs were supplied with this project. Literature figures
have not been copied. All explanatory diagrams are original to this guide.

`field-log.csv` is a blank measurement log with units, sensor orientation,
instrument calibration, camera setup, time and scene notes.

## iPhone workflow examples

The iPhone workflow section in `guide.html#iphone-workflow` uses two supplied
sessions from the sibling `LumiSnapDev` repository:

- `sample/IOScaptures/designtechspace`: 5 Bayer RAW exposures, 1200 × 900 working
  HDR, 4 reference readings, saved calibration factor 1.0267053193983378.
- `sample/IOScaptures/milsteindome`: 6 Bayer RAW exposures, 900 × 1200 working
  HDR, 3 reference readings, saved calibration factor 0.9090177104813378.

Both were captured on October 21, 2026 using the iPhone Ultra Wide lens.
Original DNGs, HDRs and acquisition metadata remain unchanged in the development
repository. The website contains only derived display assets in `iphone/`.

Regenerate from the website repository with Python 3, NumPy and Pillow:

```sh
python3 tools/build-iphone-examples.py
# For a different checkout arrangement:
python3 tools/build-iphone-examples.py --source-root /path/to/IOScaptures
```

`*-preview.webp` follows the iPhone `HDRImage.preview()` method: Rec.709 sampled
log-average auto exposure, global Reinhard tone mapping, 1.1 display gain and
sRGB encoding. It is a visual preview, not measurement data or an app screenshot.
No objects are removed or retouched. Images retain their full orientation and view.

`*-luminance.webp` uses Radiance luminance
`179 × (0.265 R + 0.670 G + 0.065 B)` with the project calibration factor applied
once to the uncalibrated working HDR. Both use a shared logarithmic 10–10,000 cd/m²
scale and the same 1024-entry Turbo polynomial lookup as the app. Values outside
the range use the end colours. Grey (96, 96, 96) marks the saved reliability mask;
these maps use lossless WebP so the mask and palette are preserved. The legend is
in `luminance-legend.webp`.

`*-points.svg` contains only numbered markers at the normalized coordinates in
`session.hlab.json`. It overlays the corresponding preview without changing it.
Table readings and residuals come from `calibration-ios.json`, rounded for display.
The saved unreliable fractions are 1.2034% and 3.7598%, respectively. RGBE export
quantization can cause small differences from the app's internal Float32 values.

The reference points were used to fit the scale; their residuals do not establish
independent accuracy. Neither export identifies its meter model, and neither
Ultra Wide view is a complete 180° fisheye suitable for the desktop glare workflow.
