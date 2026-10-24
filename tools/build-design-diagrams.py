#!/usr/bin/env python3
"""Build the seven editable "design question" diagrams for guide.html#design.

Same conventions as build-tutorial-diagrams.py: 1200 px wide, live Arial text,
named groups, no external fonts. Python 3 standard library only.
Values marked "example" explain a metric; they are not measurements.
"""
from pathlib import Path
from html import escape
from math import cos, sin, tan, exp, radians
import zipfile

OUT = Path(__file__).resolve().parents[1] / "assets" / "tutorial"
INK, MUTED, GREEN, LIME, PAPER, LINE = "#162d26", "#50665b", "#306848", "#cdfc80", "#f0f3e9", "#b8c9ba"
GLASS, SAGE, DESK, WALL, PALE = "#a5c7dd", "#e4ebdf", "#d9dfce", "#929e88", "#e9f5c9"


def text(x, y, value, size=20, color=INK, weight="normal", anchor="start"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def lines(x, y, values, size=20, color=MUTED, step=29):
    return "".join(text(x, y + i * step, v, size, color) for i, v in enumerate(values))


def rect(x, y, w, h, fill="white", stroke=LINE, radius=0, width=2, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{extra}/>'


def card(x, y, w, h, label):
    return rect(x, y, w, h, "white", LINE, 12) + text(x + 22, y + 40, label, 19, GREEN, "bold")


def path(d, color=GREEN, width=3, dash="", arrow=False, fill="none"):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"' + (' marker-end="url(#arrow)"' if arrow else "") + "/>"


def line(a, b, color=GREEN, width=3, dash="", arrow=False):
    return path(f"M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}", color, width, dash, arrow)


def circle(c, r, fill="none", stroke=INK, width=2, dash=""):
    return f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def poly(points, fill, stroke=INK, width=2, opacity=1):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{width}"/>'


def group(name, body):
    return f'<g id="{name}">{body}</g>'


def save(name, title, desc, height, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/></marker></defs>
<g id="background"><rect width="1200" height="{height}" fill="{PAPER}"/></g>
<g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>'''
    (OUT / name).write_text(svg + "\n")


def fp(c, r, theta, phi):
    """Angular fisheye: theta from the view direction maps linearly to the radius."""
    return (c[0] + r * theta / 90 * cos(radians(phi)), c[1] - r * theta / 90 * sin(radians(phi)))


def fisheye(c, r, rings=(30, 60)):
    out = circle(c, r, SAGE, INK, 3)
    for t in rings:
        out += circle(c, r * t / 90, "none", LINE, 2, "6 6")
    out += line((c[0] - r, c[1]), (c[0] + r, c[1]), LINE, 2, "6 6") + line((c[0], c[1] - r), (c[0], c[1] + r), LINE, 2, "6 6")
    return out


def camera(x, y, w=56, h=38):
    """Camera body facing right, lens at (x + w, y + h/2)."""
    return rect(x, y, w, h, INK, INK, 5) + f'<circle cx="{x + w:.1f}" cy="{y + h / 2:.1f}" r="13" fill="{GLASS}" stroke="{INK}" stroke-width="3"/>'


# USE 1. Glare.
body = text(44, 54, "USE 1 / WILL THIS BE UNCOMFORTABLE? GLARE", 21, GREEN, "bold")
C, R = (320, 395), 215
g = card(40, 90, 560, 580, "A / 180° FISHEYE AT THE EYE, ALONG THE GAZE") + fisheye(C, R)
w = [fp(C, R, 72, 150), fp(C, R, 40, 135), fp(C, R, 40, 205), fp(C, R, 72, 200)]
g += path(f"M {w[0][0]:.1f} {w[0][1]:.1f} Q {w[0][0] + 48:.1f} {w[0][1] - 26:.1f} {w[1][0]:.1f} {w[1][1]:.1f} L {w[2][0]:.1f} {w[2][1]:.1f} Q {w[3][0] + 48:.1f} {w[3][1] + 22:.1f} {w[3][0]:.1f} {w[3][1]:.1f} Z", INK, 3, fill=GLASS)
g += path(f"M {w[0][0]:.1f} {w[0][1]:.1f} Q {w[0][0] + 48:.1f} {w[0][1] - 26:.1f} {w[1][0]:.1f} {w[1][1]:.1f} L {w[2][0]:.1f} {w[2][1]:.1f} Q {w[3][0] + 48:.1f} {w[3][1] + 22:.1f} {w[3][0]:.1f} {w[3][1]:.1f} Z", LIME, 7, "10 6")
sun = fp(C, R, 58, 160)
g += circle(sun, 14, "#ffffff", INK, 3) + line(C, sun, GREEN, 2.5, "7 5")
g += text(C[0] - 60, C[1] - 60, "P: position", 19, GREEN, "bold")
g += text(76, 162, "Glare source: Ls, ωs", 20, INK, "bold") + line((150, 170), (175, 268), GREEN, 2)
task = (C[0] + 40, C[1] + 85)
g += rect(C[0] - 135, C[1] + 125, 290, 16, DESK, GREEN, 0) + circle(task, 40, "none", GREEN, 3, "8 6") + text(task[0] + 50, task[1] + 7, "Task zone", 19, GREEN, "bold")
g += text(C[0] + 10, C[1] + 26, "View direction", 18, MUTED)
body += group("fisheye", g)
x0, x1, y = 670, 1130, 230
X = lambda v: x0 + (v - .25) / .3 * (x1 - x0)
s = card(640, 90, 520, 580, "B / DGP FOR TWO DESIGN MOVES (EXAMPLE)")
for a, b, fill, name, tc in [(.25, .35, "#ffffff", "imperceptible", INK), (.35, .40, PALE, "perceptible", INK), (.40, .45, LIME, "disturbing", INK), (.45, .55, GREEN, "intolerable", "#ffffff")]:
    s += rect(X(a), y, X(b) - X(a), 44, fill, GREEN, 0) + text((X(a) + X(b)) / 2, y - (36 if name == "perceptible" else 12), name, 16, INK, anchor="middle")
    if name == "perceptible":
        s += line(((X(a) + X(b)) / 2, y - 30), ((X(a) + X(b)) / 2, y - 2), GREEN, 1.5)
for v in (.25, .35, .40, .45, .55):
    s += text(X(v), y + 70, f"{v:.2f}", 16, MUTED, anchor="middle")
for v, label, row in [(.48, "A / desk facing the window", 0), (.33, "B / desk turned 90°, blind", 1)]:
    yy = y + 115 + row * 62
    s += poly([(X(v), y + 46), (X(v) - 9, y + 60), (X(v) + 9, y + 60)], INK, INK, 1) + line((X(v), y + 80), (X(v), yy - 22), INK, 1.5, "4 4")
    s += text(X(v), yy, f"{label}: {v:.2f}", 19, INK, "bold", "end" if v > .4 else "start")
s += lines(670, 462, ["Report with DGP: Ev at the lens and each", "source’s Ls, ωs and position.", "evalglare source threshold: 5 × task-zone", "mean (-T), or a fixed 2,000 cd/m² (-b 2000).", "UGR is for electric lighting (office limit ~19)."], 19)
body += group("dgp-scale", s)
body += text(55, 708, "A clipped sun underestimates Ls² ωs, and with it DGP: capture the sun with a characterized ND filter.", 21)
save("design-glare.svg", "Glare: sources in the fisheye view and the DGP scale", "A 180-degree fisheye at eye position with a window glare source, the sun, its position and the task zone. A DGP scale from imperceptible to intolerable compares two design moves: a desk facing the window at 0.48 and a desk turned 90 degrees with a blind at 0.33. Example values.", 740, body)

# USE 2. Perceived brightness.
body = text(44, 54, "USE 2 / DOES IT FEEL BRIGHT OR GLOOMY? THE 40° BAND", 21, GREEN, "bold")
for i, (label, wall, floor, value, verdict) in enumerate([("A / DARK WALLS, LIGHT FLOOR", "#5d6b5f", "#ffffff", 18, "below ~30: reads gloomy"), ("B / LIGHT WALLS, DARK FLOOR", "#ffffff", "#5d6b5f", 46, "above ~30: reads adequately lit")]):
    x = 40 + i * 580
    g = card(x, 90, 540, 520, label)
    fy, cy, xl, xr = 420, 140, x + 40, x + 500
    g += line((xl, cy), (xr, cy), INK, 4) + line((xl, fy), (xr, fy), INK, 4) + line((xl, cy), (xl, 210), INK, 4) + line((xl, 300), (xl, fy), INK, 4) + rect(xl - 5, 210, 10, 90, GLASS, INK, 0)
    g += rect(xr - 28, cy, 28, fy - cy, wall, INK, 0) + rect(xl, fy - 14, xr - xl - 28, 14, floor, INK, 0)
    g += text(xr - 36, cy + 30, "light finish, ρ ≈ 0.8" if wall == "#ffffff" else "dark finish, ρ ≈ 0.2", 17, INK, anchor="end")
    g += rect(xl + 30, 330, 160, 10, DESK, GREEN, 0) + line((xl + 40, 340), (xl + 40, fy - 14), INK, 3) + line((xl + 180, 340), (xl + 180, fy - 14), INK, 3)
    g += text(xl + 40, 318, "Eh = 500 lx", 19, GREEN, "bold")
    eye = (xl + 150, 285)
    d = xr - 28 - eye[0]
    top, bot = (xr - 28, eye[1] - d * tan(radians(20))), (xr - 28, eye[1] + d * tan(radians(20)))
    g += poly([eye, top, bot], LIME, GREEN, 2, .55) + line(top, bot, GREEN, 8) + circle(eye, 9, "#ffffff", INK, 3)
    g += text(eye[0] + 70, eye[1] - 30, "40°", 19, GREEN, "bold")
    g += text(x + 270, 500, f"{value} cd/m²", 40, GREEN, "bold", "middle") + text(x + 270, 535, "mean luminance in the 40° band", 18, MUTED, anchor="middle") + text(x + 270, 568, verdict, 20, INK, "bold", "middle")
    body += group(["dark-walls", "light-walls"][i], g)
body += text(55, 652, "Same window, same desk illuminance. People judge brightness by the surfaces they look at, not the desk plane.", 21)
body += text(55, 684, "Band: ±20° about the horizon of a level capture (Loe et al.). Example values.", 20, MUTED)
save("design-brightness.svg", "Perceived brightness: mean luminance in the 40-degree horizontal band", "Two room sections with the same 500 lux on the desk. With dark walls the 40-degree band at eye level averages 18 cd/m2 and reads gloomy; with light walls it averages 46 cd/m2 and reads adequately lit. Example values.", 720, body)

# USE 3. Contrast.
body = text(44, 54, "USE 3 / IS IT CALM OR DRAMATIC? CONTRAST", 21, GREEN, "bold")
g = card(40, 90, 520, 560, "A / LUMINANCE RATIOS")
g += rect(70, 150, 460, 290, SAGE, GREEN, 0) + rect(150, 215, 300, 165, "#ffffff", GREEN, 0, 2, ' stroke-dasharray="8 6"') + rect(235, 262, 130, 72, LIME, GREEN, 0)
g += text(300, 305, "task", 21, INK, "bold", "middle") + text(300, 243, "surround", 19, INK, anchor="middle") + text(300, 180, "periphery", 19, INK, anchor="middle")
g += text(70, 492, "1 : 1/3 : 1/10", 34, GREEN, "bold") + lines(70, 530, ["IES ballpark, task : surround : periphery.", "Beyond it, the eye keeps re-adapting."], 19)
body += group("ratios", g)
h = card(600, 90, 560, 560, "B / LOG-LUMINANCE HISTOGRAM OF THE VIEW")
hx, hw, n = 630, 500, 30
gauss = lambda i, m, s: exp(-(((i + .5) / n * 4 - m) ** 2) / (2 * s * s))
for y0, bins, label, sub in [(160, [gauss(i, 1.8, .25) for i in range(n)], "Calm: diffuse, even", "σ(log₁₀ L) ≈ 0.25, narrow"),
                             (330, [gauss(i, .9, .3) + .7 * gauss(i, 3.2, .25) + .25 * gauss(i, 2, .5) for i in range(n)], "Dramatic: sun patch, deep shade", "σ(log₁₀ L) ≈ 0.9, wide")]:
    H, top = 110, max(bins)
    h += text(hx, y0, label, 19, INK, "bold") + text(hx + hw, y0, sub, 17, GREEN, "bold", "end")
    for i, v in enumerate(bins):
        if v > .01:
            bh = v / top * H
            h += rect(hx + i * hw / n, y0 + 15 + H - bh, hw / n, bh, LIME, GREEN, 0, 1)
    h += line((hx, y0 + 15 + H), (hx + hw, y0 + 15 + H), INK, 2)
for e, lab in enumerate(["1", "10", "100", "1,000", "10,000"]):
    h += text(hx + e / 4 * hw, 485, lab, 16, MUTED, anchor="middle")
h += text(hx + hw / 2, 512, "Luminance, cd/m² (log scale)", 17, MUTED, anchor="middle")
h += lines(hx, 552, ["Spatial contrast (Rockcastle and Andersen) sums neighbour", "differences at several image resolutions."], 18)
body += group("histograms", h)
body += text(55, 692, "Neither is right in itself: a studio needs even light on the work; a chapel or a stair can use sharp contrast.", 21)
save("design-contrast.svg", "Contrast: luminance ratios and the log-luminance histogram", "Task, surround and periphery zones with the IES ballpark ratio 1 : 1/3 : 1/10, and two log-luminance histograms: a narrow, calm view and a wide, two-peaked dramatic view. Example histograms.", 730, body)

# USE 4. Change over a day.
DAY = [(t, 22 + 70 * exp(-(((t - 15.2) / 2.6) ** 2)), .24 + .27 * exp(-(((t - 16.2) / 1.25) ** 2))) for t in range(8, 19)]
body = text(44, 54, "USE 4 / HOW DOES IT CHANGE OVER TIME? AN HDR TIME-LAPSE", 21, GREEN, "bold")
g = card(40, 90, 1120, 580, "WEST-FACING STUDIO, CLEAR AUTUMN DAY, ONE CALIBRATED CAPTURE PER HOUR (EXAMPLE)")
x0, x1 = 200, 1110
X = lambda t: x0 + (t - 8) / 10 * (x1 - x0)
for t, _, _ in DAY:
    g += camera(X(t) - 16, 160, 26, 18).replace('r="13"', 'r="6"') + text(X(t), 205, f"{t}:00", 16, MUTED, anchor="middle")
Y1 = lambda v: 400 - v / 120 * 160
g += line((x0, 400), (x1, 400), INK, 2) + line((x0, 240), (x0, 400), INK, 2) + line((x0, Y1(30)), (x1, Y1(30)), INK, 2, "8 6")
g += text(x0 + 10, Y1(30) - 10, "30 cd/m²", 17, INK, "bold") + lines(60, 270, ["40° band", "mean L", "(cd/m²)"], 18, GREEN, 24)
g += path("M " + " L ".join(f"{X(t):.1f} {Y1(b):.1f}" for t, b, _ in DAY), GREEN, 4) + "".join(circle((X(t), Y1(b)), 6, GREEN, GREEN, 1) for t, b, _ in DAY)
for v in (0, 60, 120):
    g += text(x0 - 12, Y1(v) + 6, str(v), 16, MUTED, anchor="end")
Y2 = lambda v: 610 - (v - .2) / .35 * 160
above = [d for d in DAY if d[2] >= .4]
for t, _, _ in above:
    g += rect(X(t) - 40, 450, 80, 160, LIME, "none", 0, 0, ' fill-opacity="0.6"')
g += line((x0, 610), (x1, 610), INK, 2) + line((x0, 450), (x0, 610), INK, 2) + line((x0, Y2(.4)), (x1, Y2(.4)), INK, 2, "8 6")
g += text(x0 + 10, Y2(.4) - 10, "DGP 0.40", 17, INK, "bold") + text(60, 480, "DGP", 18, GREEN, "bold")
g += path("M " + " L ".join(f"{X(t):.1f} {Y2(d):.1f}" for t, _, d in DAY), INK, 4) + "".join(circle((X(t), Y2(d)), 6, INK, INK, 1) for t, _, d in DAY)
for v in (.2, .3, .4, .5):
    g += text(x0 - 12, Y2(v) + 6, f"{v:.1f}", 16, MUTED, anchor="end")
g += text(X(above[0][0]) - 52, 478, f"{len(above)} of {len(DAY)} captures ≥ 0.40", 19, INK, "bold", "end")
body += group("timeline", g)
body += text(55, 712, "Morning: calm and dim. Late afternoon: low sun brightens the band, then crosses into glare. A midday capture misses both.", 21)
save("design-dynamics.svg", "Change over a day: 40-degree band luminance and DGP from hourly captures", "Eleven hourly captures from 8:00 to 18:00 in a west-facing studio. The 40-degree band mean rises above 30 cd/m2 in the afternoon and DGP exceeds 0.40 in two captures in the late afternoon. Example values.", 750, body)

# USE 5. Reflectance.
body = text(44, 54, "USE 5 / WHAT IS THIS MATERIAL ACTUALLY DOING? REFLECTANCE", 21, GREEN, "bold")
g = card(40, 90, 560, 580, "A / REFLECTANCE FROM L AND E")
g += rect(520, 140, 30, 400, WALL, GREEN, 0) + rect(496, 260, 24, 120, "#ffffff", INK, 0, 3)
for a in range(110, 251, 35):
    g += line((493, 320), (493 + 95 * cos(radians(a)), 320 - 95 * sin(radians(a))), GREEN, 2.5, arrow=True)
g += path("M 493 225 A 95 95 0 0 0 493 415", GREEN, 2, "5 5")
g += text(80, 172, "Diffuse surface: the same L", 18, GREEN) + text(80, 196, "in every direction", 18, GREEN)
g += text(470, 208, "Matte sample", 19, INK, "bold", "end") + line((474, 212), (500, 258), GREEN, 2)
g += rect(502, 420, 16, 44, GLASS, INK, 3) + text(500, 545, "Lux sensor on the wall, facing out: E", 18, INK, "bold", "end")
for y in (360, 395, 430):
    g += line((310, y + 30), (498, y + 52 + (y - 395) * .3), GREEN, 2.5, arrow=True)
g += camera(70, 302) + line((105, 340), (105, 540), INK, 3)
g += line((395, 320), (150, 320), GREEN, 3, arrow=True) + text(270, 306, "L from the HDR", 19, GREEN, "bold", "middle")
g += rect(70, 580, 500, 64, LIME, GREEN, 8) + text(320, 620, "ρ = π L / E   e.g. π × 40 / 250 = 0.50", 22, INK, "bold", "middle")
body += group("lux-method", g)
g = card(640, 90, 520, 580, "B / AGAINST A GREY CARD IN THE FRAME")
g += rect(670, 150, 460, 270, SAGE, GREEN, 0) + rect(720, 200, 140, 140, "#9aa39a", INK, 0) + rect(940, 200, 140, 140, "#ffffff", INK, 0, 3)
g += text(790, 372, "Grey card ρ = 0.18", 18, INK, anchor="middle") + text(790, 400, "L = 14 cd/m²", 19, GREEN, "bold", "middle")
g += text(1010, 372, "Sample", 18, INK, anchor="middle") + text(1010, 400, "L = 49 cd/m²", 19, GREEN, "bold", "middle")
g += lines(670, 460, ["Same plane, same light, both matte, view not", "grazing. No lux meter needed.", "Glossy or textured finishes are not diffuse:", "they have no single ρ."], 19)
g += rect(670, 580, 460, 64, LIME, GREEN, 8) + text(900, 620, "ρx = 0.18 × 49 / 14 = 0.63", 22, INK, "bold", "middle")
body += group("grey-card", g)
body += text(55, 712, "Use measured reflectances to choose finishes and as inputs to daylight simulation instead of guessed values.", 21)
save("design-reflectance.svg", "Reflectance of a matte sample from luminance and illuminance, or against a grey card", "A matte sample on a wall reflects the same luminance in every direction. Reflectance equals pi times luminance over illuminance, for example pi times 40 over 250 equals 0.50. Alternatively, compare with an 18 percent grey card in the same light: 0.18 times 49 over 14 equals 0.63. Example values.", 750, body)

# USE 6. Model, real space and simulation.
body = text(44, 54, "USE 6 / DOES MY MODEL OR SIMULATION TELL THE TRUTH? VALIDATION", 21, GREEN, "bold")


def room(x, y, w, h, floor="#ffffff", ceiling="#ffffff", labels=False):
    ix, iy, iw, ih = x + w * .3, y + h * .28, w * .4, h * .44
    out = rect(x, y, w, h, "#ffffff", INK, 0, 3)
    out += poly([(x, y), (ix, iy), (ix + iw, iy), (x + w, y)], ceiling, INK, 2) + poly([(x, y + h), (ix, iy + ih), (ix + iw, iy + ih), (x + w, y + h)], floor, INK, 2)
    out += rect(ix, iy, iw, ih, "#ffffff", INK, 0, 2) + poly([(x + w * .07, y + h * .3), (x + w * .21, y + h * .37), (x + w * .21, y + h * .63), (x + w * .07, y + h * .7)], GLASS, INK, 2)
    if labels:
        for (px, py), s in [((x + w / 2, y + h * .13), "C"), ((x + w / 2, y + h / 2), "W"), ((x + w / 2, y + h * .87), "F"), ((x + w * .14, y + h / 2), "G")]:
            out += circle((px, py), 15, LIME, GREEN, 2) + text(px, py + 6, s, 16, INK, "bold", "middle")
    return out


g = ""
for i, (label, kw) in enumerate([("REAL SPACE", {"labels": True}), ("SCALE MODEL, 1:20", {"floor": WALL}), ("RADIANCE RENDERING", {"ceiling": PALE})]):
    x = 40 + i * 380
    g += card(x, 90, 360, 290, label) + room(x + 25, 150, 310, 205, **kw)
body += group("views", g)
VAL = [("ceiling", .26, .04, "light leak at the model roof?"), ("back wall", -.05, -.06, ""), ("floor", -.19, .08, "model material too dark"), ("window", .31, -.12, "model sky ≠ real sky")]
x0, x1, y0 = 230, 760, 470
X = lambda r: x0 + (r + .4) / .8 * (x1 - x0)
g = card(40, 405, 1120, 330, "LOG RATIO PER REGION: log₁₀(L / L real)")
g += rect(X(-.1), y0 - 14, X(.1) - X(-.1), len(VAL) * 46 + 10, LIME, "none", 0, 0, ' fill-opacity="0.55"')
for r in (-.4, -.2, 0, .2, .4):
    g += line((X(r), y0 - 14), (X(r), y0 + len(VAL) * 46), INK if r == 0 else LINE, 2, "" if r == 0 else "5 5")
    g += text(X(r), y0 + len(VAL) * 46 + 24, ("+" if r > 0 else "−" if r < 0 else "") + f"{abs(r):.1f}", 16, MUTED, anchor="middle")
for i, (name, m, s, why) in enumerate(VAL):
    yy = y0 + 14 + i * 46
    g += text(x0 - 18, yy + 7, name, 19, INK, anchor="end") + rect(X(m) - 8, yy - 8, 16, 16, INK, INK, 0) + circle((X(s), yy), 8, "#ffffff", GREEN, 3)
    if why:
        g += text(x1 + 22, yy + 7, why, 18, GREEN)
g += rect(x0, 696, 16, 16, INK, INK, 0) + text(x0 + 26, 710, "model / real", 18) + circle((x0 + 190, 704), 8, "#ffffff", GREEN, 3) + text(x0 + 206, 710, "rendering / real", 18) + text(x0 + 400, 710, "band: ±0.1 ≈ ±26 %", 18, GREEN, "bold")
body += group("log-ratios", g)
body += text(55, 772, "Mismatches in a scale model, such as light leaks, materials and sky, are the lesson, not a failure. Example values.", 21)
save("design-validation.svg", "Validation: per-region log ratios between a scale model, a rendering and the real space", "The same view of a real space, a 1:20 scale model and a Radiance rendering, with regions ceiling, back wall, floor and window. A dot plot of log10 luminance ratios per region shows the model too bright at the ceiling and window and too dark at the floor, while the rendering stays within plus or minus 0.1. Example values.", 800, body)

# USE 7. What the eye receives.
body = text(44, 54, "USE 7 / WHAT DOES THE EYE RECEIVE? VERTICAL ILLUMINANCE", 21, GREEN, "bold")
C, R = (320, 395), 215
g = card(40, 90, 560, 590, "A / Ev FROM THE FISHEYE IMAGE") + fisheye(C, R, (15, 30, 45, 60, 75))
for t in (0, 30, 60, 90):
    p = fp(C, R, t, -35)
    g += text(p[0] + 6, p[1] + 22, "cos 90° = 0" if t == 90 else f"cos {t}° = {cos(radians(t)):.2f}", 17, GREEN, "bold")
px = fp(C, R, 50, 125)
g += line(C, px, GREEN, 2.5, "7 5") + rect(px[0] - 11, px[1] - 11, 22, 22, LIME, INK, 0, 2)
g += text(px[0] + 20, px[1] - 16, "pixel i: Li, ωi, θi", 19, INK, "bold")
g += text(C[0], C[1] + R + 45, "Centre pixels count fully; the rim counts nothing.", 18, MUTED, anchor="middle")
body += group("fisheye", g)
g = card(640, 90, 520, 590, "B / READ IT AS")
g += rect(670, 150, 460, 60, LIME, GREEN, 8) + text(900, 188, "Ev = Σ Li · cos θi · ωi", 23, INK, "bold", "middle")
g += lines(670, 248, ["Check it against the lux sensor at the lens.", "A large gap points to clipped sources, a", "cropped view or the wrong projection."], 19)
g += text(670, 362, "MELANOPIC ESTIMATE, AN APPROXIMATION", 17, GREEN, "bold")
g += lines(670, 394, ["m-EDI ≈ Ev × M-DER of an assumed spectrum", "Daylight through glazing: M-DER ≈ 0.9–1.0", "Warm-white LED, ~2700 K: roughly 0.4–0.5", "RGB does not measure the spectrum: state the", "assumed source or use a spectrometer."], 18, MUTED, 27)
Xb = lambda v: 670 + v / 1000 * 440
g += rect(670, 548, Xb(620) - 670, 26, "#ffffff", GREEN, 0, 3) + text(Xb(620) + 10, 568, "Ev 620 lx", 17, INK, "bold")
g += rect(670, 584, Xb(560) - 670, 26, LIME, GREEN, 0, 3) + text(Xb(560) + 10, 604, "m-EDI ≈ 560", 17, INK, "bold")
g += line((Xb(250), 538), (Xb(250), 624), INK, 2, "6 4") + text(Xb(250), 648, "250 lx m-EDI daytime recommendation", 15, INK, anchor="middle")
body += group("reading", g)
body += text(55, 722, "Ev drives DGP and the non-visual effects of light. It is also the check on the whole capture. Example values.", 21)
save("design-eye.svg", "Vertical illuminance at the eye from a fisheye HDR, with a melanopic estimate", "In an angular fisheye, each pixel contributes its luminance times the cosine of its angle from the view direction times its solid angle to the vertical illuminance Ev. A melanopic estimate multiplies Ev by the melanopic daylight efficacy ratio of an assumed spectrum, compared with a 250 lux daytime recommendation. Example values.", 760, body)

print("Wrote seven design diagrams to", OUT)
with zipfile.ZipFile(OUT / "lumisnap-editable-diagrams.zip", "r") as archive:
    keep = {n: archive.read(n) for n in archive.namelist() if not n.startswith("design-")}
with zipfile.ZipFile(OUT / "lumisnap-editable-diagrams.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for n, data in keep.items():
        archive.writestr(n, data)
    for file in sorted(OUT.glob("design-*.svg")):
        archive.write(file, file.name)
print("Added the design diagrams to the editable-diagram ZIP.")
