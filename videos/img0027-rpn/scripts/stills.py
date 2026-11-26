"""Stills, match-cut sheet and contact sheet from a reel's preview. Usage: <venv>/python stills.py <reel>
- stills/: one frame per beat (label_time.jpg)
- <reel>_matchcut_cuts.jpg: one row per burst cut: last frame before | first frame after | 50% overlay with the landing point
- <reel>_contact.jpg: a frame every 2 s"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..')
REEL = sys.argv[1]; OUT = f'{R}/renders/{REEL}'; G = os.path.expanduser('~/Movies/FCP/img0027-rpn-graphics')
PV = f'{OUT}/img0027_rpn_preview.mp4'; RJ = json.load(open(f'{OUT}/runs.json'))


def grab(f):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', PV, '-vf', f'select=eq(n\\,{f})', '-fps_mode', 'passthrough', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (1080, 1920), b)


bu = RJ['burst']; cuts = [bu['b0'] + k * bu['fpi'] for k in range(len(bu['items']) + 1)]
rows = []
for c in cuts:
    a, b = grab(c - 1), grab(c); ov = Image.blend(a, b, 0.5); d = ImageDraw.Draw(ov); x, y = bu['target']; s = bu['size'] / 2
    d.ellipse([x - s, y - s, x + s, y + s], outline=(0, 255, 120), width=4); d.line([x - 30, y, x + 30, y], fill=(0, 255, 120), width=3); d.line([x, y - 30, x, y + 30], fill=(0, 255, 120), width=3)
    rows.append([a, b, ov])
sh = Image.new('RGB', (3 * 360, len(rows) * 640), (0, 0, 0))
for i, r in enumerate(rows):
    for j, im in enumerate(r): sh.paste(im.resize((360, 640)), (j * 360, i * 640))
for d_ in (OUT, G): sh.save(f'{d_}/img0027_matchcut_cuts.jpg', quality=85)
os.makedirs(f'{G}/stills', exist_ok=True)
tot = RJ['total_frames']; step = 60
cs = [grab(f).resize((216, 384)) for f in range(15, tot, step)]
n = 10; ct = Image.new('RGB', (216 * n, 384 * ((len(cs) + n - 1) // n)))
for k, im in enumerate(cs): ct.paste(im, (k % n * 216, k // n * 384))
for d_ in (OUT, G): ct.save(f'{d_}/img0027_contact.jpg', quality=85)
for t in map(float, sys.argv[2:]):
    grab(round(t * 30)).save(f'{G}/stills/img0027_{t:05.2f}.jpg', quality=90)
print(REEL, 'cut sheet', len(rows), 'rows; contact', len(cs))
