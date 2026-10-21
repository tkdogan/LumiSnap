# HDR field guide assets

Used by [the student guide](../../guide.html). These are local site assets; no
external image host or font is required.

## Editable diagrams

- `capture-setup.svg`: camera position, view hemisphere, eye height and sensor orientation.
- `exposure-strategy.svg`: conceptual usable ranges and exposure overlap.
- `measurement-methods.svg`: spot luminance, vertical eye illuminance and horizontal workplane illuminance.
- `processing-workflow.svg`: merge, lens correction, calibration, validation and analysis.
- `sample-calibration.svg`: actual portrait capture with editable target annotations.

Open an SVG directly in Illustrator or Inkscape. Labels are live Arial text;
geometry consists of vector paths, shapes and named groups. The photograph in
`sample-calibration.svg` is an embedded raster image; its markers and text are
editable vectors. No text is outlined. All SVGs are self-contained.
The same five SVGs are packaged in `lumisnap-editable-diagrams.zip` for download.

The optional generator is [`tools/build-tutorial-diagrams.py`](../../tools/build-tutorial-diagrams.py)
(Python 3 with Pillow).
Editing an SVG directly is sufficient; rerunning the generator replaces it.

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

WebP images are resized display copies with metadata removed, not HDR files or
measurement inputs. They have no applied creative edits or added tonal processing.
The fisheye series spans log2(1.3 / 0.02) ≈ 6.02 stops between exposure endpoints.
Its frame spacing is uneven, people move, and highlight validity has not been
established. It is presented as an example to inspect, not as an ideal capture.

The example photographs were supplied with this project. Literature figures
have not been copied. All explanatory diagrams are original to this guide.

`field-log.csv` is a blank measurement log with units, sensor orientation,
instrument calibration, camera setup, time and scene notes.
