#!/usr/bin/env python3
"""Render documentation assets from saved iPhone HDR sessions (NumPy and Pillow)."""
from pathlib import Path
import argparse
import json, math, re
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-root', type=Path, default=ROOT.parent / 'LumiSnapDev/sample/IOScaptures')
SOURCE = parser.parse_args().source_root
OUT = ROOT / 'assets/tutorial/iphone'
OUT.mkdir(exist_ok=True)

def read_hdr(path):
    with path.open('rb') as f:
        assert f.readline().strip() == b'#?RADIANCE'
        while f.readline().strip():
            pass
        resolution = f.readline().decode().strip()
        match = re.fullmatch(r'-Y (\d+) \+X (\d+)', resolution)
        if not match:
            raise ValueError(f'Unsupported HDR orientation: {resolution}')
        height, width = map(int, match.groups())
        rgbe = np.empty((height, width, 4), dtype=np.uint8)
        for row in range(height):
            assert f.read(4) == bytes([2, 2, width >> 8, width & 255])
            for channel in range(4):
                x = 0
                while x < width:
                    code = f.read(1)[0]
                    if code > 128:
                        count = code - 128
                        value = f.read(1)[0]
                        rgbe[row, x:x+count, channel] = value
                    elif code:
                        count = code
                        data = f.read(count)
                        assert len(data) == count
                        rgbe[row, x:x+count, channel] = np.frombuffer(data, dtype=np.uint8)
                    else:
                        raise ValueError('Invalid RGBE run')
                    x += count
                    assert x <= width
        assert not f.read(), 'Unexpected trailing HDR data'
    exponent = rgbe[:, :, 3].astype(np.int32)
    rgb = rgbe[:, :, :3].astype(np.float64) * np.exp2(exponent[:, :, None] - 136)
    rgb[exponent == 0] = 0
    return rgb

def turbo(t):
    r = .13572138+t*(4.61539260+t*(-42.66032258+t*(132.13108234+t*(-152.94239396+t*59.28637943))))
    g = .09140261+t*(2.19418839+t*(4.84296658+t*(-14.18503333+t*(4.27729857+t*2.82956604))))
    b = .10667330+t*(12.64194608+t*(-60.58204836+t*(110.36276771+t*(-89.90310912+t*27.34824973))))
    return np.floor(np.clip(np.stack([r,g,b],axis=-1),0,1)*255+.5).astype(np.uint8)

def save(name, array):
    Image.fromarray(array).save(OUT/name, 'WEBP', quality=90, method=6)

for name in ['designtechspace', 'milsteindome']:
    source = SOURCE/name
    project_file = next(p for p in (source/'session.lumisnap.json', source/'session.hlab.json') if p.exists())
    project = json.loads(project_file.read_text())
    rgb = read_hdr(source/project['WorkingImage'])
    h,w,_ = rgb.shape
    assert (w,h) == (project['ImageWidth'], project['ImageHeight'])
    mask = np.asarray(Image.open(source/project['ClipMaskImage']).convert('L')) > 0
    assert mask.shape == (h,w)
    # Match HDRImage.preview(): sampled Rec.709 log average, global Reinhard,
    # 1.1 display gain and exact sRGB encoding. Only a display copy is tone mapped.
    display_luminance = rgb @ np.array([.2126,.7152,.0722])
    exposure = .18 / np.exp(np.log(1e-9+np.maximum(0,display_luminance.reshape(-1)[::7])).mean())
    linear = np.clip(rgb*(exposure*1.1/(1+np.maximum(0,display_luminance*exposure)))[:,:,None],0,1)
    srgb = np.where(linear <= .0031308, 12.92*linear, 1.055*linear**(1/2.4)-.055)
    save(name+'-preview.webp', np.floor(srgb*255+.5).astype(np.uint8))
    # The working HDR is uncalibrated. Apply the saved project factor once.
    luminance = 179 * (rgb @ np.array([.265,.670,.065])) * project['CalibrationFactor']
    t = np.clip((np.log(np.maximum(luminance,1e-30))-math.log(10))/(math.log(10000)-math.log(10)),0,1)
    lut = turbo(np.linspace(0,1,1024))
    false_colour = lut[np.floor(t*1023+.5).astype(int)]
    false_colour[mask | ~np.isfinite(luminance) | (luminance < 0)] = 96
    # Preserve grey reliability pixels exactly in the numerical display asset.
    Image.fromarray(false_colour).save(OUT/(name+'-luminance.webp'), 'WEBP', lossless=True, method=6)
    points = []
    for i,spot in enumerate(project['Spots'],1):
        x,y = spot['NormalizedX']*w, spot['NormalizedY']*h
        points.append(f'<g><circle cx="{x:.3f}" cy="{y:.3f}" r="24" fill="#101919" stroke="#cdfc80" stroke-width="4"/><text x="{x:.3f}" y="{y:.3f}" text-anchor="middle" dominant-baseline="central" fill="#edf3ee" font-family="Arial, sans-serif" font-size="26" font-weight="700">{i}</text></g>')
    (OUT/(name+'-points.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-label="Recorded calibration point positions">'+''.join(points)+'</svg>\n')
    print(name, w,h,'unreliable',float(mask.mean()), 'reliable luminance percentiles', np.percentile(luminance[~mask],[1,50,99]).round(2).tolist())
Image.fromarray(turbo(np.linspace(0,1,1024))[None,:,:].repeat(24,axis=0)).save(OUT/'luminance-legend.webp','WEBP',lossless=True)
