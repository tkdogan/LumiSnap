#!/usr/bin/env python3
"""Build editable SVG teaching diagrams. No outlined text or external fonts.

Run with Python 3 and Pillow. The annotated example embeds a JPEG copy so that
each downloaded SVG is self-contained when opened in Illustrator or Inkscape.
"""
from pathlib import Path
import base64
import zipfile
from io import BytesIO
from html import escape
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "assets" / "tutorial"
INK, MUTED, GREEN, LIME, PAPER, LINE = "#162d26", "#50665b", "#306848", "#cdfc80", "#f0f3e9", "#b8c9ba"


def text(x, y, value, size=23, color=INK, weight="normal", anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def lines(x, y, values, size=23, color=MUTED, step=32):
    return "".join(text(x, y + i * step, value, size, color) for i, value in enumerate(values))


def rect(x, y, w, h, fill="white", stroke=LINE, radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def path(d, color=GREEN, width=3, dash="", arrow=False):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"' + (' marker-end="url(#arrow)"' if arrow else '') + '/>'


def save(name, title, desc, height, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/></marker></defs>
<g id="background"><rect width="1200" height="{height}" fill="{PAPER}"/></g>
<g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>'''
    (OUT / name).write_text(svg + "\n")


# 1. Two views of the same measurement position.
body = '<g id="headings">' + text(44, 54, "01 / A POSITION, A DIRECTION, A HEMISPHERE", 21, GREEN, "bold")
body += text(55, 112, "Plan: capture the view in front of the observer", 25, weight="bold")
body += text(755, 112, "Section: place the lens at eye level", 25, weight="bold") + '</g>'
body += '<g id="room-plan">' + rect(65, 150, 620, 420, "#e4ebdf", LINE, 0)
body += '<path d="M 110 425 A 250 250 0 0 1 610 425 L 360 425 Z" fill="#cdfc80" fill-opacity="0.45"/>'
body += path("M 110 425 A 250 250 0 0 1 610 425", GREEN, 3, "9 7")
body += rect(235, 144, 250, 12, "#a5c7dd", GREEN, 0) + text(360, 197, "WINDOW", 20, GREEN, "bold", "middle")
body += path("M 360 395 L 360 240", arrow=True) + text(380, 310, "View direction", 22)
body += rect(328, 413, 64, 40, INK, INK, 5) + '<circle cx="360" cy="415" r="15" fill="#a5c7dd" stroke="#162d26" stroke-width="3"/>'
body += text(360, 495, "Lens at observer position", 22, anchor="middle")
body += text(360, 535, "180° in plan; the full forward hemisphere in 3D", 20, MUTED, anchor="middle")
body += '<circle cx="177" cy="308" r="20" fill="#8b9984" stroke="#306848" stroke-width="2"/>'
body += path("M 177 330 L 177 372") + text(95, 402, "Matte target", 20) + '</g>'
body += '<g id="eye-height-section">' + path("M 745 565 L 1145 565", INK)
body += rect(868, 303, 65, 42, INK, INK, 5) + '<circle cx="933" cy="323" r="18" fill="#a5c7dd" stroke="#162d26" stroke-width="3"/>'
body += path("M 900 345 L 900 395 M 900 395 L 835 565 M 900 395 L 965 565 M 900 395 L 905 565", INK)
body += path("M 950 323 L 1130 323", arrow=True) + text(975, 300, "Level axis", 21)
body += path("M 785 565 L 785 323 M 775 323 L 795 323 M 775 565 L 795 565", GREEN, 2)
body += lines(755, 220, ["Use the actual seated or", "standing eye height."], 22)
body += text(803, 457, "Record", 20) + text(803, 482, "height", 20)
body += text(946, 393, "Lux sensor:", 21, weight="bold") + lines(946, 421, ["same position", "and view direction"], 21)
body += path("M 958 359 L 948 329", GREEN, 2) + '</g>'
body += text(55, 634, "Keep the operator behind the lens during capture. Record location, time, view direction and sky conditions.", 22)
body += text(55, 670, "For a scale model, place the lens at the equivalent eye position and keep the opening from blocking daylight.", 21, MUTED)
save("capture-setup.svg", "Camera setup for a lighting study", "Plan and section: a level fisheye at the observer's eye position captures the forward hemisphere. A lux sensor is placed at the same position facing the same direction. A matte calibration target is visible.", 710, body)

# 2. Conceptual range and exposure overlap, deliberately not a data chart.
body = text(44, 54, "02 / CHANGE SHUTTER SPEED, KEEP THE SETUP FIXED", 21, GREEN, "bold")
body += text(250, 115, "Darker surfaces", 24, weight="bold") + text(1070, 115, "Brighter sources", 24, weight="bold", anchor="end")
body += path("M 250 140 L 1070 140", arrow=True)
for y, label, sub, x, width in [(215,"Long exposure","e.g. 1/30 s",250,460),(325,"Middle exposure","e.g. 1/125 s",425,460),(435,"Short exposure","e.g. 1/500 s",600,460)]:
    body += '<g id="'+label.lower().replace(' ','-')+'">' + text(55,y+12,label,23,weight="bold") + text(55,y+43,sub,21,MUTED)
    body += rect(x,y-22,width,64,"#cdfc80",GREEN,7) + text(x+width/2,y+17,"Usable signal",23,INK,anchor="middle") + '</g>'
body += path("M 595 288 L 595 301 M 770 398 L 770 411", GREEN, 3, arrow=True)
body += text(785, 282, "Overlap links the exposures.", 21, GREEN)
body += path("M 250 525 L 1060 525", GREEN, 7) + text(655, 570, "MERGE → ONE LINEAR HDR → CALIBRATE TO cd/m²", 25, INK, "bold", "middle")
body += lines(55, 630, ["At least one exposure must record each important area above the noise floor and below clipping.", "If a source clips in every frame, the merge cannot recover it. Extend the bracket or revise the capture setup."], 22)
body += text(55, 714, "Conceptual ranges only. These shutter speeds illustrate two-stop spacing; they are not a universal capture recipe.", 20, MUTED)
save("exposure-strategy.svg", "Why exposure brackets need overlap", "Long exposures record darker surfaces, short exposures record brighter sources, with overlapping usable ranges. Merge the exposures into a linear HDR and then calibrate. A clipped source cannot be recovered by merging.", 750, body)

# 3. Distinct instruments and planes.
body = text(44,54,"03 / THREE MEASUREMENTS, THREE DIFFERENT QUESTIONS",21,GREEN,"bold")
panels=[(40,"A / SPOT LUMINANCE",["cd/m²", "How bright is this surface?"]),(430,"B / EYE ILLUMINANCE",["lx", "How much light arrives", "at the eye?"]),(820,"C / WORKPLANE ILLUMINANCE",["lx", "How much light reaches", "the desk?"])]
for x,label,sub in panels:
    body += rect(x,90,340,530,"#ffffff",LINE) + text(x+20,132,label,19,GREEN,"bold")
    body += lines(x+20,166,sub,21,INK,29)
body += '<g id="spot-meter">' + rect(280,260,58,130,"#929e88",GREEN,0)
body += '<path d="M 105 330 L 280 305 L 280 355 Z" fill="#cdfc80" stroke="#306848" stroke-width="2"/>'
body += rect(65,313,62,35,INK,INK,4) + text(210,278,"Matte target",20,anchor="middle")
body += lines(60,442,["Aim from near the lens position.","Keep the meter's entire spot", "inside one uniform surface.","Repeat on several targets."],20)
body += text(60,594,"Sets the image luminance scale.",20,GREEN) + '</g>'
body += '<g id="eye-lux-meter">' + path("M 625 250 L 520 320 M 665 330 L 530 330 M 625 410 L 520 340",GREEN,3,arrow=True)
body += rect(485,285,18,90,"#a5c7dd",GREEN,4) + path("M 494 375 L 494 408",INK)
body += text(550,244,"Incoming light",20,anchor="middle")
body += lines(450,442,["Sensor vertical at the lens.","Face the same way as the", "camera; avoid shading it.","Read before and after."],20)
body += text(450,594,"Checks the hemispheric total (Ev).",20,GREEN) + '</g>'
body += '<g id="desk-lux-meter">' + rect(860,368,250,14,"#d9dfce",GREEN,0)
body += path("M 875 382 L 875 405 M 1095 382 L 1095 405",INK) + rect(960,350,65,16,"#a5c7dd",GREEN,4)
body += path("M 990 255 L 990 335 M 905 280 L 968 337 M 1075 280 L 1015 337",GREEN,3,arrow=True)
body += lines(840,442,["Sensor horizontal, facing up.","Measure a grid on the actual", "desk or model workplane.","Record height and locations."],20)
body += text(840,594,"Tests daylight reaching the task.",20,GREEN) + '</g>'
body += text(55,674,"A lux reading cannot be entered into a cd/m² calibration field. Surface reflectance and light direction matter.",22)
body += text(55,711,"Match each measurement to its image, location, orientation and time. Record the instrument and its calibration status.",21,MUTED)
save("measurement-methods.svg","Luminance and illuminance measurements","A spot luminance meter measures a target in cd/m² and scales the image. A vertical illuminance sensor at the lens measures Ev in lux for validation. A horizontal upward-facing sensor measures workplane illuminance in lux for daylight studies.",750,body)

# 4. Workflow aligned with the implemented desktop features.
body = text(44,54,"04 / FROM EXPOSURES TO EVIDENCE",21,GREEN,"bold")
steps=[(50,110,"1 / MERGE",["Read exposure metadata.","Align frames; undo the", "JPEG response curve."]),(440,110,"2 / LENS",["Set projection and field of view.","Check the image circle.","Apply measured vignetting."]),(830,110,"3 / CALIBRATE",["Select the measured targets.","Enter spot readings in cd/m².","Inspect fit and disagreements."])]
for x,y,label,ls in steps:
    body+=rect(x,y,320,195,"white",LINE)+text(x+20,y+40,label,23,GREEN,"bold")+lines(x+20,y+88,ls,21)
body+=path("M 375 207 L 425 207",arrow=True)+path("M 765 207 L 815 207",arrow=True)
body+=path("M 990 315 L 990 360 L 600 360 L 600 390",arrow=True)
body+=rect(325,400,550,132,"#cdfc80",GREEN)+text(600,442,"4 / CHECK INDEPENDENT MEASUREMENTS",22,INK,"bold","middle")
body+=text(600,477,"Hold out a spot; compare image Ev with measured Ev.",21,INK,anchor="middle")+text(600,508,"Check clipping, movement, flare and scene changes.",21,INK,anchor="middle")
body+=path("M 465 540 L 465 574 L 280 574 L 280 602",arrow=True)+path("M 735 540 L 735 574 L 920 574 L 920 602",arrow=True)
body+=rect(50,615,480,136,"white",LINE)+text(75,652,"DAYLIGHT / LUMINANCE STUDY",23,GREEN,"bold")+lines(75,690,["Compare surfaces and design alternatives.","Match the view, sky and false-colour scale."],21)
body+=rect(670,615,480,136,"white",LINE)+text(695,652,"GLARE / FISHEYE REQUIRED",23,GREEN,"bold")+lines(695,690,["Use a calibrated 180° view at eye position.","Inspect sources; analyse DGP with evalglare."],21)
body+=text(55,805,"Archive original exposures, calibration data, lens profile, HDR, view information and analysis settings together.",22)
save("processing-workflow.svg","Processing and validation workflow","Merge, correct lens geometry and vignetting, calibrate to spot luminance readings, then independently validate. Branch to daylight studies or glare analysis, which requires a fisheye and a calibrated hemispheric view.",845,body)

# 5. Editable annotations over the user's actual portrait capture; no student metadata.
photo_bytes = BytesIO()
Image.open(OUT / "portrait-2043.webp").convert("RGB").save(photo_bytes, format="JPEG", quality=92)
photo = base64.b64encode(photo_bytes.getvalue()).decode()
body = text(44,54,"05 / MATCH THE METER READING TO THE SAME IMAGE REGION",21,GREEN,"bold")
body += '<g id="example-photo"><image x="55" y="95" width="490" height="735" xlink:href="data:image/jpeg;base64,'+photo+'"/></g>'
body += '<g id="editable-target-markers">'
targets=[("A",.384,.795,"67","Timber floor"),("B",.072,.705,"165","Timber floor"),("C",.326,.546,"77","Painted wall"),("D",.466,.541,"415","Painted wall"),("E",.666,.123,"65","Ceiling panel")]
for i,(label,px,py,value,material) in enumerate(targets):
    x,y=55+px*490,95+py*735
    body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="none" stroke="#ffffff" stroke-width="4"/><circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="none" stroke="#162d26" stroke-width="2"/>'
    body += rect(round(x+18),round(y-19),32,34,INK,INK,4)
    body += text(round(x+25),round(y+7),label,26,"#ffffff","bold")
    yy=140+i*104
    body += rect(600,yy-30,535,88,"white",LINE,7)+text(622,yy+4,label,27,GREEN,"bold")+text(674,yy,value+" cd/m²",27,INK,"bold")+text(674,yy+32,material,21,MUTED)
body += '</g><g id="teaching-notes">'+lines(600,713,["Supplied course notes: Oct. 5, 2026, 4:30 pm.","Photo EXIF: 4:45:53 pm; timing is unverified.","These readings illustrate target selection.","They are not a validated calibration for this frame."],21)
body += text(55,890,"Source: 3X6A2043.JPG and the accompanying portrait measurement sheet. Marker positions are approximate.",21,MUTED)+'</g>'
save("sample-calibration.svg","Annotated portrait example with supplied luminance readings","The supplied portrait sample is annotated with five approximate target regions: A 67, B 165, C 77, D 415 and E 65 cd/m². Course-note and photo timestamps differ, so the readings illustrate target selection rather than a validated calibration.",930,body)
print("Wrote five editable SVG diagrams to", OUT)
with zipfile.ZipFile(OUT / "lumisnap-editable-diagrams.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(OUT.glob("*.svg")):
        archive.write(file, file.name)
    archive.writestr("EDITING.md", "# LumiSnap HDR field guide diagrams\n\nOpen any SVG directly in Adobe Illustrator or Inkscape. Labels are live Arial text; shapes, paths and annotations remain editable. The sample photograph is an embedded JPEG. The diagrams have no external dependencies. Editing an SVG does not require rerunning a generator.\n\nThe photograph and readings are supplied course examples. Timestamps differ; the readings illustrate target selection and are not a validated calibration of the displayed frame.\n\nGuide, references and image notes: https://lumisnap.io/guide.html\n")
print("Bundled the SVGs for download.")
