"""Waveform check of every end cut that needs a look: risky endings (t s d k ch, numbers, percent) and
anything the envelope check flags. Each cell: 10 ms RMS envelope (dB) from 0.5 s before the ASR word end to 0.7 s
after; red = ASR word end, blue = the cut (end of the kept piece), green = next word onset, grey = floor +4 dB.
The kept audio is the white part left of the blue line. Usage: python3 cutsheet.py OUT.png"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import build, check, ENV, HOP, W, FPS, floor_at
from spec import REELS

cells = []
for n in REELS:
    ps, _ = build(n)
    for p, r in zip(ps, check(n, ps)):
        if p['note'] == 'contiguous': continue
        if r[5] or r[3] > 8 or r[2] < 120:
            cells.append((n, p, r))
CW, CH, cols = 360, 170, 4
rows = (len(cells) + cols - 1) // cols
im = Image.new('RGB', (cols * CW, rows * CH), (20, 20, 24)); d = ImageDraw.Draw(im)
f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 13)
for k, (n, p, r) in enumerate(cells):
    x0, y0 = (k % cols) * CW, (k // cols) * CH
    e = W[p['w1']]['e']; t0 = e - 0.5; t1 = e + 0.7
    seg = ENV[int(t0 / HOP):int(t1 / HOP)]
    fl = floor_at(e)
    lo, hi = fl - 6, max(seg.max(), fl + 20)
    Y = lambda v: y0 + 30 + (CH - 40) * (1 - (v - lo) / (hi - lo))
    X = lambda t: x0 + 6 + (CW - 12) * (t - t0) / (t1 - t0)
    cut = p['f1'] / FPS
    d.rectangle([X(t0), y0 + 30, X(cut), y0 + CH - 10], fill=(40, 40, 48))
    pts = [(X(t0 + i * HOP), Y(v)) for i, v in enumerate(seg)]
    d.line(pts, fill=(235, 235, 235), width=1)
    d.line([X(t0), Y(fl + 4), X(t1), Y(fl + 4)], fill=(110, 110, 110))
    d.line([X(e), y0 + 30, X(e), y0 + CH - 10], fill=(230, 70, 70))
    d.line([X(cut), y0 + 30, X(cut), y0 + CH - 10], fill=(80, 150, 255), width=2)
    nx = W[p['w1'] + 1]['s']
    if nx < t1: d.line([X(nx), y0 + 30, X(nx), y0 + CH - 10], fill=(80, 210, 110))
    d.text((x0 + 6, y0 + 4), f"{n} w{p['w1']} '{W[p['w1']]['w']}' -> '{W[p['w1'] + 1]['w']}'", font=f, fill=(255, 255, 255))
    d.text((x0 + 6, y0 + 17), f"tail {r[2]} ms  cut@floor+{r[3]:.1f} dB", font=f, fill=(180, 180, 180))
im.save(sys.argv[1]); print(len(cells), 'cells')
